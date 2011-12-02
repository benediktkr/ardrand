void setup() {
  Serial.begin(9600);
  randomSeed(1908);
  int i;
  for(i=0; i < 10; i++) { 
     Serial.println(random());
  }
}

void loop() { }
