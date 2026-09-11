#define BLYNK_TEMPLATE_ID "TMPL3phzbIfGV"
#define BLYNK_TEMPLATE_NAME "Smart Agriculture System"
#define BLYNK_AUTH_TOKEN "0RoxE8WOp5NwC7vtVXETGe08mIgQA_ey"

#include <WiFi.h>
#include <WiFiClient.h>
#include <BlynkSimpleEsp32.h>

char ssid[] = "Airtel_hima_7761";
char pass[] = "Air@44243";

BlynkTimer timer;

void sendSensor()
{
  int moisture = analogRead(34);

  Serial.print("Soil Moisture: ");
  Serial.println(moisture);

  Blynk.virtualWrite(V2, moisture);
}

void setup()
{
  Serial.begin(115200);

  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);

  timer.setInterval(2000L, sendSensor);
}

void loop()
{
  Blynk.run();
  timer.run();
}
