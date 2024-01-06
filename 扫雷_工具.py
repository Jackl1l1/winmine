# -*- coding=UTF-8 -*-
# @Time      :2024-01-05  20:58
# @Author   :Jack
# @File         :扫雷_工具.py
# @Software:PyCharm

# 科学计算
# pip install numpy
# 截图
# pip install pillow
# 寻找视口
# pip install pywin32
# 点击
# pip install pymouse

import numpy as np
from PIL import ImageGrab
import win32gui as gui
from pymouse import PyMouse

# 电脑缩放比例  系统 --> 屏幕  --> 缩放
# win10 默认100%
# win11 默认125%
proportion = 1.25
mine_size = int(16 * proportion)


class WinmineUtil:
    __mouse = PyMouse()

    def __init__(self):
        handle = gui.FindWindow(None, "扫雷")
        gui.SetForegroundWindow(handle)
        x0, y0, x1, y1 = gui.GetWindowRect(handle)
        self.__x = x0, y0, x1, y1
        self.__X_old = (x0 + 15, y0 + 102)
        self.__X = int((x0 + 15) * proportion), int((y0 + 102) * proportion), int((x1 - 11) * proportion), int(
            (y1 - 10) * proportion)
        self.__img = np.array(ImageGrab.grab(self.__X))
        self.__board = np.full(((self.__X[3] - self.__X[1]) // mine_size, (self.__X[2] - self.__X[0]) // mine_size), -1)
        self.__mine = 10 if len(self.__board[0]) == 9 else 40 if len(self.__board[0]) == 16 else 99

    # 获取格子的数字（已经获取的会保存到 board数组，不会二次截图获取）
    def getNum(self, x, y):
        # -1 : 未被点击的格子，0 : 已经点击的格子
        num = self.__board[x][y]
        if num != -1:
            return num
        num = 0
        img = np.array(self.__img[x * mine_size:x * mine_size + mine_size, y * mine_size:y * mine_size + mine_size])
        for i in img:
            if (i == np.array([255, 255, 255])).all(1).any():
                if (i == np.array([0, 0, 0])).all(1).any():
                    num = -9
                    self.__board[x][y] = num
                    return num
                else:
                    num = -1
            elif (i == np.array([0, 0, 0])).all(1).any():
                print("呀，踩到雷啦")
                exit(0)
                self.__mine = -1
                return
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
        self.__board[x][y] = num
        return num

    # 点击
    def click(self, x, y, button=1):
        if self.getNum(x, y) == -1:
            self.__mouse.click(self.__X_old[0] + y * 16 + 8, self.__X_old[1] + x * 16 + 8, button=button)

    # 插旗
    def plantFlag(self, x, y):
        if self.__board[x][y] == -9:
            return
        self.click(x, y, 2)
        self.__board[x][y] = -9
        self.__mine -= 1

    # 查看雷数
    map = {
        0b0000001: -1,
        0b1111110: 0,
        0b0110000: 1,
        0b1101101: 2,
        0b1111001: 3,
        0b0110011: 4,
        0b1011011: 5,
        0b1011111: 6,
        0b1110000: 7,
        0b1111111: 8,
        0b1111011: 9,
    }
    def getMineNumber(self):
        x0, y0, x1, y1 = self.__x
        img = np.array(ImageGrab.grab((int((x0 + 21) * proportion),
                                       int((y0 + 63) * proportion),
                                       int((x0 + 58) * proportion),
                                       int((y0 + 85) * proportion))))
        d = np.array([[7, 2], [12, 6], [12, 19], [7, 24], [2, 19], [2, 6], [7, 14]])
        num = [0, 0, 0]
        for i in range(3):
            if i != 0:
                d[:, 0] += 16
            for x, y in d:
                num[i] <<= 1
                # print(x,y)
                # print(img[y][x])
                if img[y][x][0]>128:
                    num[i] |= 1

        # print(bin(num[0]))
        # print(bin(num[1]))
        # print(bin(num[2]))
        # print(self.map.get(num[0]))
        # print(self.map.get(num[1]))
        # print(self.map.get(num[2]))

        if self.map.get(num[0]) < 0:
            return -(self.map.get(num[1]) * 10 + self.map.get(num[2]))
        return self.map.get(num[0]) * 100 + self.map.get(num[1]) * 10 + self.map.get(num[2])

    # 全格子遍历
    def __serch(self):
        self.__img = np.array(ImageGrab.grab(self.__X))
        for x in range(0, len(self.__board)):
            for y in range(0, len(self.__board[0])):
                self.getNum(x, y)

    # 打印 数组
    def look(self):
        for i in self.__board:
            print(i)
        print("\n")

    # 获取数组
    def getBoard(self):
        self.__serch()
        return self.__board

    # 重来
    def again(self):
        self.__board = np.full(((self.__X[3] - self.__X[1]) // mine_size, (self.__X[2] - self.__X[0]) // mine_size), -1)
        self.__mine = 10 if len(self.__board[0]) == 9 else 40 if len(self.__board[0]) == 16 else 99
        self.__mouse.click(self.__X_old[0] + 130, self.__X_old[1] - 30)

# u = WinmineUtil()
# u.getMineNumber()
