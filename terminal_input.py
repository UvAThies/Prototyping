from controls import MotorControl
import time


def main():
    controls = MotorControl()

    controls.stop()

    # listen for arrow keys
    while True:
        key = input()
        trigger_input = 0
        joy_input = 127

        if "w" in key:
            trigger_input = 1
        elif "s" in key:
            trigger_input = -1
        if "a" in key:
            joy_input = 0
        elif "d" in key:
            joy_input = 255

        controls.motor_instructions(trigger_input, joy_input)
        time.sleep(1)
        controls.stop()


if __name__ == "__main__":
    main()
