#include <stdlib.h>

#include <Servo.h>

// pwm instances
Servo steeringServo;
Servo motorEsc;

// global variables
int angle = 90;
int throttle = 90;
int neutral = 90;
int minAngle = 60;
int maxAngle = 120;
int centerAngle = 90;
int minThrottleForward = 90;
int maxThrottleFortward = 160;
int minThrottleaReverse = 90;
int maxThrottleReverse = 20;

char throttleIndex = 't';
char steeringIndex = 's';
char escapeIndex = '#';

int steeringPin = 6;
int motorPin = 5;

// safety nonce
int waiting = 0;

void setup() {
  // setup serial communication over usb port
  Serial.begin(115200);
  // wait for serial port to connect
  while (!Serial) {
    ;
  }
  Serial.println("serial port is connected");
  // setup pwm pins for steering and motor control
  steeringServo.attach(steeringPin);
  motorEsc.attach(motorPin);
}

bool steering_safe(int value)
{
  if (value > maxAngle) 
  {
    return false;
  }
  if (value < minAngle) 
  {
    return false;
  }
  return true;
}

bool throttle_safe(int value)
{
  if (value > maxThrottleFortward) 
  {
    return false;
  }
  if (value < maxThrottleReverse) 
  {
    return false;
  }
  return true;
}

int normalize(int value) {
  if (value > 90) {
    value = value - 1; 
  } else if (value < 90) {
    value = value + 1;
  }
  return value;
}

void loop() {
  delay(1);
  if (Serial.available())
  {
    waiting = 0;
    char serialMsg[20];
    size_t msgLength = Serial.readBytesUntil(escapeIndex, serialMsg, 20);

    if (msgLength == 4)
    {
      // parse serial data
      char header;
      int value;
      sscanf(serialMsg, "%c%3d", header, &value);

      if (serialMsg[0] == throttleIndex) {
        if (throttle_safe(value))
        {
          throttle = value;
        }
      }
      else if (serialMsg[0] == steeringIndex)
      {
        if (steering_safe(value))
        {
          angle = value;
        }
      }
    }
  }
  else
  {
    // throttle down when serial not connected
    waiting  = waiting+1;
    if (waiting >= 1000) {
      throttle = normalize(throttle);
      waiting = 0;
    }
  }
  motorEsc.write(throttle);
  steeringServo.write(angle);
}
