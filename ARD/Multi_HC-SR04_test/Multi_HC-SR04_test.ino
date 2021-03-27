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
byte echoPin1State = LOW;
byte echoPin2State = LOW;
byte echoPin3State = LOW;
byte echoPin4State = LOW;

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
}

// PCINT2
ISR (PCINT2_vect) {
  if (digitalRead(echoPin1) && !echoPin1State) {
    echoPin1State = !echoPin1State;
    interruptHandler(echoPin1State, 0);
  } else {
    echoPin1State = !echoPin1State;
    interruptHandler(echoPin1State, 0);
  }

  if (digitalRead(echoPin2) && !echoPin2State) {
    echoPin2State = !echoPin2State;
    interruptHandler(echoPin2State, 1);  
  } else {
    echoPin2State = !echoPin2State;
    interruptHandler(echoPin2State, 1);
  }

  if (digitalRead(echoPin3) && !echoPin3State) {
    echoPin3State = !echoPin3State;
    interruptHandler(echoPin3State, 2);
  } else {
    echoPin3State = !echoPin3State;
    interruptHandler(echoPin3State, 2);
  }

  if (digitalRead(echoPin4) && !echoPin4State) {
    echoPin4State = !echoPin4State;
    interruptHandler(echoPin4State, 3);
  } else {
    echoPin4State = !echoPin4State;
    interruptHandler(echoPin4State, 3);
  }
}

// Common function for interrupts
void interruptHandler(bool pinState, int nIRQ) {
  unsigned long currentTime = micros();  // Get current time (in µs)
  
  if (pinState) {
    // If pin state has changed to HIGH -> remember start time (in µs)
    startTime[nIRQ] = currentTime;
  } else {
    // If pin state has changed to LOW -> calculate time passed (in µs)
    travelTime[nIRQ] = currentTime - startTime[nIRQ];
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
