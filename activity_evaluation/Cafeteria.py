import pynput
import time
"""
왼쪽 위를 기준으로 
x는 가로
y는 세로
"""


MOUSE_CONTROLLER= pynput.mouse.Controller()
MOUSE_BUTTON = pynput.mouse.Button

def Upload_Data():
	MOUSE_CONTROLLER.position=(402, 393)
	mouse.click(Button.left,1)
	time.sleep(0.5)
	mouse.click(Button.left,1)
	MOUSE_CONTROLLER.press(MOUSE_BUTTON.left)
	time.sleep(9)
	print("done")
	MOUSE_CONTROLLER.release(MOUSE_BUTTON.left)

def Empty_Garbage():
	MOUSE_CONTROLLER.position=(573, 259)
	time.sleep(0.03)
	mouse.click(Button.left,1)
	MOUSE_CONTROLLER.press(MOUSE_BUTTON.left)
	for i in range(260,450,4):
	    time.sleep(0.02)
	    MOUSE_CONTROLLER.position=(573, i)
	time.sleep(2)
	MOUSE_CONTROLLER.release(MOUSE_BUTTON.left)
	