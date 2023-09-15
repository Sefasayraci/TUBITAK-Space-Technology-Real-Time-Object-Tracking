#include <Servo.h>

Servo servoMotor;

int servoPin = 9;  // Servo sinyal pini (başka bir pin kullanabilirsiniz)
int servoAcisi = 0;  // Servo açısı

void setup() {
  servoMotor.attach(servoPin);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    servoAcisi = Serial.parseInt();  // Python kodundan servo açısını alın

    // Servo açısını sınırlayın (örneğin, 0 ile 180 arasında)
    servoAcisi = constrain(servoAcisi, 0, 180);

    // Servo motorunu belirtilen açıya hareket ettirin
    servoMotor.write(servoAcisi);
  }
}
