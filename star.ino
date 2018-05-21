/*
  Blink
  Turns on an LED on for one second, then off for one second, repeatedly.

  Most Arduinos have an on-board LED you can control. On the UNO, MEGA and ZERO 
  it is attached to digital pin 13, on MKR1000 on pin 6. LED_BUILTIN is set to
  the correct LED pin independent of which board is used.
  If you want to know what pin the on-board LED is connected to on your Arduino model, check
  the Technical Specs of your board  at https://www.arduino.cc/en/Main/Products
  
  This example code is in the public domain.

  modified 8 May 2014
  by Scott Fitzgerald
  
  modified 2 Sep 2016
  by Arturo Guadalupi
  
  modified 8 Sep 2016
  by Colby Newman
*/

int redpin = 7;
int yellowpin = 8;
int whitepin = 9;

int modepin1 = 11;
int modepin2 = 12;

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(redpin, OUTPUT);
  pinMode(yellowpin, OUTPUT);
  pinMode(whitepin, OUTPUT);

  pinMode(modepin1, INPUT);
  pinMode(modepin2, INPUT);
  
}

// the loop function runs over and over again forever
void loop() {


  if (digitalRead(modepin1) == HIGH) {
    digitalWrite(yellowpin, HIGH);
//    digitalWrite(whitepin, 500);
//    digitalWrite(whitepin, LOW);
    digitalWrite(yellowpin, LOW);
  }
  else if (digitalRead(modepin2) == HIGH) {
    digitalWrite(redpin, HIGH);
    delay(50);
    digitalWrite(redpin, LOW);
    digitalWrite(yellowpin, HIGH);
    delay(50);
    digitalWrite(yellowpin, LOW);
    digitalWrite(whitepin, 300);
    delay(50);
    digitalWrite(whitepin, LOW);
  }                 // wait for a second
}
