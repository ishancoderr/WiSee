#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "ESP32_Emitter";  
const char* password = "123@ishan";
const char* serverAddress = "http://192.168.4.1/data"; // ESP32 Server IP

String deviceID = "Receiver_2"; // Change this for each device (Receiver_1, Receiver_2, etc.)

void setup() {
    Serial.begin(115200);

    // Connect to the ESP32 Emitter's WiFi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nConnected to ESP32 Emitter");

    // Print WiFi connection details
    Serial.print("SSID: ");
    Serial.println(WiFi.SSID());
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());

    // Check RSSI immediately after connection
    int rssi = WiFi.RSSI();
    Serial.print("Initial RSSI: ");
    Serial.println(rssi);
}

void loop() {
    if (WiFi.status() == WL_CONNECTED) {
        int rssi = WiFi.RSSI(); // Measure signal strength

        // Create data in CSV format: "DeviceID, RSSI, Timestamp"
        String data = deviceID + "," + String(rssi) + "," + String(millis());
        Serial.print("Sending Data: ");
        Serial.println(data);

        // Send data to the server
        HTTPClient http;
        http.begin(serverAddress);
        http.addHeader("Content-Type", "text/plain");

        int responseCode = http.POST(data);
        Serial.print("Server Response: ");
        Serial.println(responseCode);

        http.end();
    } else {
        Serial.println("WiFi Disconnected!");
    }

    delay(1000); // Send every second
}