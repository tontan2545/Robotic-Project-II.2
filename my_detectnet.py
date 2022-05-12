import jetson.inference
import jetson.utils
from jetson.utils import cudaDrawLine as draw_line
from jetson.utils import cudaDrawRect as draw_rect
from jetson.utils import cudaFont

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.3)
camera = jetson.utils.videoSource("csi://0")      # '/dev/video0' for V4L2
display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file
font = cudaFont(size=24)

def check_boundary(left:int, right: int, img_width: int, no_sections=8, padding=2, acceptable_zone=1) -> str:
	#if the object 
	if(left < img_width//no_sections*padding and right > img_width//no_sections*(no_sections-padding)):
		return "Go backwards"
	# if the object is in between the left and right acceptable zone
	if(left > img_width//no_sections*(padding+acceptable_zone) and right <  img_width//no_sections*(no_sections-padding-acceptable_zone)):
		return "Go forward"
	if(left < img_width//no_sections*padding or right < img_width//no_sections*(no_sections - padding - acceptable_zone)):
		return "Go left"
	if(right > img_width//no_sections*(no_sections-padding) or left > img_width//no_sections*(padding + acceptable_zone)):
		return "Go right"
	return "Ok"

def marker(img, detection):
	font.OverlayText(img, int(img.width), int(img.height), "I'm detecting this person na ja", int(detection.Left), int(detection.Top-24), font.White)

def display_line_segments(img, width, height, no_sections=8, color=(255,255,255,180), thickness=1, padding=2, acceptable_zone=1):
	for section in range(no_sections):
		draw_line(img, (width//no_sections * section - thickness,0), (width//no_sections * section - thickness,height), color, thickness)

while display.IsStreaming():
	img = camera.Capture()
	height, width = img.height, img.width
	detections = net.Detect(img)
	# for detection in detections:
	# 		print(detection.ClassID)
	# 		print(detection.Confidence)
	# 		print(detection.Left, detection.Right, detection.Top, detection.Bottom)

	display_line_segments(img, width, height)
	# draw_line(img, (width//8 * 2,0), (width//8 * (2+1),height), (152,255,152,180), 3)
	draw_rect(img,(width//8*2, height, width//8*(2+1), 0), (152,255,152,100))
	# draw_line(img, (width//8 * (8-2),0), (width//8 * (8-2-1),height), (152,255,152,180), 3)
	draw_rect(img,(width//8*(8-2), height, width//8*(8-2-1), 0), (152,255,152,100))
	most_sig = net.GetClassDesc(detections[0].ClassID) if detections else "None"
	for detection in detections:
		if(detection.ClassID == 1):
			result = check_boundary(detection.Left, detection.Right, width)
			font.OverlayText(img, width, height, result, 20, height-40, font.White)
			marker(img, detection)
			break
	font.OverlayText(img, width, height, f"Most significant object: {most_sig}", 0, 0, font.White)
	print([detected.Confidence for detected in detections])
	display.Render(img)
	display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))
