const int sensorPin = A0;
const int ledPins[] = {2, 3, 4};
const int numLeds = 3;

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < numLeds; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
}

void loop() {
  int sensorValue = analogRead(sensorPin);
  Serial.println(sensorValue);

  int threshold = map(sensorValue, 0, 1023, 0, numLeds);

  for (int i = 0; i < numLeds; i++) {
    digitalWrite(ledPins[i], i < threshold ? HIGH : LOW);
  }

  delay(200);
}