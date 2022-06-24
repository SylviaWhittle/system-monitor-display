from asyncio import start_server
import socket
import threading
import sys
import time
import psutil
import logging
import os
import json
import math

# For the display
from samplebase import SampleBase
from rgbmatrix import graphics
from PIL import Image, ImageFont
from datetime import datetime


class Display(SampleBase):
    def __init__(self, *args, **kwargs):
        super(Display, self).__init__(*args, **kwargs)

    def run(self):

        # Load Canvas
        self.canvas = self.matrix
        self.canvas.brightness = 60

        # Load fonts
        self.font = graphics.Font()
        self.font.LoadFont("tinyfont.bdf")
        # font.LoadFont("../../../fonts/tom-thumb.bdf")
        # font.LoadFont("../../../fonts/4x6.bdf")
        # font = ImageFont.truetype("tiny.ttf")

        # Load colours
        self.red = graphics.Color(255, 0, 0)
        self.green = graphics.Color(50, 255, 50)
        self.blue = graphics.Color(0, 0, 255)
        self.black = graphics.Color(0, 0, 0)
        self.white = graphics.Color(200, 200, 200)
        self.pink1 = graphics.Color(255, 100, 100)
        self.pink2 = graphics.Color(255, 100, 120)
        self.grey = graphics.Color(50, 50, 50)

        # Draw background image
        image = Image.open("StatsDisplayV2.png")
        rgb_image = image.convert("RGB")
        data = rgb_image.getdata()
        for index, pixel in enumerate(data):
            y, x = divmod(index, 64)
            # print(pixel)
            self.canvas.SetPixel(x, y, pixel[0], pixel[1], pixel[2])

        # Threading
        format = "%(asctime)s: %(message)s"
        logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
        logging.info("main : before running thread")
        # process_clock = threading.Thread(target=self.clock, args=())
        # process_clock.start()
        process_stats = threading.Thread(target=self.draw_stats, args=())
        process_stats.start()

    def draw_clock(self):
        # Draw time and date
        width = 18
        height = 12
        tx = 37
        ty = 55
        # while True:

        for yy in range(height):
            graphics.DrawLine(
                self.canvas, tx, ty - yy - 1, tx + width, ty - yy - 1, self.black
            )

        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_date = now.strftime("%d.%m")
        # graphics.DrawText(canvas, font, tx, ty - 6, timecol, str(calendar.day_name[datetime.today().weekday()]))
        graphics.DrawText(self.canvas, self.font, tx, ty - 6, self.white, current_time)
        graphics.DrawText(self.canvas, self.font, tx, ty, self.white, current_date)
        time.sleep(0.5)

    def draw_stats(self):
        global data

        ram_history = []
        ram_history_size = 29
        ram_history_delay = 0
        for i in range(ram_history_size):
            ram_history.append(0)

        while True:
            if data == None:
                continue

            self.draw_cpu()
            self.draw_ram()
            ram_history_delay += 1
            if ram_history_delay >= 1:
                ram_history_delay = 0
                self.draw_ram_history(ram_history)
            self.draw_gpu()
            self.draw_storage()
            self.draw_clock()

            time.sleep(0.5)

    def draw_ram(self):
        self.draw_bar(data["RAM_load"], 33, 2, width=28)

        for i in range(5):
            graphics.DrawLine(self.canvas, 43, 22 - i, 49, 22 - i, self.black)

        graphics.DrawText(
            self.canvas,
            self.font,
            43,
            23,
            self.white,
            f'{round(data["RAM_used"])}',
        )

    def draw_ram_history(self, ram_history: list):
        global data

        graph_x = 33
        graph_y = 11

        ram_history.pop(0)
        ram_history.append(data["RAM_load"])

        for index, value in enumerate(ram_history):
            self.draw_vertical_bar(value, graph_x + index, graph_y)

    def draw_vertical_bar(self, value, px, py):

        start_r = 0
        start_g = 180
        start_b = 255
        end_r = 255
        end_g = 0
        end_b = 180

        height = 6
        draw_height = round(max((height / 100) * value, 1))

        # Draw the bar
        for i in range(draw_height):
            col_r = start_r + (end_r - start_r) * i / height
            col_g = start_g + (end_g - start_g) * i / height
            col_b = start_b + (end_b - start_b) * i / height
            col = graphics.Color(col_r, col_g, col_b)
            graphics.DrawLine(self.canvas, px, py + i, px, py + i, col)
            graphics.DrawLine(self.canvas, px, py - i, px, py - i, col)

        # height = 6
        # intensity = max(2.5 * value, 50)
        # color = graphics.Color(intensity, intensity, intensity)
        # draw_height = round((height / 100) * value)
        # graphics.DrawLine(
        #     self.canvas, px, py - draw_height, px, py + draw_height, color
        # )

        # self.canvas.SetPixel(px, py, intensity, intensity, intensity)

    def draw_bar(self, value, px, py, width=25):

        start_r = 0
        start_g = 180
        start_b = 255
        end_r = 255
        end_g = 0
        end_b = 180

        draw_width = math.floor((width / 100) * value)

        graphics.DrawLine(self.canvas, px, py, px + width, py, self.grey)
        graphics.DrawLine(self.canvas, px, py + 1, px + width, py + 1, self.grey)
        for i in range(draw_width):
            col_r = start_r + (end_r - start_r) * i / width
            col_g = start_g + (end_g - start_g) * i / width
            col_b = start_b + (end_b - start_b) * i / width
            col = graphics.Color(col_r, col_g, col_b)
            graphics.DrawLine(self.canvas, px + i, py, px + i, py + 1, col)

        # col_r = start_r + (end_r - start_r) * value / 100
        # col_g = start_g + (end_g - start_g) * value / 100
        # col_b = start_b + (end_b - start_b) * value / 100

        # Draw the bar
        # intensity = max(2.5 * value, 100)
        # color = graphics.Color(intensity, intensity, intensity)
        # color = graphics.Color(255, 255, 255)
        # color = graphics.Color(col_r, col_g, col_b)
        # draw_width = math.floor((width / 100) * value)
        # graphics.DrawLine(self.canvas, px, py, px + width, py, self.grey)
        # graphics.DrawLine(self.canvas, px, py + 1, px + width, py + 1, self.grey)
        # graphics.DrawLine(self.canvas, px, py, px + draw_width, py, color)
        # graphics.DrawLine(self.canvas, px, py + 1, px + draw_width, py + 1, color)

    def draw_cpu(self):
        global data

        for i in range(5):
            graphics.DrawLine(self.canvas, 17, 34 - i, 23, 34 - i, self.black)

        self.draw_bar(data["CPU_load_total"], 2, 2)
        self.draw_bar(data["CPU_load_1"], 2, 6)
        self.draw_bar(data["CPU_load_2"], 2, 10)
        self.draw_bar(data["CPU_load_3"], 2, 14)
        self.draw_bar(data["CPU_load_4"], 2, 18)
        self.draw_bar(data["CPU_load_5"], 2, 22)
        self.draw_bar(data["CPU_load_6"], 2, 26)

        graphics.DrawText(
            self.canvas,
            self.font,
            17,
            35,
            self.white,
            f'{round(data["CPU_temp"])}',
        )

    def draw_gpu(self):
        global data

        self.draw_bar(data["GPU_load"], 2, 39)
        self.draw_bar(data["GPU_RAM_load"], 2, 43)

        for i in range(5):
            graphics.DrawLine(self.canvas, 19, 51 - i, 25, 51 - i, self.black)

        graphics.DrawText(
            self.canvas,
            self.font,
            19,
            52,
            self.white,
            f'{round(data["GPU_temperature"])}',
        )

    def draw_storage(self):
        global data
        self.draw_bar(data["C_drive_load"], 33, 26, width=28)
        self.draw_bar(data["D_drive_load"], 33, 31, width=28)


def wait_for_packet():
    global received
    global address
    while True:
        received, address = s.recvfrom(4096)


if __name__ == "__main__":
    # Set up global variables
    global received
    global data
    global address
    data = None
    received = None
    address = None

    # Get IP address
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname + ".local")
    print(f"hostname: {hostname} | ip address: {ip_address}")
    port = 5005

    # Create a UDP socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the port
    server_address = (ip_address, port)
    s.bind(server_address)

    # Set up network thread
    T1 = threading.Thread(target=wait_for_packet, args=())
    T1.start()

    # Set up display
    display = Display()
    display.process()
    # Main loop
    while True:
        time.sleep(0.5)

        if received == None:
            continue

        data = json.loads(received)

        # print(f"packet: {received} | address: {address}")

        # CPU_temp = data["CPU_temp"]
        # CPU_load_total = data["CPU_load_total"]

        # cpu_load_1 = data["CPU_load_1"]
        # cpu_load_2 = data["CPU_load_2"]
        # cpu_load_3 = data["CPU_load_3"]
        # cpu_load_4 = data["CPU_load_4"]
        # cpu_load_5 = data["CPU_load_5"]
        # cpu_load_6 = data["CPU_load_6"]

        # RAM_load = data["RAM_load"]
        # RAM_used = data["RAM_used"]
