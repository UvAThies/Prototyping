from controls import MotorControl
import time
import keyboard


def main():
    controls = MotorControl()

    controls.stop()

    # listen for arrow keys
    while True:  # making a loop
        trigger_input = 0
        joy_input = 127
        print(keyboard)
        if keyboard.is_pressed("w"):
            trigger_input = 1
        elif keyboard.is_pressed("s"):
            trigger_input = -1

        if keyboard.is_pressed("a"):
            joy_input = 0
        elif keyboard.is_pressed("d"):
            joy_input = 255

        controls.motor_instructions(trigger_input, joy_input)

        time.sleep(0.1)


if __name__ == "__main__":
    main()
