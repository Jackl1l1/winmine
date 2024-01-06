# -*- coding=UTF-8 -*-
# @Time      :2024-01-05  20:58
# @Author   :Jack
# @File         :AI扫雷3.0.py
# @Software:PyCharm

import 扫雷_工具 as WinmineUtil

class AI_winmine(WinmineUtil.WinmineUtil):
    def __init__(self):
        super().__init__()
        self.__list = []
        self.__board = None
        self.winmine()

    def winmine(self):
        self.__board = self.getBoard()
        self.__list = []
        for x in range(len(self.__board)):
            for y in range(len(self.__board[0])):
                self.serchNum(x, y)
        self.flush()
        # print(self.getMineNumber())

    # 搜索数字
    def serchNum(self, x, y):
        num = self.__board[x][y]
        if num != 0 and num != -1:
            list_ = []
            direction = [[x - 1, y - 1], [x, y - 1], [x + 1, y - 1], [x + 1, y], [x + 1, y + 1], [x, y + 1],
                         [x - 1, y + 1], [x - 1, y]]
            for X, Y in direction:
                if 0 <= X < len(self.__board) and 0 <= Y < len(self.__board[0]):
                    if self.__board[X][Y] == -1:
                        list_.append((X, Y))
                    elif self.__board[X][Y] == -9:
                        # self.clean(X, Y)
                        num -= 1
            if num == len(list_):
                for X, Y in list_:
                    self.plantFlag(X, Y)
            elif num == 0:
                for X, Y in list_:
                    self.click(X, Y)
            elif num > 0:
                list_ = [list_, num]
                if list_ not in self.__list:
                    self.__list.append(list_)

    def flush(self):
        # print(self.__list)
        list_ = self.__list
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
                            self.plantFlag(X, Y)
                    if list1[1] == 0:
                        for X, Y in list1[0]:
                            self.click(X, Y)
                sameList(list_[i], list_[j])
        while [[], 0] in list_:
            list_.remove([[], 0])

    # def clean(self, x, y):
    #     direction = [[x - 1, y - 1], [x, y - 1], [x + 1, y - 1], [x + 1, y], [x + 1, y + 1], [x, y + 1],
    #                  [x - 1, y + 1], [x - 1, y]]
    #     for X, Y in direction:
    #         if 0 <= X < len(self.__board) and 0 <= Y < len(self.__board[0]):
    #             if self.__board[X][Y] == -1:
    #                 return
    #     self.__board[x][y] = 0
    #     for X, Y in direction:
    #         if 0 <= X < len(self.__board) and 0 <= Y < len(self.__board[0]) and self.__board[X][Y] != 0 and \
    #                 self.__board[X][Y] != -9:
    #             self.__board[X][Y] -= 1

w = AI_winmine()

while 1:
    w.winmine()
    # if w.getMineNumber()<=0:
    #     w.again()

