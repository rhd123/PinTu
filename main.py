#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import sleep
import pygame
import sys
import random
from pygame.locals import *

window_width = 500
window_height = 500
background = (225,225,225)
blue = (0,0,255)
green = (0, 255, 0)
black = (0, 0, 0)
white = (255,255,255)
gray = (128,128,128)
bright_gray = (150,150,150)
rows = 3
blocks = rows * rows

# 退出
def terminate():
    pygame.quit()
    sys.exit()


# 随机生成游戏盘面
def init_board():
    board = []
    for i in range(blocks):
        board.append(i)
    blackCell = blocks - 1
    board[blackCell] = -1
# 随机移动拼图
    for i in range(100):
        direction = random.randint(0, 3)
        if (direction == 0):
            blackCell = moveLeft(board, blackCell)
        elif (direction == 1):
            blackCell = moveRight(board, blackCell)
        elif (direction == 2):
            blackCell = moveUp(board, blackCell)
        elif (direction == 3):
            blackCell = moveDown(board, blackCell)
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


# 初始化
pygame.init()
# 加载图片
gameImage1 = pygame.image.load('./无框字符/a_.jpg')
# 缩小图片作为参考图片
gameImage = pygame.transform.scale(gameImage1,(500,500))
pic = pygame.transform.scale(gameImage1, (150, 150))
gameRect = gameImage.get_rect()
# 设置窗口
windowSurface = pygame.display.set_mode([window_width+200, window_height])
pygame.display.set_caption('拼图')
# 每块拼图大小
width = int(window_height / rows)
height = int(window_width / rows)

finish = False
gameBoard, blackCell = init_board()
# 用于设置并绘制文字
def showText(fontObj, text, x, y) :
    textSurfaceObj = fontObj.render(text, True, black, background)  # 配置要显示的文字
    textRectObj = textSurfaceObj.get_rect()  # 获得要显示的对象的rect
    textRectObj.center = (x, y)  # 设置显示对象的坐标
    windowSurface.blit(textSurfaceObj, textRectObj)  #绘制字体
fontminObj = pygame.font.SysFont("",24)
steps = 0

# 游戏主循环
while True:
    for event in pygame.event.get() :
        if event.type == pygame.MOUSEBUTTONDOWN and 550<= event.pos[0]<= 700 and 10<=event.pos[1]<=60:
            init_board()
            gameBoard, blackCell = init_board()
            sleep(0.5)
            steps = 0
            finish = False
            pygame.display.flip()
        if event.type == pygame.MOUSEBUTTONDOWN and 550<=event.pos[0]<=700 and 70<=event.pos[1]<=120 :
            pygame.quit()
            sys.exit()
        if event.type == QUIT:
            terminate()
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
    replay = pygame.image.load('./无框字符/restart.png')
    out = pygame.image.load('./无框字符/quit.png')
    windowSurface.blit(replay, [550, 10])
    windowSurface.blit(out,[550,70])
    windowSurface.blit(pic,[550,350])
    step = str(steps)
    showText(fontminObj, "Steps:", 600, 200)
    showText(fontminObj, step, 660, 220)

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