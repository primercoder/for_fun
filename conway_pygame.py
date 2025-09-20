import argparse
import pygame
import numpy as np

GRIDBACKGROUND = (0x44, 0x01, 0x54)
GRIDLINE = (0x50, 0x30, 0x30)
CELL = (0xfd, 0xe7, 0x24)
BUTTONBACKGROUND = (0xe4, 0xed, 0xfb)
BUTTONUNCHECKED = (0x1d, 0xa1, 0xf2)
BUTTONCHECKED = (0x00, 0x5c, 0xbf)
TEXTCOLOR = (0xff, 0xff, 0xff)

screenW = 1001
screenH = 1100
gridW = 1001
gridWidth = 10
grid = np.array([])

glides = np.array(
    [
        [
            [1, 1, 0], 
            [1, 0, 1], 
            [1, 0, 0]
        ], 
        [
            [1, 1, 1],
            [0, 0, 1],
            [0, 1, 0]
        ],
        [
            [0, 1, 0],
            [1, 0, 0],
            [1, 1, 1]
        ],
        [
            [0, 0, 1],
            [1, 0, 1],
            [0, 1, 1]
        ]
    ], dtype=np.uint8)


class Button:
    def __init__(self, x, y, width, height, text, color, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.ischecked = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 20)
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):  # 左键点击
                return True
        return False

def zeroInitial(N):
    global grid
    grid = np.zeros(N*N, dtype=np.uint8).reshape(N, N)

def randomInitial(N):
    global grid
    grid = np.random.choice([1, 0], N*N, p=[0.2, 0.8]).reshape(N, N)
    
def updateGrid():
    global grid
    newGrid = grid.copy()
    size = grid.shape[0]
    for i in range(size):
        for j in range(size):
            total = int(
                (grid[i, (j-1)%size] + grid[i, (j+1)%size] +
                grid[(i-1)%size, j] + grid[(i+1)%size, j] +
                grid[(i-1)%size, (j-1)%size] + grid[(i+1)%size, (j+1)%size] +
                grid[(i-1)%size, (j+1)%size] + grid[(i+1)%size, (j-1)%size]) / 1
            )
            if grid[i, j] == 1:
                if total<2 or total>3:
                    newGrid[i, j] = 0
            else:
                if total == 3:
                    newGrid[i, j] = 1
    grid[:] = newGrid[:]

def addGlide(i, j, n):
    global grid
    global glides
    grid[i:i+3][j:j+3] = glides[n][:][:]
    
def drawGrid(screen):
    for i in range(grid.shape[0]):
        for j in range(grid.shape[0]):
            if grid[i, j] == 1:
                pygame.draw.rect(screen, CELL, (j*gridWidth+1, i*gridWidth+1, gridWidth-1, gridWidth-1))
            else:
                pygame.draw.rect(screen, GRIDBACKGROUND, (j*gridWidth+1, i*gridWidth+1, gridWidth-1, gridWidth-1))

def drawLine(screen):
    for i in range(grid.shape[0]+1):
        pygame.draw.line(screen, GRIDLINE, (i*gridWidth, 0), (i*gridWidth, gridW-1), 1)
    for i in range(grid.shape[0]+1):
        pygame.draw.line(screen, GRIDLINE, (0, i*gridWidth), (gridW-1, i*gridWidth), 1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run Conway's Game of Life simulation.")
    parser.add_argument('--grid-size', dest='N', help='set the scale', required=False)
    args = parser.parse_args()
    N = 50
    if args.N and int(args.N)>8:
        N = int(args.N)
    gridWidth = gridW // N
    
    randomInitial(N)
    # 暂停/继续  清空  随机化  添加个体  滑翔机左上 滑翔机右上 滑翔机左下 滑翔机右下  消除
    buttonPause = Button(20, screenH-79, 100, 59, "Start", BUTTONUNCHECKED, TEXTCOLOR)
    buttonClear = Button(130, screenH-79, 100, 59, "Clear", BUTTONUNCHECKED, TEXTCOLOR)
    buttonRandom = Button(240, screenH-79, 100, 59, "Randomize", BUTTONUNCHECKED, TEXTCOLOR)
    buttonAdd = Button(350, screenH-79, 100, 59, "Add", BUTTONUNCHECKED, TEXTCOLOR)
    buttonLU = Button(460, screenH-99, 200, 49, "Glide Left Up", BUTTONUNCHECKED, TEXTCOLOR)
    buttonRU = Button(661, screenH-99, 200, 49, "Glide Right Up", BUTTONUNCHECKED, TEXTCOLOR)
    buttonLD = Button(460, screenH-49, 200, 49, "Glide Left Down", BUTTONUNCHECKED, TEXTCOLOR)
    buttonRD = Button(661, screenH-49, 200, 49, "Glide Right Down", BUTTONUNCHECKED, TEXTCOLOR)
    buttonKill = Button(screenW-120, screenH-79, 100, 59, "Kill", BUTTONUNCHECKED, TEXTCOLOR)
    buttons = []
    buttons.append(buttonPause)
    buttons.append(buttonClear)
    buttons.append(buttonRandom)
    buttons.append(buttonAdd)
    buttons.append(buttonLU)
    buttons.append(buttonRU)
    buttons.append(buttonLD)
    buttons.append(buttonRD)
    buttons.append(buttonKill)
    
    clock = pygame.time.Clock()
    pygame.init()
    screen = pygame.display.set_mode((screenW, screenH))
    pygame.display.set_caption("Conway Life Game")
    screen.fill(BUTTONBACKGROUND)
    drawGrid(screen)
    drawLine(screen)
    for button in buttons:
        button.draw(screen)
    pygame.display.flip()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if buttonPause.is_clicked(event):
                if buttonPause.ischecked:
                    buttonPause.text = "Start"
                    buttonPause.color = BUTTONUNCHECKED
                    buttonPause.ischecked = False
                else:
                    buttonPause.text = "Pause"
                    buttonPause.color = BUTTONCHECKED
                    buttonPause.ischecked = True
                buttonPause.draw(screen)
            elif buttonClear.is_clicked(event):
                grid[:] = 0
            elif buttonRandom.is_clicked(event):
                randomInitial(N)
            elif buttonAdd.is_clicked(event):
                if buttonAdd.ischecked:
                    buttonAdd.ischecked = False
                    buttonAdd.color = BUTTONUNCHECKED
                else:
                    buttonAdd.ischecked = True
                    buttonAdd.color = BUTTONCHECKED
                    if buttonKill.ischecked:
                        buttonKill.ischecked = False
                        buttonKill.color = BUTTONUNCHECKED
                        buttonKill.draw(screen)
                    if buttonLU.ischecked:
                        buttonLU.ischecked = False
                        buttonLU.color = BUTTONUNCHECKED
                        buttonLU.draw(screen)
                    if buttonRU.ischecked:
                        buttonRU.ischecked = False
                        buttonRU.color = BUTTONUNCHECKED
                        buttonRU.draw(screen)
                    if buttonLD.ischecked:
                        buttonLD.ischecked = False
                        buttonLD.color = BUTTONUNCHECKED
                        buttonLD.draw(screen)
                    if buttonRD.ischecked:
                        buttonRD.ischecked = False
                        buttonRD.color = BUTTONUNCHECKED
                        buttonRD.draw(screen)
                buttonAdd.draw(screen)
            elif buttonKill.is_clicked(event):
                if buttonKill.ischecked:
                    buttonKill.ischecked = False
                    buttonKill.color = BUTTONUNCHECKED
                else:
                    buttonKill.ischecked = True
                    buttonKill.color = BUTTONCHECKED
                    if buttonAdd.ischecked:
                        buttonAdd.ischecked = False
                        buttonAdd.color = BUTTONUNCHECKED
                        buttonAdd.draw(screen)
                    if buttonLU.ischecked:
                        buttonLU.ischecked = False
                        buttonLU.color = BUTTONUNCHECKED
                        buttonLU.draw(screen)
                    if buttonRU.ischecked:
                        buttonRU.ischecked = False
                        buttonRU.color = BUTTONUNCHECKED
                        buttonRU.draw(screen)
                    if buttonLD.ischecked:
                        buttonLD.ischecked = False
                        buttonLD.color = BUTTONUNCHECKED
                        buttonLD.draw(screen)
                    if buttonRD.ischecked:
                        buttonRD.ischecked = False
                        buttonRD.color = BUTTONUNCHECKED
                        buttonRD.draw(screen)
                buttonKill.draw(screen)
            elif buttonLU.is_clicked(event):
                if buttonLU.ischecked:
                    buttonLU.ischecked = False
                    buttonLU.color = BUTTONUNCHECKED
                else:
                    buttonLU.ischecked = True
                    buttonLU.color = BUTTONCHECKED
                    if buttonAdd.ischecked:
                        buttonAdd.ischecked = False
                        buttonAdd.color = BUTTONUNCHECKED
                        buttonAdd.draw(screen)
                    if buttonKill.ischecked:
                        buttonKill.ischecked = False
                        buttonKill.color = BUTTONUNCHECKED
                        buttonKill.draw(screen)
                    if buttonRU.ischecked:
                        buttonRU.ischecked = False
                        buttonRU.color = BUTTONUNCHECKED
                        buttonRU.draw(screen)
                    if buttonLD.ischecked:
                        buttonLD.ischecked = False
                        buttonLD.color = BUTTONUNCHECKED
                        buttonLD.draw(screen)
                    if buttonRD.ischecked:
                        buttonRD.ischecked = False
                        buttonRD.color = BUTTONUNCHECKED
                        buttonRD.draw(screen)
                buttonLU.draw(screen)
            elif buttonRU.is_clicked(event):
                if buttonRU.ischecked:
                    buttonRU.ischecked = False
                    buttonRU.color = BUTTONUNCHECKED
                else:
                    buttonRU.ischecked = True
                    buttonRU.color = BUTTONCHECKED
                    if buttonAdd.ischecked:
                        buttonAdd.ischecked = False
                        buttonAdd.color = BUTTONUNCHECKED
                        buttonAdd.draw(screen)
                    if buttonKill.ischecked:
                        buttonKill.ischecked = False
                        buttonKill.color = BUTTONUNCHECKED
                        buttonKill.draw(screen)
                    if buttonLU.ischecked:
                        buttonLU.ischecked = False
                        buttonLU.color = BUTTONUNCHECKED
                        buttonLU.draw(screen)
                    if buttonLD.ischecked:
                        buttonLD.ischecked = False
                        buttonLD.color = BUTTONUNCHECKED
                        buttonLD.draw(screen)
                    if buttonRD.ischecked:
                        buttonRD.ischecked = False
                        buttonRD.color = BUTTONUNCHECKED
                        buttonRD.draw(screen)
                buttonRU.draw(screen)
            elif buttonLD.is_clicked(event):
                if buttonLD.ischecked:
                    buttonLD.ischecked = False
                    buttonLD.color = BUTTONUNCHECKED
                else:
                    buttonLD.ischecked = True
                    buttonLD.color = BUTTONCHECKED
                    if buttonAdd.ischecked:
                        buttonAdd.ischecked = False
                        buttonAdd.color = BUTTONUNCHECKED
                        buttonAdd.draw(screen)
                    if buttonKill.ischecked:
                        buttonKill.ischecked = False
                        buttonKill.color = BUTTONUNCHECKED
                        buttonKill.draw(screen)
                    if buttonRU.ischecked:
                        buttonRU.ischecked = False
                        buttonRU.color = BUTTONUNCHECKED
                        buttonRU.draw(screen)
                    if buttonLU.ischecked:
                        buttonLU.ischecked = False
                        buttonLU.color = BUTTONUNCHECKED
                        buttonLU.draw(screen)
                    if buttonRD.ischecked:
                        buttonRD.ischecked = False
                        buttonRD.color = BUTTONUNCHECKED
                        buttonRD.draw(screen)
                buttonLD.draw(screen)
            elif buttonRD.is_clicked(event):
                if buttonRD.ischecked:
                    buttonRD.ischecked = False
                    buttonRD.color = BUTTONUNCHECKED
                else:
                    buttonRD.ischecked = True
                    buttonRD.color = BUTTONCHECKED
                    if buttonAdd.ischecked:
                        buttonAdd.ischecked = False
                        buttonAdd.color = BUTTONUNCHECKED
                        buttonAdd.draw(screen)
                    if buttonKill.ischecked:
                        buttonKill.ischecked = False
                        buttonKill.color = BUTTONUNCHECKED
                        buttonKill.draw(screen)
                    if buttonRU.ischecked:
                        buttonRU.ischecked = False
                        buttonRU.color = BUTTONUNCHECKED
                        buttonRU.draw(screen)
                    if buttonLU.ischecked:
                        buttonLU.ischecked = False
                        buttonLU.color = BUTTONUNCHECKED
                        buttonLU.draw(screen)
                    if buttonLD.ischecked:
                        buttonLD.ischecked = False
                        buttonLD.color = BUTTONUNCHECKED
                        buttonLD.draw(screen)
                buttonRD.draw(screen)
            else:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    i = event.pos[1]//gridWidth
                    j = event.pos[0]//gridWidth
                    if i < N:
                        if buttonAdd.ischecked:
                            grid[i][j] = 1
                        elif buttonKill.ischecked:
                            grid[i][j] = 0
                        elif buttonLU.ischecked:
                            for gi in range(3):
                                for gj in range(3):
                                    grid[(i+gi)%N, (j+gj)%N] = glides[0][gi, gj]
                        elif buttonRU.ischecked:
                            for gi in range(3):
                                for gj in range(3):
                                    grid[(i+gi)%N, (j+gj)%N] = glides[1][gi, gj]
                        elif buttonLD.ischecked:
                            for gi in range(3):
                                for gj in range(3):
                                    grid[(i+gi)%N, (j+gj)%N] = glides[2][gi, gj]
                        elif buttonRD.ischecked:
                            for gi in range(3):
                                for gj in range(3):
                                    grid[(i+gi)%N, (j+gj)%N] = glides[3][gi, gj]
        
        if buttonPause.ischecked:
            updateGrid()
        drawGrid(screen)   
        pygame.display.update()
        clock.tick(30)
                
                