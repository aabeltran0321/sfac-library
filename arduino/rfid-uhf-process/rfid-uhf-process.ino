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
}

void loop() {
	mfrc522_process();
  if((millis()-prevMillis) > 1000){
    uhf_rfid_process1();
    uhf_rfid_process2();
    uhf_rfid_process3();
    prevMillis = millis();
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
