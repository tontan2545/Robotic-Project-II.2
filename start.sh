xterm -e bash -c "/usr/bin/python3 /home/rootuser/Desktop/Project-2/detect_serial.py" &
xterm -e bash -c "sleep 30; screen /dev/ttyACM0 115200" &



