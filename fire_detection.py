#!/usr/bin/python
# encoding:utf-8
import RPi.GPIO as GPIO
import time


Buzzer = 11

CL = [0, 131, 147, 165, 175, 196, 211, 248]     # Frequency of Low C notes

CM = [0, 262, 294, 330, 350, 393, 441, 495]     # Frequency of Middle C notes

CH = [0, 525, 589, 661, 700, 786, 882, 990]     # Frequency of High C notes

song_1 = [  CM[3], CM[5], CM[6], CM[3], CM[2], CM[3], CM[5], CM[6], # Notes of song1
            CH[1], CM[6], CM[5], CM[1], CM[3], CM[2], CM[2], CM[3], 
            CM[5], CM[2], CM[3], CM[3], CL[6], CL[6], CL[6], CM[1],
            CM[2], CM[3], CM[2], CL[7], CL[6], CM[1], CL[5] ]

beat_1 = [  1, 1, 3, 1, 1, 3, 1, 1,             # Beats of song 1, 1 means 1/8 beats
            1, 1, 1, 1, 1, 1, 3, 1, 
            1, 3, 1, 1, 1, 1, 1, 1, 
            1, 2, 1, 1, 1, 1, 1, 1, 
            1, 1, 3 ]

song_2 = [  CM[1], CM[1], CM[1], CL[5], CM[3], CM[3], CM[3], CM[1], # Notes of song2
            CM[1], CM[3], CM[5], CM[5], CM[4], CM[3], CM[2], CM[2], 
            CM[3], CM[4], CM[4], CM[3], CM[2], CM[3], CM[1], CM[1], 
            CM[3], CM[2], CL[5], CL[7], CM[2], CM[1]    ]

beat_2 = [  1, 1, 2, 2, 1, 1, 2, 2,             # Beats of song 2, 1 means 1/8 beats
            1, 1, 2, 2, 1, 1, 3, 1, 
            1, 2, 2, 1, 1, 2, 2, 1, 
            1, 2, 2, 1, 1, 3 ]
pin_fire=27
G = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_fire, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(G, GPIO.OUT)
GPIO.setup(Buzzer, GPIO.OUT)    # Set pins' mode is output
global Buzz                     # Assign a global variable to replace GPIO.PWM
Buzz = GPIO.PWM(Buzzer, 440)    # 440 is initial frequency.
Buzz.start(50) 
try:
    while True:
        status = GPIO.input(pin_fire)
        if status == True:
            print('没有检测到火')
            GPIO.output(G, False)
            time.sleep(0.25)
        else:
            print('检测到火灾')
            GPIO.output(G, True)  # AIN1
            Buzz.ChangeFrequency(song_1[i]) # Change the frequency along the song note
            time.sleep(beat_1[i] * 0.5)     # delay a note for beat * 0.5s
            if i < 10:
                i = i+1
            else:
                i = 0
except KeyboradInterrupt:
    GPIO.cleanup()