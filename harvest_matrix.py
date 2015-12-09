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
                graphics.DrawCircle(canvas, 16, 8, 5, self.red_color)
                graphics.DrawLine(canvas, 16, 8, 16, 4, self.red_color)
                graphics.DrawLine(canvas, 16, 8, 18, 10, self.red_color)
                # graphics.DrawText(canvas, self.total_hours_font, 28, 16, self.total_hours_color, str(int(self.display_info['total_hours'])))
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
