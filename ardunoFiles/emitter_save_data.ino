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

     //Init SD
    Serial.begin(9600);
    pinMode(SD_ENABLE,OUTPUT);
    digitalWrite(SD_ENABLE,LOW);
    sdspi.begin(VSPI_SCLK,VSPI_MISO,VSPI_MOSI,VSPI_SS);
    SD.begin(VSPI_SS,sdspi);
    SaveData = SD.open("/SaveData.txt", FILE_WRITE);
    SaveData.close();
}

// Function to handle incoming data from receivers
void handleData() {
    if (server.hasArg("plain")) {
        String receivedData = server.arg("plain");
        // Serial.print("Received Data: ");
        // Serial.println(receivedData);
        SaveData = SD.open("/SaveData.txt", FILE_APPEND);
        // Serial.println(SaveData);
        SaveData.println(receivedData);
        SaveData=SD.open("/SaveData.txt");
          while (SaveData.available()) {
             Serial.write(SaveData.read());
        }
        SaveData.close();
        // Respond to the client
        server.send(200, "text/plain", "Data Received: " + receivedData);
    } else {
        server.send(400, "text/plain", "Bad Request: No Data Received");
    }
}

void loop() {
    server.handleClient(); // Process incoming HTTP requests
}