#!/usr/bin/env python
import json
import sys
from rgbmatrix import RGBMatrix
from rgbmatrix import graphics
import time
import harvest
from multiprocessing import Process, Manager
from threading import Thread
import argparse


class Matrix(object):
    STATE_STOPPED = 0
    STATE_STARTED = 1
    STATE_NO_TASK = 2
    STATE_TASK_RUNNING = 3
    STATE_MESSAGE = 4
    STATE_END = 5

    def __init__(self):
        self.display_state = self.STATE_STOPPED
        self.width = 32
        self.height = 16
        self.matrix = RGBMatrix(self.height, 1, 1)
        self.matrix.brightness = 45
        self.matrix.luminanceCorrect = False
        self.display_info = {
            'project_code': '',
            'task_hours': 0.0,
            'total_hours': 0.0,
            'message': ''
        }
        self.message_font = graphics.Font()
        self.message_font.LoadFont("./rpi-rgb-led-matrix/fonts/5x7.bdf")
        self.hours_font = graphics.Font()
        self.hours_font.LoadFont("./rpi-rgb-led-matrix/fonts/5x7.bdf")
        self.total_hours_font = graphics.Font()
        self.total_hours_font.LoadFont("./rpi-rgb-led-matrix/fonts/4x6.bdf")
        self.message_color = graphics.Color(255, 255, 0)
        self.red_color = graphics.Color(255, 0, 0)
        self.hours_color = graphics.Color(200, 0, 200)
        self.total_hours_color = graphics.Color(200, 200, 200)

    def run(self):
        while self.display_state != Matrix.STATE_END:
            if self.display_state == self.STATE_STOPPED:
                canvas = self.matrix.CreateFrameCanvas()
                myText = "Stopped"
                graphics.DrawText(canvas, self.message_font, 0, 10, self.message_color, myText)
                self.matrix.SwapOnVSync(canvas)
                time.sleep(.5)
            elif self.display_state == self.STATE_STARTED:
                canvas = self.matrix.CreateFrameCanvas()
                myText = "Started"
                graphics.DrawText(canvas, self.message_font, 0, 10, self.message_color, myText)
                self.matrix.SwapOnVSync(canvas)
                time.sleep(.5)
            elif self.display_state == self.STATE_MESSAGE:
                canvas = self.matrix.CreateFrameCanvas()
                graphics.DrawText(canvas, self.message_font, 0, 10, self.message_color, self.display_info['message'])
                self.matrix.SwapOnVSync(canvas)
                time.sleep(.5)
            elif self.display_state == self.STATE_NO_TASK:
                canvas = self.matrix.CreateFrameCanvas()
                canvas.Fill(255, 255, 255)
                canvas.SetPixel(1, 1, 0, 0, 0)
                canvas.SetPixel(8, 0, 255, 255, 255)
                canvas.SetPixel(9, 0, 255, 255, 255)
                canvas.SetPixel(10, 0, 255, 255, 255)
                canvas.SetPixel(11, 0, 255, 255, 255)
                canvas.SetPixel(12, 0, 255, 255, 255)
                canvas.SetPixel(13, 0, 255, 255, 255)
                canvas.SetPixel(14, 0, 255, 255, 255)
                canvas.SetPixel(15, 0, 255, 255, 255)
                canvas.SetPixel(16, 0, 255, 255, 255)
                canvas.SetPixel(17, 0, 255, 255, 255)
                canvas.SetPixel(18, 0, 255, 255, 255)
                canvas.SetPixel(19, 0, 255, 255, 255)
                canvas.SetPixel(20, 0, 255, 255, 255)
                canvas.SetPixel(21, 0, 255, 255, 255)
                canvas.SetPixel(22, 0, 255, 255, 255)
                canvas.SetPixel(23, 0, 255, 255, 255)
                canvas.SetPixel(8, 1, 255, 255, 255)
                canvas.SetPixel(9, 1, 255, 255, 255)
                canvas.SetPixel(10, 1, 255, 255, 255)
                canvas.SetPixel(11, 1, 255, 255, 255)
                canvas.SetPixel(12, 1, 0, 0, 0)
                canvas.SetPixel(13, 1, 0, 0, 0)
                canvas.SetPixel(14, 1, 0, 0, 0)
                canvas.SetPixel(15, 1, 0, 0, 0)
                canvas.SetPixel(16, 1, 0, 0, 0)
                canvas.SetPixel(17, 1, 0, 0, 0)
                canvas.SetPixel(18, 1, 0, 0, 0)
                canvas.SetPixel(19, 1, 0, 0, 0)
                canvas.SetPixel(20, 1, 0, 0, 0)
                canvas.SetPixel(21, 1, 255, 255, 255)
                canvas.SetPixel(22, 1, 255, 255, 255)
                canvas.SetPixel(23, 1, 255, 255, 255)
                canvas.SetPixel(8, 2, 255, 255, 255)
                canvas.SetPixel(9, 2, 255, 255, 255)
                canvas.SetPixel(10, 2, 23, 23, 23)
                canvas.SetPixel(11, 2, 54, 54, 54)
                canvas.SetPixel(12, 2, 82, 82, 82)
                canvas.SetPixel(13, 2, 179, 179, 179)
                canvas.SetPixel(14, 2, 179, 179, 179)
                canvas.SetPixel(15, 2, 179, 179, 179)
                canvas.SetPixel(16, 2, 179, 179, 179)
                canvas.SetPixel(17, 2, 179, 179, 179)
                canvas.SetPixel(18, 2, 214, 214, 214)
                canvas.SetPixel(19, 2, 255, 255, 255)
                canvas.SetPixel(20, 2, 214, 214, 214)
                canvas.SetPixel(21, 2, 0, 0, 0)
                canvas.SetPixel(22, 2, 255, 255, 255)
                canvas.SetPixel(23, 2, 255, 255, 255)
                canvas.SetPixel(8, 3, 255, 255, 255)
                canvas.SetPixel(9, 3, 0, 0, 0)
                canvas.SetPixel(10, 3, 255, 255, 255)
                canvas.SetPixel(11, 3, 179, 179, 179)
                canvas.SetPixel(12, 3, 255, 255, 255)
                canvas.SetPixel(13, 3, 179, 179, 179)
                canvas.SetPixel(14, 3, 179, 179, 179)
                canvas.SetPixel(15, 3, 179, 179, 179)
                canvas.SetPixel(16, 3, 179, 179, 179)
                canvas.SetPixel(17, 3, 179, 179, 179)
                canvas.SetPixel(18, 3, 179, 179, 179)
                canvas.SetPixel(19, 3, 214, 214, 214)
                canvas.SetPixel(20, 3, 255, 255, 255)
                canvas.SetPixel(21, 3, 54, 54, 54)
                canvas.SetPixel(22, 3, 255, 255, 255)
                canvas.SetPixel(23, 3, 255, 255, 255)
                canvas.SetPixel(8, 4, 255, 255, 255)
                canvas.SetPixel(9, 4, 54, 54, 54)
                canvas.SetPixel(10, 4, 214, 214, 214)
                canvas.SetPixel(11, 4, 13, 13, 13)
                canvas.SetPixel(12, 4, 0, 0, 0)
                canvas.SetPixel(13, 4, 13, 13, 13)
                canvas.SetPixel(14, 4, 133, 133, 133)
                canvas.SetPixel(15, 4, 255, 255, 255)
                canvas.SetPixel(16, 4, 54, 54, 54)
                canvas.SetPixel(17, 4, 0, 0, 0)
                canvas.SetPixel(18, 4, 39, 39, 39)
                canvas.SetPixel(19, 4, 179, 179, 179)
                canvas.SetPixel(20, 4, 255, 255, 255)
                canvas.SetPixel(21, 4, 133, 133, 133)
                canvas.SetPixel(22, 4, 0, 0, 0)
                canvas.SetPixel(23, 4, 255, 255, 255)
                canvas.SetPixel(8, 5, 23, 23, 23)
                canvas.SetPixel(9, 5, 179, 179, 179)
                canvas.SetPixel(10, 5, 54, 54, 54)
                canvas.SetPixel(11, 5, 54, 54, 54)
                canvas.SetPixel(12, 5, 255, 255, 255)
                canvas.SetPixel(13, 5, 54, 54, 54)
                canvas.SetPixel(14, 5, 255, 255, 255)
                canvas.SetPixel(15, 5, 255, 255, 255)
                canvas.SetPixel(16, 5, 54, 54, 54)
                canvas.SetPixel(17, 5, 54, 54, 54)
                canvas.SetPixel(18, 5, 54, 54, 54)
                canvas.SetPixel(19, 5, 133, 133, 133)
                canvas.SetPixel(20, 5, 54, 54, 54)
                canvas.SetPixel(21, 5, 133, 133, 133)
                canvas.SetPixel(22, 5, 133, 133, 133)
                canvas.SetPixel(23, 5, 23, 23, 23)
                canvas.SetPixel(8, 6, 23, 23, 23)
                canvas.SetPixel(9, 6, 179, 179, 179)
                canvas.SetPixel(10, 6, 255, 255, 255)
                canvas.SetPixel(11, 6, 54, 54, 54)
                canvas.SetPixel(12, 6, 255, 255, 255)
                canvas.SetPixel(13, 6, 54, 54, 54)
                canvas.SetPixel(14, 6, 255, 255, 255)
                canvas.SetPixel(15, 6, 133, 133, 133)
                canvas.SetPixel(16, 6, 107, 107, 107)
                canvas.SetPixel(17, 6, 179, 179, 179)
                canvas.SetPixel(18, 6, 214, 214, 214)
                canvas.SetPixel(19, 6, 133, 133, 133)
                canvas.SetPixel(20, 6, 13, 13, 13)
                canvas.SetPixel(21, 6, 54, 54, 54)
                canvas.SetPixel(22, 6, 54, 54, 54)
                canvas.SetPixel(23, 6, 54, 54, 54)
                canvas.SetPixel(8, 7, 0, 0, 0)
                canvas.SetPixel(9, 7, 214, 214, 214)
                canvas.SetPixel(10, 7, 13, 13, 13)
                canvas.SetPixel(11, 7, 133, 133, 133)
                canvas.SetPixel(12, 7, 214, 214, 214)
                canvas.SetPixel(13, 7, 54, 54, 54)
                canvas.SetPixel(14, 7, 54, 54, 54)
                canvas.SetPixel(15, 7, 54, 54, 54)
                canvas.SetPixel(16, 7, 255, 255, 255)
                canvas.SetPixel(17, 7, 54, 54, 54)
                canvas.SetPixel(18, 7, 54, 54, 54)
                canvas.SetPixel(19, 7, 13, 13, 13)
                canvas.SetPixel(20, 7, 54, 54, 54)
                canvas.SetPixel(21, 7, 133, 133, 133)
                canvas.SetPixel(22, 7, 107, 107, 107)
                canvas.SetPixel(23, 7, 23, 23, 23)
                canvas.SetPixel(8, 8, 255, 255, 255)
                canvas.SetPixel(9, 8, 54, 54, 54)
                canvas.SetPixel(10, 8, 54, 54, 54)
                canvas.SetPixel(11, 8, 54, 54, 54)
                canvas.SetPixel(12, 8, 54, 54, 54)
                canvas.SetPixel(13, 8, 13, 13, 13)
                canvas.SetPixel(14, 8, 13, 13, 13)
                canvas.SetPixel(15, 8, 54, 54, 54)
                canvas.SetPixel(16, 8, 13, 13, 13)
                canvas.SetPixel(17, 8, 54, 54, 54)
                canvas.SetPixel(18, 8, 54, 54, 54)
                canvas.SetPixel(19, 8, 13, 13, 13)
                canvas.SetPixel(20, 8, 54, 54, 54)
                canvas.SetPixel(21, 8, 255, 255, 255)
                canvas.SetPixel(22, 8, 23, 23, 23)
                canvas.SetPixel(23, 8, 255, 255, 255)
                canvas.SetPixel(8, 9, 255, 255, 255)
                canvas.SetPixel(9, 9, 54, 54, 54)
                canvas.SetPixel(10, 9, 0, 0, 0)
                canvas.SetPixel(11, 9, 0, 0, 0)
                canvas.SetPixel(12, 9, 0, 0, 0)
                canvas.SetPixel(13, 9, 0, 0, 0)
                canvas.SetPixel(14, 9, 0, 0, 0)
                canvas.SetPixel(15, 9, 0, 0, 0)
                canvas.SetPixel(16, 9, 39, 39, 39)
                canvas.SetPixel(17, 9, 54, 54, 54)
                canvas.SetPixel(18, 9, 255, 255, 255)
                canvas.SetPixel(19, 9, 13, 13, 13)
                canvas.SetPixel(20, 9, 255, 255, 255)
                canvas.SetPixel(21, 9, 133, 133, 133)
                canvas.SetPixel(22, 9, 0, 0, 0)
                canvas.SetPixel(23, 9, 255, 255, 255)
                canvas.SetPixel(8, 10, 0, 0, 0)
                canvas.SetPixel(9, 10, 133, 133, 133)
                canvas.SetPixel(10, 10, 54, 54, 54)
                canvas.SetPixel(11, 10, 54, 54, 54)
                canvas.SetPixel(12, 10, 255, 255, 255)
                canvas.SetPixel(13, 10, 54, 54, 54)
                canvas.SetPixel(14, 10, 255, 255, 255)
                canvas.SetPixel(15, 10, 54, 54, 54)
                canvas.SetPixel(16, 10, 255, 255, 255)
                canvas.SetPixel(17, 10, 13, 13, 13)
                canvas.SetPixel(18, 10, 39, 39, 39)
                canvas.SetPixel(19, 10, 255, 255, 255)
                canvas.SetPixel(20, 10, 255, 255, 255)
                canvas.SetPixel(21, 10, 23, 23, 23)
                canvas.SetPixel(22, 10, 255, 255, 255)
                canvas.SetPixel(23, 10, 255, 255, 255)
                canvas.SetPixel(8, 11, 0, 0, 0)
                canvas.SetPixel(9, 11, 255, 255, 255)
                canvas.SetPixel(10, 11, 255, 255, 255)
                canvas.SetPixel(11, 11, 54, 54, 54)
                canvas.SetPixel(12, 11, 54, 54, 54)
                canvas.SetPixel(13, 11, 54, 54, 54)
                canvas.SetPixel(14, 11, 54, 54, 54)
                canvas.SetPixel(15, 11, 54, 54, 54)
                canvas.SetPixel(16, 11, 39, 39, 39)
                canvas.SetPixel(17, 11, 179, 179, 179)
                canvas.SetPixel(18, 11, 255, 255, 255)
                canvas.SetPixel(19, 11, 54, 54, 54)
                canvas.SetPixel(20, 11, 0, 0, 0)
                canvas.SetPixel(21, 11, 255, 255, 255)
                canvas.SetPixel(22, 11, 255, 255, 255)
                canvas.SetPixel(23, 11, 255, 255, 255)
                canvas.SetPixel(8, 12, 0, 0, 0)
                canvas.SetPixel(9, 12, 255, 255, 255)
                canvas.SetPixel(10, 12, 214, 214, 214)
                canvas.SetPixel(11, 12, 179, 179, 179)
                canvas.SetPixel(12, 12, 179, 179, 179)
                canvas.SetPixel(13, 12, 179, 179, 179)
                canvas.SetPixel(14, 12, 179, 179, 179)
                canvas.SetPixel(15, 12, 179, 179, 179)
                canvas.SetPixel(16, 12, 214, 214, 214)
                canvas.SetPixel(17, 12, 54, 54, 54)
                canvas.SetPixel(18, 12, 0, 0, 0)
                canvas.SetPixel(19, 12, 255, 255, 255)
                canvas.SetPixel(20, 12, 255, 255, 255)
                canvas.SetPixel(21, 12, 255, 255, 255)
                canvas.SetPixel(22, 12, 255, 255, 255)
                canvas.SetPixel(23, 12, 255, 255, 255)
                canvas.SetPixel(8, 13, 255, 255, 255)
                canvas.SetPixel(9, 13, 23, 23, 23)
                canvas.SetPixel(10, 13, 255, 255, 255)
                canvas.SetPixel(11, 13, 179, 179, 179)
                canvas.SetPixel(12, 13, 179, 179, 179)
                canvas.SetPixel(13, 13, 82, 82, 82)
                canvas.SetPixel(14, 13, 27, 27, 27)
                canvas.SetPixel(15, 13, 27, 27, 27)
                canvas.SetPixel(16, 13, 0, 0, 0)
                canvas.SetPixel(17, 13, 255, 255, 255)
                canvas.SetPixel(18, 13, 255, 255, 255)
                canvas.SetPixel(19, 13, 255, 255, 255)
                canvas.SetPixel(20, 13, 255, 255, 255)
                canvas.SetPixel(21, 13, 255, 255, 255)
                canvas.SetPixel(22, 13, 255, 255, 255)
                canvas.SetPixel(23, 13, 255, 255, 255)
                canvas.SetPixel(8, 14, 255, 255, 255)
                canvas.SetPixel(9, 14, 255, 255, 255)
                canvas.SetPixel(10, 14, 0, 0, 0)
                canvas.SetPixel(11, 14, 0, 0, 0)
                canvas.SetPixel(12, 14, 0, 0, 0)
                canvas.SetPixel(13, 14, 0, 0, 0)
                canvas.SetPixel(14, 14, 255, 255, 255)
                canvas.SetPixel(15, 14, 255, 255, 255)
                canvas.SetPixel(16, 14, 255, 255, 255)
                canvas.SetPixel(17, 14, 255, 255, 255)
                canvas.SetPixel(18, 14, 255, 255, 255)
                canvas.SetPixel(19, 14, 255, 255, 255)
                canvas.SetPixel(20, 14, 255, 255, 255)
                canvas.SetPixel(21, 14, 255, 255, 255)
                canvas.SetPixel(22, 14, 255, 255, 255)
                canvas.SetPixel(23, 14, 255, 255, 255)
                canvas.SetPixel(8, 15, 255, 255, 255)
                canvas.SetPixel(9, 15, 255, 255, 255)
                canvas.SetPixel(10, 15, 255, 255, 255)
                canvas.SetPixel(11, 15, 255, 255, 255)
                canvas.SetPixel(12, 15, 255, 255, 255)
                canvas.SetPixel(13, 15, 255, 255, 255)
                canvas.SetPixel(14, 15, 255, 255, 255)
                canvas.SetPixel(15, 15, 255, 255, 255)
                canvas.SetPixel(16, 15, 255, 255, 255)
                canvas.SetPixel(17, 15, 255, 255, 255)
                canvas.SetPixel(18, 15, 255, 255, 255)
                canvas.SetPixel(19, 15, 255, 255, 255)
                canvas.SetPixel(20, 15, 255, 255, 255)
                canvas.SetPixel(21, 15, 255, 255, 255)
                canvas.SetPixel(22, 15, 255, 255, 255)
                canvas.SetPixel(23, 15, 255, 255, 255)
                self.matrix.SwapOnVSync(canvas)
                time.sleep(1)
            elif self.display_state == self.STATE_TASK_RUNNING:
                canvas = self.matrix.CreateFrameCanvas()
                graphics.DrawText(canvas, self.message_font, 16, 7, self.message_color, self.display_info['project_code'])
                graphics.DrawText(canvas, self.hours_font, 0, 16, self.hours_color, str(self.display_info['task_hours']))
                # graphics.DrawText(canvas, self.total_hours_font, 28, 16, self.total_hours_color, str(int(self.display_info['total_hours'])))
                self.matrix.SwapOnVSync(canvas)
                time.sleep(.5)
        self.matrix.Clear()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('company_name')
    parser.add_argument('email')
    parser.add_argument('password')
    options = parser.parse_args()

    # 1. Start display process
    matrix = Matrix()
    matrix.display_info['message'] = 'Loading'
    matrix.display_state = Matrix.STATE_MESSAGE
    matrix_thread = Thread(target=matrix.run)
    matrix_thread.start()

    # 2. Start getting harvest information
    harvest_client = harvest.Harvest("https://" + options.company_name + ".harvestapp.com", options.email,
                                     options.password)

    # Cache all projects keyed by project id
    project_codes = {}
    harvest_projects = harvest_client.projects()
    for project_entry in harvest_projects:
        if 'code' in project_entry['project']:
            project_codes[int(project_entry['project']['id'])] = project_entry['project']['code']

    del harvest_projects

    try:
        while True:
            matrix.display_info['total_hours'] = 0.0
            running_entry = False
            for entry in harvest_client.today['day_entries']:
                matrix.display_info['total_hours'] += float(entry['hours'])
                if 'timer_started_at' in entry:
                    running_entry = entry
            if running_entry:
                matrix.display_info['project_code'] = project_codes[int(running_entry['project_id'])]
                matrix.display_info['task_hours'] = running_entry['hours']
                matrix.display_state = Matrix.STATE_TASK_RUNNING

            else:
                matrix.display_state = Matrix.STATE_NO_TASK
        time.sleep(5)

    except (KeyboardInterrupt, SystemExit):
        matrix.display_state = Matrix.STATE_END
        matrix_thread.join()
        sys.exit(0)

    matrix.display_state = Matrix.STATE_END
    matrix_thread.join()


if __name__ == "__main__":
    main()
