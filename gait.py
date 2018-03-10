import numpy as np
import cv2
import argparse
import imutils
from math import atan2, pi
import math
import matplotlib.pyplot as plt
from scipy.interpolate import spline,interp1d
from matplotlib.backends.backend_pdf import PdfPages

#global declerations
angle_arr=[]
angle_arr_red=[]
angle_arr_yellow=[]
knee_angle=[]
knee_angle_red=[]
ankle_angle=[]
hip_angle=[]
pelvis_angle=[]
angle_arr_pelvis=[]
pp=PdfPages('report.pdf')
knee_final_arr=[]
ankle_final_arr=[]
hip_final_arr=[]
pelvis_final_arr=[]

greenLower = np.array([25, 80, 5])	#green
greenUpper = np.array([80, 255, 255])

#redLower_1=(0,100,100)
#redUpper_1=(10,255,255)
redLower = (112,75,75)	#red
redUpper = (200, 255, 255)

#greenLower = np.array([40,60,30])	#green
#greenUpper = np.array([87,100,83])

yellowLower=np.array([20,100,100])
yellowUpper=np.array([30,255,255])

#camera source mobile or video[0 or 1]
#cam_source = 'http://192.168.43.1:8080/videofeed'
cam_source='abc.mp4'
camera = cv2.VideoCapture(cam_source)


def calc_angle():
	while True:

		(grabbed, frame) = camera.read()
	
		frame = imutils.resize(frame, width=800, height=600)
	
		hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) 
		#LAB=cv2.cvtColor(frame,cv2.COLOR_BGR2LAB)
		mask_red = cv2.inRange(hsv, redLower, redUpper)
		#mask_red_1 = cv2.inRange(hsv, redLower_1, redUpper_1)
		#mask_red=cv.Add(mask_red,mask_red_1)
		mask_green = cv2.inRange(hsv, greenLower, greenUpper)
		mask_yellow = cv2.inRange(hsv, yellowLower, yellowUpper)
		
		
		#erode and dilate
		mask_red = cv2.erode(mask_red, None, iterations=2)
		mask_red = cv2.dilate(mask_red, None, iterations=2)
		mask_green = cv2.erode(mask_green, None, iterations=2)
		mask_green = cv2.dilate(mask_green, None, iterations=2)
		mask_yellow = cv2.erode(mask_yellow, None, iterations=2)
		mask_yellow = cv2.dilate(mask_yellow, None, iterations=2)
		
	
	
		result_red=cv2.bitwise_and(frame, frame, mask=mask_red)
		result_green=cv2.bitwise_and(frame, frame, mask=mask_green)
		result_yellow=cv2.bitwise_and(frame, frame, mask=mask_yellow)
		
		
		mask_red, contours_red, hierarchy_red = cv2.findContours(mask_red, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
		mask_green, contours_green, hierarchy_green = cv2.findContours(mask_green, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
		mask_yellow, contours_yellow, hierarchy_yellow = cv2.findContours(mask_yellow, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
		
	
		coord=np.array(contours_green)
	
		cv2.drawContours(mask_green, contours_green, -1, (0, 255, 0), 2)
		cv2.drawContours(mask_red, contours_red, -1, (255, 0, 0), 2)
		cv2.drawContours(mask_yellow, contours_yellow, -1, (255, 0, 0), 2)
		
		
		cv2.imshow('mask green',mask_green)
		cv2.imshow('mask red',mask_red)
		cv2.imshow('mask yellow',mask_yellow)
		cv2.imshow('res green',result_green)
		#cv2.imshow('res red',result_red)
		
		
		contours_green=np.asarray(contours_green)
		contours_red=np.asarray(contours_red)
		contours_yellow=np.asarray(contours_yellow)
		
		
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break
		
		if(len(contours_green)==6):
			
			#nu=nu+1
			for x in range(1,len(contours_green)):
				#cv2.imwrite(str(x)+'.png',mask)
				
				x2=contours_green[x][0]
				y2=contours_green[x][1]		
				x1=contours_green[x-1][0]
				y1=contours_green[x-1][1]
				deltax = x2-x1
				deltay = y2 - y1
				m=deltay/deltax
				
				angle_rad = math.atan(m[0][1])
				angle_deg = angle_rad*180.0/pi
		
				angle_arr.append(angle_deg)
				#print(angle_arr,"\n")
		nu=1		
		if(len(contours_red)>=5):
			#cv2.imwrite(str(nu)+'.png',mask_red)
			nu=nu+1
			for x in range(1,len(contours_red)):
				#cv2.imwrite(str(x)+'.png',frame)
				
				x1=contours_red[x][0]
				y1=contours_red[x][1]		
				x2=contours_red[x-1][0]
				y2=contours_red[x-1][1]

				deltax_1 = x2-x1
				deltay_1 = y2 - y1
				m_1=deltay_1/deltax_1
				
				angle_rad_red = math.atan(m_1[0][1])
				angle_deg_red = angle_rad_red*180.0/pi
		
				angle_arr_red.append(angle_deg_red)
				#print(angle_arr_red,"\n")		


		if(len(contours_yellow)>=1 and len(contours_green)==6):
			#cv2.imwrite(str(nu)+'.png',mask_red)
			nu=3
			
			#cv2.imwrite(str(x)+'.png',frame)
			
			x1=contours_yellow[0][0]
			y1=contours_yellow[0][1]		
			x2=contours_green[nu][0]
			y2=contours_green[nu][1]

			deltax_2 = x2-x1
			deltay_2 = y2 - y1
			m_2=deltay_2/deltax_2
				
			angle_rad_yellow = math.atan(m_2[0][1])
			angle_deg_yellow = angle_rad_yellow*180.0/pi
	
			angle_arr_pelvis.append(angle_deg_yellow)
			#print(angle_arr_red,"\n")		

		#print(angle_arr_pelvis)
def draw_graph():
	
	print("length of array is ",len(angle_arr))
	v=3

	for y in range(1,len(angle_arr)):
		v=v+4
		w=v+1
		#print(v)
		if(v<len(angle_arr) and w<len(angle_arr)):
			z=90-angle_arr[v]-angle_arr[w]
			knee_angle.append(z)

	#y=1
	v=3	
	
	
	print(len(knee_angle))
	for ki in range(0,len(knee_angle)):
		knee_final_arr.append(ki)
	#knee_final_arr.append(ki+1)
	
	#plt.plot(knee_angle)
	#x=np.array([1,2,3,4,5,6,7,8,9,10,11])
	x_smooth=np.linspace(0,ki,150)
	y_smooth=spline(knee_final_arr,knee_angle,x_smooth)	
	plt.plot(x_smooth,y_smooth)
	#plt.plot(knee_angle)
	#plt.plot(knee_angle_red)
	plt.ylabel('knee angle')
	plt.show()
	#plt.savefig('report.pdf')
	'''pp.savefig(knee)
	pp.close()'''
	
	
	
def draw_graph_ankle():
	y=1
	v=5
	for y in range(1,(len(angle_arr))):
		v=v+4
		if(v<len(angle_arr)):
			z=45-angle_arr[v]
			ankle_angle.append(z)
			
	for ai in range(0,len(ankle_angle)):
		ankle_final_arr.append(ai)
	#ankle_final_arr.append(ai+1)
	#x=np.array([1,2,3,4,5,6,7,8,9,10,11])
	x_smooth=np.linspace(0,ai,300)
	y_smooth=spline(ankle_final_arr,ankle_angle,x_smooth)	
	plt.plot(x_smooth,y_smooth)		
	#plt.plot(ankle_angle)
	plt.ylabel('ankle angles')
	#plt.savefig('report.pdf')
	plt.show()
	
def draw_graph_hip():
	y=1
	v=1
	for y in range(1,(len(angle_arr))):
		v=v+4
		if(v<len(angle_arr)):
			z=90-angle_arr[v]
			hip_angle.append(z)
	
	for hi in range(0,len(hip_angle)):
		hip_final_arr.append(hi)
	#hip_final_arr.append(hi+1)
	#x=np.array([1,2,3,4,5,6,7,8,9,10,11])
	
	x_smooth=np.linspace(0,hi,300)
	y_smooth=spline(hip_final_arr,hip_angle,x_smooth)	
	plt.plot(x_smooth,y_smooth)
	

	plt.plot(hip_angle)
	plt.ylabel('hip angles')
	plt.show()
	#plt.savefig('report.pdf')
		
def draw_graph_pelvis():
	for y in range(1,len(angle_arr_pelvis)):
		z1=45-angle_arr_pelvis[y]
		pelvis_angle.append(z1)
	
	for pi in range(1,len(pelvis_angle)):
		pelvis_final_arr.append(pi)
	pelvis_final_arr.append(pi+1)
	
	
	x_smooth=np.linspace(0,pi+1,300)
	y_smooth=spline(pelvis_final_arr,pelvis_angle,x_smooth)	
	plt.plot(x_smooth,y_smooth)

	#plt.plot(pelvis_angle)
	plt.ylabel('pelvis tilt')
	plt.show()	
try:		
	calc_angle();
except:
	draw_graph_pelvis();
	draw_graph();
	draw_graph_ankle();
	draw_graph_hip();
	