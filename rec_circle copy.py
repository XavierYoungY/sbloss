import numpy as np
import cv2
import random
from math import cos, sin, pi
import matplotlib.pyplot as plt
import loss

def get_r_point(x0, y0, r):
    _ = []
    angles = np.arange(0.0, 2 * pi, 0.1) - pi
    for angle in angles:
        x1 = x0 + r * cos(angle)
        y1 = y0 + r * sin(angle)
        _.append([x1, y1])

    return _


def randomcolor():
    color = []
    for i in range(3):
        color.append(random.randint(0, 255))
    return color


def int_(a):
    _ = []
    for i in a:
        _.append(int(i))
    return tuple(_)


def draw_rec(img, x, y, w, h, color):
    # cv2.rectangle(img, pt1, pt2, color[, thickness[, lineType[, shift]]])
    c1 = int_([x - w / 2, y - h / 2])
    c2 = int_([x + w / 2, y + h / 2])

    cv2.rectangle(img, c1, c2, color, 2)
    return img


def find_extreme_points(A, B):
    x = []
    y = []
    for a in A:
        x.append(a[0])
        y.append(a[1])
    for b in B:
        y.append(b[1])
        x.append(b[0])
    xmin, ymin, xmax, ymax = min(x), min(y), max(x), max(y)
    c1 = np.array((xmin, ymin), dtype=int)
    c2 = np.array((xmax, ymax), dtype=int)
    return c1, c2


def draw_r(img, x1, y1, w1, h1, x2, y2, w2, h2, color):
    a1 = int_([x1 - w1 / 2, y1 - h1 / 2])
    a2 = int_([x1 + w1 / 2, y1 + h1 / 2])
    a3 = int_([x1 + w1 / 2, y1 - h1 / 2])
    a4 = int_([x1 - w1 / 2, y1 + h1 / 2])
    A = [a1, a2, a3, a4]

    b1 = int_([x2 - w2 / 2, y2 - h2 / 2])
    b2 = int_([x2 + w2 / 2, y2 + h2 / 2])
    b3 = int_([x2 + w2 / 2, y2 - h2 / 2])
    b4 = int_([x2 - w2 / 2, y2 + h2 / 2])
    B = [b1, b2, b3, b4]
    s = []
    # max_r
    for i in range(4):
        a = np.array(A[i], dtype=int)
        b = np.array(B[i], dtype=int)
        r = np.sqrt(np.sum(np.square(a - b)))

        cv2.circle(img, A[i], int(r), color[i + 2], 2)
        cv2.circle(img, A[i], 5, color[i + 2], -1)
        s.append(np.square(r))
    c1, c2 = find_extreme_points(A, B)

    r = np.sqrt(np.sum(np.square(c1 - c2))) / 2

    c = int_((c1 + c2) / 2)
    cv2.circle(img, c, int(r), color[6], 2)
    cv2.circle(img, c, 5, color[6], -1)
    s.append(np.square(r))

    sum = 0
    for i in range(3):
        sum += (s[i])
    inter_r = np.square(get_inter_r(x1, y1, w1, h1, x2, y2, w2, h2))

    ratio = round((sum - inter_r) / (s[4]) , 3)


    # print(ratio)
    # print(s)
    font = cv2.FONT_HERSHEY_SIMPLEX
    imgzi = cv2.putText(img, str(ratio), (50, 50), font, 1.2, (255, 255, 255),
                        2)
    return ratio


def get_inter_r(x1, y1, w1, h1, x2, y2, w2, h2):
    box1 = [x1, y1, w1, h1]
    box2 = [x2, y2, w2, h2]
    box1 = np.array(box1, dtype=float)
    box1 = np.append(box1[:2] - box1[2:] * 0.5, box1[:2] + box1[2:] * 0.5)
    box1 = np.append(np.minimum(box1[:2], box1[2:]),
                     np.maximum(box1[:2], box1[2:]))

    box2 = np.array(box2, dtype=float)
    # xmin ymin xmax ymax

    box2 = np.append(box2[:2] - box2[2:] * 0.5,
                        box2[:2] + box2[2:] * 0.5)

    box2 = np.append(np.minimum(box2[:2], box2[2:]),
                        np.maximum(box2[:2], box2[2:]))
    left_up = np.maximum(box1[:2], box2[:2])
    right_down = np.minimum(box1[2:], box2[2:])
    inter_section = np.maximum(right_down - left_up, 0.0)
    inter_area = inter_section[..., 0] * inter_section[..., 1]
    if inter_area == 0.0:
        inter_r = 0
    else:
        inter_r = np.sqrt(np.sum(np.square(left_up - right_down))) / 2
    print(inter_r)

    return inter_r


def test1(color):
    # Create a black image
    l = 1100

    x1 = l // 2
    y1 = l // 2
    w1 = 200
    h1 = 300

    x2 = x1 + 1100
    y2 = y1 + 1300
    w2 = 250
    h2 = 200

    wait_time = 5
    break_flag = True
    ratio = []
    while (break_flag):

        if x2 > x1:
            x2 -= 1
        if y2 > y1:
            y2 -= 1
        if (x2 == x1 and y2 == y1):
            if w2 > w1:
                w2 -= 1
            if w2 < w1:
                w2 += 1

            if h2 > h1:
                h2 -= 1
            if h2 < h1:
                h2 += 1
            if w2 == w1 and h2 == h1:
                break_flag = False
                wait_time = 2000
        img = np.zeros((l, l, 3), np.uint8)
        draw_rec(img, x1, y1, w1, h1, color[0])
        draw_rec(img, x2, y2, w2, h2, color[1])
        # 画圆，圆心为：(160, 160)，半径为：60，颜色为：point_color，实心线

        ratio.append((draw_r(img, x1, y1, w1, h1, x2, y2, w2, h2, color)))

        cv2.imshow('', img)
        cv2.waitKey(wait_time)


def draw_rec2(img, x1, y1, x2, y2, color):
    x = int((x1 + x2) / 2)
    y = int((y1 + y2) / 2)
    w = abs(x1 - x2)
    h = abs(y1 - y2)
    img = draw_rec(img, x, y, w, h, color)
    return img


    # ratio = (r1 + r2) / r
def get_r(a, b):
    a = np.array(a, dtype=int)
    b = np.array(b, dtype=int)
    return np.sqrt(np.sum(np.square(a - b)))


def get_extreme_point(a, b, l_or_r):
    _ = []
    if l_or_r == 'r':
        _.append(max(a[0], b[0]))
        _.append(min(a[1], b[1]))
    else:
        _.append(min(a[0], b[0]))
        _.append(max(a[1], b[1]))
    _ = np.array(_, dtype=int)
    return _



def test3(color):

    l = 1100
    wait_time = 500
    c0 = l // 2 - 100
    r0 = 200
    b1_r_t = [c0, c0]
    b1_l_d = [c0 - 300, c0 + 400]
    b2_r_ts = get_r_point(c0, c0, r0)
    b2_l_d = [c0 - 310, c0 + 410]

    box1 = [c0 - 150, c0 + 200, 150, 200]
    box1 = np.array(box1, dtype=float)
    box1 = np.append(box1[:2] - box1[2:] * 0.5,
                                box1[:2] + box1[2:] * 0.5)
    box1 = np.append(np.minimum(box1[:2], box1[2:]),
                             np.maximum(box1[:2], box1[2:]))

    r1 = r0
    r2 = get_r(b1_l_d, b2_l_d)
    tmp_ratio = 0
    ratios=[]
    while (True and tmp_ratio==0):
        for b2_r_t in b2_r_ts:
            img = np.zeros((l, l, 3), np.uint8)
            cv2.circle(img, (c0, c0), r0, color[0], 2)
            img = draw_rec2(img, b1_r_t[0], b1_r_t[1], b1_l_d[0], b1_l_d[1],
                            color[1])
            img = draw_rec2(img, b2_r_t[0], b2_r_t[1], b2_l_d[0], b2_l_d[1],
                            color[2])

            top_right = get_extreme_point(b1_r_t, b2_r_t, 'r')
            b_left = get_extreme_point(b1_l_d, b2_l_d, 'l')
            c = int_((b_left[:] + top_right[:]) / 2)
            r = np.sqrt(np.sum(np.square(top_right - b_left))) / 2

            box2 = [(b2_l_d[0] + b2_r_t[0]) / 2, (b2_l_d[1] + b2_r_t[1]) / 2,
                    b2_r_t[0] - b2_l_d[0], b2_l_d[1] - b2_r_t[1]]


            box2 = np.array(box2, dtype=float)
            # xmin ymin xmax ymax

            box2 = np.append(box2[:2] - box2[2:] * 0.5,
                             box2[:2] + box2[2:] * 0.5)

            box2 = np.append(np.minimum(box2[:2], box2[2:]),
                             np.maximum(box2[:2], box2[2:]))
            ratio = loss.bbd(box1, box2)
            ratio = round(ratio, 3)
            if tmp_ratio != 0:
                if ratio > tmp_ratio:
                    text = str(ratio) + ': UP '
                else:
                    text = str(ratio) + ': DOWN '
            else:
                text = str(ratio)

            # print(ratio)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, text, (50, 50), font, 1.2,
                                (255, 255, 255), 2)

            cv2.imshow('', img)
            cv2.waitKey(wait_time)
            tmp_ratio = ratio
            ratios.append(ratio)
    x = range(len(ratios))

    plt.scatter(x, ratios, s=50, c='r', marker='o', alpha=0.5)
    plt.show()
    return ratios


if __name__ == '__main__':
    color = []
    colors = [[226, 90, 83], [253, 179, 93], [251, 245, 232], [164, 217, 214],
             [43, 146, 228], [248, 181, 193], [217, 113, 111], [141, 160, 119],
             [212, 128, 92], [245, 109, 145]]

    for i in colors:
        color.append([i[2],i[1],i[0]])
    # for i in range(10):
    #     color.append(randomcolor())
    # test1(color)

    ratios=test3(color)
