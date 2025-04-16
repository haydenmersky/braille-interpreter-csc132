#include <Servo.h>

const int NUM_SERVOS = 11;
Servo servos[NUM_SERVOS];
int servoPins[NUM_SERVOS] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};

const float degree = 12.8571; // degrees per character
int servoPositions[28];
char characters[28] = {
  'a','b','c','d','e','f','g','h','i','j',
  'k','l','m','n','o','p','q','r','s','t',
  'u','v','w','x','y','z',' ', '#'
};

char lastMoved[NUM_SERVOS] = {0}; // track last character per servo

int getIndex(char c) {
  c = tolower(c);
  for (int i = 0; i < 28; i++) {
    if (characters[i] == c) return i;
  }
  return -1;
}

void moveServo(int servoIndex, char c) {
  int index = getIndex(c);
  if (index != -1 && lastMoved[servoIndex] != c) {
    servos[servoIndex].attach(servoPins[servoIndex]);
    servos[servoIndex].write(servoPositions[index]);
    delay(300); // wait for motion
    servos[servoIndex].write(0); // return to zero
    delay(1000);
    servos[servoIndex].detach();
    lastMoved[servoIndex] = c;
  }
}

void setup() {
  for (int i = 0; i < 28; i++) {
    servoPositions[i] = (i + 1) * degree;
  }
}

void loop() {
  // Example: move all servos to different letters
  moveServo(0, 'a');
  moveServo(1, 'b');
  moveServo(2, 'c');
  moveServo(3, 'd');
  moveServo(4, 'e');
  moveServo(5, 'f');
  moveServo(6, 'g');
  moveServo(7, 'z');
  moveServo(8, ' ');
  moveServo(9, '#');
  moveServo(10, 'a');
}
