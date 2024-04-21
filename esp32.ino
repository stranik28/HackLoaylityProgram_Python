#include <Arduino.h>
#include <BLEDevice.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#include "WiFi.h"
#include <HTTPClient.h>
#include <set> // Включите заголовочный файл для std::set

std::set<String> discoveredUUIDs;

int scanTime = 2; // In seconds
BLEScan *pBLEScan;
const char* ssid = "aquarium";
const char* password = "innovation";
const char* serverAddress = "185.192.246.110";
const int serverPort = 8000;

void sendUUIDToServer(const char* uuid) {
  HTTPClient http;
  String url = "http://" + String(serverAddress) + ":" + String(serverPort) + "/touch_esp/1/" + String(uuid);
  http.begin(url);
  int httpResponseCode = http.GET();
  if (httpResponseCode < 300) {
    String response = http.getString();
    Serial.println("Send uuid with " + String(uuid));
  } else {
    String response = http.getString();
    Serial.println("Not success uuid with " + String(uuid));
    
  }
    http.end();
}

class MyAdvertisedDeviceCallbacks : public BLEAdvertisedDeviceCallbacks {
  void onResult(BLEAdvertisedDevice advertisedDevice) {
    if (advertisedDevice.haveServiceUUID()) {
      BLEUUID devUUID = advertisedDevice.getServiceUUID();
      String uuidStr = devUUID.toString().c_str();
      if (discoveredUUIDs.find(uuidStr) == discoveredUUIDs.end()) {
        // Устройство еще не обнаружено, обработайте его
        sendUUIDToServer(uuidStr.c_str());
        discoveredUUIDs.insert(uuidStr); // Добавьте UUID в набор
      }
    }
  }
};

void setup() {
  Serial.println("Tarting...");
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Non Connecting to WiFi..");
  } else {
    BLEDevice::init("");
    pBLEScan = BLEDevice::getScan();
    pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
    pBLEScan->setActiveScan(true);
    pBLEScan->setInterval(100);
    pBLEScan->setWindow(99);
  }
}

void loop() {
  BLEScanResults foundDevices = pBLEScan->start(scanTime, false);
  pBLEScan->clearResults();
  Serial.println("Next round..");
  discoveredUUIDs.clear();
  delay(2000);
}
