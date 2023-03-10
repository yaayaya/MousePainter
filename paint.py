# mouse monitoring
from pynput.mouse import Listener
import tkinter as tk
from tkinter import *
from datetime import datetime
import os
import json



# 顏色列表
colorList = ["" , "", "", "" ,"","","",""]
posFix = None

fileCount = 0
                        

dataCount = 0
colorChangeTime = 2400
oralWidth = 12

current_time = datetime.now().strftime('%H:%M %S')
canvas = None
topLevel = None
fileNo = 0
toggleTopCanvas = 0
isExit = False
lastX = -1
lastY = -1

# 螢幕解析度
screenSizeX = None
screenSizeY = None

# 計數器
count = 0

# 創建主視窗
root = tk.Tk()
root.geometry("600x980")



# 定義展開畫布的方法
def toggleCanvas():
    global canvas
    global toggleTopCanvas
    global topLevel

    if (toggleTopCanvas == 0):
        top = tk.Toplevel(root, width = 1920, height = 1080)
        # top.title("Second window")
        top.bind("<Escape>", lambda e: toggleCanvas())
        cc = Canvas(top, width=1920, height=1080 ,background=backgroundColorInput.get(), highlightthickness=1, highlightbackground=backgroundColorInput.get())
        cc.pack(fill="both", expand=True)
        cc.bind("<MouseWheel>", do_zoom)
        cc.bind('<ButtonPress-1>', lambda event: canvas.scan_mark(event.x, event.y))
        cc.bind("<B1-Motion>", lambda event: canvas.scan_dragto(event.x, event.y, gain=1))

        top.bind("<F1>" , lambda event: toggleCanvas())
        top.bind("<F2>" , lambda event: showData())
        top.bind("<F3>" , lambda event: showData(17))
        top.bind("<F4>" , lambda event: showData(1))
        top.bind("<F5>" , lambda event: clearCanvas())
        top.bind("<F7>" , lambda event: toggle_fullscreen(cc))
        top.bind("<F8>" , lambda event: toggle_titlebar(cc))

        toggleTopCanvas = 1
        topLevel = top
        canvas = cc
    else :
        topLevel.destroy()
        toggleTopCanvas = 0
        root.title("Mouse Painter")

# 定義函式以讀取txt檔案
def read_txt_file(completeName):
    # 建立空的列表，用以儲存每行資料轉換後的Dict
    data = []
    # 開啟txt檔案
    with open(completeName, 'r') as f:
        # 逐行讀取txt檔案內容
        for line in f:
            # 將每行資料以逗號為分隔符號分割成一個列表
            line_data = line.strip().split(',')
            # 將分割後的列表轉換為Dict格式，並指定對應的key值
            dict_data = {
                'Time': line_data[0],
                'x': line_data[1],
                'y': line_data[2],
                'isClick': line_data[3]
            }
            # 將轉換後的Dict加入data列表中
            data.append(dict_data)
    # 回傳儲存所有資料的列表
    return data

# 讀取log.txt 
def showData(delayTime = 50):
    global topLevel
    global canvas
    global fileNo
    global fileCount
    global loadFolderNameInput
    global dataCount
    colorIdx = 0

    canvasAlpha = canvasAlphaInput.get()

    datas = []
    specificFile = specificFileInput.get()

    # 總檔案數 迴圈抓取檔案存取
    for fileNo in range(0,fileCount):
        completeName = os.path.join(f"./{loadFolderNameInput.get()}/", f"{fileNo}.txt")
        data = read_txt_file(completeName)
        datas.append(data)

    if (canvas == None):
        topLevel.title("請先展開畫布")
        root.title("請先展開畫布")
        return None
    else :
        root.title("繪畫中")
    if (specificFile == ""):
        print("alll")
        for i ,data in enumerate(datas):
            # 畫畫
            for idx, x in enumerate(data):
                dataCount += 1
                if (dataCount >= colorChangeTime):
                    colorIdx +=1
                    dataCount = 0
                root.after(delayTime ,drawCanvas(colorIdx , idx , canvasAlpha, data))
                canvas.update()
                topLevel.title(data[idx]["Time"])
    else:
        data = datas[int(specificFile)]
        # 畫畫
        for idx, x in enumerate(data):
            root.after(delayTime ,drawCanvas(2 , idx ,"gray75", data))
            canvas.update()
            topLevel.title(data[idx]["Time"])

            
            
    topLevel.title(f"完成、共讀取{fileCount}個檔案")
    root.title(f"完成、共讀取{fileCount}個檔案")


def clearCanvas():
    global canvas
    canvas.delete("all")
    topLevel.title("畫布已清空")
    root.title("畫布已清空")

def drawCanvas(colorIdx , idx , stipple,data):
    global lastX
    global lastY
    global canvas
    global posFix

    if (lastX == -1):
        lastX = int(int(data[idx]["x"]) * posFix)
        lastY = int(int(data[idx]["y"]) * posFix)
    else:
        dataX_2 = int(int(data[idx]["x"]) * posFix)
        dataY_2 = int(int(data[idx]["y"]) * posFix)
        colorCode = colorList[colorIdx % 8]
        if (data[idx]["isClick"] == "1"):
            canvas.create_line(lastX, lastY, dataX_2, dataY_2, width=12 , fill=f"{colorCode}" , stipple = stipple)
            canvas.create_oval(dataX_2, dataY_2, dataX_2 + 5, dataY_2 + 5, width= int(oralWidth_Input.get()), fill=f"{colorCode}" ,outline=f"{colorCode}" , stipple = stipple)
        else:
            if (lastX == dataX_2 and lastY == dataY_2):
                return
            
            canvas.create_line(lastX, lastY, dataX_2, dataY_2, width=12 , fill=f"{colorCode}" ,  stipple = stipple )

        lastX = int(int(data[idx]["x"]) * posFix)
        lastY = int(int(data[idx]["y"]) * posFix)

# 儲存、讀取
def save_data():
    data = {}
    for i in range(1, 9):
        data[f"color_{i}"] = inputs[i-1].get()
    data["loadFolderNameInput"] = loadFolderNameInput.get()
    data["canvasAlphaInput"] = canvasAlphaInput.get()
    data["screenSizeX_Input"] = screenSizeX_Input.get()
    data["oralWidth_Input"] = oralWidth_Input.get()
    data["specificFileInput"] = specificFileInput.get()
    data["colorChangeTime_Input"] = colorChangeTime_Input.get()
    data["backgroundColorInput"] = backgroundColorInput.get()

    with open('config.json', 'w') as f:
        json.dump(data, f)
    print("Data saved.")
    load_data()

def load_data():
    global colorList
    global loadFolderNameInput
    global fileCount
    global colorChangeTime
    colorList = []

    try:
        with open('config.json', 'r') as f:
            data = json.load(f)
        for i in range(1, 9):
            inputs[i-1].delete(0, 'end')
            inputs[i-1].insert(0, data[f"color_{i}"])
            colorList.append(data[f"color_{i}"])
        
        backgroundColorInput.delete(0, 'end')
        backgroundColorInput.insert(0, data["backgroundColorInput"])

        loadFolderNameInput.delete(0, 'end')
        loadFolderNameInput.insert(0, data["loadFolderNameInput"])

        canvasAlphaInput.delete(0 , "end")
        canvasAlphaInput.insert(0, data["canvasAlphaInput"])

        screenSizeX_Input.delete(0 , "end")
        screenSizeX_Input.insert(0, data["screenSizeX_Input"])

        oralWidth_Input.delete(0 , "end")
        oralWidth_Input.insert(0, data["oralWidth_Input"])
        oralWidth = int(oralWidth_Input.get())

        specificFileInput.delete(0 , "end")
        specificFileInput.insert(0, data["specificFileInput"])

        colorChangeTime_Input.delete(0 , "end")
        colorChangeTime_Input.insert(0, data["colorChangeTime_Input"])
        colorChangeTime = int(colorChangeTime_Input.get()) * 20


        fileCount = 0
        for file in os.listdir(f'./{data["loadFolderNameInput"]}'):
            if file.endswith(".txt"):
                fileCount += 1 
        
        global posFix
        posFix = 1920/int(screenSizeX_Input.get())
        print("Data loaded.")
    except FileNotFoundError:
        print("Data file not found.")


# 右上叉叉
def on_closing():
    global isExit
    isExit = True
    root.destroy()


# 創建按鍵佈局
button_frame = tk.Frame(root, width=480, height=80)
button_frame.pack(side=tk.BOTTOM)

# 創建按鍵並將其添加到按鍵佈局中

button1 = tk.Button(button_frame, text="展開畫布", width=10, height=3, command=toggleCanvas)
button1.pack(side=tk.LEFT, padx=10, pady=10)

button2 = tk.Button(button_frame, text="繪畫", width=10, height=3 , command = lambda: showData(50))
button2.pack(side=tk.LEFT, padx=10, pady=10)

button3 = tk.Button(button_frame, text="繪畫3倍速", width=10, height=3 , command = lambda: showData(17))
button3.pack(side=tk.LEFT, padx=10, pady=10)

save_button = tk.Button(button_frame, text="儲存", width=10, height=3 ,command=save_data)
save_button.pack(side=tk.LEFT, padx=10, pady=10)

load_button = tk.Button(button_frame, text="讀取", width=10, height=3 ,command=load_data)
load_button.pack(side=tk.LEFT, padx=10, pady=10)


button5 = tk.Button(button_frame, text="Exit", width=10, height=3 , command=on_closing)
button5.pack(side=tk.LEFT, padx=10, pady=10)

root.bind("<F1>" , lambda event: toggleCanvas())

# 顏色

input_labels = ['Color 1', 'Color 2', 'Color 3', 'Color 4', 'Color 5', 'Color 6', 'Color 7', 'Color 8']
inputs = []

for i, label in enumerate(input_labels):
    tk.Label(root, text=label).pack( padx=5, pady=5)
    input_box = tk.Entry(root)
    input_box.pack( padx=5, pady=5)
    inputs.append(input_box)

# 背景顏色
label = tk.Label(root, text="畫布顏色")
label.pack(padx=5, pady=5)

backgroundColorInput = tk.Entry(root)  
backgroundColorInput.pack(padx=5, pady=5)
    
# 資料夾名稱
label = tk.Label(root, text="讀取的資料夾名稱")
label.pack(padx=5, pady=5)

loadFolderNameInput = tk.Entry(root)  
loadFolderNameInput.pack(padx=5, pady=5)



# 透明度
label = tk.Label(root, text="透明度")
label.pack(padx=5, pady=5)

canvasAlphaInput = tk.Entry(root)  
canvasAlphaInput.pack(padx=5, pady=5)

# 螢幕解析度
label = tk.Label(root, text="目標螢幕解析度 X")
label.pack(padx=5, pady=5)

screenSizeX_Input = tk.Entry(root)  
screenSizeX_Input.pack(padx=5, pady=5)

# 圓點大小
label = tk.Label(root, text="圓點大小")
label.pack(padx=5, pady=5)
oralWidth_Input = tk.Entry(root)  
oralWidth_Input.pack(padx=5, pady=5)

# 顏色交換時間(秒)
label = tk.Label(root, text="顏色交換時間(秒)")
label.pack(padx=5, pady=5)
colorChangeTime_Input = tk.Entry(root)  
colorChangeTime_Input.pack(padx=5, pady=5)

# 指定檔案讀取
label = tk.Label(root, text="指定檔案讀取")
label.pack(padx=5, pady=5)

specificFileInput = tk.Entry(root)  
specificFileInput.pack(padx=5, pady=5)

def do_zoom(event):
    global canvas
    x = canvas.canvasx(event.x)
    y = canvas.canvasy(event.y)
    factor = 1.001 ** event.delta
    canvas.scale(ALL, x, y, factor, factor)


# 快捷鍵
def toggle_fullscreen(self, event=None):
    self.master.attributes('-fullscreen', not self.master.attributes('-fullscreen'))

def toggle_titlebar(self, event=None):
    self.master.overrideredirect(not self.master.overrideredirect())


root.title("Mouse Painter")
root.protocol("WM_DELETE_WINDOW", on_closing)
load_data()



# 啟動主迴圈
root.mainloop()



