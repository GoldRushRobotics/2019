#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_TFTLCD.h> // Hardware-specific library
#include <MCUFRIEND_kbv.h>
//#include <Wire.h> //this line caused problems for compiling for the normal arduino

//touchscreen bits
#include <TouchScreen.h>

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
//end of touchscreen bits

#define LCD_CS A3 // Chip Select goes to Analog 3
#define LCD_CD A2 // Command/Data goes to Analog 2
#define LCD_WR A1 // LCD Write goes to Analog 1
#define LCD_RD A0 // LCD Read goes to Analog 0
//#define PIN_SD_CS 10 // Adafruit SD shields and modules: pin 10 (but we aren't using this anymore)

#define LCD_RESET A4 //*** Can alternately just connect to Arduino's reset pin *** (seems like A5 is also not used)

// Assign human-readable names to some common 16-bit color values:
#define BLACK   0x0000
#define BLUE    0x001F
#define RED     0xF800
#define GREEN   0x07E0
#define CYAN    0x07FF
#define MAGENTA 0xF81F
#define YELLOW  0xFFE0
#define WHITE   0xFFFF

MCUFRIEND_kbv tft;

float v1,v2,v3,v4=0.0; //variables for i2c, the motor controller's voltages will go here

const uint16_t identifier = 0x9486; //We are only using this with one type of screen, so no need to identify it via conditional code

//Wibbly-wobbly Timey-wymey
long int unsigned times = 0;
bool going,raised = false;
int countdown = 180;

const int COUNTFROM = 10; //change this around to change where it counts down from
//

//these are for the flag
int x = 120;
int y = 55;

//these are for the memes
String meme1 = "Sponsored";
String meme2 = "by";
String meme3 = "Walmart";
String meme4 = "Robit";


void drawFlag(int xOffset, int yOffset) { 
   
  //x is distance from left, y is distance from top, max width appears to be around 480ish before it goes off the screen. The max y height is 320
  //width and height seem to make the rectangle go up? as in towards the origin. 3rd integer is for x width
  
  tft.fillTriangle(211+xOffset, 82+yOffset, 202+xOffset, 73+yOffset, 211+xOffset, 65+yOffset, GREEN); //diamond part
  tft.fillTriangle(176+xOffset, 81+yOffset, 183+xOffset, 94+yOffset, 183+xOffset, 81+yOffset, GREEN); //whisker top
  tft.fillTriangle(205+xOffset, 81+yOffset, 210+xOffset, 122+yOffset, 197+xOffset, 93+yOffset, GREEN); //whisker top long
  tft.fillTriangle(164+xOffset, 97+yOffset, 175+xOffset, 108+yOffset, 175+xOffset, 97+yOffset, GREEN); //bottom whisker
  tft.fillTriangle(185+xOffset, 97+yOffset, 185+xOffset, 108+yOffset, 201+xOffset, 125+yOffset, GREEN); //whisker bottom long
  tft.fillTriangle(172+xOffset, 113+yOffset, 181+xOffset, 113+yOffset, 183+xOffset, 126+yOffset, GREEN); //parallelogramish thing 1
  tft.fillTriangle(183+xOffset, 126+yOffset, 193+xOffset, 126+yOffset, 181+xOffset, 113+yOffset, GREEN); //parallelogramish thing 2
  tft.fillTriangle(190+xOffset, 129+yOffset, 199+xOffset, 138+yOffset, 199+xOffset, 129+yOffset, YELLOW); //gold trapezoid point

  tft.fillRect(183+xOffset, 81+yOffset, 22, 13, GREEN); //whisker top rectangle
  tft.fillRect(175+xOffset, 97+yOffset, 10, 11, GREEN); //whisker bottom rectangle

  tft.fillRect(199+xOffset, 129+yOffset, 26, 9, YELLOW); //gold trapezoid body (NOT SYMMETRICAL)

  tft.fillRect(220+xOffset, 81+yOffset, 22, 13, GREEN); //whisker top rectangle 2
  tft.fillRect(237+xOffset, 97+yOffset, 10, 11, GREEN); //whisker bottom rectangle 2

  tft.fillTriangle(211+xOffset, 82+yOffset, 220+xOffset, 73+yOffset, 211+xOffset, 65+yOffset, GREEN); //diamond part 2
  tft.fillTriangle(246+xOffset, 81+yOffset, 239+xOffset, 94+yOffset, 239+xOffset, 81+yOffset, GREEN); //whisker top 2
  tft.fillTriangle(217+xOffset, 81+yOffset, 212+xOffset, 122+yOffset, 225+xOffset, 93+yOffset, GREEN); //whisker top long 2
  tft.fillTriangle(258+xOffset, 97+yOffset, 247+xOffset, 108+yOffset, 247+xOffset, 97+yOffset, GREEN); //bottom whisker 2
  tft.fillTriangle(237+xOffset, 97+yOffset, 237+xOffset, 108+yOffset, 221+xOffset, 125+yOffset, GREEN); //whisker bottom long 2
  tft.fillTriangle(250+xOffset, 113+yOffset, 241+xOffset, 113+yOffset, 239+xOffset, 126+yOffset, GREEN); //parallelogramish thing 1 (2)
  tft.fillTriangle(239+xOffset, 126+yOffset, 229+xOffset, 126+yOffset, 241+xOffset, 113+yOffset, GREEN); //parallelogramish thing 2
  tft.fillTriangle(232+xOffset, 129+yOffset, 223+xOffset, 138+yOffset, 223+xOffset, 129+yOffset, YELLOW); //gold trapezoid point

  tft.fillRect(0,0,480,75,GREEN); //the top green rectangle
  tft.fillRect(0,245,480,75,GREEN); //the bottom green rectangle
  tft.fillRect(405,0,75,320,YELLOW); //the gold bar on the right

  tft.fillTriangle(405,0,405,75,480,0,GREEN); //top green triangle
  tft.fillTriangle(405,320,405,245,480,320,GREEN); //bottom green triangle
}

void setup(void) {
  
  Serial.begin(9600);
  Serial.println("Screen starting up...");

  tft.reset();
  tft.begin(identifier);  

  //BUTTON DRAWING//
  tft.setRotation(3);
  tft.fillScreen(WHITE);//making the background
  tft.fillRect(0,0,180,160,GREEN); //tft.fillRect(300,160,180,160,GREEN); //1000>x>600 and 900>y>500
  tft.fillRect(0,160,180,160,MAGENTA); //tft.fillRect(300,0,180,160,MAGENTA); //940ish>x>620 (130 to 905 y total so 522 is the middle)
  
  //MEME TEXT//
  //Limit memes to 12 characters per line (including spaces)
  tft.setTextSize(4);
  tft.setTextColor(BLACK);
  
  //Line 1
  tft.setCursor(200,25);
  tft.print(meme1);

  //Line 2
  tft.setCursor(200,75);
  tft.print(meme2);

  //Line 3
  tft.setTextColor(BLUE);
  tft.setCursor(200,125);
  tft.print(meme3);

  //Line 4
  tft.setTextColor(BLACK);
  tft.setCursor(200,175);
  tft.print(meme4);

  
  //TOUCHSCREEN STUFF//  
  pinMode(XM, OUTPUT);
  pinMode(YP, OUTPUT);

  //EXTRA SETUP THINGS AND I2C GO HERE//
 
}

void loop(void) {
  
  if((micros()-times) >= 977777) { //every second, adjusted to fit the arduino's clock (maybe need to readjust for the nano on the pcb)
    if(going) {
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
    
    if(p.y > 200) { //remember the screen coordinate system was rotated and even with the mapping the touch coords are still kind of weird
      if(p.x < 242) { //green 
        if(!raised) {
          times = micros();
          Serial.write("G\n");
          going = true;
          countdown = COUNTFROM;           
          tft.setCursor(200,275);
          tft.setTextColor(WHITE);
          tft.print("Timer: #:##");
            tft.setTextSize(4);
          tft.setTextColor(BLACK);
          
          //Line 1
          tft.setCursor(200,25);
          tft.print(meme1);
        
          //Line 2
          tft.setCursor(200,75);
          tft.print(meme2);
        
          //Line 3
          tft.setTextColor(BLUE);
          tft.setCursor(200,125);
          tft.print(meme3);
        
          //Line 4
          tft.setTextColor(BLACK);
          tft.setCursor(200,175);
          tft.print(meme4);
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
        Serial.write("S\n");
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
    if(countdown < 5) {
      tft.fillRect(0,0,180,320,WHITE); //all this stuff is here to make screen clearing faster--the micro seems to struggle writing lots of pixles
      tft.setCursor(200,275);
      tft.setTextColor(WHITE);
      tft.print("Timer: 0: 5");

      tft.setTextSize(4);
      tft.setTextColor(WHITE);
  
      //Line 1
      tft.setCursor(200,25);
      tft.print(meme1);
    
      //Line 2
      tft.setCursor(200,75);
      tft.print(meme2);
    
      //Line 3
      tft.setCursor(200,125);
      tft.print(meme3);
    
      //Line 4
      tft.setCursor(200,175);
      tft.print(meme4);
      
      drawFlag(x,y);
      raised = true;
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
}
