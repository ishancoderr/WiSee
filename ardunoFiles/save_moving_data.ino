#include <WiFi.h>
#include <WebServer.h>
#include <SD.h>
#include <SPI.h>
#include "FS.h"

File SaveData;
SPIClass sdspi = SPIClass();

const char* ssid = "ESP32_Emitter";  
const char* password = "123@ishan";   

WebServer server(80); // Create an HTTP server on port 80

unsigned long tileNo = 1;
unsigned long startTime = 0;
const unsigned long measurementDuration = 60000; // 1 minute in milliseconds
const unsigned long transitionDelay = 10000; // 5 seconds in milliseconds
bool measuring = true;

void setup() {
    Serial.begin(115200);

    // Start ESP32 as a WiFi Access Point (Emitter)
    WiFi.softAP(ssid, password);
    Serial.println("ESP32 Emitter (AP & Server) started...");
    Serial.print("IP Address: ");
    Serial.println(WiFi.softAPIP()); 

    // Setup HTTP server to receive data
    server.on("/data", HTTP_POST, handleData);
    server.begin();
    Serial.println("HTTP Server Started!");

    // Init SD
    pinMode(SD_ENABLE, OUTPUT);
    digitalWrite(SD_ENABLE, LOW);
    sdspi.begin(VSPI_SCLK, VSPI_MISO, VSPI_MOSI, VSPI_SS);
    SD.begin(VSPI_SS, sdspi);
    SaveData = SD.open("/SaveData.txt", FILE_WRITE);
    SaveData.close();

    startTime = millis(); // Start the timer
}

// Function to handle incoming data from receivers
void handleData() {
    if (server.hasArg("plain")) {
        String receivedData = server.arg("plain");
        Serial.println(receivedData);
        if (measuring) {
            SaveData = SD.open("/SaveData.txt", FILE_APPEND);
            SaveData.println(receivedData);
            SaveData.close();
        }
        // Respond to the client
        server.send(200, "text/plain", "Data Received: " + receivedData);
    } else {
        server.send(400, "text/plain", "Bad Request: No Data Received");
    }
}

void loop() {
    server.handleClient(); // Process incoming HTTP requests

    unsigned long currentTime = millis();

    if (measuring) {
        if (currentTime - startTime >= measurementDuration) {
            measuring = false;
            Serial.println("Move to next tile");
            delay(transitionDelay);
            SaveData = SD.open("/SaveData.txt", FILE_APPEND);
            SaveData.print("finished tile No");
            SaveData.println(tileNo); // Print tileNo on the same line
            SaveData.println("Move to next tile");
            SaveData.print("current time: ");
            SaveData.println(currentTime); // Print currentTime on a new line
            SaveData.close();
            tileNo = tileNo+1;
            startTime = currentTime; // Reset the timer for the transition delay
        }
    } else {
        if (currentTime - startTime >= transitionDelay) {
            measuring = true;
            startTime = currentTime; // Reset the timer for the next measurement
        }
    }
}