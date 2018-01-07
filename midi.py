import sys
import os

import pyautogui
import directkeys

from time import sleep
from win32gui import GetWindowText, GetForegroundWindow


import pygame
import pygame.midi
from pygame.locals import *

pyautogui.PAUSE = 0.01

timelast = 0

NotePressArray = 100 * [0]
KeyToNoteDictWhite = {
24:0x02,26:0x03,28:0x04,29:0x05,31:0x06,33:0x07,35:0x08,
36:0x09,38:0x0A,40:0x0B,41:0x10,43:0x11,45:0x12,47:0x13,
48:0x14,50:0x15,52:0x16,53:0x17,55:0x18,57:0x19,59:0x1E,
60:0x1F,62:0x20,64:0x21,65:0x22,67:0x23,69:0x24,71:0x25,
72:0x26,74:0x2C,76:0x2D,77:0x2E,79:0x2F,81:0x30,83:0x31
}

KeyToNoteDictBlack = {
25:0x02,27:0x03,30:0x05,32:0x06,34:0x07,
37:0x09,39:0x0A,42:0x10,44:0x11,46:0x12,
49:0x14,51:0x15,54:0x17,56:0x18,58:0x19,
61:0x1F,63:0x20,66:0x22,68:0x23,70:0x24,
73:0x26,75:0x2C,78:0x2E,80:0x2F,82:0x30}

def print_device_info():
    pygame.midi.init()
    _print_device_info()
    pygame.midi.quit()

def _print_device_info():
    for i in range( pygame.midi.get_count() ):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print ("%2i: interface :%s:, name :%s:, opened :%s:  %s" %
               (i, interf, name, opened, in_out))

def input_main(device_id = None):
    pygame.init()
    pygame.fastevent.init()
    event_get = pygame.fastevent.get
    event_post = pygame.fastevent.post

    pygame.midi.init()

    _print_device_info()


    if device_id is None:
        input_id = pygame.midi.get_default_input_id()
    else:
        input_id = device_id

    print ("using input_id :%s:" % input_id)
    i = pygame.midi.Input( input_id )

    pygame.display.set_mode((1,1))


    threshold = 0
    going = True
    while going:
        sleep(0.001)
        events = event_get()
        if "arry" in GetWindowText(GetForegroundWindow()):
            for e in events:
                print(e)
                if e.type in [QUIT]:
                    going = False
                if e.type in [KEYDOWN]:
                    going = False
                if e.type in [pygame.midi.MIDIIN] and e.data1 in KeyToNoteDictWhite and e.data2>threshold:
                    print (e)
                    directkeys.PressKey(KeyToNoteDictWhite[e.data1])						
                    print("Regular Key down")
            sleep(0.015)
            for e in events:
                if e.type in [QUIT]:
                    going = False
                if e.type in [KEYDOWN]:
                    going = False
                if e.type in [pygame.midi.MIDIIN] and e.data1 in KeyToNoteDictWhite and e.data2>threshold:
                    print (e)					
                    directkeys.ReleaseKey(KeyToNoteDictWhite[e.data1])
                    print("Regular Key up")	
            sleep(0.005)				
            for e in events:
                if e.type in [QUIT]:
                    going = False
                if e.type in [KEYDOWN]:
                    going = False
                if e.type in [pygame.midi.MIDIIN] and e.data1 in KeyToNoteDictBlack and e.data2>threshold:
                    print (e)
                    print("black")
                    print("Shift Key Down")
                    directkeys.PressKey(0x36)
                    sleep(0.01)
                    directkeys.PressKey(KeyToNoteDictBlack[e.data1])
            sleep(0.015)
            for e in events:
                if e.type in [QUIT]:
                    going = False
                if e.type in [KEYDOWN]:
                    going = False
                if e.type in [pygame.midi.MIDIIN] and e.data1 in KeyToNoteDictBlack and e.data2>threshold:
                    directkeys.ReleaseKey(KeyToNoteDictBlack[e.data1])                        
                    directkeys.ReleaseKey(0x36)
                    print("Shift Key Up")
            sleep(0.005)
        for e in events:
            if e.type in [QUIT]:
                going = False
            if e.type in [KEYDOWN]:
                going = False
        if i.poll():
            midi_events = i.read(5)
            # convert them into pygame events.
            midi_evs = pygame.midi.midis2events(midi_events, i.device_id)

            for m_e in midi_evs:
                event_post( m_e )

    del i
    pygame.midi.quit()
	
def main(mode='input', device_id=None):
    """Run a Midi example
    Arguments:
    mode - if 'output' run a midi keyboard output example
              'input' run a midi event logger input example
              'list' list available midi devices
           (default 'output')
    device_id - midi device number; if None then use the default midi input or
                output device for the system
    """
    directkeys.ReleaseKey(0x36)
    if mode == 'input':
        input_main(device_id)
    elif mode == 'output':
        output_main(device_id)
    elif mode == 'list':
        print_device_info()
    else:
        raise ValueError("Unknown mode option '%s'" % mode)

main()
