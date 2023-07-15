import math
import yaml


# write Messsage class 
class Message:
  def __init__(self, steering=(90, 60, 120), throttle=(90, 60, 120)):
    # set steering
    # set throttle
    self.steering = steering = steering
    self.throttle = throttle = throttle

  def normalize_steering(self, val):
    return round(self.steering[0] + val * ((self.steering[2] - self.steering[1])/2))

  def normalize_throttle(self, val):
    if val > 0:
      return round(self.throttle[0] + math.pow(10, val))
    else:
      return round(self.throttle[0] - math.pow(10, val*-1))

  def format_msg(self, prefix, val):
    str_msg = "{}{:03d}{}".format(prefix, val, "#")
    return bytes(str_msg, 'UTF-8')

  def steering_safe(self, val):
    if val > self.steering[2]:
      return self.steering[2]
    if val < self.steering[1]:
      return self.steering[1]
    return val

  def throttle_safe(self, val):
    if val < self.throttle[1]:
      return self.throttle[1]
    if val > self.throttle[2]:
      return self.throttle[2]
    return val

  
