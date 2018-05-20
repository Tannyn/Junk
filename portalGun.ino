/*
 * 
 * Modified by @TannynFox
 * 
 */
 
#include <Adafruit_GFX.h>
#include <gfxfont.h>

// Code to control a Rick and Morty Portal Gun
// Written by Brandon Pomeroy, 2015

/*
******** Required Libraries *************
* ClickEncoder - https://github.com/0xPIT/encoder
* Adafruit_GFX - https://github.com/adafruit/Adafruit-GFX-Library
* Adafruit_LEDBackpack - https://github.com/adafruit/Adafruit-LED-Backpack-Library
*/


/*
********** Required Hardware *********************
* Adafruit Pro Trinket 5V 16MHz - http://www.adafruit.com/product/2000
* LiPoly BackPack - http://www.adafruit.com/product/2124
* LiPoly Battety 3.7V - http://www.adafruit.com/products/1578
* Rotary Encoder - http://www.adafruit.com/products/377
* Metal Knob - http://www.adafruit.com/products/2056
* Quad Alphanumeric Display (Red 0.54") - http://www.adafruit.com/products/1911
* 10mm Diffused Green LED (x4) - https://www.adafruit.com/products/844
* 10mm Plastic Bevel LED Holder (x4) - https://www.adafruit.com/products/2171
* 150 Ohm Resistor (x4) for LEDs
* Inductive Charging Set - 5V - https://www.adafruit.com/products/1407
* 2.1mm Panel Mount Barrel Jack - http://www.adafruit.com/products/610
* 9VDC Power Supply - http://www.adafruit.com/products/63
*/

#include <Wire.h>
#include "Adafruit_LEDBackpack.h"
#include "Adafruit_GFX.h"
#include <ClickEncoder.h>
#include <TimerOne.h>
#include <avr/sleep.h>
#include <avr/power.h>

// Set up our LED display
Adafruit_AlphaNum4 alpha4 = Adafruit_AlphaNum4();
char displayBuffer[4];
uint8_t dimensionLetter='C';

// Set up the click encoder
ClickEncoder *encoder;
int16_t last, value;
#define encoderPinA          A0
#define encoderPinB          A1
#define encoderButtonPin     A2

// Steps per notch can be 1, 4, or 8. If your encoder is counting
// to fast or too slow, change this!
#define stepsPerNotch        6

// Comment this line to make the encoder increment in the opposite direction
#define reverseEncoderWheel


// FX Board output delay (ms)
const int msDelay = 500;

// Set up the Green LEDs
#define topBulbPin1           9
#define topBulbPin2  10
#define frontR        3
#define frontG       5
#define frontB         4
#define maximumBright        255
#define mediumBright         127
int topBulbBrightness = 255;
bool encoderAlphaMode = false;

const uint8_t message[] = "WUBBA LUBBA DUB DUB";
const uint8_t message2[] = "CRONENBERG";
const uint8_t message3[] = "WARNING POO EATERS";
const uint8_t message4[] = "INITIATING SLEEP MODE";

// Set up what we need to sleep/wake the Trinket
// Define the pins you'll use for interrupts - CHANGE THESE to match the input pins
// you are using in your project
#define NAV0_PIN A2

//Let us know if our Trinket woke up from sleep
volatile bool justWokeUp;


void timerIsr() {
  encoder->service();
}

void setup() {
  enablePinInterupt(NAV0_PIN);
  
  //Set up pin modes[
  pinMode(topBulbPin1, OUTPUT);
  pinMode(topBulbPin2, OUTPUT);
  pinMode(frontR, OUTPUT);
  pinMode(frontG, OUTPUT);
  pinMode(frontB, OUTPUT);
  
  
  digitalWrite(frontR, LOW);
  digitalWrite(frontG, HIGH);
  digitalWrite(frontB, LOW);
  digitalWrite(topBulbPin1, HIGH);
  digitalWrite(topBulbPin2, HIGH);
  
  
  encoderSetup();
  alpha4.begin(0x70);  // pass in the address for the LED display
  
  justWokeUp = false;
  
  //uncomment this to make the display run through a test at startup
  //displayTest();
}

void loop() {
  if (justWokeUp) {
    digitalWrite(frontR, LOW);
    digitalWrite(frontG, HIGH);
    digitalWrite(frontB, LOW);
    digitalWrite(topBulbPin1, HIGH);
    digitalWrite(topBulbPin2, HIGH);
    justWokeUp = false;
  }  

  
  ClickEncoder::Button b = encoder->getButton();
  switch (b) {
    case ClickEncoder::Held:
      // Holding the button will put your trinket to sleep.
      // The trinket will wake on the next button press
      alpha4.clear();
      scroll(message4, sizeof(message4)/sizeof(uint8_t)-1);
      digitalWrite(frontR, LOW);
      digitalWrite(frontG, LOW);
      digitalWrite(frontB, LOW);
      digitalWrite(topBulbPin1, LOW);
      digitalWrite(topBulbPin2, LOW);
      alpha4.writeDisplay();
      delay(5000);
      alpha4.clear();
      alpha4.writeDisplay();
      delay(5000);
      justWokeUp = true;
      goToSleep();
    break;
    case ClickEncoder::Clicked:
      if (dimensionLetter=='C' && displayBuffer[0]=='1'&& displayBuffer[1]=='3'&& displayBuffer[2]=='7') {
      
      digitalWrite(frontR, HIGH);
      digitalWrite(frontG, LOW);
      digitalWrite(frontB, LOW);
      scroll(message2, sizeof(message2)/sizeof(uint8_t)-1);
      digitalWrite(frontR, LOW);
      digitalWrite(frontG, HIGH);
      
      }

      if (dimensionLetter=='J' && displayBuffer[0]=='1'&& displayBuffer[1]=='9'&& displayBuffer[2]=='7') {
      
      digitalWrite(frontR, HIGH);
      digitalWrite(frontG, LOW);
      digitalWrite(frontB, HIGH);
      scroll(message3, sizeof(message3)/sizeof(uint8_t)-1);
      digitalWrite(frontR, LOW);
      digitalWrite(frontG, HIGH);
      digitalWrite(frontB, LOW);
      
      }
      // When the encoder wheel is single clicked
      else {
      digitalWrite(frontG, LOW);
      delay(200);
      digitalWrite(frontG, HIGH);
      digitalWrite(frontR, HIGH);
      delay(200);
      digitalWrite(frontR, LOW);
  }
   
    break;
    case ClickEncoder::DoubleClicked:
      if (dimensionLetter=='C' && displayBuffer[0]=='1'&& displayBuffer[1]=='3'&& displayBuffer[2]=='6' && encoderAlphaMode == false) {
        encoderAlphaMode = true;
      }
      else if (encoderAlphaMode == true) {
        encoderAlphaMode = false;
      }
      else {
        scroll(message, sizeof(message)/sizeof(uint8_t)-1);
        //If you double click the button, it sets the dimension to C137
        dimensionLetter = 'C';
        value = 137;
      }
    break;
    case ClickEncoder::Open:
      // The dimension will increment from 0-999, then roll over to the next
      // letter. (A999 -> B000)
      if (encoderAlphaMode == false) {
        updateDimension();
        if (dimensionLetter=='F' && displayBuffer[0]=='2'&& displayBuffer[1]=='4'&& displayBuffer[2]=='7')
          colorCycle();
      }
      else {
        updateLetter();
      }
    break;
  }
}


void encoderSetup(){

    // set up encoder
    encoder = new ClickEncoder(encoderPinA, encoderPinB, encoderButtonPin, stepsPerNotch);
    encoder->setAccelerationEnabled(true);
  
    Timer1.initialize(1000);
    Timer1.attachInterrupt(timerIsr); 
    last = -1;
    value = 137;
}

void updateLetter() {
  #ifdef reverseEncoderWheel
  value -= encoder->getValue();
  #endif
  
  #ifndef reverseEncoderWheel
  value += encoder->getValue();
  #endif

  if (value != last) {
    if (value<=40)
      dimensionLetter = 'A';
    else if (value>40&&value<=80)
      dimensionLetter = 'B';
    else if (value>80&&value<=120)
      dimensionLetter = 'C';
    else if (value>120&&value<=160)
      dimensionLetter = 'D';
    else if (value>160&&value<=200)
      dimensionLetter = 'E';
    else if (value>200&&value<=240)
      dimensionLetter = 'F';
    else if (value>240&&value<=280)
      dimensionLetter = 'G';
    else if (value>280&&value<=320)
      dimensionLetter = 'H';
    else if (value>320&&value<=360)
      dimensionLetter = 'I';
    else if (value>360&&value<=400)
      dimensionLetter = 'J';
    else if (value>400&&value<=440)
      dimensionLetter = 'K';
    else if (value>440&&value<=480)
      dimensionLetter = 'L';
    else if (value>480&&value<=520)
      dimensionLetter = 'M';
    else if (value>520&&value<=560)
      dimensionLetter = 'N';
    else if (value>560&&value<=600)
      dimensionLetter = 'O';
    else if (value>600&&value<=640)
      dimensionLetter = 'P';
    else if (value>640&&value<=680)
      dimensionLetter = 'Q';
    else if (value>680&&value<=720)
      dimensionLetter = 'R';
    else if (value>720&&value<=760)
      dimensionLetter = 'S';
    else if (value>760&&value<=800)
      dimensionLetter = 'T';
    else if (value>800&&value<=840)
      dimensionLetter = 'U';
    else if (value>840&&value<=880)
      dimensionLetter = 'V';
    else if (value>880&&value<=920)
      dimensionLetter = 'W';
    else if (value>920&&value<=960)
      dimensionLetter = 'X';
    else if (value>960&&value<=980)
      dimensionLetter = 'Y';
    else
      dimensionLetter = 'Z';
    last = value;

    sprintf(displayBuffer, "%03i", value);
//  alpha4.clear();
  alpha4.writeDigitAscii(0, dimensionLetter);
//  alpha4.writeDigitAscii(1, displayBuffer[0]);
//  alpha4.writeDigitAscii(2, displayBuffer[1]);
//  alpha4.writeDigitAscii(3, displayBuffer[2]);
  alpha4.writeDisplay();
  }
}

void updateDimension(){
  #ifdef reverseEncoderWheel
  value -= encoder->getValue();
  #endif
  
  #ifndef reverseEncoderWheel
  value += encoder->getValue();
  #endif
  
  if (value != last) {
    if (value > 999){
      value = 0;
      if (dimensionLetter == 'Z') {
        dimensionLetter = 'A';
      } else {
        dimensionLetter ++;        
      }
    } else if ( value < 0 ) {
      value = 999;
      if (dimensionLetter == 'A') {
        dimensionLetter = 'Z';
      } else {
        dimensionLetter --;
      }
    }
    last = value;
  }
  
  sprintf(displayBuffer, "%03i", value);
  alpha4.clear();
  alpha4.writeDigitAscii(0, dimensionLetter);
  alpha4.writeDigitAscii(1, displayBuffer[0]);
  alpha4.writeDigitAscii(2, displayBuffer[1]);
  alpha4.writeDigitAscii(3, displayBuffer[2]);
  alpha4.writeDisplay();
}





/*
============== Sleep/Wake Methods ==================
====================================================
*/

// Most of this code comes from seanahrens on the adafruit forums
// http://forums.adafruit.com/viewtopic.php?f=25&t=59392#p329418


void enablePinInterupt(byte pin)
{
    *digitalPinToPCMSK(pin) |= bit (digitalPinToPCMSKbit(pin));  // enable pin
    PCIFR  |= bit (digitalPinToPCICRbit(pin)); // clear any outstanding interrupt
    PCICR  |= bit (digitalPinToPCICRbit(pin)); // enable interrupt for the group
}

void goToSleep()   
{
// The ATmega328 has five different sleep states.
// See the ATmega 328 datasheet for more information.
// SLEEP_MODE_IDLE -the least power savings 
// SLEEP_MODE_ADC
// SLEEP_MODE_PWR_SAVE
// SLEEP_MODE_STANDBY
// SLEEP_MODE_PWR_DOWN -the most power savings
// I am using the deepest sleep mode from which a
// watchdog timer interrupt can wake the ATMega328

 


set_sleep_mode(SLEEP_MODE_PWR_DOWN); // Set sleep mode.
sleep_enable(); // Enable sleep mode.
sleep_mode(); // Enter sleep mode.
// After waking the code continues
// to execute from this point.

sleep_disable(); // Disable sleep mode after waking.                   
}

ISR (PCINT0_vect) // handle pin change interrupt for D8 to D13 here
{    
  // if I wired up D8-D13 then I'd need some code here
} 

ISR (PCINT1_vect) // handle pin change interrupt for A0 to A5 here // NAV0
{
    /* This will bring us back from sleep. */
  
  /* We detach the interrupt to stop it from 
   * continuously firing while the interrupt pin
   * is low.
   */
  
  detachInterrupt(0);

}

ISR (PCINT2_vect) // handle pin change interrupt for D0 to D7 here // NAV1, NAV2
{
  // Check it was NAV1 or NAV2 and nothing else
}
  

/*
============== Testing Methods ==================
=================================================
*/

void colorCycle() {
  //red
      digitalWrite(frontR, HIGH);
      digitalWrite(frontG, LOW);
      digitalWrite(frontB, LOW);
      delay(200);
  //orange
      digitalWrite(frontR, HIGH);
      digitalWrite(frontG, HIGH);
      digitalWrite(frontB, LOW);
      delay(200);
  //blue
      digitalWrite(frontR, LOW);
      digitalWrite(frontG, LOW);
      digitalWrite(frontB, HIGH);
      delay(200);
  //purple
      digitalWrite(frontR, HIGH);
      digitalWrite(frontG, LOW);
      digitalWrite(frontB, HIGH);
      delay(200);
  //aqua
      digitalWrite(frontR, LOW);
      digitalWrite(frontG, HIGH);
      digitalWrite(frontB, HIGH);
      delay(200);
  //green
      digitalWrite(frontR, LOW);
      digitalWrite(frontG, HIGH);
      digitalWrite(frontB, LOW);
      delay(200);
  
}

void displayTest() {
  
  alpha4.writeDigitRaw(3, 0x0);
  alpha4.writeDigitRaw(0, 0xFFFF);
  alpha4.writeDisplay();
  delay(200);
  alpha4.writeDigitRaw(0, 0x0);
  alpha4.writeDigitRaw(1, 0xFFFF);
  alpha4.writeDisplay();
  delay(200);
  alpha4.writeDigitRaw(1, 0x0);
  alpha4.writeDigitRaw(2, 0xFFFF);
  alpha4.writeDisplay();
  delay(200);
  alpha4.writeDigitRaw(2, 0x0);
  alpha4.writeDigitRaw(3, 0xFFFF);
  alpha4.writeDisplay();
  delay(200);
  
  alpha4.clear();
  alpha4.writeDisplay();

  // display every character, 
  for (uint8_t i='!'; i<='z'; i++) {
    alpha4.writeDigitAscii(0, i);
    alpha4.writeDigitAscii(1, i+1);
    alpha4.writeDigitAscii(2, i+2);
    alpha4.writeDigitAscii(3, i+3);
    alpha4.writeDisplay();
    delay(300);
  }
}

void wub() {

alpha4.writeDigitAscii(4, 'W');
delay(500);
alpha4.writeDigitAscii(4, 'U');
alpha4.writeDigitAscii(3, 'W');
delay(500);
alpha4.writeDigitAscii(4, 'B');
alpha4.writeDigitAscii(3, 'U');
alpha4.writeDigitAscii(2, 'W');
delay(500);
alpha4.writeDigitAscii(4, 'A');
alpha4.writeDigitAscii(3, 'B');
alpha4.writeDigitAscii(2, 'U');
alpha4.writeDigitAscii(1, 'W');
delay(500);
alpha4.writeDigitAscii(4, ' ');
alpha4.writeDigitAscii(3, 'A');
alpha4.writeDigitAscii(2, 'B');
alpha4.writeDigitAscii(1, 'U');
delay(500);
alpha4.writeDigitAscii(4, ' ');
alpha4.writeDigitAscii(3, ' ');
alpha4.writeDigitAscii(2, 'A');
alpha4.writeDigitAscii(1, 'B');
delay(500);
alpha4.writeDigitAscii(4, ' ');
alpha4.writeDigitAscii(3, ' ');
alpha4.writeDigitAscii(2, ' ');
alpha4.writeDigitAscii(1, 'A');
delay(500);
alpha4.clear();
delay(5000);


  
}

void scroll(uint8_t words[], int len) {

    alpha4.clear();
    alpha4.writeDisplay();
for (int x = 0; x < len; x=x+1) {
  if (x == 0) {
    alpha4.writeDigitAscii(3, words[0]);
    alpha4.writeDisplay();
delay(200);
  }
  else if (x == 1){
    alpha4.writeDigitAscii(3, words[1]);
    alpha4.writeDigitAscii(2, words[0]);
    alpha4.writeDisplay();
delay(200);
    
  }
  else if (x == 2){
    alpha4.writeDigitAscii(3, words[2]);
    alpha4.writeDigitAscii(2, words[1]);
    alpha4.writeDigitAscii(1, words[0]);
    alpha4.writeDisplay();
delay(200);
    
  }
  else if (x>2) {
    alpha4.writeDigitAscii(3, words[x]);
    alpha4.writeDigitAscii(2, words[x-1]);
    alpha4.writeDigitAscii(1, words[x-2]);
    alpha4.writeDigitAscii(0, words[x-3]);
    alpha4.writeDisplay();
delay(200);
}
}
 // delay(5000);
    alpha4.writeDigitAscii(3, ' ');
    alpha4.writeDigitAscii(2, words[len-1]);
    alpha4.writeDigitAscii(1, words[len-2]);
    alpha4.writeDigitAscii(0, words[len-3]);
    alpha4.writeDisplay();
delay(200);
    
    alpha4.writeDigitAscii(3, ' ');
    alpha4.writeDigitAscii(2, ' ');
    alpha4.writeDigitAscii(1, words[len-1]);
    alpha4.writeDigitAscii(0, words[len-2]);
    alpha4.writeDisplay();
delay(200);


    alpha4.writeDigitAscii(3, ' ');
    alpha4.writeDigitAscii(2, ' ');
    alpha4.writeDigitAscii(1, ' ');
    alpha4.writeDigitAscii(0, words[len-1]);
    alpha4.writeDisplay();
delay(200);

    alpha4.clear();
    alpha4.writeDisplay();
delay(1000);
}

