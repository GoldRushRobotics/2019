#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_TFTLCD.h> // Hardware-specific library
//#include <SD.h>
//#include <SPI.h> Don't even need it lol
//#include <Wire.h> //this line caused problems for compiling for the normal arduino

//touchscreen bits
#include <TouchScreen.h>

#if defined(__SAM3X8E__)
#undef __FlashStringHelper::F(string_literal)
#define F(string_literal) string_literal
#endif

#define YP A2  // must be an analog pin, use "An" notation!
#define XM A3  // must be an analog pin, use "An" notation!
#define YM 8   // can be a digital pin
#define XP 9   // can be a digital pin

#define TS_MINX 130
#define TS_MAXX 905

#define TS_MINY 75
#define TS_MAXY 930

TouchScreen ts = TouchScreen(XP, YP, XM, YM, 300);

#define MINPRESSURE 10
#define MAXPRESSURE 1000
//

#define LCD_CS A3 // Chip Select goes to Analog 3
#define LCD_CD A2 // Command/Data goes to Analog 2
#define LCD_WR A1 // LCD Write goes to Analog 1
#define LCD_RD A0 // LCD Read goes to Analog 0
#define PIN_SD_CS 10 // Adafruit SD shields and modules: pin 10

#define LCD_RESET A4 //*** Can alternately just connect to Arduino's reset pin *** seems like A5 is also not used

// Assign human-readable names to some common 16-bit color values:
#define  BLACK   0x0000
#define BLUE    0x001F
#define RED     0xF800
#define GREEN   0x07E0
#define CYAN    0x07FF
#define MAGENTA 0xF81F
#define YELLOW  0xFFE0
#define WHITE   0xFFFF
#include <MCUFRIEND_kbv.h>
MCUFRIEND_kbv tft;



/*********************************************/
// This procedure reads a bitmap and draws it to the screen
// its sped up by reading many pixels worth of data at a time
// instead of just one pixel at a time. increading the buffer takes
// more RAM but makes the drawing a little faster. 20 pixels' worth
// is probably a good place


/*********************************************/
// These read data from the SD card file and convert them to big endian
// (the data is stored in little endian format!)

// LITTLE ENDIAN!


// LITTLE ENDIAN!



void setup(void) {
  //SCREEN IDENTIFICATION AND SD SD CARD DETECTION//

  Serial.begin(9600);
  Serial.println(("Let us start the screen..."));

  tft.reset();

  uint16_t identifier = 0x9486; //We are only using this with one type of screen, so no need to identify it
  /*tft.readID();*/

  tft.begin(identifier);
  tft.setRotation(1);
  //making the background
  tft.fillScreen(WHITE);

  //Init SD_Card
  pinMode(10, OUTPUT);


  //BUTTON DRAWING AND TOUCHSCREEN SETUP//

  //tft.setRotation(3);
  //making buttons and text fields
  //tft.fillRect(300,160,180,160,GREEN); //1000>x>600 and 900>y>500
  //tft.fillRect(300,0,180,160,MAGENTA); //940ish>x>620 (130 to 905 y total so 522 is the middle)
  tft.setTextSize(4);
  //set the rotation down here so that the text will draw correctly. Maybe the program could start at rotation 3 and then switch to 1 right before the flag goes up?
  //for rotation 3, upper right corner is 0,0
  pinMode(XM, OUTPUT);
  pinMode(YP, OUTPUT);
  Serial.println(("Screen started, time to begin"));
  //EXTRA SETUP THINGS AND I2C//
  //bmpFile = SD.open(__Gsbmp_files[0]);

}

void loop(void) {

  tft.fillTriangle(211, 82, 202, 73, 211, 65, GREEN); //diamond part
  tft.fillTriangle(176, 81, 183, 94, 183, 81, GREEN); //whisker top
  tft.fillTriangle(205, 81, 210, 122, 197, 93, GREEN); //whisker top long
  tft.fillTriangle(164, 97, 175, 108, 175, 97, GREEN); //bottom whisker
  tft.fillTriangle(185, 97, 185, 108, 201, 125, GREEN); //whisker bottom long
  tft.fillTriangle(172, 113, 181, 113, 183, 126, GREEN); //parallelogramish thing 1
  tft.fillTriangle(183, 126, 193, 126, 181, 113, GREEN); //parallelogramish thing 2
  tft.fillTriangle(190, 129, 199, 138, 199, 129, YELLOW); //gold trapezoid point

  tft.fillRect(183, 81, 22, 13, GREEN); //whisker top rectangle
  tft.fillRect(175, 97, 10, 11, GREEN); //whisker bottom rectangle

  tft.fillRect(199, 129, 26, 9, YELLOW); //gold trapezoid body (NOT SYMMETRICAL)

  tft.fillRect(220, 81, 22, 13, GREEN); //whisker top rectangle 2
  tft.fillRect(237, 97, 10, 11, GREEN); //whisker bottom rectangle 2

  

  tft.fillTriangle(211, 82, 220, 73, 211, 65, GREEN); //diamond part 2
  tft.fillTriangle(246, 81, 239, 94, 239, 81, GREEN); //whisker top 2
  tft.fillTriangle(217, 81, 212, 122, 225, 93, GREEN); //whisker top long 2
  tft.fillTriangle(258, 97, 247, 108, 247, 97, GREEN); //bottom whisker 2
  tft.fillTriangle(237, 97, 237, 108, 221, 125, GREEN); //whisker bottom long 2
  tft.fillTriangle(250, 113, 241, 113, 239, 126, GREEN); //parallelogramish thing 1 (2)
  tft.fillTriangle(239, 126, 229, 126, 241, 113, GREEN); //parallelogramish thing 2
  tft.fillTriangle(232, 129, 223, 138, 223, 129, YELLOW); //gold trapezoid point


  //(211-x)+211
  TSPoint p = ts.getPoint();
  pinMode(XM, OUTPUT);
  pinMode(YP, OUTPUT);

  if (p.z > MINPRESSURE && p.z < MAXPRESSURE) { //touch coordinate scailing from tftpaint
    p.x = p.x + p.y;
    p.y = p.x - p.y;
    p.x = p.x - p.y;
    p.x = map(p.x, TS_MINX, TS_MAXX, tft.width(), 0);
    p.y = tft.height() - (map(p.y, TS_MINY, TS_MAXY, tft.height(), 0));
    //Serial.print(p.x);Serial.print(" ");Serial.println(p.y);
    if (p.y > 200) { //remember the screen coordinate system was rotated and even with the mapping the touch coords are still kind of weird
      if (p.x < 242) { //green
        //Serial.print("Green");

      }
    }
    Serial.print("x: "); Serial.print(p.x); Serial.print(" y: "); Serial.print(p.y); Serial.print(" z: "); Serial.print(p.z);
  }

}
