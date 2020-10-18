#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
pic_url = requests.get('http://47.102.118.1:8089/api/problem?stuid=031802423')
image_code = base64.b64decode(pic_url.json()['img'])
file_like = BytesIO(image_code)
image = Image.open(file_like)
image.save('image.JPG')
# 初始化
pygame.init()
# 设置窗口
windowSurface = pygame.display.set_mode([window_width+200, window_height])
pygame.display.set_caption('拼图')
# 每块拼图大小
width = int(window_height / 3)
height = int(window_width / 3)
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
mins = 0
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

# gameRect = gameImage2.get_rect()
#参考图片
cankao = pygame.image.load('cankao1.jpg')
pic = pygame.transform.scale(cankao, (180, 180))
windowSurface.blit(pic, [620, 420])

finish = False

gameBoard, blackCell = init_picture()

# 游戏主循环
while True:
    for event in pygame.event.get() :
        if event.type == pygame.MOUSEBUTTONDOWN and 650<= event.pos[0]<= 800 and 10<=event.pos[1]<=60:
            init_picture()
            gameBoard, blackCell = init_picture()
            sleep(0.5)
            mins = steps
            steps = 0
            finish = False
            pygame.display.flip()
        if event.type == pygame.MOUSEBUTTONDOWN and 650<=event.pos[0]<=800 and 70<=event.pos[1]<=120 :
            pygame.quit()
            sys.exit()
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if finish:
            mins = steps
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
    windowSurface.blit(replay, [650, 10])
    windowSurface.blit(out,[650,70])
    windowSurface.blit(pic,[620,420])
    step = str(steps)
    showText(fontminObj, "Steps:", 700, 200)
    showText(fontminObj, step, 760, 220)
    showText(fontminObj,"Past Steps:",700,300)
    showText(fontminObj,str(mins),750,320)

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