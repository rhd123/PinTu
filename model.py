import pygame, sys, random
from pygame.locals import *

# 一些常量
window_length = 500
background = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

rows = 3
blocks = rows * rows


# 随机生成游戏盘面
def newGameBoard() :
    board = []
    for i in range(blocks) :
        board.append(i)
    blackCell = blocks - 1
# 将图片的一块挖空
    board[blackCell] = -1

    return board, blackCell



# 初始化
pygame.init()
# 加载图片
gameImage = pygame.image.load('wu.jpg')
gameRect = gameImage.get_rect()

# 设置窗口
screen = pygame.display.set_mode((gameRect.width, gameRect.height))
pygame.display.set_caption('拼图')
# 每块拼图的大小
cellWidth = int(gameRect.width / rows)
cellHeight = int(gameRect.height / rows)

finish = False

gameBoard, blackCell = newGameBoard()

# 游戏主循环
while True :
    for event in pygame.event.get() :
        if event.type == QUIT :
            pygame.quit()
            sys.exit()
    screen.fill(background)
#绘制拼图
    for i in range(blocks) :
        rowDst = int(i / rows)
        colDst = int(i % rows)
        rectDst = pygame.Rect(colDst * cellWidth, rowDst * cellHeight, cellWidth, cellHeight)

        if gameBoard[i] == -1 :
            continue

        rowArea = int(gameBoard[i] / rows)
        colArea = int(gameBoard[i] % rows)
        rectArea = pygame.Rect(colArea * cellWidth, rowArea * cellHeight, cellWidth, cellHeight)
        screen.blit(gameImage, rectDst, rectArea)


    pygame.display.update()