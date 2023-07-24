import sys
import time
import serial

from util import fetch_config
from message import Message

if __name__ == "__main__":
    conf = fetch_config()
    baudrate = conf['baudrate']
    device = conf['device']
    steering = (conf['steering']['center'], conf['steering']['left'], conf['steering']['right'])
    throttle = (conf['throttle']['neutral'], conf['throttle']['reverse'], conf['throttle']['forward'])
    msg = Message(steering, throttle)
    
    # connect to mcu
    ser = serial.Serial("/dev/{}".format(device), baudrate)
    
    timeout = 10
    st = time.time()
    payload = None
    while 1:
        time.sleep(0.05)
        ct = time.time()
        payload = msg.format_msg('t', 100)
        print(payload)
        ser.write(payload)
        if ct - st > timeout:
            print("timeout")
            sys.exit(1) 
    