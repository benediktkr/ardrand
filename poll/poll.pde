#include <string.h>

int pin=5;
void setup() {
    Serial.begin(115200);
    int mode = 0;   
}

void loop() {
    poll();
}

void poll() {
    Serial.println(analogRead(pin));
}

boolean do_tlsrnd() {
    /* 1. Find a and b = (analogRead&1)^(analogRead>>1&1)
     *      the exclusive-or of the two least sign. bits of
     *      two consequtive analogRead
     * 3. vonNuemann box both values b
     */
    
    while(1) {
        bool a = (analogRead(pin)&1) ^ (analogRead(pin)>>1&1);
        bool b = (analogRead(pin)&1) ^ (analogRead(pin)>>1&1);

        if (a^b == 1) {
            return a;
        }
    }
}

void tlsr() {
    if (do_tlsrnd())
        Serial.print("1");
    else
        Serial.print("0");
}
