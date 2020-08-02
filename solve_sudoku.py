import sys
from datetime import datetime


def read_input():
    # reads input from a file and stores it in a frame
    file_name = sys.argv[1]
    f = open(file_name, "r")
    num = len(f.readlines())
    # print(num)
    # f.close()
    # f = open(file_name, "r")
    f.seek(0)
    sudoku_frame = [[0 for x in range(num)] for x in range(num)]
    for iter1, x in enumerate(f.readlines()):
        for iter2, y in enumerate([z for z in x.split()]):
            sudoku_frame[iter1][iter2] = int(y)
    # print(sudoku_frame)
    return sudoku_frame


def write_output(sudoku):
    f = open(sys.argv[2], "w")
    for x in sudoku:
        for y in x:
            f.write(str(y)+" ")
        f.write("\n")
    f.close()
    # write to file


def solve_sudoku():
    start_time = datetime.now()
    inp_sudoku = read_input()
    # print(inp_sudoku)
    from fill_sudoku import fill_sudoku
    res_sudoku = fill_sudoku(inp_sudoku)
    write_output(res_sudoku)
    end_time = datetime.now()
    print("Time Taken = ", (end_time - start_time))


if __name__ == "__main__":
    # execute only if run as a script
    solve_sudoku()
