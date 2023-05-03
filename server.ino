#include <NimBLEDevice.h>

#define SERVICE_UUID "abba0001-0000-1000-8000-00805f9b34fb"
#define CHARACTERISTIC_UUID "abba0002-0000-1000-8000-00805f9b34fb"

uint16_t sensorValues[5];
NimBLEServer* pServer;
NimBLECharacteristic* pCharacteristic;

class ServerCallbacks: public NimBLEServerCallbacks {
    void onConnect(NimBLEServer* pServer) {
        Serial.println("Client connected");
    };

    void onDisconnect(NimBLEServer* pServer) {
        Serial.println("Client disconnected");
    };
};

void setup() {
    Serial.begin(115200);

    NimBLEDevice::init("ESP32-BLE");

    pServer = NimBLEDevice::createServer();
    pServer->setCallbacks(new ServerCallbacks());

    NimBLEService* pService = pServer->createService(SERVICE_UUID);

    pCharacteristic = pService->createCharacteristic(
        CHARACTERISTIC_UUID,
        NIMBLE_PROPERTY::READ |
        NIMBLE_PROPERTY::NOTIFY
    );

    pCharacteristic->setValue((uint8_t*)sensorValues, 10);

    pService->start();

    NimBLEAdvertising* pAdvertising = NimBLEDevice::getAdvertising();
    pAdvertising->addServiceUUID(SERVICE_UUID);
    pAdvertising->start();
}

void loop() {
    readSensorValues();

    if (pServer->getConnectedCount() > 0) {
        pCharacteristic->setValue((uint8_t*)sensorValues, 10);
        pCharacteristic->notify();
    }

    delay(1000);
}

void readSensorValues() {
    // Replace these lines with your own code to read sensor values
    sensorValues[0] = 1001;
    sensorValues[1] = 1002;
    sensorValues[2] = 1003;
    sensorValues[3] = 1004;
    sensorValues[4] = 1005;
}
