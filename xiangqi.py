'''
Xiang qi
by Owen Yu

tasks:
make pieces turn when moved
make moving animation 


'''

import pygame
from pygame.locals import *
import sys
import os
from random import randint, uniform, choice
from math import sqrt

# Initializing Pygame
pygame.init()
vec = pygame.math.Vector2

FPS = 60
clock = pygame.time.Clock()

# Color
WHITE = (255, 255, 255)
BROWN = (238, 187, 85)
BLACK = (0, 0, 0)
RED = (224,2,2)
# Screen
WIDTH = 500
HEIGHT = int(10/9 * WIDTH)
DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
DISPLAY.fill(BROWN)

# Images
sourceFileDir = os.path.dirname(os.path.abspath(__file__))


C_P_SIZE = int(WIDTH/11)

ICON = pygame.image.load(os.path.join(
    sourceFileDir, os.path.join('assets', 'icon.png')))

IMAGE_CHESS_BOARD = pygame.image.load(os.path.join(
    sourceFileDir, os.path.join('assets', 'xiangqi_board.png')))
IMAGE_CHESS_BOARD = pygame.transform.smoothscale(
    IMAGE_CHESS_BOARD, (int(WIDTH*1.023), int(HEIGHT*1.025)))
IMAGE_CHESS_PIECES = pygame.image.load(os.path.join(
    sourceFileDir, os.path.join('assets', 'xiangqi_pieces.png')))
IMAGE_CHESS_PIECES = pygame.transform.smoothscale(
    IMAGE_CHESS_PIECES, (C_P_SIZE * 7, C_P_SIZE * 2))
IMAGE_SELECTED_RED = pygame.image.load(os.path.join(
    sourceFileDir, os.path.join('assets', 'selected_red.png')))
IMAGE_SELECTED_RED = pygame.transform.smoothscale(
    IMAGE_SELECTED_RED, (C_P_SIZE, C_P_SIZE))
IMAGE_SELECTED_BLACK = pygame.image.load(os.path.join(
    sourceFileDir, os.path.join('assets', 'selected_black.png')))
IMAGE_SELECTED_BLACK = pygame.transform.smoothscale(
    IMAGE_SELECTED_BLACK, (C_P_SIZE, C_P_SIZE))

# Sound
try:
    SOUND_SELECTED = pygame.mixer.Sound(os.path.join(
        sourceFileDir, os.path.join('assets', 'selected.wav')))
    SOUND_SELECTED_AND_PROCEEDED = pygame.mixer.Sound(os.path.join(
        sourceFileDir, os.path.join('assets', 'selected_and_proceeded.wav')))
    SOUND_EATEN = pygame.mixer.Sound(os.path.join(
        sourceFileDir, os.path.join('assets', 'eaten.wav')))
    SOUND_EATEN_2 = pygame.mixer.Sound(os.path.join(
        sourceFileDir, os.path.join('assets', 'death.wav')))
except:
    pass
# Font
font = pygame.font.SysFont("bahnschrift", 100)

# Set title and Icon
pygame.display.set_caption("Xiang Qi")
pygame.display.set_icon(ICON)

# Variables


A_C_X_0 = 9  # Aligning Constant X
A_C_X_1 = 75  # Aligning Constant X offset
A_C_Y_0 = 10.1  # Aligning Constant Y
A_C_Y_1 = 70  # Aligning Constant Y offset

clicked = None
only_one_selected = None  # To make sure there's only one piece selected
cant_eat = False  # To make sure the piece doesn't move if it trys to eat it's own team
turn = "red"

def VX():
    l = []
    for i in range(50):
        b = randint(-30,30)
        if abs(b) > 20:
            l.append(b)

    return choice(l)
VY = VX
RADIUS = 3 if WIDTH > 700 else 2
COLOR = RED

chess_board_x = -WIDTH/100
chess_board_y = -WIDTH/100
# Functions


def random_float(a, b):
    return round(uniform(a, b), 5)


def King(self, column, row):
    if self.color == "red":
        if row < 7 or column < 3 or column > 5:
            return False
    elif self.color == "black":
        if row > 2 or column < 3 or column > 5:
            return False
    possible_moves = [[0,1],[0,-1],[1,0],[-1,0]]
    bruh = False
    for i in possible_moves:
        if [column-self.column, row-self.row] == i:
            i_copy = i
            bruh = True
    if bruh == False:
        return False
    return True


def Guard(self, column, row):
    if self.color == "red":
        if row < 7 or column < 3 or column > 5:
            return False
    elif self.color == "black":
        if row > 2 or column < 3 or column > 5:
            return False
    possible_moves = [[1,1],[-1,-1],[1,-1],[-1,1]]
    bruh = False
    for i in possible_moves:
        if [column-self.column, row-self.row] == i:
            i_copy = i
            bruh = True
    if bruh == False:
        return False
    return True
    


def Knight(self, column, row):
    possible_moves = [[1, 2], [1, -2], [-1, 2],
                      [-1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1]]
    bruh = False
    for i in possible_moves:
        if [column-self.column, row-self.row] == i:
            i_copy = i
            bruh = True

    if bruh == False:
        return False
    dic = {"right": False, "up": False, "down": False, "left": False}
    for i in all_pieces:
        if (i.column, i.row) == (self.column + 1, self.row):
            dic["right"] = True
        elif (i.column, i.row) == (self.column, self.row - 1):
            dic["up"] = True
        elif (i.column, i.row) == (self.column, self.row + 1):
            dic["down"] = True
        elif (i.column, i.row) == (self.column - 1, self.row):
            dic["left"] = True
    if i_copy[0] == 2 and dic["right"] or i_copy[0] == -2 and dic["left"] or i_copy[1] == 2 and dic["down"] or i_copy[1] == -2 and dic["up"]:
        return False

    # print(dic)

    return True


def Elephant(self, column, row):
    if self.color == "red" and row < 5 or self.color == "black" and row > 4:
        return False

    possible_moves = [[2,2],[-2,-2],[2,-2],[-2,2]]
    bruh = False
    for i in possible_moves:
        if [column-self.column, row-self.row] == i:
            i_copy = i
            bruh = True
    if bruh == False:
        return False

    dic = {"right_up": False, "left_up": False, "right_down": False, "left_down": False}
    for i in all_pieces:
        if (i.column, i.row) == (self.column + 1, self.row - 1):
            dic["right_up"] = True
        elif (i.column, i.row) == (self.column -1, self.row - 1):
            dic["left_up"] = True
        elif (i.column, i.row) == (self.column + 1, self.row + 1):
            dic["right_down"] = True
        elif (i.column, i.row) == (self.column - 1, self.row + 1):
            dic["left_down"] = True
    if i_copy == possible_moves[2] and dic["right_up"] or i_copy == possible_moves[1] and dic["left_up"] or i_copy == possible_moves[0] and dic["right_down"] or i_copy == possible_moves[3] and dic["left_down"]:
        return False 
    
    return True       

def Rook(self, column, row):
    if self.column != column and self.row != row:
        return False
    # row or column that's changing
    column_or_row = "column" if self.column != column else "row"
    a = self.column if self.column != column else self.row
    b = column if self.column != column else row
    increment = 1 if a < b else -1
    constant = column if self.column == column else row

    for i in range(a-1 if increment == -1 else a+1, b, increment):

        for j in all_pieces:
            if column_or_row == "column":
                if j.column == i and j.row == constant:
                    return False
            elif column_or_row == "row":
                if j.row == i and j.column == constant:
                    return False

    return True


def Cannon(self, column, row):
    if self.column != column and self.row != row:
        return False
    # row or column that's changing
    column_or_row = "column" if self.column != column else "row"
    a = self.column if self.column != column else self.row
    b = column if self.column != column else row
    increment = 1 if a < b else -1
    constant = column if self.column == column else row
    amount_of_pieces_between = 0

    for i in range(a-1 if increment == -1 else a+1, b-1 if increment == -1 else b+1, increment):

        for j in all_pieces:
            if column_or_row == "column":
                if j.column == i and j.row == constant:
                    amount_of_pieces_between += 1
            elif column_or_row == "row":
                if j.row == i and j.column == constant:
                    amount_of_pieces_between += 1
    # print(amount_of_pieces_between)
    if amount_of_pieces_between > 2 or amount_of_pieces_between == 1:
        return False

    elif amount_of_pieces_between == 2:
        bruh = False
        # print(1)
        for i in all_pieces:
            if (i.column, i.row) == (column, row):
                # print(2)
                bruh = True
        if bruh == False:
            return False

    return True


def Pawn(self, column, row):

    if self.color == "red":
        if self.row > 4:

            if row - self.row != -1 or column != self.column:

                return False
        elif self.row <= 4:
            column_or_row = "column" if self.column != column else "row"
            if column_or_row == "row":
                if row - self.row != -1 or column != self.column:
                    return False
            elif column_or_row == "column":
                if abs(column - self.column) != 1 or row != self.row:
                    return False

    elif self.color == "black":
        if self.row < 5:
            if row - self.row != 1 or column != self.column:
                return False
        elif self.row >= 5:
            column_or_row = "column" if self.column != column else "row"
            if column_or_row == "row":
                if row - self.row != 1 or column != self.column:
                    return False
            elif column_or_row == "column":
                if abs(column - self.column) != 1 or row != self.row:
                    return False

    return True


# Classes

class Explosion_Particle():
    def __init__(self, x,y,v,radius,color):
        self.pos = vec(x,y)
        self.vel = vec(v,v)
        self.vel.x = random_float(-1,1) * v
        self.vn = sqrt(v**2 - self.vel.x**2)
        self.vel.y = random_float(-1,1) * self.vn
        self.radius = radius
        self.color = color
    def update(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        
        pygame.draw.circle(DISPLAY,self.color,(self.pos.x,self.pos.y),self.radius)

class Piece():
    def __init__(self, column, row, color, type_of_piece):
        self.column = column
        self.row = row
        self.x = int(column * WIDTH/A_C_X_0 + WIDTH/A_C_X_1)
        self.y = int(row * HEIGHT/A_C_Y_0 + HEIGHT/A_C_Y_1)
        self.color = color
        self.vx = 0
        self.vy = 0
        self.image_id = None  # To reference the image using c_p_size
        # Each piece has it's own moving and eating rules.
        self.type_of_piece = type_of_piece
        self.state = "neutral"
        self.previous_column = self.column
        self.previous_row = self.row
        self.rect = pygame.Rect(self.x, self.y, C_P_SIZE, C_P_SIZE)

    def update(self):

        self.rect = pygame.Rect(self.x, self.y, C_P_SIZE, C_P_SIZE)

        self.x = int(self.column * WIDTH/A_C_X_0 + WIDTH/A_C_X_1)
        self.y = int(self.row * HEIGHT/A_C_Y_0 + HEIGHT/A_C_Y_1)

        self.previous_x = int(self.previous_column *
                              WIDTH/A_C_X_0 + WIDTH/A_C_X_1)
        self.previous_y = int(self.previous_row *
                              HEIGHT/A_C_Y_0 + HEIGHT/A_C_Y_1)

        if only_one_selected != self:
            self.state = "neutral"

        if self.type_of_piece == King:
            self.image_id = C_P_SIZE*0
        elif self.type_of_piece == Guard:
            self.image_id = C_P_SIZE*1
        elif self.type_of_piece == Knight:
            self.image_id = C_P_SIZE*2
        elif self.type_of_piece == Elephant:
            self.image_id = C_P_SIZE*3
        elif self.type_of_piece == Rook:
            self.image_id = C_P_SIZE*4
        elif self.type_of_piece == Cannon:
            self.image_id = C_P_SIZE*5
        elif self.type_of_piece == Pawn:
            self.image_id = C_P_SIZE*6

        DISPLAY.blit(IMAGE_CHESS_PIECES, (self.x, self.y), (self.image_id,
                     0 if self.color == "red" else C_P_SIZE, C_P_SIZE, C_P_SIZE))

        if self.state == "selected" or self.state == "selected_and_proceeded":

            DISPLAY.blit(IMAGE_SELECTED_BLACK if self.color ==
                         "red" else IMAGE_SELECTED_RED, (self.x, self.y))

        if self.state == "selected_and_proceeded":
            if self.previous_x != None and self.previous_y != None:

                DISPLAY.blit(IMAGE_SELECTED_BLACK if self.color ==
                             "red" else IMAGE_SELECTED_RED, (self.previous_x, self.previous_y))


# Setup
all_particles = []
all_pieces = []


all_pieces.append(Piece(0, 0, "black", Rook))
all_pieces.append(Piece(8, 0, "black", Rook))
all_pieces.append(Piece(1, 0, "black", Knight))
all_pieces.append(Piece(7, 0, "black", Knight))
all_pieces.append(Piece(2, 0, "black", Elephant))
all_pieces.append(Piece(6, 0, "black", Elephant))
all_pieces.append(Piece(3, 0, "black", Guard))
all_pieces.append(Piece(5, 0, "black", Guard))
all_pieces.append(Piece(4, 0, "black", King))

for i in range(5):
    all_pieces.append(Piece(i*2, 3, "black", Pawn))

all_pieces.append(Piece(1, 2, "black", Cannon))
all_pieces.append(Piece(7, 2, "black", Cannon))

all_pieces.append(Piece(1, 7, "red", Cannon))
all_pieces.append(Piece(7, 7, "red", Cannon))

for i in range(5):
    all_pieces.append(Piece(i*2, 6, "red", Pawn))

all_pieces.append(Piece(4, 9, "red", King))
all_pieces.append(Piece(3, 9, "red", Guard))
all_pieces.append(Piece(5, 9, "red", Guard))
all_pieces.append(Piece(2, 9, "red", Elephant))  
all_pieces.append(Piece(6, 9, "red", Elephant))
all_pieces.append(Piece(1, 9, "red", Knight))
all_pieces.append(Piece(7, 9, "red", Knight))
all_pieces.append(Piece(0, 9, "red", Rook))
all_pieces.append(Piece(8, 9, "red", Rook))

# Mainloop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                new_clicked_column = round(
                    (mouse_pos[0] - C_P_SIZE/2 - WIDTH/A_C_X_1)/(WIDTH/A_C_X_0))
                new_clicked_row = round(
                    (mouse_pos[1] - C_P_SIZE/2 - HEIGHT/A_C_Y_1)/(HEIGHT/A_C_Y_0))

                cant_eat = False

                if clicked != None:
                    for i in all_pieces:
                        if (i.column, i.row) == (new_clicked_column, new_clicked_row) and i != clicked:
                            if i.color == clicked.color:
                                cant_eat = True
                                break
                try:
                    if clicked == None or clicked.state != "selected" or cant_eat == True or clicked != None and clicked.color != turn:
                        clicked = [
                            s for s in all_pieces if s.rect.collidepoint(mouse_pos)][-1]

                except:
                    clicked = None

                if clicked != None and clicked.color == turn:

                    if clicked.state == "neutral" or clicked.state == "selected_and_proceeded":
                        try:
                            SOUND_SELECTED.play()
                        except:
                            pass
                        only_one_selected = clicked
                        clicked.state = "selected"

                    elif clicked.state == "selected":

                        if (clicked.column, clicked.row) != (new_clicked_column, new_clicked_row) and clicked.type_of_piece(clicked, new_clicked_column, new_clicked_row):
                            cant_eat = False

                            for i in all_pieces:
                                if (i.column, i.row) == (new_clicked_column, new_clicked_row) and i != clicked:
                                    COLOR = i.color
                                    all_pieces.remove(i)
                                    try:
                                        SOUND_EATEN.play()
                                        ##SOUND_EATEN_2.play()
                                        for i in range(100):
                                            all_particles.append(Explosion_Particle(mouse_pos[0],mouse_pos[1],VX(),RADIUS,choice([RED if COLOR == "red" else BLACK,WHITE])))
                                    except:
                                        pass
                                    break
                            try:
                                SOUND_SELECTED_AND_PROCEEDED.play()
                            except:
                                pass
                            clicked.previous_column = clicked.column
                            clicked.previous_row = clicked.row

                            clicked.column = new_clicked_column
                            clicked.row = new_clicked_row

                            clicked.state = "selected_and_proceeded"

                            turn = "red" if turn == "black" else "black"

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                # if clicked != None:

                ##clicked = None
                pass
        elif event.type == pygame.MOUSEMOTION:
            if clicked != None:
                pass

    DISPLAY.blit(IMAGE_CHESS_BOARD, (chess_board_x, chess_board_y))

    for entity in all_particles:
        entity.update()

    for entity in all_pieces:

        entity.update()
    
    

    pygame.display.update()
    clock.tick(FPS)
