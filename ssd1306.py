
'''
    Basic ssd1306 interface.
    Pinouts-
    oled_brkout header
        +3.3    |CS
        RST     |DC
        R/W     |E/RD
        SCLK    |MOSI
        NC      |NC
        NC      |NC
        NC      |NC
        GND     |GND

    bus pirate connections to it
        3.3V-RD |CS-WT
        NC?     |AUX-BL
        NC      |NC
        SCK-PU  |MOSI-GR
        NC      |NC
        NC      |NC
        NC      |NC
        GND-BR  |NC
'''

import serial
import time
import sys

#dp logo
screenDataFruit = [
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x80,0x00,0xBC,0x3C,0xED,0x0D,0xE5,0x34,0xB4,0x00,0xC0,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x80,0xE0,0xC0,0x8E,0x8F,0xC1,0xE4,0xC3,0xEF,0xE1,0xE4,0x01,0xEF,0xDB,0x84,0x8F,0x2F,0x6E,0x78,0xE0,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x60,0xC0,0x98,0x13,0x27,0x4F,0x9F,0x3F,0x7F,0x3F,0x0F,0x07,0x07,0x03,0x03,0x02,0x06,0x06,0x1C,0x31,0x77,0xB7,0x30,0x39,0x7F,0xFF,0x3C,0xD8,0x60,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xF0,0xB4,0xE3,0x09,0xE6,0xBC,0xE1,0x0B,0x06,0x1C,0x09,0x01,0x00,0x00,0x00,0x00,0x60,0xF8,0xFC,0xF8,0xF8,0x00,0x00,0x00,0x00,0x01,0x0F,0x1F,0x20,0x09,0xE4,0xBB,0xE4,0x09,0x07,0xB8,0xF0,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xC0,0x60,0x20,0x94,0x94,0x96,0x93,0xD1,0xC8,0x6C,0x3C,0x0D,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x7F,0xFF,0xFF,0x07,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x03,0x09,0x1C,0x7E,0xFE,0xFF,0xFE,0xFF,0xFE,0xFC,0xF8,0xE0,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x80,0xC0,0x20,0x91,0xC8,0xC8,0xD6,0x3E,0x01,0x01,0x1E,0x06,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x3F,0x1F,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x06,0x1E,0x21,0xC1,0xBE,0x76,0xC1,0x81,0x1E,0x36,0x70,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xC0,0xF0,0xF8,0xFA,0x39,0x19,0xC0,0x79,0xCD,0xD3,0x13,0xFC,0xC3,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x18,0x3C,0x7C,0x3C,0x38,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x80,0xC3,0x99,0x66,0x85,0x08,0x99,0x62,0x85,0x66,0x98,0x18,0xE0,0xC0,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x78,0x7C,0x7F,0x7F,0x7F,0xFF,0xFF,0xFE,0xFE,0xFC,0xFC,0xFE,0x86,0x00,0x6F,0x6F,0x01,0x03,0x6C,0x6E,0x28,0x82,0x2C,0x6E,0x6C,0x02,0x00,0x6E,0x6E,0x02,0x02,0x6C,0x6E,0x00,0x86,0xFE,0xFE,0x7E,0x7E,0x7E,0xFE,0xB8,0x82,0x82,0xB8,0xFE,0x7E,0xFE,0xFC,0xAA,0x80,0x82,0xF8,0xFE,0x7F,0xFF,0x71,0x00,0x02,0x73,0xF9,0xFE,0xFF,0xF8,0x73,0x02,0x04,0xF0,0xFD,0xFB,0x72,0x74,0x20,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
]

screenDataFruit = ["0x%02X"%i for i in screenDataFruit]

def sendCmd(cmdstr):
    pirate.write(bytes(cmdstr))
    time.sleep(0.05)

def sendCmdWithEcho(cmdstr):
    # purge
    while pirate.inWaiting() != 0:
        ch = pirate.read()

    # write the command
    pirate.write(bytes(cmdstr))
    time.sleep(0.05)

    outstr = ''
    while pirate.inWaiting() != 0:
        ch = pirate.read()
        if ch:
            outstr += ch
        else:
            break
    return outstr

def initializeBusPirate():
    # reset
    print sendCmdWithEcho("#\n")
    # mode
    sendCmd("m\n")
    # 5=spi
    sendCmd("5\n")
    # 4=1MHz
    sendCmd("4\n")
    # clock polarity idle low
    sendCmd("1\n")
    # output clock edge idle to active
    sendCmd("2\n")
    # input sample phase middle
    sendCmd("1\n")
    # /CS
    sendCmd("2\n")
    # output normal i/o levels
    sendCmd("2\n")

    # turn on 3.3v supply
    sendCmd("W\n")

    # assign aux to aux
    sendCmdWithEcho("c\n")

def initializeSSD1306():
    initStr = "[0xAE 0xD5 0x80 0xA8 0x3F 0xD3 0x00 0x40 0x8D 0x14 0x20 0x00 0xA1 0xC8 0xDA 0x12 0x81 0xCF 0xD9 0xF1 0xDB 0x40 0xA4 0xA6 0xAF]\n"

    # aux low for cmd
    sendCmdWithEcho("a\n")
    # initialization
    sendCmdWithEcho(initStr)

    # send the default screen, from adafruit
    # set low/high column and start line
    sendCmdWithEcho("[0x00 0x10 0x40\n")

    # aux high for data
    sendCmdWithEcho("A\n")

    for i in zip(*[iter(screenDataFruit)]*32):
        sendCmdWithEcho(' '.join(i) + '\n')
    sendCmdWithEcho("]\n")

# open the com port
portname = "COM25"
if len(sys.argv) > 1:
    portname = sys.argv[1]
pirate = serial.Serial(portname, 115200, interCharTimeout=0.05)

# setup for spi mode, turn on pwr supply
initializeBusPirate()

# init ssd1306
initializeSSD1306()

### turn off pwr
##sendCmd("w\n")
### reset the bus pirate
##sendCmd("#\n")

pirate.close()
