import numpy as np
import cv2
import random
from math import cos, sin, pi
import matplotlib.pyplot as plt
import area_maze as loss


def get_r_point(x0, y0, r):
    _ = []
    angles = np.arange(0.0, 2 * pi, 0.1)
    for angle in angles:
        x1 = x0 + r * cos(angle)
        y1 = y0 + r * sin(angle)
        _.append([x1, y1])
        print((x1-x0)**2+(y1-y0)**2)

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

    ratio = round((sum - inter_r) / (s[4]), 3)

    # print(ratio)
    # print(s)
    font = cv2.FONT_HERSHEY_SIMPLEX
    imgzi = cv2.putText(img, str(ratio), (50, 50), font, 1.2, (255, 255, 255),
                        2)
    return ratio





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

def trap(color):
    l = 1100
    wait_time = 50
    c0 = l // 2 - 100
    r0 = 200
    b1_l_t = [c0, c0]
    b1_r_d = [c0 + 300, c0 + 400]
    b2_l_ts = get_r_point(c0, c0, r0)
    b2_r_d = [c0 + 310, c0 + 410]
    box1=[c0,c0,c0+150,c0+200]
    box1 = np.array(box1, dtype=float)
    tmp_ratio = 0
    ratios = []
    l2_losses = []
    while (True and tmp_ratio == 0):
        for b2_l_t in b2_l_ts:
            b2_l_t = list(map(int, b2_l_t))
            img = np.zeros((l, l, 3), np.uint8)
            cv2.circle(img, (c0, c0), r0, color[0], 2)
            img = cv2.rectangle(img, tuple(b1_l_t), tuple(b1_r_d), color[1],2)
            img = cv2.rectangle(img, tuple(b2_l_t), tuple(b2_r_d), color[2], 2)

            box2 = b2_l_t+(b2_r_d)
            box2 = np.array(box2, dtype=float)
            ratio = loss.bbd(box1, box2)
            ratio = round(ratio, 3)
            l2 = loss.l2(box1, box2)
            l2 = round(l2 / 10000, 0) - 0.03
            if tmp_ratio != 0:
                if ratio > tmp_ratio:
                    text = str(ratio) + ': UP '
                else:
                    text = str(ratio) + ': DOWN '
            else:
                text = str(ratio)

            # print(ratio)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, text, (50, 50), font, 1.2, (255, 255, 255), 2)

            # cv2.imshow('', img)
            # cv2.waitKey(wait_time)
            tmp_ratio = ratio
            ratios.append(ratio)
            l2_losses.append(l2)
    ratios=ratios[::2]
    l2_losses = l2_losses[::2]
    x = range(len(ratios))
    plt.plot(x, ratios, color='#BD332B')
    plt.scatter(x,
                ratios,
                s=20,
                c='#761F1A',
                marker='o',
                alpha=0.5,
                label='SB Loss')
    plt.plot(x, l2_losses, color='#7ECACB')
    co='\\times{10}^{-4}'
    coe = 'L2 Loss'+'$%s$'%co
    plt.scatter(x,
                l2_losses,
                s=20,
                c='#4F7E7F',
                marker='d',
                alpha=0.5,
                label=coe)
    names=[]
    for i in x:
        if i%2==0:
            names.append('')
        else:
            names.append(str(i+1))

    for doty in np.arange(2.75, 4.5, 0.5):
        dotx=[0,33]
        plt.plot(dotx, [doty, doty],
                 color='#C3C3C3',
                 linestyle='--',
                 linewidth=0.9)
    plt.xlim(-0.2, 32.2)
    # # plt.ylim(0, 4.7)
    plt.legend(loc='upper right', bbox_to_anchor=(0.8, 0.97), fontsize=14)
    plt.xticks(x, names, fontsize=8, ha="center")
    font2 = {
        'family': 'Times New Roman',
        'weight': 'normal',
        'size': 14,
    }
    plt.xlabel('Steps', font2)
    plt.ylabel('Loss', font2)
    plt.savefig('symmetric_trap.pdf', dpi=600, format='pdf')
    plt.show()
    return ratios



if __name__ == '__main__':
    color = []
    colors = [[226, 90, 83], [253, 179, 93], [251, 245, 232], [164, 217, 214],
              [43, 146, 228], [248, 181, 193], [217, 113, 111],
              [141, 160, 119], [212, 128, 92], [245, 109, 145]]

    for i in colors:
        color.append([i[2], i[1], i[0]])
    # for i in range(10):
    #     color.append(randomcolor())
    # test1(color)

    ratios = trap(color)
