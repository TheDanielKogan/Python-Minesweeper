__author__ = "D. Kogan"
'''
Name: Daniel Kogan
Date: January 23rd, 2023
Project: Minesweeper
Description: A fully working game of minesweeper with 3 different skill levels 
'''
import random
import pygame
import math
pygame.init()

BACKGROUND_COLOR = (230, 230, 255)
RED = (255,0,0)
BLACK = (0,0,0)
GRAY = (150,150,150)

# init all images
CLICKED_BOMB = pygame.image.load("cell_bomb_clicked.png")
BOMB = pygame.image.load("cell_bomb.png")
WRONG_FLAG = pygame.image.load("incorrect_flag.png")
FLAG = pygame.image.load("cell_flag.png")
REGULAR_FACE = pygame.image.load("regular_face.png")
LOSS_FACE = pygame.image.load("loss_face.png")
UNOPENED_CELL = pygame.image.load("unopened_cell.png")
OPENED_CELL = pygame.image.load("open_cell.png")
ONE = pygame.image.load("cell_1.png")
TWO = pygame.image.load("cell_2.png")
THREE = pygame.image.load("cell_3.png")
FOUR = pygame.image.load("cell_4.png")
FIVE = pygame.image.load("cell_5.png")
SIX = pygame.image.load("cell_6.png")
SEVEN = pygame.image.load("cell_7.png")
EIGHT = pygame.image.load("cell_8.png")

board = []
'''
Planning to have the board be a 2D array
This means that if I want to put the x and y into the array

it would have to go into it as board[y][x] instead of board[x][y]
[
[0,0,0],  #board[0][0-2]
[0,0,0],  #board[1][0-2]
[0,0,0]   #board[2][0-2]
]
'''

clicked = []
zeros = []
cells_clicked = 0

def check_zeros(x, y, board_length, board_height):
    '''
    Checks for nearby zeros from clicked location using recursion

    :param x: integer
    :param y: integer
    :param board_length: integer
    :param board_height: integer
    :return: nothing
    '''
    for loopy in range(-1, 2):
        for loopx in range(-1, 2):
            if 0 <= y+loopy < board_height and 0 <= x + loopx < board_length:
                if board[y][x] == 0 and clicked[loopy+y][loopx+x] == 0:
                    if [y+loopy, x+loopx] not in zeros:
                        clicked[loopy+y][loopx+x] = 1
                        zeros.append([loopy+y, loopx+x])
                        check_zeros(loopx+x, loopy+y, board_length, board_height)


def create_numbers_around_bomb(x, y, board_length, board_height):
    '''
    Create the numbers around a bomb based on it's x and y position

    :param x: integer
    :param y: integer
    :param board_length: integer
    :param board_height: integer
    :return: nothing
    '''
    for loopy in range(-1, 2):
        for loopx in range(-1, 2):
            if 0 <= loopy+y < board_height and 0 <= loopx + x < board_length:
                if board[loopy+y][loopx+x] != -1:
                    board[loopy+y][loopx+x] += 1

def create_board(board_length, board_height):
    '''
    Create the board array using the board length and height

    :param board_length: integer
    :param board_height: integer
    :return: nothing
    '''
    for y in range(board_height):
        board.append([])
        clicked.append([])
        for x in range(board_length):
            board[y].append(0)
            clicked[y].append(0)

def chord(clickx, clicky, board_length, board_height):
    '''
    Checks if the position is chordable and if it is, do the correct actions like opening squares or exploding

    :param clickx: integer
    :param clicky: integer
    :param board_length: integer
    :param board_height: integer
    :return: Boolean depending on if you exploded from the chord or not
    '''
    global cells_clicked
    bombs = 0
    for loopy in range(-1, 2):
        for loopx in range(-1, 2):
            if 0 <= loopy+clicky < board_height and 0 <= loopx + clickx < board_length:
                if clicked[loopy+clicky][loopx+clickx] == -1:
                    bombs += 1
    if bombs == board[clicky][clickx]:
        for loopy in range(-1, 2):
            for loopx in range(-1, 2):
                if 0 <= loopy+clicky < board_height and 0 <= loopx + clickx < board_length:
                    if clicked[loopy+clicky][loopx+clickx] == 0:
                        if board[loopy+clicky][loopx+clickx] == 0:
                            y = loopy+clicky
                            x = loopx+clickx
                            clicked[y][x] = 1
                            zeros.clear()
                            zeros.append([[y, x]])
                            check_zeros(x, y, board_length, board_height)
                            cells_clicked += len(zeros)
                        elif board[loopy+clicky][loopx+clickx] != -1:
                            clicked[loopy+clicky][loopx+clickx] = 1
                            cells_clicked += 1
                        else:
                            clicked[loopy+clicky][loopx+clickx] = 1
                            board[loopy+clicky][loopx+clickx] = -2
                            return True
    return False


def create_mine(amount, board_length, board_height, original_x, original_y):
    '''
    Create a specified amount of mines in the board in random positions

    :param amount: integer
    :param board_length: integer
    :param board_height: integer
    :param original_x: integer
    :param original_y: integer
    :return: nothing
    '''
    for _ in range(amount):
        mine_x = random.randint(0, board_length - 1)
        mine_y = random.randint(0, board_height - 1)
        if board[mine_y][mine_x] != -1:
            if mine_x != original_x and mine_y != original_y:
                board[mine_y][mine_x] = -1
                create_numbers_around_bomb(mine_x, mine_y, board_length, board_height)
            else:
                create_mine(1, board_length, board_height, original_x, original_y)
        else:
            create_mine(1, board_length, board_height, original_x, original_y)

def main():
    # default numbers, but they change once you click on easy, med or hard
    board_x, board_y, cell_size, mines = 10, 10, 24, 10

    # basic initialization
    screen_x, screen_y = screen_size = 840, 640

    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Minesweeper")
    pygame.display.set_icon(UNOPENED_CELL)

    global cells_clicked

    loss = False
    game_over = False
    game_started = False
    running = True
    flags_left = 0
    clock = None
    ms = 0
    seconds = 0
    first_click = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running = False

        if game_over:
            text = "You won! Press the smiley face to go again or M to go to the main menu"
            if loss:
                text = "You blew up! Press the sad face to retry or M to go to the main menu"
            game_over_text = pygame.font.Font(None, 32)
            game_over_text_render = game_over_text.render(text, True, BLACK)
            screen.blit(game_over_text_render, (screen_x-11.5*len(text), 12))
            clock = None

        if game_started:
            if seconds < 999:
                if clock is not None:
                    ms += clock.tick(60)
                if ms >= 1000:
                    seconds += 1
                    ms -= 1000

            text_font = pygame.font.Font(None, 32)
            mines_text_render = text_font.render(f"{flags_left}", True, RED)
            seconds_text_render = text_font.render(f"{seconds}", True, RED)
            pygame.draw.rect(screen, GRAY, ((screen_x-board_x*cell_size)/2-20, 60, board_x*cell_size+40, board_y*cell_size+40+40))
            pygame.draw.rect(screen, BLACK, ((screen_x - board_x * cell_size) / 2, 75, 56, 32))
            pygame.draw.rect(screen, BLACK, ((screen_x - board_x * cell_size) / 2 + board_x*cell_size-56, 75, 56, 32))
            face = REGULAR_FACE
            if loss:
                face = LOSS_FACE

            face_rect = screen.blit(face, ((screen_x - board_x * cell_size)/2+(board_x*cell_size)/2-16, 75))
            if event.type == pygame.MOUSEBUTTONDOWN and face_rect.collidepoint(event.pos):
                seconds = 0
                board.clear()
                cells_clicked = 0
                clicked.clear()
                create_board(board_x, board_y)
                first_click = True
                clock = pygame.time.Clock()
                flags_left = mines
                game_over = False
                loss = False
            if event.type == pygame.KEYDOWN and event.unicode == 'm':
                game_started = False
                game_over = False
                seconds = 0

            screen.blit(seconds_text_render, ((screen_x - board_x * cell_size) / 2 + board_x*cell_size- 46, 80))
            screen.blit(mines_text_render, ((screen_x - board_x * cell_size) / 2 + 10, 80))
            for y in range(board_y):
                for x in range(board_x):
                    # Board array correspondence:
                    # -2 = Originally clicked bomb
                    # -1 = Bomb
                    # 0-8 = Number of bombs around that cell

                    # Clicked array correspondence:
                    # -2 = Incorrect flag
                    # -1 = Flag
                    # 0 = Unopened
                    # 1 = Opened
                    square = UNOPENED_CELL
                    if clicked[y][x] == -1:
                        square = FLAG
                    elif clicked[y][x] == -2:
                        square = WRONG_FLAG
                    elif clicked[y][x] == 0:
                        square = UNOPENED_CELL
                    elif clicked[y][x] == 1:
                        if board[y][x] == 0:
                            square = OPENED_CELL
                        elif board[y][x] == 1:
                            square = ONE
                        elif board[y][x] == 2:
                            square = TWO
                        elif board[y][x] == 3:
                            square = THREE
                        elif board[y][x] == 4:
                            square = FOUR
                        elif board[y][x] == 5:
                            square = FIVE
                        elif board[y][x] == 6:
                            square = SIX
                        elif board[y][x] == 7:
                            square = SEVEN
                        elif board[y][x] == 8:
                            square = EIGHT
                        elif board[y][x] == -1:
                            square = BOMB
                        elif board[y][x] == -2:
                            square = CLICKED_BOMB

                    screen.blit(square, ((screen_x - board_x * cell_size) / 2 + x * cell_size, 120 + y * cell_size))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x = math.floor((event.pos[0]- (screen_x-board_x*cell_size)/2)/cell_size)
                y = math.floor((event.pos[1] - 120)/cell_size)
                if 0 <= x < board_x and 0 <= y < board_y:
                    if not game_over:
                        if clicked[y][x] == 1 and board[y][x] != 0:
                            explode = chord(x,y, board_x, board_y)
                            if explode:
                                game_over = True
                                loss = True
                                for y2 in range(board_y):
                                    for x2 in range(board_x):
                                        if board[y2][x2] == -1 and clicked[y2][x2] != -1:
                                            clicked[y2][x2] = 1
                                        if board[y2][x2] != -1 and clicked[y2][x2] == -1:
                                            clicked[y2][x2] = -2

                        if clicked[y][x] == 0: # if cell has not been opened
                            if first_click: # if it's the first click of the game
                                create_mine(mines, board_x, board_y, x, y) # generate the mines
                                first_click = False
                            if board[y][x] == 0:
                                clicked[y][x] = 1
                                zeros.clear()
                                zeros.append([[y, x]])
                                check_zeros(x,y, board_x, board_y)
                                cells_clicked += len(zeros)
                                zeros.clear()
                            elif board[y][x] != -1:
                                clicked[y][x] = 1
                                cells_clicked += 1
                            elif board[y][x] == -1:
                                board[y][x] = -2
                                for y2 in range(board_y):
                                    for x2 in range(board_x):
                                        if board[y2][x2] == -1 and clicked[y2][x2] != -1:
                                            clicked[y2][x2] = 1
                                        if board[y2][x2] != -1 and clicked[y2][x2] == -1:
                                            clicked[y2][x2] = -2
                                clicked[y][x] = 1
                                game_over = True
                                loss = True
                        if cells_clicked >= board_x*board_y-mines:
                            for y2 in range(board_y):
                                for x2 in range(board_x):
                                    if board[y2][x2] == -1:
                                        clicked[y2][x2] = -1
                            game_over = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                x = math.floor((event.pos[0] - (screen_x - board_x * cell_size) / 2) / cell_size)
                y = math.floor((event.pos[1] - 120) / cell_size)
                if 0 <= x < board_x and 0 <= y < board_y:
                    if clicked[y][x] == 0:
                        clicked[y][x] = -1
                        flags_left -= 1
                    elif clicked[y][x] == -1:
                        clicked[y][x] = 0
                        flags_left += 1

        else:
            title_font = pygame.font.Font(None, 48)
            regular_font = pygame.font.Font(None, 32)
            title = title_font.render("Minesweeper", True, BLACK)
            subtitle = regular_font.render("Select a difficulty to begin", True, BLACK)
            screen.blit(title, (screen_x/2-100, 100))
            screen.blit(subtitle, (screen_x/2-125, 200))

            pygame.draw.rect(screen, (0, 200, 0), (105, 285, 100, 100))
            easy_box = pygame.draw.rect(screen, (0,255,0), (100,280, 100, 100))
            easy_text_render = regular_font.render("Easy", True, BLACK)
            screen.blit(easy_text_render, (easy_box.x+25, easy_box.y+35))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if easy_box.collidepoint(event.pos):
                    board_x, board_y, mines = 10, 10, 10
                    cells_clicked = 0
                    board.clear()
                    clicked.clear()
                    first_click = True
                    create_board(board_x, board_y)
                    clock = pygame.time.Clock()
                    game_started = True

            pygame.draw.rect(screen, (200, 200, 0), (screen_x/2-45, 285, 100, 100))
            med_box = pygame.draw.rect(screen, (255, 255, 0), (screen_x/2-50, 280, 100, 100))
            med_text_render = regular_font.render("Medium", True, BLACK)
            screen.blit(med_text_render, (med_box.x+10, med_box.y + 35))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if med_box.collidepoint(event.pos):
                    board_x, board_y, mines = 16, 16, 40
                    board.clear()
                    cells_clicked = 0
                    clicked.clear()
                    create_board(board_x, board_y)
                    first_click = True
                    clock = pygame.time.Clock()
                    game_started = True

            pygame.draw.rect(screen, (200, 0, 0), (screen_x-195, 285, 100, 100))
            hard_box = pygame.draw.rect(screen, (255, 0, 0), (screen_x-200, 280, 100, 100))
            hard_text_render = regular_font.render("Hard", True, BLACK)
            screen.blit(hard_text_render, (hard_box.x + 25, hard_box.y + 35))
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if hard_box.collidepoint(event.pos):
                    board_x, board_y, mines = 24, 16, 60
                    board.clear()
                    cells_clicked = 0
                    clicked.clear()
                    create_board(board_x, board_y)
                    first_click = True
                    clock = pygame.time.Clock()
                    game_started = True
            flags_left = mines
        pygame.display.update()


if __name__ == "__main__":
    main()