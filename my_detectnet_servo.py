import jetson.inference
import jetson.utils
import serial

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = jetson.utils.videoSource("csi://0")      # '/dev/video0' for V4L2
display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file

while display.IsStreaming():
	img = camera.Capture()
	detections = net.Detect(img)
	for detection in detections:
		if detection.ClassID == 1:
			print(detection)
			angle_x = (detection.Center[0]/1280)*180
			angle_y = (detection.Center[1]/720)*180
			print(angle_x,angle_y)
			cmd = '{"servo1": %d,"servo2":%d}' %(angle_x,angle_y)
			print(cmd)
			ser.write(cmd)

	display.Render(img)
	display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))

ser.close()
