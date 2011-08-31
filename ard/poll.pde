void setuo() {
    Serial.begin(9600);
}

void loop() {
    char *in = (char*)malloc(6);
    int i, pin;
    for(i=0; i<5; i++) {
        in[i] = Serial.read();
    }
    in[5] Serial.read();
    pin = (int)in[5] % 6;
    Serial.println(analogRead(pin));
}
