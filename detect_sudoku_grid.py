import cv2
import numpy as np


def order_points(pts):
    pts = pts.reshape(4, 2)
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect


def four_points_transform(image, rect):
    (tl, tr, br, bl) = rect
    widthBottom = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthTop = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(widthBottom, widthTop)
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], dtype='float32')
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (int(maxWidth), int(maxHeight)))
    return warped


def detect_sudoku_grid():
    video = cv2.VideoCapture(0)
    while True:
        frame = []
        ret, frm = video.read()
        frame.append(frm)  # 0
        w, h = frame[-1].shape[0], frame[-1].shape[1]
        # frame.append(cv2.flip(frame[-1], 1))  # 1
        frame.append(cv2.cvtColor(frame[-1], cv2.COLOR_BGR2GRAY))  # 2
        frame.append(cv2.GaussianBlur(frame[-1], (5, 5), 0))  # 3
        frame.append(cv2.Canny(frame[-1], 50, 200, apertureSize=3))  # 4
        frame.append(
            cv2.adaptiveThreshold(frame[-1], 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 3, 2))  # 5
        minLineLength = 250
        maxLineGap = 10
        lines = cv2.HoughLinesP(frame[-1], 1, np.pi / 180, 50, minLineLength, maxLineGap)
        frame.append(cv2.cvtColor(frame[-1], cv2.COLOR_GRAY2BGR))  # 6
        if lines is not None:
            for x1, y1, x2, y2 in lines[:, 0]:
                cv2.line(frame[-1], (x1, y1), (x2, y2), (0, 255, 0), 2)
        frame.append(cv2.cvtColor(frame[-1], cv2.COLOR_BGR2GRAY))  # 7
        # cv2.rectangle(frame[-1], (x, y), (w - 1, h - 1), (255, 255, 255), 16)
        contours, hierarchy = cv2.findContours(frame[-3], cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        largest = None
        approx = None
        for cnt in contours:
            epsilon = 0.01 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            if len(approx) == 4:
                largest = cnt
                break
        frame.append(cv2.drawContours(frame[-3], [approx], -1, (255, 255, 255), 16))  # 8
        rect = order_points(approx)
        frame.append(four_points_transform(frame[-1], rect))
        for iter, x in enumerate(frame[-3:]):
            if x is not None:
                cv2.imshow("Display" + str(iter), x)
        # cv2.imshow("Display", frame[-1])
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    pass


if __name__ == "__main__":
    # execute only if run as a script
    detect_sudoku_grid()
