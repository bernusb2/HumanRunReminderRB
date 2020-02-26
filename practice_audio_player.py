# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 11:22:24 2020

@author: bernusb2
"""
import pyglet

def playAlarm(Audio):
    Audio.play()
    pyglet.app.run()
    return;
    
Alarm = pyglet.media.load('HomeMadeAlarm.mp3')
ClampAudio = pyglet.media.load('ClampingAudio.mp3')
SalineAudio = pyglet.media.load('SalineAudio.mp3')

playAlarm(ClampAudio)
