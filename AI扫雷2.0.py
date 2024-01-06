import numpy as np
from PIL import ImageGrab
import win32gui as gui
from pymouse import PyMouse


# 电脑缩放比例  系统 --> 屏幕  --> 缩放
# win10 默认100%
# win11 默认125%
proportion = 1.25
mine_size = int(16 * proportion)


# def initiate():
#     os.system('扫雷.exe')
# threading.Thread(target=initiate).start()

class AI_winmine:
    def __init__(self):
        handle = gui.FindWindow(None, "扫雷")
        gui.SetForegroundWindow(handle)
        x0, y0, x1, y1 = gui.GetWindowRect(handle)
        self.X_old = (x0 + 15, y0 + 102)
        self.X = int((x0 + 15) * proportion), int((y0 + 102) * proportion), int((x1 - 11) * proportion), int(
            (y1 - 10) * proportion)
        self.ifClick = True
        self.board = np.full(((self.X[3] - self.X[1]) // mine_size, (self.X[2] - self.X[0]) // mine_size), -1)
        self.map = np.array(ImageGrab.grab(self.X))
        self.list = []

    # 获取格子（已经获取的会保存到 board数组，不会二次截图获取）
    def getNum(self, x, y):
        # -1 : 未被点击的格子，0 : 已经点击的格子 ，
        num = self.board[x][y]
        if num != -1:
            return num
        num = 0
        img = np.array(self.map[x * mine_size:x * mine_size + mine_size, y * mine_size:y * mine_size + mine_size])
        for i in img:
            if (i == np.array([255, 255, 255])).all(1).any():
                if (i == np.array([0, 0, 0])).all(1).any():
                    num = -9
                    self.board[x][y] = num
                    return num
                else:
                    num = -1
            elif (i == np.array([0, 0, 0])).all(1).any():
                print("失败！！！")
                exit(0)
            elif (i == np.array([0, 0, 255])).all(1).any():
                num = 1
            elif (i == np.array([0, 128, 0])).all(1).any():
                num = 2
            elif (i == np.array([255, 0, 0])).all(1).any():
                num = 3
            elif (i == np.array([0, 0, 128])).all(1).any():
                num = 4
            elif (i == np.array([128, 0, 0])).all(1).any():
                num = 5
            elif (i == np.array([0, 128, 128])).all(1).any():
                num = 6
        self.board[x][y] = num
        return num

    # 全格子遍历
    def serch(self):
        self.map = np.array(ImageGrab.grab(self.X))
        for x in range(0, len(self.board)):
            for y in range(0, len(self.board[0])):
                self.getNum(x, y)

    # 找雷，并扫描
    def flushArray(self):
        self.serch()
        self.list = []
        for x in range(0, len(self.board)):
            for y in range(0, len(self.board[0])):
                self.serchNum(x, y)
        self.flush()

    def flush(self):
        list_ = self.list
        for i in range(len(list_)):
            for j in range(i + 1, len(list_)):
                def sameList(a, b):
                    list0 = a if len(a[0]) < len(b[0]) else b
                    list1 = a if len(a[0]) >= len(b[0]) else b
                    for a in list0[0]:
                        if a not in list1[0]:
                            return
                    for a in list0[0]:
                        list1[0].remove(a)
                    list1[1] -= list0[1]
                    if list1[1] == len(list1[0]):
                        for X, Y in list1[0]:
                            self.click(X, Y, 2)
                    if list1[1] == 0:
                        for X, Y in list1[0]:
                            self.click(X, Y)
                sameList(list_[i], list_[j])
        while [[], 0] in list_:
            list_.remove([[], 0])

    # 打印 数组
    def look(self):
        for i in self.board:
            print(i)
        print("\n")

    # 点击
    def click(self, x, y, button=1):
        self.ifClick = True
        if self.getNum(x, y) == -1:
            # time.sleep(0.05)
            m = PyMouse()
            if button == 2:
                self.board[x][y] = -9
            m.click(self.X_old[0] + y * 16 + 8, self.X_old[1] + x * 16 + 8, button=button)

    # 搜索数字
    def serchNum(self, x, y):
        num = self.getNum(x, y)
        if num != 0 and num != -1 and num != -9:
            direction = [[x - 1, y - 1], [x, y - 1], [x + 1, y - 1], [x + 1, y], [x + 1, y + 1], [x, y + 1],
                         [x - 1, y + 1], [x - 1, y]]
            list_ = []
            for X, Y in direction:
                if 0 <= X < len(self.board) and 0 <= Y < len(self.board[0]):
                    if self.getNum(X, Y) == -1:
                        list_.append((X, Y))
                    elif self.getNum(X, Y) == -9:
                        num -= 1
            if num == len(list_):
                for X, Y in list_:
                    self.click(X, Y, 2)
            elif num == 0:
                for X, Y in list_:
                    self.click(X, Y)
            elif num > 0:
                list_ = [list_, num]
                if list_ not in self.list:
                    self.list.append(list_)


while True:
    w = AI_winmine()
    w.flushArray()
