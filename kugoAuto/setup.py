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
	# 返回 True 以便将事件传给其它处理程序     
	# 注意，这儿如果返回 False ，则鼠标事件将被全部拦截     
	# 也就是说你的鼠标看起来会僵在那儿，似乎失去响应了
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
	# 创建一个“钩子”管理对象
	hm = pyHook.HookManager()
	# 监听所有键盘事件
	hm.KeyDown = onKeyboardEvent
	# 设置键盘“钩子”
	hm.HookKeyboard()
	# 监听所有鼠标事件
	hm.MouseAll = onMouseEvent
	# 设置鼠标“钩子”
	hm.HookMouse()
	# 创建一个线程用于判断starttime和endtime
	thread.start_new_thread(getTime,  ("Thread-1",))
	# 进入循环，如不手动关闭，程序将一直处于监听状态 
	pythoncom.PumpMessages()
 
if __name__ == "__main__":
    main()