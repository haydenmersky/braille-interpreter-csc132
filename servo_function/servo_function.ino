#include <Servo.h>

const int NUM_SERVOS = 11;
Servo servos[NUM_SERVOS];
int servoPins[NUM_SERVOS] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};

const float degree = 7; // degrees per character based off of gear ratio 
int letterPositions[28];
char characters[28] = {
  'a','b','c','d','e','f','g','h','i','j',
  'k','l','m','n','o','p','q','r','s','t',
  'u','v','w','x','y','z',' ', '#'
};

void HomeServos(){
  for (int i =0 ; i <= NUM_SERVOS; i++){
    servos[i].attach(servoPins[i]);
    servos[i].write(letterPositions[0]);
    delay(30);
  }
}


int getIndex(char c) {
  c = tolower(c);
  for (int i = 0; i < 28; i++) {
    if (characters[i] == c) return i;
  }
  return -1;
}

void moveServo(int servoIndex, char c) {
  int index = getIndex(c);
    servos[servoIndex].attach(servoPins[servoIndex]);
    servos[servoIndex].write(letterPositions[index]);
  }

  
void moveServosFromString(const char* str) {
  for (int i = 0; i <= NUM_SERVOS && str[i] != '\0'; i++) {
    moveServo(i, str[i]);
    delay(40);
  }
}

void setup() {
  for (int i = 0; i < 28; i++) {
    letterPositions[i] = (i + 1) * degree;
    delay(30);
  }

  Serial.begin(9600);
  Serial.setTimeout(10);

}

void loop() 
  if (Serial.available() > 0) {
    String strFromPi = Serial.readString();
    strFromPi.trim();
    Serial.print("Received: ");
    Serial.println(strFromPi);
    moveServosFromString(strFromPi.c_str());
}
