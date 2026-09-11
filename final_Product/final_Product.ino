#define BLYNK_TEMPLATE_ID "TMPL3phzbIfGV"
#define BLYNK_TEMPLATE_NAME "Smart Agriculture System"
#define BLYNK_AUTH_TOKEN "0RoxE8WOp5NwC7vtVXETGe08mIgQA_ey"

#include <WiFi.h>
#include <WiFiClient.h>
#include <BlynkSimpleEsp32.h>
#include <DHT.h>
#include <HardwareSerial.h>
#include <ThingSpeak.h>
#include <WiFiClient.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);


char ssid[] = "iQOO Neo6";
char pass[] = "123456789";
WiFiClient client;

unsigned long channelID = 3400396;
const char * writeAPIKey = "Z9W5PC6IAJ9N6QCR";
#define DHTPIN 4
#define DHTTYPE DHT22

#define SOIL_PIN 36
#define RAIN_PIN 34
#define PH_PIN 35
#define RE_DE 18
#define RELAY_PIN 26

HardwareSerial NPKSerial(2);

byte nitrogenCmd[]  = {0x01,0x03,0x00,0x1E,0x00,0x01,0xE4,0x0C};
byte phosphorusCmd[] = {0x01,0x03,0x00,0x1F,0x00,0x01,0xB5,0xCC};
byte potassiumCmd[]  = {0x01,0x03,0x00,0x20,0x00,0x01,0x85,0xC0};

DHT dht(DHTPIN, DHTTYPE);

BlynkTimer timer;
int manualPump = -1;
bool autoMode = true;
float temperature = 0;
float humidity = 0;
int soilMoisture = 0;
int rainValue = 0;
float pH = 0;
int nitrogen = 0;
int phosphorus = 0;
int potassium = 0;
int rainProbability = 0;
String recommendedCrop = "Waiting...";
bool pumpState = false;
BLYNK_WRITE(V10)
{
   recommendedCrop = param.asStr();

   Serial.print("Crop Received: ");
   Serial.println(recommendedCrop);
}

BLYNK_WRITE(V5)
{
  int value = param.asInt();

  if(value == 1)
  {
     manualPump = 1;    // FORCE ON
  }
  else
  {
     manualPump = 0;    // FORCE OFF
  }
  Serial.print("Manual Pump = ");
Serial.println(manualPump);
}

BLYNK_WRITE(V17)
{
   autoMode = param.asInt();


   Serial.print("V17 Received: ");
   Serial.println(autoMode);
}


// ---------------- SENSOR FUNCTION ----------------

void sendSensorData()
{
humidity = dht.readHumidity();
temperature = dht.readTemperature();

soilMoisture = analogRead(SOIL_PIN);
rainValue = analogRead(RAIN_PIN);

int phRaw = analogRead(PH_PIN);
float voltage = phRaw * (3.3 / 4095.0);
pH = 7 + ((2.5 - voltage) / 0.18);

nitrogen = readNPK(nitrogenCmd);
phosphorus = readNPK(phosphorusCmd);
potassium = readNPK(potassiumCmd);
 
  String soilHealth;


  static bool dryAlertSent = false;

if (soilMoisture > 3500 && autoMode == 0)
{
    if (!dryAlertSent)
    {
        Serial.println("SENDING SOIL DRY EVENT");

        if(Blynk.connected())
        {
            Blynk.logEvent(
                "soil_dry",
                "Soil is dry and Auto Mode is OFF. Irrigation required."
            );
        }

        dryAlertSent = true;
    }
}
else
{
    dryAlertSent = false;
}

if(pH >= 6.0 && pH <= 7.5 &&
   nitrogen >= 40 &&
   phosphorus >= 40 &&
   potassium >= 40)
{
    soilHealth = "Excellent";
}
else if(pH >= 5.5 && pH <= 8.0 &&
        nitrogen >= 20 &&
        phosphorus >= 20 &&
        potassium >= 20)
{
    soilHealth = "Good";
}
else if(pH >= 5.0 && pH <= 8.5)
{
    soilHealth = "Moderate";
}
else
{
    soilHealth = "Poor";
}
 //Send Data to Blynk

  if (!isnan(temperature) && !isnan(humidity))
  {
    Blynk.virtualWrite(V0, temperature);
    Blynk.virtualWrite(V1, humidity);
  }

  Blynk.virtualWrite(V2, soilMoisture);
  Blynk.virtualWrite(V3, pH);
  Blynk.virtualWrite(V4, rainValue);
  Blynk.virtualWrite(V6, nitrogen);
  Blynk.virtualWrite(V7, phosphorus);
  Blynk.virtualWrite(V8, potassium);
  Blynk.virtualWrite(V11, soilHealth);
  //updateOLED(soilHealth);
// ---------- PUMP CONTROL ----------
if(autoMode)
{
   // AUTOMATIC MODE

   if(soilMoisture > 3600)
   {
      pumpState = true;
   }
   else if(soilMoisture < 3000)
   {
      pumpState = false;
   }

   if(pumpState)
   {
      digitalWrite(RELAY_PIN, LOW);
      Blynk.virtualWrite(V9, "Pump ON");
   }
   else
   {
      digitalWrite(RELAY_PIN, HIGH);
      Blynk.virtualWrite(V9, "Pump OFF");
   }
}
else
{
   // MANUAL MODE

   if(manualPump == 1)
   {
      digitalWrite(RELAY_PIN, LOW);
      Blynk.virtualWrite(V9, "Pump ON");
   }
   else
   {
      digitalWrite(RELAY_PIN, HIGH);
      Blynk.virtualWrite(V9, "Pump OFF");
   }
}
  // ---------- SERIAL MONITOR ----------

  Serial.println("===== SENSOR DATA =====");

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");

  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.println(" %");

  Serial.print("Soil Moisture: ");
  Serial.println(soilMoisture);

  Serial.print("pH Raw: ");
Serial.println(phRaw);

Serial.print("Voltage: ");
Serial.println(voltage);

Serial.print("pH Value: ");
Serial.println(pH);

  Serial.print("Rain Sensor: ");
  Serial.println(rainValue);

  Serial.print("Nitrogen: ");
  Serial.println(nitrogen);

  Serial.print("Phosphorus: ");
  Serial.println(phosphorus);

  Serial.print("Potassium: ");
  Serial.println(potassium);

  if(digitalRead(RELAY_PIN) == LOW)
{
   Serial.println("Pump Status: ON");
}
else
{
   Serial.println("Pump Status: OFF");
}

  Serial.println("========================");
}

int readNPK(byte *cmd)
{
  byte response[7];

  digitalWrite(RE_DE, HIGH);
  delay(10);

  NPKSerial.write(cmd, 8);
  NPKSerial.flush();

  digitalWrite(RE_DE, LOW);
  delay(100);

  if (NPKSerial.available() >= 7)
  {
    for(int i=0;i<7;i++)
      response[i] = NPKSerial.read();

    return (response[3] << 8) | response[4];
  }
    return 0;
}
void sendToThingSpeak()
{
  ThingSpeak.setField(1, temperature);
  ThingSpeak.setField(2, humidity);
  ThingSpeak.setField(3, soilMoisture);
  ThingSpeak.setField(4, pH);
  ThingSpeak.setField(5, nitrogen);
  ThingSpeak.setField(6, phosphorus);
  ThingSpeak.setField(7, potassium);
  ThingSpeak.setField(8, rainProbability);

  int x = ThingSpeak.writeFields(channelID, writeAPIKey);

  if(x == 200)
  {
     Serial.println("ThingSpeak Update Success");
  }
  else
  {
     Serial.print("ThingSpeak Error: ");
     Serial.println(x);
  }
}

void updateOLED(String soilHealth)
{
    display.clearDisplay();

    display.setTextSize(2);
    display.setTextColor(WHITE);

    display.setCursor(0,0);
    display.println("SOIL");

    display.setCursor(0,25);
    display.println(soilHealth);

    display.display();

    delay(3000);

    display.clearDisplay();

    display.setCursor(0,0);
    display.println("CROP");

    display.setCursor(0,25);
    display.println(recommendedCrop);

    display.display();

    delay(3000);
}

// ---------------- SETUP ----------------

void setup()
{
  Serial.begin(115200);


  pinMode(RELAY_PIN, OUTPUT);

  digitalWrite(RELAY_PIN, HIGH); // Pump OFF

  dht.begin();
  
Wire.begin(21,22);

if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C))
{
   Serial.println("OLED Failed");
   while(true);
}

display.clearDisplay();
display.display();

 Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);
 ThingSpeak.begin(client);
Blynk.syncVirtual(V17);
Blynk.syncVirtual(V5);

timer.setInterval(2000L, sendSensorData);
timer.setInterval(20000L, sendToThingSpeak);
  pinMode(RE_DE, OUTPUT);
  NPKSerial.begin(9600, SERIAL_8N1, 16, 17);
}
// ---------------- LOOP ----------------

void loop()
{
  Blynk.run();
  timer.run();
}
