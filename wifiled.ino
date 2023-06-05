#include <WiFi.h>
#include <ESPAsyncWebServer.h>

#define LED_PIN 2 // Change to your LED pin if different

const char* ssid = "Your_WiFi_SSID"; // Your SSID
const char* password = "Your_WiFi_Password"; // Your WiFi password

AsyncWebServer server(80);

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  Serial.begin(115200);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println(WiFi.localIP());

  // Route for handling the LED state
  server.on("/led", HTTP_GET, [](AsyncWebServerRequest *request) {
    String state;
    if (request->hasParam("state")) {
      state = request->getParam("state")->value();
      if (state == "ON") {
        digitalWrite(LED_PIN, HIGH);
      } else if (state == "OFF") {
        digitalWrite(LED_PIN, LOW);
      }
    }
    request->send(200, "text/plain", "LED state changed to " + state);
  });

  // Start server
  server.begin();
}

void loop() {}
