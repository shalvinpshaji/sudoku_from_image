import sys
import sudoku_solver
import pygame
from rewritten import Finder
from tkinter import filedialog, Tk
root = Tk()
root.withdraw()

selected = False
solved = False
opened = False


def open_screen():
    display.fill(white)
    pygame.draw.rect(display, black, ((190, 270), (100, 60)), 2)
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render('Open', True, black, white)
    text_rect = text.get_rect()
    text_rect.center = (240, 300)
    display.blit(text, text_rect)


def draw():
    # horizontal lines
    for i in range(10):
        thickness = 4
        if i % 3 == 0:
            thickness = 6
        pygame.draw.line(display, black, (15, i * 50 + 20), (465, i * 50 + 20), thickness)
    # vertical lines
    for i in range(10):
        thickness = 4
        if i % 3 == 0:
            thickness = 6
        pygame.draw.line(display, black, (i * 50 + 15, 20), (i * 50 + 15, 470), thickness)

    for i in range(9):
        for j in range(9):
            if sudoku.board[i][j]:
                font = pygame.font.Font('freesansbold.ttf', 32)
                text = font.render(str(sudoku.board[i][j]), True, black, white)
                text_rect = text.get_rect()
                text_rect.center = (j * 50 + 25 + 15, i * 50 + 25 + 20)
                display.blit(text, text_rect)
    if selected:
        pygame.draw.rect(display, green, ((col * 50 + 15, row * 50 + 20), (50, 50)), 5)

    # solve button
    pygame.draw.rect(display, color_light, ((15, 500), (95, 60)), 0)
    solve_text = font.render('Solve', True, black, color_light)
    solve_rect = solve_text.get_rect()
    solve_rect.center = (60, 530)
    display.blit(solve_text, solve_rect)


pygame.init()
size = (480, 600)
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
color_light = (150, 150, 150)
display = pygame.display.set_mode(size)
pygame.display.set_caption('Sudoku')

while True:
    if opened:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            mouse = pygame.mouse.get_pos()
            if 15 < mouse[0] < 110 and 500 < mouse[1] < 560:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    selected = False
                    sudoku.solve()
                    solved = True
                    print('Solving')
            if 15 < mouse[0] < 465 and 20 < mouse[1] < 470:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        row = (mouse[1] - 20) // 50
                        col = (mouse[0] - 15) // 50
                        selected = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    sudoku.board[row][col] = 1
                elif event.key == pygame.K_2:
                    sudoku.board[row][col] = 2
                elif event.key == pygame.K_3:
                    sudoku.board[row][col] = 3
                elif event.key == pygame.K_4:
                    sudoku.board[row][col] = 4
                elif event.key == pygame.K_5:
                    sudoku.board[row][col] = 5
                elif event.key == pygame.K_6:
                    sudoku.board[row][col] = 6
                elif event.key == pygame.K_7:
                    sudoku.board[row][col] = 7
                elif event.key == pygame.K_8:
                    sudoku.board[row][col] = 8
                elif event.key == pygame.K_9:
                    sudoku.board[row][col] = 9
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    sudoku.board[row][col] = 0

            pygame.display.flip()
            display.fill(white)
            draw()
    else:
        open_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            mouse = pygame.mouse.get_pos()
            if 190 < mouse[0] < 290 and 270 < mouse[1] < 330:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == pygame.BUTTON_LEFT:
                        file = filedialog.askopenfilename(initialdir='C:', title='Select sudoku image',
                                                          filetypes=[('png', '.png'), ('jpeg', '.jpeg'),
                                                                     ('jpg', '.jpg')])
                        if file:
                            sudoku = sudoku_solver.Sudoku(Finder().get_board(path=file))
                            opened = True
        pygame.display.flip()
        display.fill(white)
