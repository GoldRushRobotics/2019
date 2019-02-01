/*
TFT LCD test
Found 0x9486 LCD driver
TFT size is 320x480

*/
#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_TFTLCD.h> // Hardware-specific library
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

#define LCD_CS A3
#define LCD_CD A2
#define LCD_WR A1
#define LCD_RD A0
// optional
#define LCD_RESET A4

// Assign human-readable names to some common 16-bit color values:
#define  BLACK   0x0000
#define BLUE    0x001F
#define RED     0xF800
#define GREEN   0x07E0
#define CYAN    0x07FF
#define MAGENTA 0xF81F
#define YELLOW  0xFFE0
#define WHITE   0xFFFF

long int unsigned times = 0; //maybe need to optimize this one day
bool going = false;
int counting;
int countdown = 180;

#include <MCUFRIEND_kbv.h>
MCUFRIEND_kbv tft;
// If using the shield, all control and data lines are fixed, and
// a simpler declaration can optionally be used:
// Adafruit_TFTLCD tft;

void setup(void) {
  Serial.begin(9600);

  tft.reset();

  uint16_t identifier = tft.readID(); //for our screen, this is 0x9486

  tft.begin(identifier);
  //Serial.print("TFT size is "); Serial.print(tft.width()); Serial.print("x"); Serial.println(tft.height()); this is 320x480 for our screen
  tft.setRotation(1); 
  //Sets coordinates for screen rotation
  //0: Portrait mode with bezel at bottom, (0,0) is near the usb connector/reset button on Redboard
  //1, 2, 3: continue rotating, CLOCKWISE (so use orientation 3 for the final build if the bezel will be on the left)
  //The rotation of the screen, and the coordinate grid of the screen geometry is TOTALLY INDEPENDENT OF THE TOUCHSCREEN'S REPORTING
  
  //making the background
  tft.fillScreen(WHITE);
  //making buttons and text fields
  tft.fillRect(300,160,180,160,GREEN); //1000>x>600 and 900>y>500
  tft.fillRect(300,0,180,160,MAGENTA); //940ish>x>620 (130 to 905 y total so 522 is the middle)
  tft.setTextSize(12);
  tft.setTextColor(BLACK);
  tft.setRotation(3); //set the rotation down here so that the text will draw correctly. Maybe the program could start at rotation 3 and then switch to 1 right before the flag goes up?
  //for rotation 3, upper right corner is 0,0
  pinMode(XM, OUTPUT);
  pinMode(YP, OUTPUT);
  
  }

#define MINPRESSURE 10
#define MAXPRESSURE 1000

void loop() {
  //tft.fillRect(200,0,200,275,WHITE);
  if((micros()-times) >= 980000) {countdown--;times=micros();Serial.println(micros());Serial.println(times);tft.fillRect(200,275,300,275,WHITE);}
  
  TSPoint p = ts.getPoint();
  pinMode(XM, OUTPUT);
  pinMode(YP, OUTPUT);
  
  if(p.z > MINPRESSURE && p.z < MAXPRESSURE) { //touch coordinate scailing from tftpaint
    p.x = p.x + p.y;       
    p.y = p.x - p.y;            
    p.x = p.x - p.y;   
    p.x = map(p.x, TS_MINX, TS_MAXX, tft.width(), 0);
    p.y = tft.height()-(map(p.y, TS_MINY, TS_MAXY, tft.height(), 0));
    //Serial.print(p.x);Serial.print(" ");Serial.println(p.y);
    if(p.y > 200) { //remember the screen coordinate system was rotated and even with the mapping the touch coords are still kind of weird
      if(p.x < 242) { //green 
      //Serial.print("Green");
      times = micros();
      going = true;
      countdown = 180;
      tft.fillRect(200,275,300,275,WHITE);
    }
      else {
        going = false; 
        tft.fillRect(200,275,300,275,WHITE);
        /*Serial.print("Magenta");*/
        } //magenta
  }
  }
  tft.setTextSize(4); //12 is fine for word but WAY too big for the screen. Seems to be a scale value for the text
  tft.setTextColor(BLACK);
  tft.setCursor(200,25);
  tft.print("V1= ");tft.print("###");tft.print("V"); //println will go down a line, but it will also go back to the origin which is very annoying
  tft.setCursor(200,75); //you must therefore still update the cursor's position for each new line
  tft.print("V2= ");tft.print("###");tft.print("V");
  tft.setCursor(200,125);
  tft.print("V3= ");tft.print("###");tft.print("V");
  tft.setCursor(200,175);
  tft.print("V4= ");tft.print("###");tft.print("V");
  tft.setCursor(200,275);
  if(going) {tft.setTextColor(RED);
    //tft.print("Timer: ");tft.print((micros())/(60*1000000));tft.print(":");tft.print((time-micros())%(60*1000000));
    if(countdown < 0) {tft.print("Timer: ");tft.print(0);}
    else {tft.print("Timer: ");tft.print(countdown/60);tft.print(":");tft.print(countdown%60);}
  }
  else {
    tft.setTextColor(BLUE);
    tft.print("Timer: #:##");
  }
  
}
