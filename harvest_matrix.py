#!/usr/bin/env python
from rgbmatrix import RGBMatrix
from rgbmatrix import graphics
import time
import harvest
from multiprocessing import Process, Manager
import argparse


class Matrix(object):
    STATE_STOPPED = 0
    STATE_STARTED = 1
    STATE_NO_TASK = 2
    STATE_TASK_RUNNING = 3

    def __init__(self):
        self.displayState = self.STATE_STOPPED
        self.projectCode = ''
        self.taskHours = 0.0
        self.width = 32
        self.height = 16
        self.matrix = RGBMatrix(self.height, 1, 1)

    def run(self, state):
        while True:
            print(state['state'])
            if self.displayState == self.STATE_STOPPED:
                print("Run:State Stopped")
                # self.matrix.Fill(255, 0, 0)
                # time.sleep(5)
                # self.matrix.Clear()
                # self.matrix.Fill(0, 255, 0)
                # time.sleep(5)
                # self.matrix.Clear()
                canvas = self.matrix.CreateFrameCanvas()
                font = graphics.Font()
                font.LoadFont("./rpi-rgb-led-matrix/fonts/5x7.bdf")
                textColor = graphics.Color(255, 255, 0)
                myText = "stopped"
                graphics.DrawText(canvas, font, 0, 10, textColor, myText);
                self.matrix.SwapOnVSync(canvas)
            elif self.displayState == self.STATE_STARTED:
                print("Run:State Stopped")
                canvas = self.matrix.CreateFrameCanvas()
                font = graphics.Font()
                font.LoadFont("./rpi-rgb-led-matrix/fonts/5x7.bdf")
                textColor = graphics.Color(255, 255, 0)
                myText = "Started"
                graphics.DrawText(canvas, font, 0, 10, textColor, myText);
                self.matrix.SwapOnVSync(canvas)
            elif self.displayState == self.STATE_NO_TASK:
                pass
            elif self.displayState == self.STATE_TASK_RUNNING:
                pass

#
# def matrix_process():
#     matrix = Matrix()
#
#     while True:
#         matrix.run()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('company_name')
    parser.add_argument('email')
    parser.add_argument('password')
    options = parser.parse_args()
    print(options)

    matrix = Matrix()

    manager = Manager()
    state = manager.dict()

    state['status'] = "old"
    state['projectCode'] = ''
    state['taskHours'] = 0.0

    # 1. Start display process
    matrix_process = Process(target=matrix.run, args=(state,))
    matrix_process.start()
    time.sleep(2)
    state['status'] = "new"
    time.sleep(2)
    state['status'] = "newwer"

    matrix_process.join()


    # 2. Start geting harvest information


if __name__ == "__main__":
    main()
