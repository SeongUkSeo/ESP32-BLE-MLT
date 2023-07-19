#include <WiFi.h>
#include <DHT.h>
#include <HTTPClient.h>

#define SUNLIGHT_PIN 32
#define SOIL_MOISTURE_PIN 34
#define DHT_PIN 33
#define DHT_TYPE DHT11

const char* ssid = "NETGEAR52";
const char* passwd = "Iamplant20";
const char* servername = "http://192.168.1.5:5000/data-endpoint";

DHT dht(DHT_PIN, DHT_TYPE);

void setup() {
  Serial.begin(115200);
  delay(4000);
  dht.begin();
  delay(4000);

  WiFi.begin(ssid, passwd);
  while (WiFi.status() != WL_CONNECTED){
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}
char* readSensorValues(){
  static char _post[58] = {'\0'};

  float _sensing_temperature = dht.readTemperature();
  delay(10);
  float _sensing_humidity = dht.readHumidity();
  int sensing_error_code = 0;

  while(isnan(_sensing_temperature) || isnan(_sensing_humidity)){
    _sensing_temperature = dht.readTemperature();
    delay(10);
    _sensing_humidity = dht.readHumidity();
    delay(10);
    sensing_error_code = 1;
  }

  int sensing_sunlight = analogRead(SUNLIGHT_PIN);
  int sensing_soilmoisture = analogRead(SOIL_MOISTURE_PIN);

  int sensing_temperature = (int)(_sensing_temperature * 100);
  int sensing_humidity = (int)(_sensing_humidity * 100);

  
  snprintf(
    _post,
    sizeof(_post),
    "ID=%s&TP=%d&HM=%d&SN=%d&SM=%d&EC=%d",
    WiFi.macAddress().c_str(),
    sensing_temperature,
    sensing_humidity,
    sensing_sunlight,
    sensing_soilmoisture,
    sensing_error_code);
  Serial.println(_post);
  return _post;
}

void loop(){
    Serial.println(WiFi.macAddress());
    if((WiFi.status() == WL_CONNECTED)){
        HTTPClient http;
        http.begin(servername);
        http.addHeader("Content-Type", "application/x-www-form-urlencoded");

        int httpResponseCode = http.POST(readSensorValues());
        
        if (httpResponseCode>0){
            String response = http.getString();
            Serial.println(httpResponseCode);
            Serial.println(response);
        }
        else{
            Serial.print("Error on sending POST: ");
            Serial.println(httpResponseCode);
        }
        http.end();
    }
    delay(20000);
}
