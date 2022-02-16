
#include <SPI.h>
#include <TFT_eSPI.h> // Hardware-specific library

#include "firework.h"

#define GIF_DALEY 20
#define TFT_BACKLIGHT_PIN 25

void do_GIF_frame(unsigned int animation_x_offset,
                  unsigned int animation_y_offset,
                  unsigned int animation_width,
                  unsigned int animation_height,
                  unsigned int num_of_frames,
                  const uint16_t* gif_array,
                  unsigned int frameDuration);
void   tft_sleep(void) { digitalWrite(TFT_BACKLIGHT_PIN, LOW); }
void   tft_wake(void) { digitalWrite(TFT_BACKLIGHT_PIN, HIGH); }

TFT_eSPI tft = TFT_eSPI();

void setup() {
  // put your setup code here, to run once:
  pinMode(TFT_BACKLIGHT_PIN, OUTPUT);
  tft_wake();
  tft.init();
  tft.setRotation(1);

  tft.setSwapBytes(false);
  tft.fillScreen(TFT_BLACK);
  tft.setTextColor(TFT_LIGHTGREY, TFT_BLACK);
}

void do_GIF_frame(unsigned int animation_x_offset,
                  unsigned int animation_y_offset,
                  unsigned int animation_width,
                  unsigned int animation_height,
                  unsigned int num_of_frames,
                  const uint16_t* gif_array,
                  unsigned int frameDuration)
{
  static unsigned int frameIndex = 0;
  static unsigned long lastFrameTime = 0;
  unsigned long currentTime = millis();
  const unsigned int frameSize = animation_width*animation_height;
  
  if ((currentTime - lastFrameTime) >= frameDuration)
  {
    tft.pushImage(animation_x_offset, animation_y_offset,
                    animation_width , animation_height, gif_array+(frameIndex*frameSize) );
    frameIndex = (frameIndex+1)%num_of_frames;
    lastFrameTime = currentTime;
  }
}

void loop() {
  // put your main code here, to run repeatedly:
  if (millis() > 20000) {
    static int oneTime = true;
    if (oneTime)
      tft_sleep();
    oneTime = false;
    return;
  }
  if (millis() > 10000) {
    do_GIF_frame((160-firework_width)/2 ,5,firework_width ,firework_height ,
                    firework_frames ,(const uint16_t*)firework , GIF_DALEY); //centered for 160x128 tft screen
    tft.drawString("hello world!", 10, 80, 2);
  }
  else if (millis() > 8000)
    tft.drawString("1..2..3..",   10, 80, 2);
  else if (millis() > 6000)
    tft.drawString("1..2..",      10, 80, 2);
  else if (millis() > 4000)
    tft.drawString("1..       ",  10, 80, 2);
  else
    tft.drawString("ready...",    10, 80, 2);
}
