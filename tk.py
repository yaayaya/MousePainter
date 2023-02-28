# mouse monitoring
from pynput.mouse import Listener
import time
import os
import tkinter as tk
from tkinter import *
import keyboard
from datetime import datetime
import time
import threading
import pyautogui




current_time = datetime.now().strftime('%H:%M %S')

nowFileNo = 0

isMonitor = False
isExit = False
# 計數器
count = 0

# 創建主視窗
root = tk.Tk()
root.geometry("600x200")

# time-consuming 函式
def time_consuming():
    global count
    # 監聽器on
    listener.start()
    while not isExit:
        if isMonitor:
            count += 1
            pos = pyautogui.position()
            writeData(pos.x , pos.y)
            print(pos.x, pos.y)
            time.sleep(0.05)
            root.title(f"已監聽 {int(count/20)}秒")
        else:
            time.sleep(0.05)

# 創建子執行緒
t = threading.Thread(target=time_consuming)

# 寫入資料整理
def writeData(x , y , is_click = False):
    global saveFolderName
    saveFolderName = saveFolderNameInput.get()

    if not os.path.exists(saveFolderName):
        os.makedirs(saveFolderName)


    global fileNo
    now = datetime.now().strftime("%H:%M:%S")
    data = f"{now},{x},{y},{int(is_click)}\n"
    if (int(count/20) > int(splitTime.get())):
        fileNo += 1
    # Save data to file every 0.1 seconds`
    fileNo = checkFileName()
    completeName = os.path.join(f"./{saveFolderName}/", f"{fileNo}.txt")         

    with open(completeName, "a") as f:
        f.write(data)

# 產出檔案名稱
def checkFileName():
    global nowFileNo
    global count
    global splitTime
    if (nowFileNo == int(count/20/int(splitTime.get()))):
        pass
    else:
        nowFileNo = int(count/20/int(splitTime.get()))
    return nowFileNo
    

# Listener Click
def click(x, y, button , is_press):
    is_click = False
    if is_press:
        is_click = True
        print(x,y,"click")
        writeData(x,y , is_click)
    else:
        is_click = False
    # print(f"({x}, {y}) {'press' if is_press else 'release'}")

listener = Listener(
    on_click=click,
)

# 定義 startMonitor 和 stopMonitor 方法
def startMonitor():
    global isMonitor
    isMonitor = True
    print(t.is_alive())
    if not t.is_alive():
        t.start()


def stopMonitor():
    global isMonitor
    global listener
    listener.stop()
    isMonitor = False
    global count
    count = 0
    root.title(f"停止監聽")

# 右上叉叉
def on_closing():
    root.protocol("WM_DELETE_WINDOW", on_closing)
    stopMonitor()
    global isExit
    isExit = True
    root.destroy()

# 創建按鍵佈局
button_frame = tk.Frame(root, width=480, height=80)
button_frame.pack(side=tk.BOTTOM)

# 創建按鍵並將其添加到按鍵佈局中
label = tk.Label(root, text="切換儲存檔案時間(秒)")
label.pack(side=tk.LEFT,padx=10, pady=10)

splitTime = tk.Entry(root , width=5)  
splitTime.pack(side=tk.LEFT,padx=10, pady=10 )
splitTime.insert(0, 600)

label = tk.Label(root, text="儲存的資料夾名稱")
label.pack(side=tk.LEFT,padx=10, pady=10)

saveFolderNameInput = tk.Entry(root)  
saveFolderNameInput.pack(side=tk.LEFT,padx=10, pady=10)
saveFolderNameInput.insert(0, "log")

button1 = tk.Button(button_frame, text="開始錄製", width=10, height=3, command=startMonitor)
button1.pack(side=tk.LEFT, padx=10, pady=10)

button2 = tk.Button(button_frame, text="停止錄製", width=10, height=3, command=stopMonitor)
button2.pack(side=tk.LEFT, padx=10, pady=10)

button5 = tk.Button(button_frame, text="Exit", width=10, height=3 , command=on_closing)
button5.pack(side=tk.LEFT, padx=10, pady=10)



root.protocol("WM_DELETE_WINDOW", on_closing)




# 啟動主迴圈
root.mainloop()



