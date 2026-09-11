#define RELAY_PIN 26

void setup() {
  pinMode(RELAY_PIN, OUTPUT);
}

void loop() {
  digitalWrite(RELAY_PIN, HIGH);  // OFF
  delay(3000);

  digitalWrite(RELAY_PIN, LOW);   // ON
  delay(3000);
}
