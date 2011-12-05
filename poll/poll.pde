#include <string.h>

int pin;
void setup() {
    Serial.begin(115200);
    int mode = 0;   
}

void loop() {

    if (Serial.available > 0) {
        
        char *in = (char*)malloc(Serial.available() + 1);
        int i, p;
        for(i=0; i<Serial.available()-2; i++) {
            // Read the bytes (should be 
            // Is either:
            //    POLL
            //    TLSR
            in[i] = (char)Serial.read();
        }
        
        // Discard the whitespace and set null-byte
        Serial.read();
        in[4] = '\0';
        
        // Set pin-number. 
        p = (int)Serial.read();
        pin = p;
    }
    poll();
    
    free(in);
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
