#!/usr/bin/env python
# coding=utf-8

import curses
import serial
import time

if __name__ == "__main__":
    # setup serial
    ser = serial.Serial('/dev/cu.LightBlue-Bean', 57600, timeout=0.1)

    # wait a bit
    time.sleep(0.5)

    screen = curses.initscr()
    try:
        curses.noecho()
        # curses.curs_set(0) # to hide cursor
        screen.keypad(1)
        screen.addstr("Please start typing! (ctrl-c or ctrl-d to quit)\n")
        while True:
            event = screen.getch()
            if event == curses.KEY_UP:
                event = 128  # special char for typewriter
            elif event == curses.KEY_DOWN:
                event = 129
            elif event == curses.KEY_LEFT:
                event = 130
            elif event == curses.KEY_RIGHT:
                event = 32  # space
            elif event == curses.KEY_BACKSPACE:
                event = 0x7f
            elif event == 0x7f:  # already backspace
                pass
            elif event == 393:  # shift left-arrow for micro-backspace
                event = 131
            elif event == 21:
                screen.addstr('ctrl-u')
            else:
                screen.addch(event)
            # screen.addstr(str(type(event)))
            ser.write(chr(event))  # send one byte
            ser.flush()
            response = ''
            while True:
                response = ser.read(10)
                # print(response)
                if len(response) > 0 and 'ok' in response:
                    # print("(bytes written:"+response.rstrip()+")")
                    break
                time.sleep(0.01)
    finally:
        curses.endwin()
        ser.close()
