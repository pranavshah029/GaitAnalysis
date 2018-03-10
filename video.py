import cv2
import time
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import imutils

start_time = float(round(time.time() * 1, 3))
cap= cv2.VideoCapture('pss.mp4')
start_video = 0
end_video = 0
def f1():
	while True:
		ret, frame=cap.read()
		#grabbed=imutils.resize(frame,width=600)
		cv2.imshow('Frame', frame)
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			start_video = float(round(time.time() * 1,3)) - start_time
			print(start_video)
		if key == ord("w"):
			end_video = float(round(time.time() * 1,3)) - start_time
			print(end_video)
			ffmpeg_extract_subclip("pss.mp4", start_video, end_video, targetname="output.mp4")
			break;


try:
	f1();
	t1= start_video	
	t2= end_video	
	print(t1,t2)		
	#ffmpeg_extract_subclip("pss.mp4", t1, t2, targetname="output.mp4")
except:
	print("exp")
