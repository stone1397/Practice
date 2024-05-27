#include <Servo.h>

Servo myservo;
int pirPin = 2;
int servoPin = 9;
unsigned long lastMotionDetectedTime = 0;
const unsigned long motionTimeout = 10000; // 10 seconds

void setup() {
  pinMode(pirPin, INPUT);
  myservo.attach(servoPin);
  Serial.begin(9600);
  myservo.write(90); // 기본 상태를 "열림"으로 설정
}

void loop() {
  if (digitalRead(pirPin) == HIGH) {
    Serial.println("Motion detected");
    lastMotionDetectedTime = millis(); // millis() 현재 시간 의미
    delay(1000);  // Debounce delay
  }

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // command에 Serial에서 줄바꿈을 하기 전까지의 string을 저장
    if (command == "Unlock") {
      myservo.write(90); // 잠금 해제
    } else if (command == "Lock") {
      myservo.write(0);  // 잠금
    }
  }

  // 사람이 감지되지 않은 시간이 설정된 타임아웃을 초과하면 "열림" 상태로 전환
  if (millis() - lastMotionDetectedTime > motionTimeout) {
    myservo.write(90);  // 기본 "열림" 상태로 전환
    Serial.println("No motion detected");
    delay(1000);  // Debounce delay
  }
}
