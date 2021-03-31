#define sensorCount 4
#define triggerPin 3
#define echoPin1 4
#define echoPin2 5
#define echoPin3 6
#define echoPin4 7
#define pingDelay 50      // How many milliseconds between each measurement ; keep > 5ms
#define debugDelay 200    // How many milliseconds between each Serial.print ; keep > 200ms
#define soundSpeed 343.0  // Speed of sound in m/s

volatile unsigned travelTime[sensorCount];
volatile unsigned startTime[sensorCount];
float distance[sensorCount];
unsigned long lastPollMillis;
unsigned long lastDebugMillis;

// for pin states
byte echoPinState[sensorCount];

void setup() {
  // set group PCIIE2
  PCICR |= B00000100;

  // activate PCINT for 4, 5, 6, 7
  PCMSK2 |= B11110000;

  pinMode(triggerPin, OUTPUT);   // Set common triggerpin as output
  
  Serial.begin(115200);
  while (!Serial) {
    ; // Wait for Serial
  }
  Serial.println("--- Serial monitor started ---");

  for (int i = 0; i < sensorCount; i++) {
    echoPinState[i] = false;
  }
}

// PCINT2
ISR (PCINT2_vect) {
  interruptHandler(digitalRead(echoPin1), 0);
  interruptHandler(digitalRead(echoPin2), 1); 
  interruptHandler(digitalRead(echoPin3), 2);
  interruptHandler(digitalRead(echoPin4), 3);
}

// Common function for interrupts
void interruptHandler(bool pinState, int nIRQ) {
  unsigned long currentTime = micros();  // Get current time (in µs)
  
  if (pinState && echoPinState[nIRQ] == false) {
    // If pin state has changed to HIGH -> remember start time (in µs)
    startTime[nIRQ] = currentTime;
    echoPinState[nIRQ] = true;
  } else if (!pinState && echoPinState[nIRQ] == true) {
    // If pin state has changed to LOW -> calculate time passed (in µs)
    travelTime[nIRQ] = currentTime - startTime[nIRQ];
    echoPinState[nIRQ] = false;
  }
}

void doMeasurement() {
  noInterrupts();   // cli()
  for (int i = 0; i < sensorCount; i++) {
    distance[i] = travelTime[i] / 2.0 * (float)soundSpeed / 10000.0;   // in cm
  }
  interrupts();   // sei();

  // set next trigger
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  digitalWrite(triggerPin, HIGH);    // HIGH pulse for at least 10µs
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);     // Set LOW again
}

void loop() {
   // Poll every x ms
  if (lastPollMillis == 0 || (millis() - lastPollMillis >= pingDelay)) {
    doMeasurement();
    lastPollMillis = millis();
  }
  
  // Print every y ms (comment out in production)
  if (millis() - lastDebugMillis >= debugDelay) {
    for (int i = 0; i < sensorCount; i++) {
      Serial.print(distance[i]);
      Serial.print(" - ");
    }
    Serial.println();
    lastDebugMillis = millis();
  }
}
