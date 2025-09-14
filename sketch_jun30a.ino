// Define which Arduino pin is connected to the photodetector's output
const int analogPin = A0;

// If you want to control the gain from the Arduino
// const int gainA0_Pin = 2; // Connect to J2 Pin 9
// const int gainA1_Pin = 3; // Connect to J2 Pin 8
// const int gainA2_Pin = 4; // Connect to J2 Pin 7

void setup() {
  // Initialize serial communication to view the results on the Serial Monitor
  Serial.begin(9600);

  // --- Optional: Gain Control ---
  // pinMode(gainA0_Pin, OUTPUT);
  // pinMode(gainA1_Pin, OUTPUT);
  // pinMode(gainA2_Pin, OUTPUT);

  // Set gain to 40 dB (A2=1, A1=0, A0=0) as an example
  // See the Gain Switch Table on page 5 of the manual.
  // digitalWrite(gainA2_Pin, HIGH); // A2 = 1
  // digitalWrite(gainA1_Pin, LOW);  // A1 = 0
  // digitalWrite(gainA0_Pin, LOW);  // A0 = 0
}

void loop() {
  // Read the raw ADC value (0-1023) from the analog pin
  int sensorValue = analogRead(analogPin);


  long totalValue = 0;

  for (int i = 0; i < 500; i++) {
    totalValue += analogRead(analogPin);
  }

  float averageValue = (float)totalValue / 500;

  Serial.println(averageValue);

  // Wait a bit before the next reading
  delay(100);
}