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
#blue = (0,0,255)
black = (0, 0, 0)
white = (255,255,255)
# gray = (128,128,128)
# bright_gray = (150,150,150)
# FPS = 30
rows = 3
blocks = rows * rows
max_time = 100


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

    for i in range(max_time):
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
    if blackCell % rows == 0:
        return blackCell
    board[blackCell - 1], board[blackCell] = board[blackCell], board[blackCell - 1]
    return blackCell - 1

# 若空白图像块不在最右边，则将空白块右边的块移动到空白块位置
def moveLeft(board, blackCell):
    if blackCell % rows == rows - 1:
        return blackCell
    board[blackCell + 1], board[blackCell] = board[blackCell], board[blackCell + 1]
    return blackCell + 1

# 若空白图像块不在最上边，则将空白块上边的块移动到空白块位置
def moveDown(board, blackCell):
    if blackCell < rows:
        return blackCell
    board[blackCell - rows], board[blackCell] = board[blackCell], board[blackCell - rows]
    return blackCell - rows

# 若空白图像块不在最下边，则将空白块下边的块移动到空白块位置
def moveUp(board, blackCell):
    if blackCell >= blocks - rows:
        return blackCell
    board[blackCell + rows], board[blackCell] = board[blackCell], board[blackCell + rows]
    return blackCell + rows

# 是否完成
def isFinished(board, blackCell):
    for i in range(blocks - 1):
        if board[i] != i :
            return False
    return True


# 初始化
pygame.init()
# 加载图片
gameImage = pygame.image.load('./无框字符/wu.jpg')
pic = pygame.transform.scale(gameImage, (150, 150))
gameRect = gameImage.get_rect()
# 设置窗口
windowSurface = pygame.display.set_mode([window_width+200, window_height])
pygame.display.set_caption('拼图')
# 拼图大小
width = int(window_height / rows)
height = int(window_width / rows)

finish = False

gameBoard, blackCell = init_board()

# 游戏主循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and 550 <= event.pos[0] <= 700 and 10 <= event.pos[1] <= 60:
            init_board()
            gameBoard, blackCell = init_board()
            sleep(0.5)
            pygame.display.flip()
        if event.type == pygame.MOUSEBUTTONDOWN and 550 <= event.pos[0] <= 700 and 70 <= event.pos[1] <= 120 :
            pygame.quit()
            sys.exit()
        if event.type == QUIT:
            terminate()
        if finish:
            continue
        if event.type == KEYDOWN:
            if event.key == K_d:
                blackCell = moveLeft(gameBoard, blackCell)
            if event.key == K_a:
                blackCell = moveRight(gameBoard, blackCell)
            if event.key == K_s:
                blackCell = moveUp(gameBoard, blackCell)
            if event.key == K_w:
                blackCell = moveDown(gameBoard, blackCell)

    if (isFinished(gameBoard, blackCell)):
        gameBoard[blackCell] = blocks - 1
        finish = True

    windowSurface.fill(background)
    replay = pygame.image.load('./无框字符/restart.png')
    out = pygame.image.load('./无框字符/quit.png')
    windowSurface.blit(replay, [550, 10])
    windowSurface.blit(out,[550,70])
    windowSurface.blit(pic,[550,350])
    for i in range(blocks):
        rowDst = int(i/rows)
        colDst = int(i%rows)
        rectDst = pygame.Rect(colDst*width, rowDst * height, width, height)

        if gameBoard[i] == -1:
            continue

        rowArea = int(gameBoard[i]/ rows)
        colArea = int(gameBoard[i] % rows)
        rectArea = pygame.Rect(colArea * width, rowArea * height, width, height)
        windowSurface.blit(gameImage, rectDst, rectArea)
    for i in range(rows+1):
        pygame.draw.line(windowSurface, black, (i*width, 0), (i*width, height))
    for i in range(rows+1):
        pygame.draw.line(windowSurface, black, (0, i*width), (width, i*height))
    pygame.display.update()