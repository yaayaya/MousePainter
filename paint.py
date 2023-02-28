# mouse monitoring
from pynput.mouse import Listener
import tkinter as tk
from tkinter import *
from datetime import datetime
import os
import json



# 顏色列表
colorList = ["#BABDBF" , "#3F7373", "#BF754B", "#A64826" ,"#732B1A"]
posFix = 0.7

fileCount = 0

for file in os.listdir("./log"):
    if file.endswith(".txt"):
        fileCount += 1
                        


current_time = datetime.now().strftime('%H:%M %S')
canvas = None
topLevel = None
fileNo = 0
toggleTopCanvas = 0
isExit = False
lastX = -1
lastY = -1
# 計數器
count = 0

# 創建主視窗
root = tk.Tk()
root.geometry("600x500")



# 定義展開畫布的方法
def toggleCanvas():
    global canvas
    global toggleTopCanvas
    global topLevel
    if (toggleTopCanvas == 0):
        top = tk.Toplevel(root, width = 1920, height = 1080)
        # top.title("Second window")
        top.bind("<Escape>", lambda e: top.destroy())
        cc = Canvas(top, width=1920, height=1080 ,background="white")
        cc.pack(fill="both", expand=True)
        cc.bind("<MouseWheel>", do_zoom)
        cc.bind('<ButtonPress-1>', lambda event: canvas.scan_mark(event.x, event.y))
        cc.bind("<B1-Motion>", lambda event: canvas.scan_dragto(event.x, event.y, gain=1))

        top.bind("<F1>" , lambda event: toggleCanvas())
        top.bind("<F2>" , lambda event: showData())
        top.bind("<F3>" , lambda event: showData(17))
        top.bind("<F4>" , lambda event: showData(0))
        top.bind("<F5>" , lambda event: clearCanvas())
        top.bind("<F7>" , lambda event: toggle_fullscreen(cc))
        top.bind("<F8>" , lambda event: toggle_titlebar(cc))

        toggleTopCanvas = 1
        topLevel = top
        canvas = cc
    else :
        topLevel.destroy()
        toggleTopCanvas = 0

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
    datas = []

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

    for colorIdx , data in enumerate(datas):
        # 畫畫
        for idx, x in enumerate(data):
            root.after(delayTime ,drawCanvas(colorIdx , idx , data))
            canvas.update()
            topLevel.title(data[idx]["Time"])
            
    topLevel.title(f"完成、共讀取{fileCount}個檔案")
    root.title(f"完成、共讀取{fileCount}個檔案")


def clearCanvas():
    global canvas
    canvas.delete("all")
    topLevel.title("畫布已清空")
    root.title("畫布已清空")

def drawCanvas(colorIdx , idx,data):
    global lastX
    global lastY
    global canvas
    global posFix
    if (lastX == -1):
        lastX = int(int(data[idx]["x"]) * posFix)
        lastY = int(int(data[idx]["y"]) * posFix)
    else:
        print(idx)
        dataX_2 = int(int(data[idx]["x"]) * posFix)
        dataY_2 = int(int(data[idx]["y"]) * posFix)
        colorCode = colorList[colorIdx % 5]
        if (data[idx]["isClick"] == "1"):
            canvas.create_line(lastX, lastY, dataX_2, dataY_2, width=3 , fill=f"{colorCode}")
            canvas.create_oval(dataX_2, dataY_2, dataX_2 + 1, dataY_2 + 1, width=8, fill=f"{colorCode}" ,outline=f"{colorCode}")
        else:
            canvas.create_line(lastX, lastY, dataX_2, dataY_2, width=3 , fill=f"{colorCode}")


        lastX = int(int(data[idx]["x"]) * posFix)
        lastY = int(int(data[idx]["y"]) * posFix)

# 儲存、讀取
def save_data():
    data = {}
    for i in range(1, 6):
        data[f"color_{i}"] = inputs[i-1].get()
    data["loadFolderNameInput"] = loadFolderNameInput.get()
    with open('config.json', 'w') as f:
        json.dump(data, f)
    print("Data saved.")

def load_data():
    global colorList
    global loadFolderNameInput
    colorList = []
    try:
        with open('config.json', 'r') as f:
            data = json.load(f)
        for i in range(1, 6):
            inputs[i-1].delete(0, 'end')
            inputs[i-1].insert(0, data[f"color_{i}"])
            colorList.append(data[f"color_{i}"])

        loadFolderNameInput.delete(0, 'end')
        loadFolderNameInput.insert(0, data["loadFolderNameInput"])

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

input_labels = ['Color 1:', 'Color 2:', 'Color 3:', 'Color 4:', 'Color 5:']
inputs = []

for i, label in enumerate(input_labels):
    tk.Label(root, text=label).pack( padx=5, pady=5)
    input_box = tk.Entry(root)
    input_box.pack( padx=5, pady=5)
    inputs.append(input_box)
# 資料夾名稱
label = tk.Label(root, text="讀取的資料夾名稱")
label.pack(padx=5, pady=5)

loadFolderNameInput = tk.Entry(root)  
loadFolderNameInput.pack(padx=5, pady=5)


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



root.protocol("WM_DELETE_WINDOW", on_closing)
load_data()



# 啟動主迴圈
root.mainloop()



