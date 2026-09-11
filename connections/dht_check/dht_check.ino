#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();

  Serial.println("DHT22 Test Started");
}

void loop() {

  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    Serial.println("DHT22 NOT DETECTED");
  } else {
    Serial.print("Temperature: ");
    Serial.print(t);
    Serial.println(" °C");

    Serial.print("Humidity: ");
    Serial.print(h);
    Serial.println(" %");
  }

  Serial.println("----------------");
  delay(2000);
}
