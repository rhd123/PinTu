#!/usr/bin/env python
# -*- coding: utf-8 -*-
import operator
from io import BytesIO
from PIL import ImageFile
from PIL import Image
import imagehash
import os
import cv2

import base64
import requests
from time import sleep
import pygame
import random
import sys
import numpy as np
from pygame.locals import *

window_width = 600
window_height = 600
background = (225,225,225)
blue = (0,0,255)
green = (0, 255, 0)
black = (0, 0, 0)
white = (255,255,255)
gray = (128,128,128)
rows = 3
FPS = 30
blocks = rows * rows


def init_picture():
    board = []
    for i in range(blocks):
        board.append(i)
    blackCell = 7
    board[blackCell] = -1
    return board, blackCell

# 若空白图像块不在最左边，则将空白块左边的块移动到空白块位置
def moveRight(board, blackCell):
    if blackCell % 3 == 0:
        return blackCell
    board[blackCell - 1], board[blackCell] = board[blackCell], board[blackCell - 1]

    return blackCell - 1
# 若空白图像块不在最右边，则将空白块右边的块移动到空白块位置
def moveLeft(board, blackCell):
    if blackCell % 3 == 3 - 1:
        return blackCell
    board[blackCell + 1], board[blackCell] = board[blackCell], board[blackCell + 1]
    return blackCell + 1
# 若空白图像块不在最上边，则将空白块上边的块移动到空白块位置
def moveDown(board, blackCell):
    if blackCell < 3:
        return blackCell
    board[blackCell - 3], board[blackCell] = board[blackCell], board[blackCell - 3]
    return blackCell - 3
# 若空白图像块不在最下边，则将空白块下边的块移动到空白块位置
def moveUp(board, blackCell):
    if blackCell >= blocks - 3:
        return blackCell
    board[blackCell + 3], board[blackCell] = board[blackCell], board[blackCell + 3]
    return blackCell + 3
# 是否完成
def isFinished(board, blackCell):
    for i in range(blocks - 1):
        if board[i] != i :
            return False
    return True


# 从Postman获取题目，将图片保存至文件夹
# pic_url = requests.get('http://47.102.118.1:8089/api/problem?stuid=031802423')
# image_code = base64.b64decode(pic_url.json()['img'])
# file_like = BytesIO(image_code)
# image = Image.open(file_like)
# image.save('image.JPG')
# 初始化
pygame.init()
clock = pygame.time.Clock()
# 设置窗口
windowSurface = pygame.display.set_mode([window_width+200, window_height])
pygame.display.set_caption('拼图')
# 每块拼图大小
width = int(window_height / 3)
height = int(window_width / 3)

start_ck = pygame.Surface(windowSurface.get_size())    #   充当开始界面的画布
start_ck2 = pygame.Surface(windowSurface.get_size())  #  充当第一关的画布界面暂时占位（可以理解为游戏开始了）
start_ck3 = pygame.Surface(windowSurface.get_size())  # ai界面
start_ck = start_ck.convert()
start_ck2 = start_ck2.convert()
start_ck3 = start_ck3.convert()
start_ck.fill((255,255,255))  # 白色画布1（开始界面用的）
start_ck2.fill((0,255,0))
start_ck3.fill((255,255,255))
# 加载各个素材图片 并且赋予变量名
i1 = pygame.image.load("D:/python_work/pycharmWork/huarong/botton/s1.png")
i1.convert()
i11 = pygame.image.load("D:/python_work/pycharmWork/huarong/botton/s2.png")
i11.convert()

i2 = pygame.image.load("D:/python_work/pycharmWork/huarong/botton/e1.png")
i2.convert()
i21 = pygame.image.load("D:/python_work/pycharmWork/huarong/botton/e2.png")
i21.convert()

bg = pygame.image.load('D:/python_work/pycharmWork/huarong/botton/start3.jpg')
bg.convert()

#  以下为选择开始界面鼠标检测结构。

n1 = True
while n1:
    clock.tick(30)
    buttons = pygame.mouse.get_pressed()
    x1, y1 = pygame.mouse.get_pos()
    start_ck.blit(bg,(0,0))
    if x1 >= 227 and x1 <= 555 and y1 >= 261 and y1 <=327:
        start_ck.blit(i11, (200, 240))
        if buttons[0]:
            n1 = False

    elif x1 >= 227 and x1 <= 555 and y1 >= 381 and y1 <=447:
        start_ck.blit(i21, (200, 360))
        if buttons[0]:
            pygame.quit()
            exit()

    else:
        start_ck.blit(i1, (200, 240))
        start_ck.blit(i2, (200, 360))

    windowSurface.blit(start_ck,(0,0))
    pygame.display.update()

    # 监听事件
    for event in pygame.event.get():
        # 判断事件类型是否是退出事件
        if event.type == pygame.QUIT:
            print("游戏退出...")
            # quit 卸载所有的模块
            pygame.quit()
            # exit() 直接终止当前正在执行的程序
            exit()

windowSurface.blit(start_ck2, (0, 0))
pygame.display.update()

clock = pygame.time.Clock()
# 加载图片
gameImage1 = pygame.image.load('image.JPG')
blank = pygame.image.load('blank.jpg')
# 缩小图片作为参考图片
gameImage = pygame.transform.scale(gameImage1,(600,600))
gameRect = gameImage.get_rect()
# 用于设置并绘制文字
def showText(fontObj, text, x, y) :
    textSurfaceObj = fontObj.render(text, True, black, background)  # 配置要显示的文字
    textRectObj = textSurfaceObj.get_rect()  # 获得要显示的对象的rect
    textRectObj.center = (x, y)  # 设置显示对象的坐标
    windowSurface.blit(textSurfaceObj, textRectObj)  #绘制字体
fontminObj = pygame.font.SysFont("",24)
steps = 0
#切图
def cut_image(image) :
    item_width = 300
    box_list = []
    for i in range(0, 3) :  # 两重循环，生成9张图片基于原图的位置
        for j in range(0, 3) :
            box = (j*item_width, i*item_width, (j+1)*item_width, (i+1)*item_width)
            box_list.append(box)
    image_list = [image.crop(box) for box in box_list]
    return image_list
# 保存拼图
def save_images(image_list) :
    index = 0
    for image in image_list :
        image.save(str(index) + '.jpg')
        index += 1
gameImage2 = Image.open('image.JPG')
image_list = cut_image(gameImage2)
save_images(image_list)
#对比是否为相同图片，如果相同，则返回True
def compare_image_with_hash(image_file_name_1, image_file_name_2, max_dif=0) :
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    hash_1 = None
    hash_2 = None
    with open(image_file_name_1, 'rb') as fp :
        hash_1 = imagehash.average_hash(Image.open(fp))
    with open(image_file_name_2, 'rb') as fp :
        hash_2 = imagehash.average_hash(Image.open(fp))
    dif = hash_1 - hash_2
    if dif < 0 :
        dif = -dif
    if dif <= max_dif :
        return True
    else :
        return False
#如果是空白块，则换下一块
if compare_image_with_hash("0.jpg","blank.jpg",0) :
    if compare_image_with_hash("1.jpg","black.jpg",0) :
        tu = Image.open("2.jpg")
    else :
        tu = Image.open("1.jpg")
elif compare_image_with_hash("0.jpg","black.jpg",0):
    if compare_image_with_hash("1.jpg", "blank.jpg", 0) :
        tu = Image.open("2.jpg")
    else:
        tu = Image.open("1.jpg")
else:
    tu = Image.open("0.jpg")
tu.save('tu.jpg')
#判断文件夹中的图片切块是否与选出的拼图块相同,保存成 cankao1
for pic_name in os.listdir("D://python_work//pycharmWork//huarong//zifu"):
    img = Image.open("D://python_work//pycharmWork//huarong//zifu" + "/" +pic_name)
    image_list1 = cut_image(img)
    for image in image_list1 :
            image.save('cankao' + '.jpg')
            if compare_image_with_hash('cankao.jpg', 'tu.jpg', 0):
                img.save('cankao1.jpg')
                break

#参考图片
cankao = pygame.image.load('cankao1.jpg')
pic = pygame.transform.scale(cankao, (180, 180))
windowSurface.blit(pic, [620, 420])

finish = False
def aitest(board):
    O = int(3)
    A = list(board)
    B = list([0, 1, 2, 3, 4, 5, 6, 7, 8])
    z = 0
    M = np.zeros((O, O))
    N = np.zeros((O, O))
    for i in range(O):
        for j in range(O):
            M[i][j] = A[z]
            N[i][j] = B[z]
            z = z + 1
    openlist = []  # open表

    class State:
        def __init__(self, m):
            self.node = m  # 节点代表的状态
            self.f = 0  # f(n)=g(n)+h(n)
            self.g = 0  # g(n)
            self.h = 0  # h(n)
            self.father = None  # 节点的父亲节点

    init = State(M)  # 初始状态
    goal = State(N)  # 目标状态

    # 启发函数
    def h(s):
        a = 0
        for i in range(len(s.node)):
            for j in range(len(s.node[i])):
                if s.node[i][j] != goal.node[i][j]:
                    a = a + 1
        return a

    # 对节点列表按照估价函数的值的规则排序
    def list_sort(l):
        cmp = operator.attrgetter('f')
        l.sort(key=cmp)

    # A*算法
    def A_star(s):
        global openlist  # 全局变量可以让open表进行时时更新
        openlist = [s]
        while (openlist):  # 当open表不为空
            get = openlist[0]  # 取出open表的首节点
            if (get.node == goal.node).all():  # 判断是否与目标节点一致
                return get
            openlist.remove(get)  # 将get移出open表
            # 判断此时状态的空格位置
            for a in range(len(get.node)):
                for b in range(len(get.node[a])):
                    if get.node[a][b] == 0:
                        break
                if get.node[a][b] == 0:
                    break
            # 开始移动
            for i in range(len(get.node)):
                for j in range(len(get.node[i])):
                    c = get.node.copy()
                    if (i + j - a - b) ** 2 == 1:
                        c[a][b] = c[i][j]
                        c[i][j] = 0
                        new = State(c)
                        new.father = get  # 此时取出的get节点成为新节点的父亲节点
                        new.g = get.g + 1  # 新节点与父亲节点的距离
                        new.h = h(new)  # 新节点的启发函数值
                        new.f = new.g + new.h  # 新节点的估价函数值
                        openlist.append(new)  # 加入open表中
            list_sort(openlist)  # 排序


    # 递归打印路径
    def printpath(f):
        if f is None:
            return
        # 注意print()语句放在递归调用前和递归调用后的区别。放在后实现了倒叙输出
        printpath(f.father)
        print(f.node)

    final = A_star(init)
    if final:
        print("有解，解为：")
        printpath(final)
    else:
        print("无解")

gameBoard, blackCell = init_picture()
testboard = []
testboard = gameBoard
print(testboard)
# 游戏主循环
while True:
    for event in pygame.event.get() :
        if event.type == pygame.MOUSEBUTTONDOWN and 650<= event.pos[0]<= 800 and 10<=event.pos[1]<=60:
            init_picture()
            gameBoard, blackCell = init_picture()
            sleep(0.5)
            steps = 0
            finish = False
            pygame.display.flip()
        if event.type == pygame.MOUSEBUTTONDOWN and 650<=event.pos[0]<=800 and 70<=event.pos[1]<=120 :
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and 650 <= event.pos[0] <= 800 and 130 <= event.pos[1] <= 180 :
            testboard[blackCell] = 0

            aitest(testboard)
            testboard[blackCell] = -1
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if finish:
            continue
        if event.type == KEYDOWN:
            if event.key == K_d:
                blackCell = moveLeft(gameBoard, blackCell)
                steps += 1
            if event.key == K_a:
                blackCell = moveRight(gameBoard, blackCell)
                steps += 1
            if event.key == K_s:
                blackCell = moveUp(gameBoard, blackCell)
                steps += 1
            if event.key == K_w:
                blackCell = moveDown(gameBoard, blackCell)
                steps += 1

    if (isFinished(gameBoard, blackCell)):
        gameBoard[blackCell] = blocks - 1
        finish = True
#显示按钮及步数
    windowSurface.fill(background)
    replay = pygame.image.load('./botton/restart.png')
    out = pygame.image.load('./botton/quit.png')
    ai = pygame.image.load('./botton/AI.png')  # ai按钮
    windowSurface.blit(replay, [650, 10])
    windowSurface.blit(out,[650,70])
    windowSurface.blit(ai, [650, 130])  # ai按钮位置
    windowSurface.blit(pic,[620,420])
    step = str(steps)
    showText(fontminObj, "Steps:", 700, 200)
    showText(fontminObj, step, 760, 220)

    # 绘制移动后的拼图
    for i in range(blocks):
        row = int(i/rows)
        col = int(i%rows)
        rectDst = pygame.Rect(col*width, row*height, width, height)
        if gameBoard[i] == -1:
            continue
        rowArea = int(gameBoard[i]/rows)
        colArea = int(gameBoard[i]%rows)
        rectArea = pygame.Rect(colArea*width, rowArea*height, width, height)
        windowSurface.blit(gameImage, rectDst, rectArea)

    pygame.display.update()