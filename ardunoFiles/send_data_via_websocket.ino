#include <WiFi.h>
#include <WebServer.h>
#include <WebSocketsServer.h>

const char* ssid = "ESP32_Emitter";  
const char* password = "123@ishan";  

WebServer server(80); // HTTP Server on port 80
WebSocketsServer webSocket(81); // WebSocket Server on port 81

// Device and data tracking variables
unsigned long previousMillis = 0;
const long interval = 1000;  // Interval for updating RSSI (1 second)

void setup() {
    Serial.begin(115200);

    WiFi.softAP(ssid, password);  // Start ESP32 as Access Point
    Serial.println("ESP32 Emitter (AP & Server) started...");
    Serial.print("IP Address: ");
    Serial.println(WiFi.softAPIP());

    // Start HTTP Server for POST requests
    server.on("/data", HTTP_POST, handleData); 
    server.begin();
    
    // Start WebSocket Server
    webSocket.begin();  
    webSocket.onEvent(webSocketEvent); // Set the WebSocket event handler
    Serial.println("WebSocket Server Started!");
}

void handleData() {
    if (server.hasArg("plain")) {
        String receivedData = server.arg("plain");
        Serial.print("Received Data: ");
        Serial.println(receivedData);
        
        // Send the received data to all connected WebSocket clients
        webSocket.broadcastTXT(receivedData);  // Broadcast the received data to all WebSocket clients
        
        server.send(200, "text/plain", "Data Received: " + receivedData);  // Send a response back to the HTTP client
    } else {
        server.send(400, "text/plain", "Bad Request: No Data Received");
    }
}

void loop() {
    server.handleClient(); // Handle HTTP requests
    webSocket.loop();  // Handle WebSocket connections
}

// WebSocket event handler
void webSocketEvent(uint8_t num, WStype_t type, uint8_t *payload, size_t length) {
    if (type == WStype_CONNECTED) {
        Serial.println("New WebSocket client connected");

        // Send a greeting message to the newly connected client
        String data = "Hello from ESP32! Device: ESP32, IP: " + WiFi.softAPIP().toString();
        webSocket.sendTXT(num, data);  // Send greeting message to the new client
    }
    else if (type == WStype_DISCONNECTED) {
        Serial.println("WebSocket client disconnected");
    }
}
