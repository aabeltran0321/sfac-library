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

#include <FastLED.h>

// Configuration
#define NUM_LEDS_PER_PIN 15   // Number of LEDs per strip
#define BRIGHTNESS 200        // Brightness level (0-255)
#define COLOR_ORDER GRB       // LED color order
#define LED_TYPE WS2812B      // LED type (compatible with WS2815B)

// Define pins for each strip
#define PIN1 6
#define PIN2 7
#define PIN3 8

// Create separate LED arrays for each pin
CRGB leds1[NUM_LEDS_PER_PIN]; // LEDs for Pin1
CRGB leds2[NUM_LEDS_PER_PIN]; // LEDs for Pin2
CRGB leds3[NUM_LEDS_PER_PIN]; // LEDs for Pin3

// Function prototypes
void setColorForPin(int pinNumber, CRGB color);

long prevMillis;

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
  byte byteArray[] = { 0xBB, 0x00, 0xB6, 0x00, 0x02, 0x07, 0xD0, 0x8F, 0x7E };
  int dataSize = sizeof(byteArray);

  // Send the data to Serial1
  Serial1.write(byteArray, dataSize);
  Serial2.write(byteArray, dataSize);
  Serial3.write(byteArray, dataSize);
}

void loop() {
	mfrc522_process();
  led_process();
  if((millis()-prevMillis) > 500){
    uhf_rfid_process1();
    uhf_rfid_process2();
    uhf_rfid_process3();
    prevMillis = millis();
  }

}

void uhf_rfid_process1(){
  // Define the data to send
//    byte data[] = {0xBB, 0x00, 0x27, 0x00, 0x03, 0x22, 0x27, 0x10, 0x83, 0x7E};

  byte data[] = {0xBB, 0x00, 0x22, 0x00, 0x00, 0x22, 0x7E};
  int dataSize = sizeof(data);

  // Send the data to Serial1
  Serial1.write(data, dataSize);

  // Wait for a response
  delay(100); // Allow time for the response

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

void uhf_rfid_process2(){
  // Define the data to send
//  byte data[] = {0xBB, 0x00, 0x27, 0x00, 0x03, 0x22, 0x27, 0x10, 0x83, 0x7E};
    byte data[] = {0xBB, 0x00, 0x22, 0x00, 0x00, 0x22, 0x7E};

  int dataSize = sizeof(data);

  // Send the data to Serial1
  Serial2.write(data, dataSize);

  // Wait for a response
  delay(100); // Allow time for the response

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

void uhf_rfid_process3(){
  // Define the data to send
//  byte data[] = {0xBB, 0x00, 0x27, 0x00, 0x03, 0x22, 0x27, 0x10, 0x83, 0x7E};
  byte data[] = {0xBB, 0x00, 0x22, 0x00, 0x00, 0x22, 0x7E};

  int dataSize = sizeof(data);

  // Send the data to Serial1
  Serial3.write(data, dataSize);

  // Wait for a response
  delay(100); // Allow time for the response

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
  // Initialize FastLED for each pin
  FastLED.addLeds<LED_TYPE, PIN1, COLOR_ORDER>(leds1, NUM_LEDS_PER_PIN).setCorrection(TypicalLEDStrip);
  FastLED.addLeds<LED_TYPE, PIN2, COLOR_ORDER>(leds2, NUM_LEDS_PER_PIN).setCorrection(TypicalLEDStrip);
  FastLED.addLeds<LED_TYPE, PIN3, COLOR_ORDER>(leds3, NUM_LEDS_PER_PIN).setCorrection(TypicalLEDStrip);

  // Set brightness
  FastLED.setBrightness(BRIGHTNESS);

  // Start with all LEDs off
  FastLED.clear();
  FastLED.show();

}
void led_process(){
  if (Serial.available() > 0) {
    // Read the serial input
    String input = Serial.readStringUntil('?');
    input.trim(); // Remove any whitespace or newline characters

    // Validate and process the input
    if (input.length() == 2) {
      char colorCode = input[0]; // First character: color (r, g, b)
      char pinNumber = input[1]; // Second character: pin number (1, 2, 3)

      // Determine the color
      CRGB color;
      switch (colorCode) {
        case 'r':
          color = CRGB::Green;
          break;
        case 'g':
          color = CRGB::Red;
          break;
        case 'b':
          color = CRGB::Blue;
          break;
        case 'x':
          color = CRGB::Black;
          break;
        default:
          Serial.println("Invalid color code. Use r, g, or b.");
          return;
      }

      // Set the color for the specified pin
      if (pinNumber >= '1' && pinNumber <= '3') {
        int pinIndex = pinNumber - '1'; // Convert character to index (0-2)
        setColorForPin(pinIndex, color);
        Serial.print("Set color ");
        Serial.print(colorCode);
        Serial.print(" for pin ");
        Serial.println(pinNumber);
      } else {
        Serial.println("Invalid pin number. Use 1, 2, or 3.");
      }
    } else {
      Serial.println("Invalid command. Use format r1, g2, b3.");
    }
  }
}

// Set color for a specific pin
void setColorForPin(int pinIndex, CRGB color) {
  CRGB *ledArray;

  // Select the correct LED array based on the pin index
  switch (pinIndex) {
    case 0:
      ledArray = leds1;
      break;
    case 1:
      ledArray = leds2;
      break;
    case 2:
      ledArray = leds3;
      break;
    default:
      return; // Invalid pin index
  }

  // Set all LEDs in the selected array to the specified color
  for (int i = 0; i < NUM_LEDS_PER_PIN; i++) {
    ledArray[i] = color;
  }

  // Update the LEDs
  FastLED.show();
}
