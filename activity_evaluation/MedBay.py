import pyautogui as pag
import numpy as np
import cv2, time

def Submit_scan():
	
	pag.moveTo(1797, 923)
	pag.click()
	time.sleep(11)

def Inspect_Sample():

	pag.moveTo(1797, 923)
	time.sleep(0.5)
	pag.click()

	#create Sample
	pag.moveTo(1260,930)
	time.sleep(1)
	pag.click()
	time.sleep(61)
	
	#detect Red area
	kernal = np.ones((1920, 1080), "uint8")
	red_high = np.array([180,255,255],np.uint8)
	red_low = np.array([136,87,111],np.uint8)

	Sample_img = pag.screenshot('Sample_img.png')
	Sample_img = cv2.imread('Sample_img.png', cv2.IMREAD_COLOR)
	hsv = cv2.cvtColor(Sample_img, cv2.COLOR_BGR2HSV)

	red = cv2.inRange(hsv, red_low, red_high)
	result = cv2.bitwise_and(Sample_img, Sample_img, mask = red)

	_, contours, a=cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	xp = contours[0][0][0]

	pag.moveTo(xp[0], 844)
	pag.click()
