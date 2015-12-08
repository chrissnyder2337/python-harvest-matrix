#!/usr/bin/env python
from rgbmatrix import RGBMatrix
import time
import harvest
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('company_name')
    parser.add_argument('email')
    parser.add_argument('password')
    options = parser.parse_args()

    print(options)
    # 1. Start display process

    # 2. Start geting harvest information

if __name__ == "__main__":
    main()
