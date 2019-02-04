#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_TFTLCD.h> // Hardware-specific library
#include <SD.h>
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

#define MAX_BMP         10                      // bmp file num
#define FILENAME_LEN    20                      // max file name length

float v1,v2,v3,v4=0.0; //variables for i2c, the motor controller's voltages will go here

//Wibbly-wobbly Timey-wymey
long int unsigned times = 0;
bool going,raised,checki2c = false;
int countdown = 180;

const int COUNTFROM = 30; //change this around to change where it counts down from
//

const int __Gnbmp_height = 320;                 // Initially 480, this is used in the code to define the max vertical itterations that the bmp reader will go through
const int __Gnbmp_width  = 320;                 // (pointless) 240 bmp width Does not actually change anything in code besides performing a check we have commented out 

unsigned char __Gnbmp_image_offset  = 0;        // offset for where the screen reading program will start

File bmpFile;

/*********************************************/
// This procedure reads a bitmap and draws it to the screen
// its sped up by reading many pixels worth of data at a time
// instead of just one pixel at a time. increading the buffer takes
// more RAM but makes the drawing a little faster. 20 pixels' worth
// is probably a good place

#define BUFFPIXEL       80                      // must be a divisor of 320 originally 80
#define BUFFPIXEL_X3    240                     // BUFFPIXELx3

void bmpdraw(File f, int x, int y)
{
    bmpFile.seek(__Gnbmp_image_offset);

    uint32_t time = millis();

    uint8_t sdbuffer[BUFFPIXEL_X3];                 // 3 * pixels to buffer

    for (int i=0; i< __Gnbmp_height; i++) {
        for(int j=0; j<(480/BUFFPIXEL); j++) { //this 480 was originallly 320, and is used to control the max horizontal reading that is done from the image
            bmpFile.read(sdbuffer, BUFFPIXEL_X3);
            
            uint8_t buffidx = 0;
            int offset_x = j*BUFFPIXEL;
            unsigned int __color[BUFFPIXEL];
            
            for(int k=0; k<BUFFPIXEL; k++) {
                __color[k] = sdbuffer[buffidx+2]>>3;                        // read
                __color[k] = __color[k]<<6 | (sdbuffer[buffidx+1]>>2);      // green
                __color[k] = __color[k]<<5 | (sdbuffer[buffidx+0]>>3);      // blue
                
                buffidx += 3;
            }

      for (int m = 0; m < BUFFPIXEL; m ++) {
              tft.drawPixel(m+offset_x, i,__color[m]);
      }
        }
    }
    
    Serial.print(millis() - time, DEC);
    Serial.println(" ms");
}

boolean bmpReadHeader(File f) 
{
    // read header
    uint32_t tmp;
    uint8_t bmpDepth;
    
    if (read16(f) != 0x4D42) {
        // magic bytes missing
        return false;
    }

    // read file size
    tmp = read32(f);
    Serial.print("size 0x");
    Serial.println(tmp, HEX);

    // read and ignore creator bytes
    read32(f);

    __Gnbmp_image_offset = read32(f);
    Serial.print("offset ");
    Serial.println(__Gnbmp_image_offset, DEC);

    // read DIB header
    tmp = read32(f);
    Serial.print("header size ");
    Serial.println(tmp, DEC);
    
    int bmp_width = read32(f);
    int bmp_height = read32(f);
    
    if(bmp_width != __Gnbmp_width || bmp_height != __Gnbmp_height)  {    // if image is not 320x240, return false
        /*return false*/; //this has been commented out so that we can draw partial bitmap images, reinstitute this to ensure files are not too large/small for the screen
    }

    if (read16(f) != 1)
    return false;

    bmpDepth = read16(f);
    Serial.print("bitdepth ");
    Serial.println(bmpDepth, DEC);

    if (read32(f) != 0) {
        // compression not supported!
        return false;
    }

    Serial.print("compression ");
    Serial.println(tmp, DEC);

    return true;
}

/*********************************************/
// These read data from the SD card file and convert them to big endian
// (the data is stored in little endian format!)

// LITTLE ENDIAN!
uint16_t read16(File f)
{
    uint16_t d;
    uint8_t b;
    b = f.read();
    d = f.read();
    d <<= 8;
    d |= b;
    return d;
}

// LITTLE ENDIAN!
uint32_t read32(File f)
{
    uint32_t d;
    uint16_t b;

    b = read16(f);
    d = read16(f);
    d <<= 16;
    d |= b;
    return d;
}



void setup(void) {
  //SCREEN IDENTIFICATION AND SD SD CARD DETECTION//
  
  //Serial.begin(9600);
  //Serial.println(F("TFT LCD test"));

  tft.reset();

  uint16_t identifier = 0x9486; //We are only using this with one type of screen, so no need to identify it
/*tft.readID();*/
  
  tft.begin(identifier);  
  tft.setRotation(1); 
  //making the background
  tft.fillScreen(WHITE);
  
  //Init SD_Card
  pinMode(10, OUTPUT);
   
  if (!SD.begin(10)) {
    //Serial.println("initialization failed!");
    tft.setCursor(0, 0);
    tft.setTextColor(WHITE);    
    tft.setTextSize(1);
    tft.println("SD Card Init fail.");   
  }else
  //Serial.println("initialization done."); 
  //tft.fillRect(300,0,20,480,WHITE); //for all shapes: x, y, width, height, color
  
  //BUTTON DRAWING AND TOUCHSCREEN SETUP//
  
  tft.setRotation(3);
  //making buttons and text fields
  //tft.fillRect(300,160,180,160,GREEN); //1000>x>600 and 900>y>500
  //tft.fillRect(300,0,180,160,MAGENTA); //940ish>x>620 (130 to 905 y total so 522 is the middle)
  tft.fillRect(0,0,180,160,GREEN); //spageddy code
  tft.fillRect(0,160,180,160,MAGENTA);
  tft.setTextSize(4);
  //tft.setTextColor(BLACK);
   //set the rotation down here so that the text will draw correctly. Maybe the program could start at rotation 3 and then switch to 1 right before the flag goes up?
  //for rotation 3, upper right corner is 0,0
  pinMode(XM, OUTPUT);
  pinMode(YP, OUTPUT);

  //EXTRA SETUP THINGS AND I2C//
  //bmpFile = SD.open(__Gsbmp_files[0]);
 /*
        if (! bmpFile) {
            Serial.println("didnt find image");
            tft.setTextColor(WHITE);    tft.setTextSize(1);
            tft.println("didnt find BMPimage");
            while (1);
        }
   
        if(! bmpReadHeader(bmpFile)) {
            Serial.println("bad bmp");
            tft.setTextColor(WHITE);    tft.setTextSize(1);
            tft.println("bad bmp");
            return;
        }*/
}

void loop(void) {

  
  if((micros()-times) >= 980000) { //every second
    if(going) {
      checki2c = true;
      tft.setCursor(200,275);
      tft.setTextColor(WHITE);
      tft.print("Timer: ");
      tft.print(countdown/60);
      tft.print(":");
      tft.print(countdown%60);
    countdown--;
    times=micros();
    }
    //Serial.println(micros());
    //Serial.println(times);
    }
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
      if(!raised) {
      times = micros();
      going = true;
      countdown = COUNTFROM;           
      tft.setCursor(200,275);
      tft.setTextColor(WHITE);
      tft.print("Timer: #:##");
      //tft.print("Timer: 3:00");
      }
    }
      else {
        going = false; 
        if(raised) {
          tft.fillScreen(WHITE);
          tft.fillRect(0,0,180,160,GREEN);
          tft.fillRect(0,160,180,160,MAGENTA);
        }
        else tft.fillRect(200,275,300,275,WHITE);
         //new
        raised=false;
      
        /*Serial.print("Magenta");*/
        } //magenta
  }
  }
  //the time is printed and checked up here for the sake of the flag, since the time must be on time while the i2c does not need to be
  tft.setCursor(200,275);
  if(going) {
    tft.setTextColor(RED);
    if(countdown < 15) {
      tft.fillScreen(BLACK);
      
      tft.setRotation(1);
      
        
         bmpFile = SD.open("01.bmp");
        bmpdraw(bmpFile, 0, 0);
        bmpFile.close();
        tft.setRotation(3);
        //TSPoint p = ts.getPoint();
        raised = true; //new
        /*while(!(p.z > MINPRESSURE && p.z < MAXPRESSURE)) {
          //Serial.println("shrek");
          TSPoint p = ts.getPoint();
          }*/
        going = false;
      
    }
    else {
      
      tft.print("Timer: ");
      tft.print(countdown/60);
      tft.print(":");
      tft.print(countdown%60);

      }
  }
  else {
    if(!raised){
    tft.setTextColor(BLUE);
    tft.print("Timer: #:##");
    }
  }

  
  if(checki2c && !raised){
  tft.setTextSize(4); //12 is WAY too big for the screen. Seems to be a scale value for the text
  tft.setTextColor(BLACK);
  tft.setCursor(200,25);
  
  delay(100); //these delays are to simulate an i2c communication happening
  tft.print("V1= ");tft.print(v1);tft.print("V"); //println will go down a line, but it will also go back to the origin x-wise which is very annoying
  tft.setCursor(200,75); //you must therefore still update the cursor's position for each new line
  
  delay(100); //these delays are to simulate an i2c communication happening
  tft.print("V2= ");tft.print(v2);tft.print("V");
  tft.setCursor(200,125);
  
  delay(100); //these delays are to simulate an i2c communication happening
  tft.print("V3= ");tft.print(v3);tft.print("V");
  tft.setCursor(200,175);
  
  delay(100); //these delays are to simulate an i2c communication happening
  tft.print("V4= ");tft.print(v4);tft.print("V");
  
  }
  
  checki2c = false;
}

    
