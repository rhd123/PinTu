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
    # 将空白块进行随机移动，确保每次打乱都能够有解
    for i in range(50) :
        direction = random.randint(0, 3)
        if (direction == 0) :
            blackCell = moveLeft(board, blackCell)
        elif (direction == 1) :
            blackCell = moveRight(board, blackCell)
        elif (direction == 2) :
            blackCell = moveUp(board, blackCell)
        elif (direction == 3) :
            blackCell = moveDown(board, blackCell)
    return board, blackCell
# 若空白图像块不在最左边，则将空白块左边的块移动到空白块位置
def moveRight(board, blackCell) :
    if blackCell % rows == 0 :
        return blackCell
    board[blackCell - 1], board[blackCell] = board[blackCell], board[blackCell - 1]
    return blackCell - 1


# 若空白图像块不在最右边，则将空白块右边的块移动到空白块位置
def moveLeft(board, blackCell) :
    if blackCell % rows == rows - 1 :
        return blackCell
    board[blackCell + 1], board[blackCell] = board[blackCell], board[blackCell + 1]
    return blackCell + 1


# 若空白图像块不在最上边，则将空白块上边的块移动到空白块位置
def moveDown(board, blackCell) :
    if blackCell < rows :
        return blackCell
    board[blackCell - rows], board[blackCell] = board[blackCell], board[blackCell - rows]
    return blackCell - rows


# 若空白图像块不在最下边，则将空白块下边的块移动到空白块位置
def moveUp(board, blackCell) :
    if blackCell >= blocks - rows :
        return blackCell
    board[blackCell + rows], board[blackCell] = board[blackCell], board[blackCell + rows]
    return blackCell + rows


# 是否完成
def isFinished(board, blackCell) :
    for i in range(blocks - 1) :
        if board[i] != i :
            return False
    return True


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
        if finish :
            continue
        if event.type == KEYDOWN :
            if event.key == K_d :
                blackCell = moveLeft(gameBoard, blackCell)

            if event.key == K_a :
                blackCell = moveRight(gameBoard, blackCell)

            if event.key == K_s :
                blackCell = moveUp(gameBoard, blackCell)

            if event.key == K_w :
                blackCell = moveDown(gameBoard, blackCell)


    if (isFinished(gameBoard, blackCell)) :
        gameBoard[blackCell] = blocks - 1
        finish = True

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