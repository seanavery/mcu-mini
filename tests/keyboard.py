#!/usr/bin/env python3

import serial
import curses
import time

from message import Message
from util import fetch_config

# throttle
throttle_index = "t";
steering_index = "s";
escape_char = "#";

# # throttle
throttle = 90;
# steering
steering = 90;

if __name__ == "__main__":
  # fetch config
  conf = fetch_config()
  steering_conf = (conf['steering']['center'], conf['steering']['left'], conf['steering']['right'])
  throttle_conf = (conf['throttle']['neutral'], conf['throttle']['reverse'], conf['throttle']['forward'])
  device = conf['device']

  # print controls
  print("w: throttle up")
  print("s: throttle down")
  print("d: steering right")
  print("a: steering left")

  msg = Message(steering_conf, throttle_conf)

  # connect to arduino through serial port
  try:
    ser = serial.Serial("/dev/{}".format(device), 115200);
    print("connected to serial port")
  except Exception as e:
    print("failed to connect to serial port", device, e)
    exit(1)

  # connect to keyboard
  stdscr = curses.initscr()
  stdscr.clear()

  while True:
    # fetch keypress
    try:
      key = stdscr.getch()
      if key == ord('w'):
        throttle += 1
        print(throttle)
      if key == ord('s'):
        throttle -= 1
        print(throttle)
      if key == ord('d'):
        steering += 5
        print(steering)
      if key == ord('a'):
        steering -= 5
        print(steering)

      steering = msg.steering_safe(steering)
      throttle = msg.throttle_safe(throttle)
      steering_msg = msg.format_msg(steering_index, steering)
      throttle_msg = msg.format_msg(throttle_index, throttle)

      time.sleep(0.01)
      print(steering_msg)
      ser.write(steering_msg)
      time.sleep(0.01)
      ser.write(throttle_msg)

    except KeyboardInterrupt:
      curses.endwin()
      raise

