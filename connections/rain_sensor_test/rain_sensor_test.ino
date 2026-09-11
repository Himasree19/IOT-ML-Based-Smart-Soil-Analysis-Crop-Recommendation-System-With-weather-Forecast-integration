int rainPin = 34;

void setup() {

  Serial.begin(115200);
}

void loop() {

  int rainValue = analogRead(rainPin);

  Serial.print("Rain Value: ");
  Serial.println(rainValue);

  delay(1000);
}
