import sys
from datetime import datetime
from fill_sudoku import fill_sudoku


def read_input():
    # reads input from a file and stores it in a frame
    file_name = sys.argv[1]
    f = open(file_name, "r")
    num = len(f.readlines())
    f.seek(0)
    sudoku_frame = [[0 for x in range(num)] for x in range(num)]
    for iter1, x in enumerate(f.readlines()):
        for iter2, y in enumerate([z for z in x.split()]):
            sudoku_frame[iter1][iter2] = int(y)
    return sudoku_frame


def extract_num(name):
    nums = [int(x) for x in name if x.isdigit()]
    num = 0
    for x in nums:
        num = num * 10 + x
    return str(num)


def write_output(sudoku):
    inp_file = sys.argv[1]
    num = extract_num(inp_file)
    out_file = "C:\\Users\\USER\\PycharmProjects\\Sudoku\\result\\result"+num+".txt"
    f = open(out_file, "w")
    for x in sudoku:
        for y in x:
            f.write(str(y)+" ")
        f.write("\n")
    f.close()
    # write to file


def solve_sudoku():
    start_time = datetime.now()
    inp_sudoku = read_input()   # read input from file
    res_sudoku = fill_sudoku(inp_sudoku)    # fills sudoku using backtracking
    write_output(res_sudoku)    # write into an output file
    end_time = datetime.now()
    print("Time Taken = ", (end_time - start_time))


if __name__ == "__main__":
    # execute only if run as a script
    solve_sudoku()
