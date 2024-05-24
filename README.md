## Usage Manual

To operate the Rescue Turtle, follow these steps:

1. **Prepare the Raspberry Pi**:
    - Flash Raspberry Pi OS onto a Raspberry Pi 4 computer.
    - Connect it to a network or mobile hotspot.

2. **Access the Raspberry Pi**:
    - Connect to a wired display or use VNC to access the desktop environment of the Raspberry Pi.

3. **Clone the Repository**:
    - Clone the remote repository containing a Python application for driving the robot from [UvAThies/Prototyping](https://github.com/UvAThies/Prototyping).

4. **Set Up the Python Environment**:
    - Create a Python virtual environment, activate it, and install the provided requirements from `requirements.txt` using the following commands:
    ```bash
    > python3 -m venv venv
    > source venv/bin/activate
    > pip install -r requirements.txt
    ```

5. **Start the Services**:
    - Execute the start-up script for the necessary services by running the `./start.sh` bash script.
    - This script will turn on the camera live-stream at `localhost:8081`, which can be accessed at `[hostname]:8081` from any device in the same network.
    - The script will also activate the previously installed Python virtual environment and run the Python web control application.
    - The control panel can be accessed at `[hostname]:5000`, typically at `turtle.local:5000`.

6. **Control the Robot**:
    - Use the two virtual joy-sticks in the web interface to control the robot.
        - The left joy-stick controls the camera angle.
        - The right joy-stick controls the robot movement.
    - The movement is tuned so the robot will rotate in place if the joy-stick is only moved horizontally.
