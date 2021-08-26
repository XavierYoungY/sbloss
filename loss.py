import numpy as np
import cv2
import random
from math import cos, sin, pi
import matplotlib.pyplot as plt
colors = [[131, 204, 205], [174, 116, 200], [210, 200, 111], [190, 53, 46]]


def randomcolor():
    color = []
    for i in range(3):
        color.append(random.randint(0, 255))
    return color


def l2(box1, box2):
    # xmin ymin xmax ymax
    box = box1 - box2
    sum_ = 0
    for i in box:
        sum_ += i**2
    return (sum_ / 4)**0.5


def iou_loss(box1, box2):
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
    left_up = np.maximum(box1[:2], box2[:2])
    right_down = np.minimum(box1[2:], box2[2:])
    inter_section = np.maximum(right_down - left_up, 0.0)
    inter_area = inter_section[0] * inter_section[1]
    union_area = box1_area + box2_area - inter_area
    iou = 1.0 * inter_area / union_area

    return 1 - iou


def giou(box1, box2):
    box1_area = np.abs((box1[2] - box1[0]) * (box1[3] - box1[1]))
    box2_area = np.abs((box2[2] - box2[0]) * (box2[3] - box2[1]))

    left_up = np.maximum(box1[:2], box2[:2])
    right_down = np.minimum(box1[2:], box2[2:])

    inter_section = np.maximum(right_down - left_up, 0.0)
    inter_area = inter_section[0] * inter_section[1]
    union_area = box1_area + box2_area - inter_area
    iou = inter_area / union_area

    enclose_left_up = np.minimum(box1[:2], box2[:2])
    enclose_right_down = np.maximum(box1[2:], box2[2:])
    enclose = np.maximum(enclose_right_down - enclose_left_up, 0.0)
    enclose_area = enclose[0] * enclose[1]
    giou = iou - 1.0 * (enclose_area - union_area) / enclose_area

    return 1 - giou


def SB(box1, box2):

    diagonal = box1 - box2
    diagonal = diagonal * diagonal
    # 对角距离平方和

    diagonal_diatance = 0
    for i in range(4):
        diagonal_diatance += diagonal[i]

    # 相交区域
    left_up = np.maximum(box1[:2], box2[:2])
    right_down = np.minimum(box1[2:], box2[2:])

    inter_section = np.maximum(right_down - left_up, 0.0)
    inter_area = inter_section[0] * inter_section[1]
    inter_section = inter_section * inter_section
    # 相交区域对角距离一半平方 不相交=-1*
    inter_section_distance = (inter_section[0] + inter_section[1]) / 4

    if inter_area <= 0:
        inter_section_distance = -1 * (inter_section_distance)

    # 外接矩形对角线一半的平方
    enclose_left_up = np.minimum(box1[:2], box2[:2])
    enclose_right_down = np.maximum(box1[2:], box2[2:])
    enclose = np.maximum(enclose_right_down - enclose_left_up, 0.0)

    enclose = enclose * enclose
    enclose_distance = (enclose[0] + enclose[1]) / 4
    if enclose_distance <= 0:
        enclose_distance = minimum_num

    SB = (diagonal_diatance * 2 -
           inter_section_distance) / enclose_distance + 1

    return SB


def stairs(begin, stairh, stepsize, stpnum):

    stairs_list = []
    for i in range(stpnum):
        tmp_x = begin[0] - i * stairh
        tmp_y = begin[1] - i * stairh
        for x in range(tmp_x, (tmp_x - stairh), -stepsize):
            stairs_list.append([x, tmp_y])
        for y in range(tmp_y, (tmp_y - stairh), -stepsize):
            stairs_list.append([tmp_x - stairh, y])
        if i == stpnum - 1:
            tmp_x = begin[0] - stpnum * stairh
            for x in range(tmp_x, (tmp_x - stairh), -stepsize):
                stairs_list.append([x, 0])
    for i in range(len(stairs_list)):

        stairs_list[i][0] += stairh // 2
        if stairs_list[i][0] < 0 or stairs_list[i][0] > begin[0]:
            stairs_list[i] = []
        else:
            stairs_list[i] = tuple(stairs_list[i])
    while [] in stairs_list:
        stairs_list.remove([])

    img = np.zeros((1000, 1000, 3), np.uint8)

    point_size = 1
    color = randomcolor()
    thickness = 0

    for point in stairs_list:
        cv2.circle(img, point, point_size, color, thickness)

    return img, stairs_list


def scatter_show(ratios, i, label):
    x = range(len(ratios))
    color = RGB_to_Hex(colors[i])
    # plt.scatter(x, ratios, s=1, c=color, marker='o', alpha=0.5)
    plt.plot(x, ratios, color=color, label=label)


def RGB_to_Hex(RGB):
    color = '#'
    for num in RGB:
        # 将R、G、B分别转化为16进制拼接转换并大写  hex() 函数用于将10进制整数转换成16进制，以字符串形式表示
        color += str(hex(num))[-2:].replace('x', '0').upper()
    return color
