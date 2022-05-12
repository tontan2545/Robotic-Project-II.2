xterm -T "Computer Vision" -e bash -c "/usr/bin/python3 /home/rootuser/Desktop/Project-2/detect_serial.py" &
xterm -T "Serial Monitor" -e bash -c "sleep 30; screen /dev/ttyACM0 115200" &



