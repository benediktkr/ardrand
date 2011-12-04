void setup() {
    Serial.begin(115200);
}

void loop() {
    char *in = (char*)malloc(6);
    int i, p;
    for(i=0; i<5; i++)
        Serial.read();
    p = (int)Serial.read();
    Serial.println(analogRead(p));
}
