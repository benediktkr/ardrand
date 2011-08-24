void setup() {
    Serial.begin(9600);
    Serial.println("test");

    
    // http://www.arduino.cc/cgi-bin/yabb2/YaBB.pl?num=1270982692
    // port 14 → random, 0 → 1023, 14 → 1
}

void loop() {
    int i;
    for(i=0; i<10000; i++)
      analogRead(0);
      
    Serial.println(analogRead(3));
  
}



