# -*- coding=UTF-8 -*-
# @Time   :2022/12/8 16:21
# @Author :Jack
# @File   :a.py
# @Software:PyCharm

import time
import numpy as np
from PIL import ImageGrab
import win32gui as gui
from pymouse import *


class ai_winmine:
    def __init__(self):
        handle = gui.FindWindow(None, "扫雷")
        gui.SetForegroundWindow(handle)
        x0, y0, x1, y1 = gui.GetWindowRect(handle)
        x0, y0 = x0 + 15, y0 + 101
        x1, y1 = x1 - 10, y1 - 10
        m, n = (x1 - x0) // 16, (y1 - y0) // 16
        self.mine = 99
        if (m == 9 and n == 9):
            self.mine = 10
        if (m == 16 and n == 16):
            self.mine = 40

        self.x0 = x0
        self.y0 = y0
        self.m = m
        self.n = n
        self.array = [1]
        self.arrayRemove = []
        self.arrayRemove0 = []
        self.boolean = True

        self.board = np.full((n,m),-1)
        self.booleanBoard = np.full((n,m),False)

    def look(self):
        for i in self.board:
            print(i)

    def getNum(self, x, y):
        num = self.board[y][x]
        if num != -1:
            return num
        num = 0
        x0, y0 = (self.x0 // 0.8) + x * 20, (self.y0 // 0.8) + y * 20
        img = np.array(ImageGrab.grab((x0, y0, x0 + 20, y0 + 20)))
        for i in img:
            if (i == np.array([255, 255, 255])).all(1).any():
                if (i == np.array([0, 0, 0])).all(1).any():
                    num = -9
                    self.board[y][x] = num
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
        self.board[y][x] = num
        return num

    def click(self, x, y, button=1):
        if self.booleanBoard[y][x] ==False:
            self.booleanBoard[y][x] = True
            self.boolean = False
            if button == 2:
                if self.getNum(x, y) == -9:
                    return self.getNum(x, y)
                self.mine -= 1
                self.arrayRemove0.append([x, y])
            m = PyMouse()
            m.click(self.x0 + x * 16 + 8, self.y0 + y * 16 + 8, button=button)
            return self.getNum(x, y)

    def serch(self):
        arr = self.board
        for x in range(0, len(arr[0])):
            for y in range(0, len(arr)):
                arr[y][x] = self.getNum(x, y)


    def count(self, k):
        num = 0
        for i in self.board:
            for j in i:
                if j == k:
                    num += 1
        return num

    def get(self, k):
        for i in range(0, len(self.board) - 1):
            for j in range(0, len(self.board[0]) - 1):
                if self.board[j][i] == k:
                    return [j, i]

    def choice(self):
        min_ = [1,[0,0]]
        for i in self.array:
            if len(i[0])!=0 and min_[0] > i[1] / len(i[0]):
                min_ = [i[1] / len(i[0]), i[0][0]]
        self.click(min_[1][0], min_[1][1])
        time.sleep(0.02)
        self.getNum(min_[1][0], min_[1][1])


    def flushArray(self):
        arr = self.board
        self.array = []
        for y in range(0, len(arr)):
            for x in range(0, len(arr[0])):
                num = arr[y][x]
                if num != 0 and num != -1 and num != -9:
                    self.serchNum(x, y)

    def serchNum(self, x, y):
        num = self.board[y][x]
        list = []
        direction = [[x - 1, y - 1], [x, y - 1], [x + 1, y - 1], [x + 1, y], [x + 1, y + 1], [x, y + 1], [x - 1, y + 1], [x - 1, y]]
        for X, Y in direction:
            if X >= 0 and Y >= 0 and X < self.m and Y < self.n:
                serch_num = self.board[Y][X]
                if serch_num == -9:
                    num -= 1
                if serch_num == -1:
                    list.append([X, Y])
        if len(list) == num:
            for i in list:
                self.click(i[0], i[1], 2)
        if num == 0:
            for i in list:
                self.click(i[0], i[1], 1)
        else:
            self.array.append([list, num])

    def flush(self):
        array = self.array
        for i in range(0, len(array)):
            for j in range(i + 1, len(array)):
                def in_(arr1, arr2):
                    if len(arr1[0]) > len(arr2[0]):
                        loop = arr1
                        arr1 = arr2
                        arr2 = loop
                    num = 0
                    for i in arr1[0]:
                        for j in arr2[0]:
                            if i == j:
                                num += 1
                    if len(arr1[0]) == num:
                        for r in arr1[0]:
                            arr2[0].remove(r)
                        arr2[1] -= arr1[1]
                    if arr2[1] == 0:
                        for c in arr2[0]:
                            self.click(c[0], c[1])
                    if len(arr2[0]) == arr2[1]:
                        for c in arr2[0]:
                            self.click(c[0], c[1], 2)
                in_(array[i], array[j])

    def clean(self):
        arr = self.board
        for x in range(0, len(arr[0])):
            for y in range(0, len(arr)):
                if arr[y][x] == -1:
                    self.click(x,y)




w = ai_winmine()
x, y = 0, 0


def winmine(x, y):
    w.serch()
    w.mine -= w.count(-9)
    while (w.mine):
        w.boolean = True
        w.flushArray()
        arr = w.array
        if w.boolean:
            w.boolean = False
            w.serch()
            w.look()
            w.flush()
            if arr ==w.array:
                w.choice()
            if w.array == []:
                break
    print("成功！！！")
    w.clean()

winmine(x, y)
