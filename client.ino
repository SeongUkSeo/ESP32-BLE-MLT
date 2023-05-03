#include <NimBLEDevice.h>
#include <NimBLERemoteCharacteristic.h>

#define SERVICE_UUID "abba0001-0000-1000-8000-00805f9b34fb"
#define CHARACTERISTIC_UUID "abba0002-0000-1000-8000-00805f9b34fb"

bool doConnect = false;
bool connected = false;
uint16_t sensorValues[5];

class ClientCallbacks: public NimBLEClientCallbacks {
    void onConnect(NimBLEClient* pClient) {
        connected = true;
        Serial.println("Connected to server");
    };

    void onDisconnect(NimBLEClient* pClient) {
        connected = false;
        Serial.println("Disconnected from server");
        doConnect = true;
    };
};

void notifyCallback(
    NimBLERemoteCharacteristic* pRemoteCharacteristic,
    uint8_t* pData,
    size_t length,
    bool isNotify) {

    memcpy(sensorValues, pData, length);

    Serial.print("Received Notification: ");
    for (int i = 0; i < length / 2; i++) {
        Serial.print(sensorValues[i]);
        Serial.print(" ");
    }
    Serial.println();
}

void setup() {
    Serial.begin(115200);

    NimBLEDevice::init("");

    NimBLEDevice::setPower(ESP_PWR_LVL_P9);
    NimBLEScan* pScan = NimBLEDevice::getScan();
    pScan->setInterval(45);
    pScan->setWindow(15);
    pScan->setActiveScan(true);
    pScan->start(5, onScanEnd);
}

void onScanEnd(NimBLEScanResults results) {
    NimBLEAdvertisedDevice* myDevice;

    for (int i = 0; i < results.getCount(); i++) {
        myDevice = results.getDevice(i);
        if (myDevice->isAdvertisingService(NimBLEUUID(SERVICE_UUID))) {
            Serial.print("Found Service on device: ");
            Serial.println(myDevice->getAddress().toString().c_str());
            doConnect = true;
            break;
        }
    }

    if (doConnect) {
        connectToServer(myDevice);
    } else {
        NimBLEDevice::getScan()->start(0);
    }
}

void connectToServer(NimBLEAdvertisedDevice* device) {
    NimBLEClient* pClient = NimBLEDevice::createClient();

    pClient->setClientCallbacks(new ClientCallbacks());

    if (!pClient->connect(device)) {
        Serial.println("Failed to connect, starting scan");
        NimBLEDevice::getScan()->start(0);
        return;
    }

    NimBLERemoteService* pService = pClient->getService(SERVICE_UUID);
    if (pService == nullptr) {
        Serial.println("Failed to find service");
        pClient->disconnect();
        return;
    }

    NimBLERemoteCharacteristic* pCharacteristic = pService->getCharacteristic(CHARACTERISTIC_UUID);
    if (pCharacteristic == nullptr) {
        Serial.println("Failed to find characteristic");
        pClient->disconnect();
        return;
    }

    if (pCharacteristic->canNotify()) {
        pCharacteristic->subscribe(true, notifyCallback);
    } else {
        Serial.println("Unable to subscribe to notifications");
        pClient->disconnect();
    }
}

void loop() {
    // Your main loop code here
}
