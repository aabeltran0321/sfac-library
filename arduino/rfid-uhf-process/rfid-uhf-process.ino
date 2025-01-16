/*
 * --------------------------------------------------------------------------------------------------------------------
 * Example sketch/program showing how to read data from a PICC to serial.
 * --------------------------------------------------------------------------------------------------------------------
 * This is a MFRC522 library example; for further details and other examples see: https://github.com/miguelbalboa/rfid
 * 
 * Example sketch/program showing how to read data from a PICC (that is: a RFID Tag or Card) using a MFRC522 based RFID
 * Reader on the Arduino SPI interface.
 * 
 * When the Arduino and the MFRC522 module are connected (see the pin layout below), load this sketch into Arduino IDE
 * then verify/compile and upload it. To see the output: use Tools, Serial Monitor of the IDE (hit Ctrl+Shft+M). When
 * you present a PICC (that is: a RFID Tag or Card) at reading distance of the MFRC522 Reader/PCD, the serial output
 * will show the ID/UID, type and any data blocks it can read. Note: you may see "Timeout in communication" messages
 * when removing the PICC from reading distance too early.
 * 
 * If your reader supports it, this sketch/program will read all the PICCs presented (that is: multiple tag reading).
 * So if you stack two or more PICCs on top of each other and present them to the reader, it will first output all
 * details of the first and then the next PICC. Note that this may take some time as all data blocks are dumped, so
 * keep the PICCs at reading distance until complete.
 * 
 * @license Released into the public domain.
 * 
 * Typical pin layout used:
 * -----------------------------------------------------------------------------------------
 *             MFRC522      Arduino       Arduino   Arduino    Arduino          Arduino
 *             Reader/PCD   Uno/101       Mega      Nano v3    Leonardo/Micro   Pro Micro
 * Signal      Pin          Pin           Pin       Pin        Pin              Pin
 * -----------------------------------------------------------------------------------------
 * RST/Reset   RST          9             5         D9         RESET/ICSP-5     RST
 * SPI SS      SDA(SS)      10            53        D10        10               10
 * SPI MOSI    MOSI         11 / ICSP-4   51        D11        ICSP-4           16
 * SPI MISO    MISO         12 / ICSP-1   50        D12        ICSP-1           14
 * SPI SCK     SCK          13 / ICSP-3   52        D13        ICSP-3           15
 */

#include <SPI.h>
#include <MFRC522.h>

constexpr uint8_t RST_PIN = 48;          // Configurable, see typical pin layout above
constexpr uint8_t SS_PIN = 53;         // Configurable, see typical pin layout above

MFRC522 mfrc522(SS_PIN, RST_PIN);  // Create MFRC522 instance


//LED INIT

#include "FastLED.h"

/*************************************************
   ANDROID AMBILIGHT APPLICATION ARDUINO SKETCH

   set following values to your needs
 *************************************************/

#define INITIAL_LED_TEST_ENABLED true
#define INITIAL_LED_TEST_BRIGHTNESS 16  // 0..255
#define INITIAL_LED_TEST_TIME_MS 500  // 10..

// Number of leds in your strip.
// Tested with 500 leds and is fine (despite the warning)
// We will use a maximum of 300
#define MAX_LEDS 82

// type of your led controller, possible values, see below
#define LED_TYPE WS2812B 

// 3 wire (pwm): NEOPIXEL BTM1829 TM1812 TM1809 TM1804 TM1803 UCS1903 UCS1903B UCS1904 UCS2903 WS2812 WS2852
//               S2812B SK6812 SK6822 APA106 PL9823 WS2811 WS2813 APA104 WS2811_40 GW6205 GW6205_40 LPD1886 LPD1886_8BIT 
// 4 wire (spi): LPD8806 WS2801 WS2803 SM16716 P9813 APA102 SK9822 DOTSTAR

// For 3 wire led stripes line Neopixel/Ws2812, which have a data line, ground, and power, you just need to define DATA_PIN.
// For led chipsets that are SPI based (four wires - data, clock, ground, and power), both defines DATA_PIN and CLOCK_PIN are needed

// DATA_PIN, or DATA_PIN, CLOCK_PIN
#define LED_PINS 6        // 3 wire leds
//#define LED_PINS 6, 13  // 4 wire leds

#define COLOR_ORDER GRB  // colororder of the stripe, set RGB in hyperion

#define OFF_TIMEOUT 8000    // ms to switch off after no data was received, set 0 to deactivate

#define BRIGHTNESS 255                      // maximum brightness 0-255
#define DITHER_MODE BINARY_DITHER           // BINARY_DITHER or DISABLE_DITHER
#define COLOR_TEMPERATURE CRGB(255,255,255) // RGB value describing the color temperature
#define COLOR_CORRECTION  TypicalLEDStrip   // predefined fastled color correction
//#define COLOR_CORRECTION  CRGB(255,255,255) // or RGB value describing the color correction

// Baudrate, higher rate allows faster refresh rate and more LEDs
#define BAUD_RATE 115200      // use 115200 for ftdi based boards


/*************************************************
   ANDROID AMBILIGHT APPLICATION ARDUINO SKETCH

   no user changes needed
 *************************************************/

// Adalight sends a "Magic Word" before sending the pixel data
uint8_t prefix[] = {'A', 'd', 'a'}, hi, lo, chk, i;

unsigned long endTime;

// Define the array of leds
CRGB leds[MAX_LEDS];

// set color to all leds
void showColor(const CRGB& led) {
  #if MAX_LEDS > 1
  LEDS.showColor(led);
  #endif
}

// switch of leds
void switchOff() {
  #if MAX_LEDS > 1
  memset(leds, 0, MAX_LEDS * sizeof(struct CRGB));
  FastLED.show();
  #endif
}


void setup() {
	Serial.begin(115200);		// Initialize serial communications with the PC
  Serial1.begin(115200);	
  Serial2.begin(115200);	
  Serial3.begin(115200);	
	while (!Serial);		// Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)
	SPI.begin();			// Init SPI bus
	mfrc522.PCD_Init();		// Init MFRC522
	mfrc522.PCD_DumpVersionToSerial();	// Show details of PCD - MFRC522 Card Reader details
	Serial.println(F("Scan PICC to see UID, SAK, type, and data blocks..."));
  led_init();
}

void loop() {
	mfrc522_process();
  led_process();
  if((millis()-prevMillis) > 1000){
    uhf_rfid_process();
    prevMillis = millis();
  }

}

void uhf_rfid_process1(){
  // Define the data to send
  byte data[] = {0xBB, 0x00, 0x27, 0x00, 0x03, 0x22, 0x27, 0x10, 0x83, 0x7E};
  int dataSize = sizeof(data);

  // Send the data to Serial1
  Serial1.write(data, dataSize);

  // Wait for a response
  delay(100); // Allow time for the response

  // Collect and print the response as a hex string
  if (Serial1.available() > 0) {
    String response = ""; // Initialize an empty string to store the response
    while (Serial1.available() > 0) {
      byte responseByte = Serial1.read();
      
      if (responseByte < 0x10) response += "0"; // Add leading zero if necessary
      response += String(responseByte, HEX);   // Convert to hex and append
      response += " ";                         // Add space between hex values
    }
    response.trim();                           // Remove trailing space
    Serial.print("uhf1-");
    Serial.println(response);                  // Print the response as a single string
  }
}

void uhf_rfid_process2(){
  // Define the data to send
  byte data[] = {0xBB, 0x00, 0x27, 0x00, 0x03, 0x22, 0x27, 0x10, 0x83, 0x7E};
  int dataSize = sizeof(data);

  // Send the data to Serial1
  Serial2.write(data, dataSize);

  // Wait for a response
  delay(100); // Allow time for the response

  // Collect and print the response as a hex string
  if (Serial2.available() > 0) {
    String response = ""; // Initialize an empty string to store the response
    while (Serial2.available() > 0) {
      byte responseByte = Serial2.read();
      
      if (responseByte < 0x10) response += "0"; // Add leading zero if necessary
      response += String(responseByte, HEX);   // Convert to hex and append
      response += " ";                         // Add space between hex values
    }
    response.trim();                           // Remove trailing space
    Serial.print("uhf2-");
    Serial.println(response);                  // Print the response as a single string
  }
}

void uhf_rfid_process3(){
  // Define the data to send
  byte data[] = {0xBB, 0x00, 0x27, 0x00, 0x03, 0x22, 0x27, 0x10, 0x83, 0x7E};
  int dataSize = sizeof(data);

  // Send the data to Serial1
  Serial3.write(data, dataSize);

  // Wait for a response
  delay(100); // Allow time for the response

  // Collect and print the response as a hex string
  if (Serial3.available() > 0) {
    String response = ""; // Initialize an empty string to store the response
    while (Serial3.available() > 0) {
      byte responseByte = Serial3.read();
      
      if (responseByte < 0x10) response += "0"; // Add leading zero if necessary
      response += String(responseByte, HEX);   // Convert to hex and append
      response += " ";                         // Add space between hex values
    }
    response.trim();                           // Remove trailing space
    Serial.print("uhf3-");
    Serial.println(response);                  // Print the response as a single string
  }
}

void mfrc522_process(){
  if (mfrc522.PICC_IsNewCardPresent()) {
    if (mfrc522.PICC_ReadCardSerial()) {
      Serial.print("PROCESS");
      byte scannedUID[4]; // Store the scanned UID
      for (byte i = 0; i < mfrc522.uid.size; i++) {
        scannedUID[i] = mfrc522.uid.uidByte[i];
        Serial.print(scannedUID[i] < 0x10 ? " 0" : " ");
        Serial.print(scannedUID[i], HEX);
      }
      Serial.println();
    }
  }
}

void led_init(){
  int ledCount = MAX_LEDS;

  #if MAX_LEDS > 1
    FastLED.addLeds<LED_TYPE, LED_PINS, COLOR_ORDER>(leds, ledCount);
  #endif
  
  // color adjustments
  FastLED.setBrightness ( BRIGHTNESS );
  FastLED.setTemperature( COLOR_TEMPERATURE );
  FastLED.setCorrection ( COLOR_CORRECTION );
  FastLED.setDither     ( DITHER_MODE );

  // initial RGB flash
  #if INITIAL_LED_TEST_ENABLED == true
  for (int v=0;v<INITIAL_LED_TEST_BRIGHTNESS;v++)
  {
    showColor(CRGB(255,0,0));  
    delay(INITIAL_LED_TEST_TIME_MS/2/INITIAL_LED_TEST_BRIGHTNESS);
  }
  for (int v=0;v<INITIAL_LED_TEST_BRIGHTNESS;v++)
  {
    showColor(CRGB(0,255,0));  
    delay(INITIAL_LED_TEST_TIME_MS/2/INITIAL_LED_TEST_BRIGHTNESS);
  }
  for (int v=0;v<INITIAL_LED_TEST_BRIGHTNESS;v++)
  {
    showColor(CRGB(0,0,255));  
    delay(INITIAL_LED_TEST_TIME_MS/2/INITIAL_LED_TEST_BRIGHTNESS);
  }
  #endif
  showColor(CRGB(0, 0, 0));
}

void led_process(){
  while(Serial.available()){
    char c = Serial.read();
    if (c == 'r'){
      showColor(CRGB(0,255,0));  
    }
    if (c == 'g'){
      showColor(CRGB(255,0,0));  
    }
    if (c == 'b'){
      showColor(CRGB(0,0,255));  
    }
    if (c == 'x'){
      showColor(CRGB(0,0,0));  
    }
  }
}