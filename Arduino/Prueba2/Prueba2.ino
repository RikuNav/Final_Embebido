int sensorPin = A0; // the potentiometer is connected to analog pin 0
int sensorValue; // an integer variable to store the potentiometer reading

void setup() { // this function runs once when the sketch starts up
  // initialize serial communication :
  Serial.begin(9600);
}

void loop() { // this loop runs repeatedly after setup() finishes
  sensorValue = analogRead(sensorPin); // read the sensor
  Serial.println(sensorValue); // output reading to the serial line
  delay (100); // Pause in milliseconds before next reading
}
