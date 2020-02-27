# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 17:44:52 2020

@author: bernusb2
"""
#Run this block if this is your first time and you need the libraries:
#pip install pyglet==1.3.2
#pip install selenium
#pip install pycaw


##This block will turn your speakers to full blast in case you were muted
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume.GetMute()
volume.GetMasterVolumeLevel()
volume.GetVolumeRange()
volume.SetMasterVolumeLevel(-0.0, None)


    
##Now, we will use the webscraper to watch the values in the DEO and alarm when ready
import pyglet
from time import sleep
Alarm = pyglet.media.load('HomeMadeAlarm.mp3')
ClampAudio = pyglet.media.load('ClampingAudio.mp3')
SalineAudio = pyglet.media.load('SalineAudio.mp3')

#Function that will play the song
def playAlarm(Audio):
    Audio.play()
    pyglet.app.run()
    return;

from selenium import webdriver
driver = webdriver.Chrome()
driver.get("http://172.21.127.255/deo.html")
sleep(10) #Allow the page to load for 10 seconds
PlsValve_element = driver.find_element_by_id('PlasmaValveCapRepoDisposableValveStatus._valveState.Value')
SValve_element = driver.find_element_by_id('SalineValveCapRepoDisposableValveStatus._valveState.Value')

while(1):
    ret_speed_elem = driver.find_element_by_id('ReturnPumpCapRepoDisposablePumpCommands._speedMlPerMin.Value')
    ac_speed_elem = driver.find_element_by_id('AcPumpCapRepoDisposablePumpCommands._speedMlPerMin.Value')
    ret_speed_cmds = float(ret_speed_elem.text)
    ac_speed_cmds = float(ac_speed_elem.text)
    ##Wait until AC Pump and Return Pump are both commanded on at the same time to show we are in fluidprime
    if (ac_speed_cmds > 5) and (ret_speed_cmds > 5):
        print('ret_speed_cmds')
        ret_speed_cmds = float(ret_speed_elem.text)
        if ret_speed_cmds < 1:
            print('Mark Saline Line')
            playAlarm(Alarm)
            break

##Wait to watch all of those elements until we have entered the first Draw (evidenced by Cent Motor at full speed)
while (1):
    sleep(5)
    CentStat_element = driver.find_element_by_id('CentrifugeCentrifugeMotorStatus._commandedRpm.Value')
    CentStatRpm = int(CentStat_element.text)
    if CentStatRpm > 4000:
        print('Centrifuge has passed 4000 and we are in the middle of the run')
        break
    
##Watch for the point when the saline valve is open, plasma valve is closed, and cent commanded to zero
while (1):
    sleep(0.125)
    CentStat_element = driver.find_element_by_id('CentrifugeCentrifugeMotorStatus._commandedRpm.Value')
    CentStatRpm = int(CentStat_element.text)
    PlsValve_element = driver.find_element_by_id('PlasmaValveCapRepoDisposableValveStatus._valveState.Value')
    SValve_element = driver.find_element_by_id('SalineValveCapRepoDisposableValveStatus._valveState.Value')
    print(CentStatRpm)
    print(PlsValve_element.text)
    print(SValve_element.text)

    if(("Closed" in PlsValve_element.text) and ("Opened" in SValve_element.text) and (CentStatRpm==0)):
        print('PlayClampAlarm')
        playAlarm(Alarm)
        print('BREAK')
        break

#Play the song because it is now time to flip the clamps. 
print('Run Complete')
    
    
    