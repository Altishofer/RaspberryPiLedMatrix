[![GitHub issues](https://img.shields.io/github/issues/Altishofer/SraLedMatrix.svg)](https://github.com/Altishofer/SraLedMatrix/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/Altishofer/SraLedMatrix.svg)](https://github.com/Altishofer/SraLedMatrix/pulls)

# SraLedMatrix: 
🎉 990 Pixel Led Matrix 🎉

![SraLedMatrix]

This project is a LED matrix of 990 ping pong balls with WS2811 (RGB) LEDs. It was created for a traditional carnival festival in Switzerland. The LED matrix can display various animations and patterns, controlled by a Raspberry Pi.

## Installation and Setup

### Hardware

- A Raspberry Pi model with GPIO pins
- A WS2811 LED strip with 990 LEDs
- A 5V power supply for the LED strip
- A level shifter to convert 3.3V to 5V for the LED data signal
- A lot of ping pong balls and a frame to hold them

### Billboard
- Connect the power supply to the LED strip, following the polarity of the wires
- Connect the data input of the LED strip to GPIO18 of the Raspberry Pi, using a level shifter
- Cut holes in the ping pong balls and insert the LEDs into them
- Arrange the ping pong balls in a 18x55 matrix on a frame

## Overview

The **SraLedMatrix** project is a mesmerizing LED matrix featuring 990 ping pong balls adorned with WS2811 RGB LEDs. Originally designed for a traditional carnival festival, this project brings vibrant colors and dynamic patterns to life. Whether you're building your own LED matrix or contributing to the project, this guide provides essential information to get you started.

## Installation

Follow these steps to set up the project:

### Raspberry Pi Configuration

1. Clone this repository to your local machine:

 ```shell
 git clone https://github.com/Altishofer/GuessMyWord.git
 ```
2. sound must be disabled on GPIO18 -> else segmentation fault
```console
sudo nano /boot/config.txt
```
change "dtparam=audio=on" to "dtparam=audio=off" 
ctrl+s (save) -> ctrl+x (exit)
```console
sudo reboot
```
3. Install dependencies
```console
foo@bar:~$ sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
```console
```
foo@bar:~$ sudo pip3 install rpi-ws281x
```console
foo@bar:~$ sudo python3 -m pip install --force-reinstall adafruit-blinka
```

## Trouble Shooting
### Hardware is rare revision and not yet registered in library ([described here]([https://www.gatsbyjs.com](https://github.com/jgarff/rpi_ws281x/issues/483)))

```console
foo@bar:~$ ws2811_init failed with code -3 (Hardware revision is not supported)
```
Must clone repository and add to c file
```console
pip uninstall rpi_ws281x
```
```console
sudo reboot
```
```console
cat /proc/cpuinfo
```
Hardware	: BCM2711
Revision	: a52082
Serial		: 100000000ed9a28c
Model		: Raspberry Pi 3 Model B Rev 1.2
```console
git clone --recurse-submodules https://github.com/rpi-ws281x/rpi-ws281x-python
```console
sudo nano rpi-ws281x-python/library/lib/rpihw.c
```
search for simila entry (Model) and add element with cpuinfo
```console

{
    .hwver  = 0xa52082,
    .type = RPI_HWVER_TYPE_PI2,
    .periph_base = PERIPH_BASE_RPI2,
    .videocore_base = VIDEOCORE_BASE_RPI2,
    .desc = "Raspberry Pi 3 Model B Rev 1.2"
}
```
ctrl+s (save) -> ctrl+x (exit)
```console
cd rpi-ws281x-python/library/
```
```console
sudo python3 setup.py install
```
```console
sudo reboot
```
should work now :)

### no permission to edit file?
```console
sudo chown -R pi ~/SraLedMatrix/
```

##Impressions

![SraLedMatrix](path/to/your/image.jpg)
