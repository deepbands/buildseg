import cv2


def open_and_close_op(img, ksize=3, iter=3):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=iter)  # open
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=iter)  # close
    return img


def del_samll_area(img, limit=64):
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area < limit:
            cv2.drawContours(img, [contours[i]], 0, 0, -1)
    return img


def bound_smooth(img, ksize=5):
    img = cv2.medianBlur(img, ksize)
    return img