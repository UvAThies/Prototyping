# Prototyping

\subsection{Usage manual} \label{manual}
To operate the Rescue Turtle, first flash Raspberry Pi OS onto a Raspberry Pi 4 computer and connect it to a network or mobile hotspot. Next, establish a connection to a wired display or connect with VNC in order to access the desktop environment of the Raspberry Pi. Now clone the remote repository containing a Python application for driving the robot from \href{https://github.com/UvAThies/Prototyping}{UvAThies/Prototyping}. Now create a Python virtual environment, activate it and install the provided requirements from \texttt{requirements.txt} using the following commands:
\begin{verbatim}
    > python3 -m venv venv
    > source venv/bin/activate
    > pip install -r requirements.txt
\end{verbatim}.
Now simply execute the start-up script for the necessary services by running the \texttt{./start.sh} bash script. This will turn on the camera live-stream at localhost:8081 which can be accessed at [hostname]:8081 from any device in the same network. This script will also activate the previously installed Python virtual environment and run the Python web control application. This control panel can be accessed at [hostname]:5000, so in our case at turtle.local:5000. The robot can now be controlled using the two virtual joy-sticks in the web-interface. The left joy-stick controls the camera angle, and the right joy-stick controls the robot movement. The movement has been tuned, so the robot will rotate in-place if the joy-stick is only moved horizontally.
