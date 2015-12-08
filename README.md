

## Installation

1. Install python-harvest library:
```bash
sudo python ./python-harvest/setup.py install
```
1. Make any changes need in ./rpi-rbg-led-matrix/lib/Makefile
1. Install rpi-rgb-led-matrix library:  
```bash
cd ./rpi-rgb-led-matrix
make
make build-python
sudo make install-python
sudo python ./rpi-rgb-led-matrix/python/setup.py install
```
