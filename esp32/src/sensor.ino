#include <WiFi.h>
#include <HTTPClient.h>

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

const char* ssid = "IOT-Station";
const char* password = "epitech2022";

String apiUrl = "http://iot.station:8000/metrics";
String hostname = "HW611-001";

unsigned long lastTime = 0;
unsigned long timerDelay = 5 * 1000;

#define SEA_LEVEL_PRESSURE_HPA (1013.25)
Adafruit_BME280 bme;

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  Serial.println("Connecting to WiFi...");
  while(WiFi.status() != WL_CONNECTED) {
    Serial.println("Connecting to wifi...");
    delay(500);
  }
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());

  Serial.println("Connecting to sensor...");
  bme.begin(0x77);
  Serial.println("Connected to sensor.");
}

void loop() {
  if ((millis() - lastTime) > timerDelay) { // Is the 5seconds delay done
    if(WiFi.status()== WL_CONNECTED){
      WiFiClient client;
      HTTPClient http;

      http.begin(client, apiUrl);
      http.addHeader("Content-Type", "application/json");

      String altitude = String(!isnan(bme.readAltitude(0)) ? bme.readAltitude(SEA_LEVEL_PRESSURE_HPA) : 0 );
      String pressure = String(!isnan(bme.readPressure()) ? bme.readPressure() / 100.0F : 0);
      String temperature = String(!isnan(bme.readTemperature()) ? bme.readTemperature() : 0);

      int httpResponseCode = http.POST("{\"hostname\":\"" + hostname + "\",\"altitude\":" + altitude + ",\"pressure\":" + pressure + ",\"temperature\":" + temperature + "}");

      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);

      http.end();
    }
    else {
      Serial.println("Lost connection to WiFi.");
    }
    lastTime = millis();
  }
}
