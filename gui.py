import sys
import sudoku_solver
import pygame
from main import finder

pygame.init()
size = (480, 500)
black = (0, 0, 0)
white = (255, 255, 255)
display = pygame.display.set_mode(size)
pygame.display.set_caption('Sudoku')
sudoku = sudoku_solver.Sudoku(finder().get())


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
                text_rect.center = (j*50+25+15, i*50+25+20)
                display.blit(text, text_rect)


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        pygame.display.flip()
        display.fill(white)
        draw()
