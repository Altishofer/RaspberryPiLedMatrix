[![GitHub issues](https://img.shields.io/github/issues/Altishofer/raspberryPiLedMatrix.svg)](https://github.com/Altishofer/raspberryPiLedMatrix/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/Altishofer/raspberryPiLedMatrix.svg)](https://github.com/Altishofer/raspberryPiLedMatrix/pulls)

# Rpi Led Matrix: 
🎉 990 Pixel Led Matrix 🎉

The LED matrix features 990 ping pong balls adorned with WS2811 single controlled RGB LEDs running on very simple hardware. Originally designed for a traditional carnival festival, this project brings vibrant colors and dynamic patterns to life. Whether you're building your own LED matrix or contributing to the project, this guide provides essential high level information to get you started.

<span> 
<img src="https://github.com/Altishofer/raspberryPiLedMatrix/blob/main/readmeImages/WireLedsSnakePattern.jpg" height="200" alt="WireLedsSnakePattern"/>
<img src="https://github.com/Altishofer/raspberryPiLedMatrix/blob/main/readmeImages/DebugSoftware.jpg" height="200" alt="DebugSoftware"/> 
 
</span>

### Features
- coded in a simplistic way for python newbies
- Colorful shell emulator for coding without being connected to the matrix
- many different creative patterns and the toolset to add more
- coded using Multiprocessing to separate processes for increased stability
- Excel with VBA macros for designing letters/numbers and exporting them into the code

## Installation and Setup

### Hardware
- A Raspberry Pi model (3B+ or higher)
- 990x WS2811 DC5V RGB LED 1.2x15cm IP68 (240$)
- DC5V 70Amps (350W) power supply, active cooled (25$) 
- A level shifter to convert 3.3V to 5V for the LED data signal (optional 5$)
- 990 white ping pong balls without logo (40$)

### Instructions
- use fire proof board which has space for 18x55 ping pong balls plus frame
- drill 990 holes so that all balls nearly touch each others
- drill holes into the balls and glue them over the drilled holes
- plug LEDs into drilled holes (snake pattern along the whole board)
- solder all data pins of the LED stripes together (check polarity direction again)
- solder blocks of 2-3 LED stripes together (more parallel power source increases brightnes)
- connect power source to soldered LED stripes in parallel (use cables for min 70 Amps)
- Connect the data input of the LED strip to GPIO18 of the Raspberry Pi (level shifter)
- set brightness to minimum in code and start testing the wiring

### Raspberry Pi Configuration

1. Clone this repository to your local machine:
  ```shell
  git clone https://github.com/Altishofer/GuessMyWord.git
  ```
2. disable PWM channel for sound on GPIO18
  ```console
  sudo nano /boot/config.txt
  # change "dtparam=audio=on" to "dtparam=audio=off" 
  ```
3. reboot
 ```console
 sudo reboot
 ```
4. Install dependencies
 ```console
 sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
 ```
 ```console
 sudo python3 -m pip install --force-reinstall adafruit-blinka
 ```
___
### Troubleshooting
#### Got a rare Rpi revision (e.g. 3B 1.2) which is not compatible with rpi_ws281x library
 ```console
 foo@bar:~ws2811_init failed with code -3 (Hardware revision is not supported)
 ```
 follow description [https://github.com/jgarff/rpi_ws281x/issues/483](https://github.com/jgarff/rpi_ws281x/issues/483)

#### no permission to execute file
```console
sudo chown -R pi ~/SraLedMatrix/
```
___
### Run matrix
```console
sudo python3 raspberryPiLedMatrix/ledMatrix.py
```
___
## Impressions

<span>
 <img src="https://github.com/Altishofer/raspberryPiLedMatrix/blob/main/readmeImages/AddPingPongBallsPlexiCover.jpg" height="200" alt="Add Ping Pong Balls and Plexiglass Cover"/>
 <img src="https://github.com/Altishofer/raspberryPiLedMatrix/blob/main/readmeImages/CoverBackFireSafety.jpg" height="200" alt="Cover Back of Matrix Fire Proof"/> 
</span>

