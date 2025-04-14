#include <Servo.h>

Servo servo1, servo2, servo3, servo4, servo5, servo6;
Servo servo7, servo8, servo9, servo10, servo11;

const float degree = 12.8571;
int servoPositions[28];
char characters[28] = {
  'a','b','c','d','e','f','g','h','i','j',
  'k','l','m','n','o','p','q','r','s','t',
  'u','v','w','x','y','z',' ', '#'};

char lastMoved[11] = {0}; // track last character per servo

int getIndex(char c) {
  c = tolower(c);
  for (int i = 0; i < 28; i++) {
    if (characters[i] == c) return i;
  }
  return -1;
}

// Macro for defining servo move functions with attach/detach
#define DEFINE_MOVE_SERVO_FN(NUM, PIN) \
void moveServo##NUM(char c) { \
  int index = getIndex(c); \
  if (index != -1 && lastMoved[NUM - 1] != c) { \
    servo##NUM.attach(PIN); \
    servo##NUM.write(servoPositions[index]); \
    delay(300); /* ensure motion finishes */ \
    servo##NUM.write(0); /* return to zero before detaching */ \
    delay(1000); \
    servo##NUM.detach(); \
    lastMoved[NUM - 1] = c; \
  } \
}


// Define all 11 servo functions
DEFINE_MOVE_SERVO_FN(1, 2)
DEFINE_MOVE_SERVO_FN(2, 3)
DEFINE_MOVE_SERVO_FN(3, 4)
DEFINE_MOVE_SERVO_FN(4, 5)
DEFINE_MOVE_SERVO_FN(5, 6)
DEFINE_MOVE_SERVO_FN(6, 7)
DEFINE_MOVE_SERVO_FN(7, 8)
DEFINE_MOVE_SERVO_FN(8, 9)
DEFINE_MOVE_SERVO_FN(9, 10)
DEFINE_MOVE_SERVO_FN(10, 11)
DEFINE_MOVE_SERVO_FN(11, 12)

void setup() {
  for (int i = 0; i < 26; i++) {
    servoPositions[i] = (i + 1) * degree;
  }
  servoPositions[26] = 27 * degree;  // space
  servoPositions[27] = 28 * degree;  // prefix
}

void loop() {
  // Example: move all servos to 'a' (only once each)
  moveServo1('a');
  moveServo2('a');
  moveServo3('a');
  moveServo4('a');
  moveServo5('a');
  moveServo6('a');
  moveServo7('a');
  moveServo8('z');
  moveServo9('a');
  moveServo10('a');
  moveServo11('a');


}
