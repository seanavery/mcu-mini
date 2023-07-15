#!/usr/bin/env python3

import sys
import time
import serial

import pygame
from util import fetch_config
from message import Message

def find_gamepad(gamepad_name, gamepad_guid):
  pygame.init()
  pygame.joystick.init()
  ctrl_idx = None
  for x in range(pygame.joystick.get_count()):
    js = pygame.joystick.Joystick(x)
    if js.get_name() == gamepad_name and js.get_guid() == gamepad_guid:
      print("found gamepad")
      found = True
      ctrl_idx = x
  if ctrl_idx == None:
    print("could not find gamepad")
    sys.exit(1)
  gp = pygame.joystick.Joystick(0)
  gp.init()
  name = gp.get_name()
  guid = gp.get_guid()

  return gp

if __name__ == "__main__":
  # fetch config
  conf = fetch_config() # ./esc.yaml

  # prefix
  throttle_index = conf['throttle']['prefix']
  steering_index = conf['steering']['prefix']
  escape_char = conf['escape']
  baudrate = conf['baudrate']
  
  gamepad_name = conf['gamepad']['name']
  gamepad_guid = conf['gamepad']['guid']
  steering = (conf['steering']['center'], conf['steering']['left'], conf['steering']['right'])
  throttle = (conf['throttle']['neutral'], conf['throttle']['reverse'], conf['throttle']['forward'])
  device = conf['device']
  msg = Message(steering, throttle)

  # find gamepad
  gp = find_gamepad(gamepad_name, gamepad_guid)

  # connect to serial port
  ser = serial.Serial("/dev/{}".format(device), baudrate)

  # controller state poll
  payload = None
  while True:
    time.sleep(0.05)
    es = pygame.event.get()
    if es:
      for e in es:
        if e.type == pygame.JOYAXISMOTION:
          # print("axis:", e.axis, "value:", e.value)
          # steering
          if e.axis == 2:
            payload = msg.format_msg(steering_index, msg.normalize_steering(e.value))
          # throttle
          if e.axis == 1:
            payload = msg.format_msg(throttle_index, msg.normalize_throttle(e.value * -1))
          if payload:
            ser.write(payload)
