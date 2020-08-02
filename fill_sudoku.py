import math
import time


def print_sudoku(inp_sudoku):
    for row in inp_sudoku:
        for col in row:
            print(col, end=" ")
        print()
    pass


def perm_frame_flag(inp_sudoku):
    ln = len(inp_sudoku)
    perm_frame = [[0 for x in range(ln)] for x in range(ln)]
    for iter1, x in enumerate(inp_sudoku):
        for iter2, y in enumerate(x):
            if y != 0:
                perm_frame[iter1][iter2] = 1
    return perm_frame, ln


def find_next_empty(perm_frame, ln, row, col):
    for y in range(col, ln):
        if perm_frame[row][y] == 0:
            return row, y
    for x in range(row + 1, ln):
        for y in range(0, ln):
            # print(x, y)
            if perm_frame[x][y] == 0:
                return x, y
    return row+1, 0


def check_safe(inp_sudoku, ln, number, row, col):
    for x in range(ln):
        if inp_sudoku[row][x] == number:
            return False
    for x in range(ln):
        if inp_sudoku[x][col] == number:
            return False
    size = int(math.sqrt(ln))
    start_row_ind = (row // size) * size
    end_row_ind = start_row_ind + size
    start_col_ind = (col // size) * size
    end_col_ind = start_col_ind + size
    for x in range(start_row_ind, end_row_ind):
        for y in range(start_col_ind, end_col_ind):
            if inp_sudoku[x][y] == number:
                return False
    return True


def backtrack_fill_sudoku(inp_sudoku, perm_frame, ln, number, row, col):
    rown = coln = -1
    if number > ln:
        return False
    elif row >= ln:
        return True
    elif col >= ln:
        col = 0
        row += 1
        row, col = find_next_empty(perm_frame, ln, row, col)
    if perm_frame[row][col] == 1:
        col += 1
        row, col = find_next_empty(perm_frame, ln, row, col)
    elif not check_safe(inp_sudoku, ln, number, row, col):
        return False
    else:
        if perm_frame[row][col] != 1:
            inp_sudoku[row][col] = number
            rown = row
            coln = col
            col += 1
            row, col = find_next_empty(perm_frame, ln, row, col)
    for num in range(1, ln + 1):
        if backtrack_fill_sudoku(inp_sudoku, perm_frame, ln, num, row, col):
            return True
    else:
        if 0 <= coln < ln and perm_frame[rown][coln] == 0:
            inp_sudoku[rown][coln] = 0
    return False


def backtrack_fill_sudoku_util(inp_sudoku, perm_frame, ln):
    row, col = find_next_empty(perm_frame, ln, 0, 0)
    for num in range(1, ln + 1):
        if backtrack_fill_sudoku(inp_sudoku, perm_frame, ln, num, row, col):
            return True
    return False


def fill_sudoku(inp_sudoku):
    # logic
    perm_frame, ln = perm_frame_flag(inp_sudoku)
    # print_sudoku(perm_frame)
    if not backtrack_fill_sudoku_util(inp_sudoku, perm_frame, ln):
        print("Cannot Complete")
    else:
        print_sudoku(inp_sudoku)
    return inp_sudoku


if __name__ == "__main__":
    # execute only if run as a script
    fill_sudoku()
