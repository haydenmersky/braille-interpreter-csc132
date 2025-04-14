#include<Servo.h>


Servo servo1; // Creat servo object which we'll put on GPIO 2
Servo servo2; // Creat servo object which we'll put on GPIO 3
Servo servo3; // Creat servo object which we'll put on GPIO 4
Servo servo4; // Creat servo object which we'll put on GPIO 5
Servo servo5; // Creat servo object which we'll put on GPIO 6
Servo servo6; // Creat servo object which we'll put on GPIO 7
Servo servo7; // Creat servo object which we'll put on GPIO 8
Servo servo8; // Creat servo object which we'll put on GPIO 9
Servo servo9; // Creat servo object which we'll put on GPIO 10
Servo servo10; // Creat servo object which we'll put on GPIO 11
Servo servo11; // Creat servo object which we'll put on GPIO 12

const float degree = 12.8571;  // each character is 12.8571 degrees apart
float servoPositions[28]; // Array to hold the servo positions for each character
char characters [28] = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 
                        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z','space','prefix'}; // Array to hold the characters corresponding to the servo positions

void setup() {
  // put your setup code here, to run once:
  for (int i = 0; i < 2;: i++) {
    servoPositions[i] = (i+1) * degree;  // sets the degree for all the characters
  }

  servoPositions[26] = 27 * degree;  // degree for the space character
  servoPositions[27] = 28 * degree;  // degree for the prefix character

// Attach the servos to the pins 
  servo1.attach(2);
  servo2.attach(3);
  servo3.attach(4);
  servo4.attach(5);
  servo5.attach(6);
  servo6.attach(7);
  servo7.attach(8);
  servo8.attach(9);
  servo9.attach(10);
  servo10.attach(11);
  servo11.attach(12);

  int getIndex(char c){
    c = tolower(c)
    for (int i = 0; i < 28; i++){
      if (characters[i] == c) return i:  // returns the index of the character in the array of the given character
    }
    return -1
  }

  // UDF for each servo to move to the position of the character
  void moveServo1(char c) {
    int index = getIndex(c);
    if (index != -1) servo1.write(servoPositions[index]);
  }
  
  void moveServo2(char c) {
    int index = getIndex(c);
    if (index != -1) servo2.write(servoPositions[index]);
  }
  
  void moveServo3(char c) {
    int index = getIndex(c);
    if (index != -1) servo3.write(servoPositions[index]);
  }
  
  void moveServo4(char c) {
    int index = getIndex(c);
    if (index != -1) servo4.write(servoPositions[index]);
  }
  
  void moveServo5(char c) {
    int index = getIndex(c);
    if (index != -1) servo5.write(servoPositions[index]);
  }
  
  void moveServo6(char c) {
    int index = getIndex(c);
    if (index != -1) servo6.write(servoPositions[index]);
  }
  
  void moveServo7(char c) {
    int index = getIndex(c);
    if (index != -1) servo7.write(servoPositions[index]);
  }
  
  void moveServo8(char c) {
    int index = getIndex(c);
    if (index != -1) servo8.write(servoPositions[index]);
  }
  
  void moveServo9(char c) {
    int index = getIndex(c);
    if (index != -1) servo9.write(servoPositions[index]);
  }
  
  void moveServo10(char c) {
    int index = getIndex(c);
    if (index != -1) servo10.write(servoPositions[index]);
  }
  
  void moveServo11(char c) {
    int index = getIndex(c);
    if (index != -1) servo11.write(servoPositions[index]);

}
}

void loop() {
  // put your main code here, to run repeatedly:

}
