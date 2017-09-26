#!/usr/bin/env python
# -*- coding: utf-8 -*-
# writen for python 2.7

# should reset a ciscos password and configuration if plugged into a 2911
# router when it is rebooting
# EDIT THE TWO port= LINES IF YOUR COM PORT IS DIFFERENT
import serial
import subprocess
import shlex

#baudrate = get_baudrate('COM1') # linux

console = serial.Serial(
        port='COM1', #windows
        #port='/dev/ttyUSB0', #what I expect it to be on Linux, dmesg when you plug in to find out
        baudrate=9600, #default baudrate
        parity='N', #default parity
        stopbits=1, #default stopbits
        bytesize=8, #default bytesize
        timeout=8
)

print(console.isOpen())

#wait until break will do something
startup_text = ''
while 'program load complete,' not in startup_text:
    startup_text += console.read(console.inWaiting())

#send break command
while 'rommon' not in startup_text:
    console.send_break()
    startup_text += console.read(console.inWaiting())
    print(startup_text)

#make sure we enter rommon and set config register
if 'rommon' in startup_text:
    print("entered rommon")
    console.write('flash_init\r\n')
    print("flash_init")
    console.write('load_helper\r\n')
	print('load_helper')
	console.write('rename flash:config.txt flash:config.old\r\n')
	print('renamed config')
	console.write('boot')
    print("booting")

print("entering boot read loop")
#watch for the initialization prompt
startup_text = ''
while '[yes/no]:' not in startup_text:
    startup_text += console.read(console.inWaiting())

print("Removing the current configuration")
#reset the device
console.write('no\r\n')

print("waiting for Router>")
startup_text = ''
while 'Router>' not in startup_text:
    console.write('\r\n')
    startup_text += console.read(console.inWaiting())
print(startup_text)

console.write('enable\r\n')
console.write('delete flash:config.old\r\n')
console.write('\r\n')
console.write('\r\n')
console.write('write erase\r\n')
console.write('\r\n')
console.write('\r\n')
print(console.read(console.inWaiting()))
console.write('reload\r\n')
console.write('no\r\n')
print("completed")
#console.write('...\r\n') #\r\n is windows syntax? need to write a break

def get_baudrate(device):
    command = 'stty < {0}'.format(device)
    proc_retval = subprocess.check_output(shlex.split(command))
    baudrate = int(proc_retval.split()[1])
    return baudrate
