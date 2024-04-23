# Code from old groups
# Modified by: Thies Nieborg & Tijn Schuitevoerder

import RPi.GPIO as GPIO
import signal
import sys


class MotorControl:
    def __init__(self):
        PIN = 18
        self.M1 = 6
        self.M2 = 13
        self.M3 = 20
        self.M4 = 21

        PWMA = 12
        PWMB = 26

        self.motor_1_PWM = None
        self.motor_2_PWM = None

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN, GPIO.IN, GPIO.PUD_UP)
        GPIO.setup(self.M1, GPIO.OUT)
        GPIO.setup(self.M2, GPIO.OUT)
        GPIO.setup(self.M3, GPIO.OUT)
        GPIO.setup(self.M4, GPIO.OUT)
        GPIO.setup(PWMA, GPIO.OUT)
        GPIO.setup(PWMB, GPIO.OUT)

        self.motor_1_PWM = GPIO.PWM(PWMA, 50)
        self.motor_2_PWM = GPIO.PWM(PWMB, 50)
        self.motor_1_PWM.start(100)
        self.motor_2_PWM.start(100)

    def play_sound(self):
        print("Playing sound")

    def stop_sound(self):
        print("Stopping sound")

    # https://www.waveshare.com/wiki/RPi_Motor_Driver_Board
    # Motor A: PWA1, PWA2.
    # Motor B: PWB1, PWB2.
    def set_motor(self, A1, A2, B1, B2):
        assert A1 != A2 or (A1 == 0 and A2 == 0)
        assert B1 != B2 or (B1 == 0 and B2 == 0)

        GPIO.output(self.M1, A1)
        GPIO.output(self.M2, A2)
        GPIO.output(self.M3, B1)
        GPIO.output(self.M4, B2)

    def forward(self):
        self.set_motor(1, 0, 0, 1)

    def stop(self):
        self.set_motor(0, 0, 0, 0)

    def reverse(self):
        self.set_motor(0, 1, 1, 0)

    def set_motor_new(self, left_dir, right_dir):
        if left_dir == 1 and right_dir == 1:
            # both forwards
            self.set_motor(1, 0, 0, 1)

        if left_dir == -1 and right_dir == -1:
            # both backwards
            self.set_motor(0, 1, 1, 0)

        if left_dir == 1 and right_dir == -1:
            # left forward, right backward
            self.set_motor(1, 0, 1, 0)  # wellicht omkeren

        if left_dir == -1 and right_dir == 1:
            # left backward, right forward
            self.set_motor(0, 1, 0, 1)  # wellicht omkeren

        if left_dir == 0 and right_dir == 0:
            # both stop
            self.set_motor(0, 0, 0, 0)

    # motor instructions, expects values:
    # Trigger_inp: waarde tussen -1 en 1 die aangeeft hoeveel gas wordt gegeven. 1=vol gas vooruit, -1=vol gas achteruit, 0=neutraal
    # Joy_inp: waarde tussen 0 en 255 die aangeeft hoeveel naar links of rechts wordt gestuurd. 0=volledig naar links, 255=volledig naar rechts, 127=neutraal
    def motor_instructions(self, trigger_inp, joy_inp):
        # Steer_value: waarde tussen 0 en 100 die aangeeft hoeveel naar links of rechts wordt gestuurd. 100=rechts, 0=links, 50=niet sturen
        steer_value = joy_inp * 100 / 255

        # Neutral steering;
        if abs(trigger_inp) * 100 <= 1:
            if steer_value - 50 >= 2:
                self.motor_1_PWM.ChangeDutyCycle(abs(steer_value - 50))
                self.motor_2_PWM.ChangeDutyCycle(abs(steer_value - 50))
                self.set_motor(1, 0, 1, 0)
            elif steer_value - 50 <= -2:
                self.motor_1_PWM.ChangeDutyCycle(abs(steer_value - 50))
                self.motor_2_PWM.ChangeDutyCycle(abs(steer_value - 50))
                self.set_motor(0, 1, 0, 1)
            else:
                self.stop()
        else:
            voor_achter = trigger_inp / abs(trigger_inp)  # 1: vooruit, -1: achteruit

            # Override voor meetfouten
            if steer_value < 0:
                steer_value = 0
            elif steer_value > 100:
                steer_value = 100

            steer_value_1 = steer_value
            steer_value_2 = 100 - steer_value
            steer_max = max(steer_value_1, steer_value_2)
            steer_value_1_scaled = steer_value_1 / steer_max * 100 * abs(trigger_inp)
            steer_value_2_scaled = steer_value_2 / steer_max * 100 * abs(trigger_inp)
            print("trigger_inp:{}".format(trigger_inp))
            print("steer_value:{}".format(steer_value))
            print("dutycycle_motor_1:{}".format(steer_value_1_scaled))
            print("dutycycle_motor_2:{}".format(steer_value_2_scaled))
            if voor_achter == 1:  # Gas vooruit en sturen
                self.motor_1_PWM.ChangeDutyCycle(steer_value_2_scaled)
                self.motor_2_PWM.ChangeDutyCycle(steer_value_1_scaled)
                self.forward()
            elif voor_achter == -1:  # Gas achteruit en sturen
                self.motor_1_PWM.ChangeDutyCycle(steer_value_2_scaled)
                self.motor_2_PWM.ChangeDutyCycle(steer_value_1_scaled)
                self.reverse()

    def motor_instructions_new(self, joy_x, joy_y):

        # opposite track movement on steering, scaled
        left_track = (joy_x + joy_y * 0.5) * 100 / 2**0.5
        right_track = (joy_x - joy_y * 0.5) * 100 / 2**0.5

        if left_track > 0:
            left_dir = 1
        elif left_track < 0:
            left_dir = -1
        else:
            left_dir = 0

        if right_track > 0:
            right_dir = 1
        elif right_track < 0:
            right_dir = -1
        else:
            right_dir = 0

        left_speed = abs(left_track)
        right_speed = abs(right_track)
        self.set_motor_new(left_dir, right_dir)

        if (
            left_speed <= 100
            and left_speed <= 100
            and left_speed >= 0
            and right_speed >= 0
        ):
            self.motor_1_PWM.ChangeDutyCycle(left_speed)
            self.motor_2_PWM.ChangeDutyCycle(right_speed)

    def signal_handler(self, sig, frame):
        self.stop()
        GPIO.cleanup()
        sys.exit(0)

    def setup_sig_handler(self):
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)


class ServoControl:
    def __init__(self):
        self.servoPIN = 14
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.servoPIN, GPIO.OUT)
        self.servo = GPIO.PWM(self.servoPIN, 50)
        self.servo.start(7.5)

    def move(self, servo_x):
        # map angle from -1 1 to 2.5-12.5
        duty = servo_x * 5 + 7.5
        self.servo.ChangeDutyCycle(duty)

    def stop(self):
        print("Stopping servo")  # tijdelijk
        self.servo.ChangeDutyCycle(0)
        # self.servo.stop()
