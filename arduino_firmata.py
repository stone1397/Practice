from pyfirmata import Arduino, util
import time

# 아두이노 보드와 시리얼 포트 연결
board = Arduino('/dev/ttyACM0')  # 포트 번호는 환경에 따라 다를 수 있습니다.

# 서보 핀 설정
servo_pin = 9

# 서보 모터 제어 함수
def move_servo(angle):
    board.digital[servo_pin].write(angle)

# 아두이노 보드 초기화 대기 시간
time.sleep(2)

while True:
    # 예시로 잠금/잠금 해제 명령을 주기적으로 실행
    move_servo(0)  # 잠금 해제 (0도)
    print("Servo moved to 0 degrees (Unlocked)")
    time.sleep(5)  # 5초 대기
    move_servo(90)  # 잠금 (90도)
    print("Servo moved to 90 degrees (Locked)")
    time.sleep(5)  # 5초 대기
