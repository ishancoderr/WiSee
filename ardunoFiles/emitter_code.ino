#include <WiFi.h>
#include <WebServer.h>

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
}

// Function to handle incoming data from receivers
void handleData() {
    if (server.hasArg("plain")) {
        String receivedData = server.arg("plain");
        Serial.print("Received Data: ");
        Serial.println(receivedData);

        // Respond to the client
        server.send(200, "text/plain", "Data Received: " + receivedData);
    } else {
        server.send(400, "text/plain", "Bad Request: No Data Received");
    }
}

void loop() {
    server.handleClient(); // Process incoming HTTP requests
}