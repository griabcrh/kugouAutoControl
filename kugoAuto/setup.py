import pythoncom
import pyHook
import time
import sys
import win32api
import win32con
import thread

# 监听鼠标的键盘时，判断是否执行Alt + F5，防止多次操作
count = 0
# 监听等待时长时，判断是否执行Alt + F5，防止多次操作
timeCount = 0
# 表示松开键盘
KEYEVENTF_KEYUP = 0x0002
# 开始时间
starttime = 0
# 结束时间
endtime = 0
# 防止执行Alt + F5操作被键盘事件监听
preventTimeCauseKeyboart = 0
# 打印出当前状态
status = "running"

def onMouseEvent(event):
	global count
	global KEYEVENTF_KEYUP
	global starttime
	global timeCount
	global status
	if count == 0:
		count = 1
		win32api.keybd_event(18,0,0,0)
		win32api.keybd_event(116,0,0,0)
		win32api.keybd_event(116,0,KEYEVENTF_KEYUP,0)
		win32api.keybd_event(18,0,KEYEVENTF_KEYUP,0)
		timeCount = 0
		status = "stop"
		print status
	starttime = time.time()
	return True
	
	
def onKeyboardEvent(event):
	if event.Key == 'Escape':
		sys.exit()
	global preventTimeCauseKeyboart
	if preventTimeCauseKeyboart == 0:
		global count
		global KEYEVENTF_KEYUP
		global starttime
		global timeCount
		global status
		if count == 0:
			count = 1
			win32api.keybd_event(18,0,0,0)
			win32api.keybd_event(116,0,0,0)
			win32api.keybd_event(116,0,KEYEVENTF_KEYUP,0)
			win32api.keybd_event(18,0,KEYEVENTF_KEYUP,0)
			timeCount = 0
			status = "stop"
			print status
		starttime = time.time()
	return True


def getTime(threadName):
	global count
	global starttime
	global timeCount
	global preventTimeCauseKeyboart
	global status
	while True:
		if timeCount == 0:
			endtime = time.time()
			if (endtime - starttime > 10):
				count = 0
				timeCount = 1
				status = "running"
				print status
				preventTimeCauseKeyboart = 1
				win32api.keybd_event(18,0,0,0)
				win32api.keybd_event(116,0,0,0)
				win32api.keybd_event(116,0,KEYEVENTF_KEYUP,0)
				win32api.keybd_event(18,0,KEYEVENTF_KEYUP,0)
				time.sleep(4)
				preventTimeCauseKeyboart = 0
		
def main():
	global starttime
	starttime = time.time()
	hm = pyHook.HookManager()
	hm.KeyDown = onKeyboardEvent
	hm.HookKeyboard()
	hm.MouseAll = onMouseEvent
	hm.HookMouse()
	thread.start_new_thread(getTime,  ("Thread-1",))
	pythoncom.PumpMessages()
 
if __name__ == "__main__":
    main()