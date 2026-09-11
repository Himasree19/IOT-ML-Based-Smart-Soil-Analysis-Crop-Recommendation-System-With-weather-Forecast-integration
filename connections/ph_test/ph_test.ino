#define PH_PIN 35

void setup() {
  Serial.begin(115200);
}

void loop() {

  int phRaw = analogRead(PH_PIN);

  Serial.print("pH Raw Value: ");
  Serial.println(phRaw);

  delay(1000);
}
