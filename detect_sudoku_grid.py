import cv2


def detect_sudoku_grid():
    video = cv2.VideoCapture(0)
    while True:
        frame = []
        ret, frm = video.read()
        frame.append(frm)
        frame.append(cv2.flip(frame[-1], 1))
        frame.append(cv2.cvtColor(frame[-1], cv2.COLOR_BGR2GRAY))
        frame.append(cv2.GaussianBlur(frame[-1], (5, 5), 0))
        frame.append(cv2.adaptiveThreshold(frame[-1], 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 11, 2))
        for iter, x in enumerate(frame[1:]):
            cv2.imshow("Display" + str(iter), x)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    pass


if __name__ == "__main__":
    # execute only if run as a script
    detect_sudoku_grid()
