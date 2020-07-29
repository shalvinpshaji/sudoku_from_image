class Sudoku:

    def __init__(self, board):
        self.board = board

    def set_board(self, board):
        self.board = board

    def print_board(self):
        for i in range(9):
            if i % 3 == 0:
                print('-----------------------------')
            for j in range(9):
                if j%3==0:
                    print(' | ', end='')
                print(str(self.board[i][j]), end=' ')
            print('| ')
        print('-----------------------------')

    def is_valid(self, num, pos) -> bool:
        row, col = pos
        for i in range(9):
            if self.board[row][i] == num:
                # print('Row ', end='')
                return False
        for i in range(9):
            if self.board[i][col] == num:
                # print('Column ', end='')
                return False
        box_col = col // 3
        box_row = row // 3
        for i in range(3):
            for j in range(3):
                if self.board[box_row * 3 + i][box_col * 3 + j] == num:
                    # print('box ', end='')
                    return False
        return True

    def find_empty(self):
        num = 0
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    num = 1
                    return [i, j, num]
        return [-1, -1, num]

    def solve(self):
        empty = self.find_empty()
        if not empty[2]:
            return True
        row, column = empty[0], empty[1]
        for i in range(1, 10):
            if self.is_valid(i, (row, column)):
                self.board[row][column] = i
                if self.solve():
                    return True
                self.board[row][column] = 0
        return False


if __name__ == '__main__':
    board = [[0, 0, 0, 0, 0, 0, 0, 2, 8],
             [0, 6, 0, 0, 0, 0, 0, 0, 7],
             [0, 0, 0, 4, 0, 1, 0, 0, 0],
             [5, 0, 0, 9, 7, 0, 3, 0, 0],
             [2, 0, 4, 0, 0, 8, 0, 0, 0],
             [3, 0, 0, 0, 0, 4, 5, 0, 0],
             [1, 3, 0, 0, 9, 0, 0, 0, 0],
             [0, 5, 7, 0, 0, 0, 0, 9, 0],
             [0, 0, 8, 3, 1, 7, 0, 0, 0]]

    sud = Sudoku(board)
    sud.solve()
    sud.print_board()