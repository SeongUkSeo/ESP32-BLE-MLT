#include <NimBLEDevice.h>
#include <WiFi.h>

#define MAX_DEVICES 3
#define WIFI_SSID "YOUR_SSID"
#define WIFI_PASSWORD "YOUR_PASSWORD"
#define SERVER_URL "http://your-server-url.com/data"

NimBLEAdvertisedDevice* devices[MAX_DEVICES];
uint8_t deviceCount = 0;

void setup() {
    Serial.begin(115200);

    // Wi-Fi 연결
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");

    // BLE 장치 초기화
    NimBLEDevice::init("");
    NimBLEDevice::setPower(ESP_PWR_LVL_P9); // 최대 전력 설정
    NimBLEScan* pScan = NimBLEDevice::getScan();
    pScan->setAdvertisedDeviceCallbacks(new AdvertisedDeviceCallbacks());
    pScan->setActiveScan(true);
    pScan->start(5, scanEndedCallback);
}

void loop() {
    for (uint8_t i = 0; i < deviceCount; i++) {
        if(devices[i] != nullptr) {
            NimBLEClient* pClient = NimBLEDevice::getDisconnectedClient();

            if(pClient->connect(devices[i])) {
                Serial.println("Connected to device");
                NimBLERemoteCharacteristic* pRemoteCharacteristic = pClient->getService("YOUR_SERVICE_UUID")->getCharacteristic("YOUR_CHARACTERISTIC_UUID");
                
                if(pRemoteCharacteristic && pRemoteCharacteristic->canNotify()) {
                    pRemoteCharacteristic->subscribe(true);
                    std::string value = pRemoteCharacteristic->readValue();
                    Serial.println(value.c_str());

                    // Send the value to the server
                    HTTPClient http;
                    http.begin(SERVER_URL);
                    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
                    http.POST("value=" + value);
                    http.end();
                }
                pClient->disconnect();
            } else {
                Serial.println("Failed to connect to the device");
            }

            delete devices[i];
            devices[i] = nullptr;
        }
    }

    deviceCount = 0;
    NimBLEDevice::getScan()->start(5, scanEndedCallback);
    delay(1000);
}

class AdvertisedDeviceCallbacks: public NimBLEAdvertisedDeviceCallbacks {
    void onResult(NimBLEAdvertisedDevice* advertisedDevice) {
        if (deviceCount < MAX_DEVICES && advertisedDevice->getName() == "YOUR_TARGET_DEVICE_NAME") {
            devices[deviceCount] = new NimBLEAdvertisedDevice(*advertisedDevice);
            deviceCount++;
        }
    }
};

void scanEndedCallback(NimBLEScanResults results) {
    Serial.println("Scan Ended");
}
