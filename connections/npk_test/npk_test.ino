#include <ModbusMaster.h>

#define RE_DE 18

ModbusMaster node;

void preTransmission() {
  digitalWrite(RE_DE, HIGH);
}

void postTransmission() {
  digitalWrite(RE_DE, LOW);
}

void setup() {
  Serial.begin(115200);

  pinMode(RE_DE, OUTPUT);
  digitalWrite(RE_DE, LOW);

  Serial2.begin(9600, SERIAL_8N1, 16, 17);

  node.begin(2, Serial2);

  node.preTransmission(preTransmission);
  node.postTransmission(postTransmission);

  Serial.println("NPK Test Started");
}

void loop() {

  uint8_t result = node.readHoldingRegisters(0x001E, 3);

  if (result == node.ku8MBSuccess) {

    Serial.print("Nitrogen: ");
    Serial.println(node.getResponseBuffer(0));

    Serial.print("Phosphorus: ");
    Serial.println(node.getResponseBuffer(1));

    Serial.print("Potassium: ");
    Serial.println(node.getResponseBuffer(2));

  } else {

    Serial.print("Modbus Error: ");
    Serial.println(result);

  }

  Serial.println("----------------");
  delay(3000);
}
