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
    return sum_ / 4


def iou(box1, box2):
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
    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])

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


def bbd(box1, box2):

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

    bbd = (diagonal_diatance * 2 -
           inter_section_distance) / enclose_distance + 1

    return bbd


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


if __name__ == "__main__":
    begin = (600, 600)
    stairh = 100
    stepsize = 1
    stpnum = 6
    img, stairs_list = stairs(begin, stairh, stepsize, stpnum)
    #GT box
    gt_color = randomcolor()
    cv2.rectangle(img, (0, 0), (3 * stairh, 3 * stairh), gt_color, 2)
    #pr box
    pr_color = randomcolor()

    l2_loss = []
    iou_loss = []
    giou_loss = []
    bbd_loss = []
    font = cv2.FONT_HERSHEY_SIMPLEX

    fps = 35  #视频每秒24帧
    size = (1000, 1000)  #需要转为视频的图片的尺寸
    #可以使用cv2.resize()进行修改

    video = cv2.VideoWriter("loss.avi",
                            cv2.VideoWriter_fourcc('I', '4', '2', '0'), fps,
                            size)

    for i in stairs_list:
        new_img = img.copy()
        p1 = i
        p2 = list(p1)
        p2[0] += int(stairh * 2)
        p2[1] += int(stairh * 2)
        p2 = tuple(p2)
        cv2.rectangle(new_img, p1, p2, pr_color, 2)

        gt = np.array([0, 0, 3 * stairh, 3 * stairh])
        pr = np.array([p1[0], p1[1], p2[0], p2[1]])
        l2_ = l2(gt, pr) / 10000
        l2_loss.append(l2_)
        cv2.putText(new_img, 'l2: ' + str(l2_), (500, 50), font, 1.2,
                    (255, 255, 255), 2)

        iou_ = iou(gt, pr) * 15
        iou_loss.append(iou_)
        cv2.putText(new_img, 'iou: ' + str(iou_), (500, 100), font, 1.2,
                    (255, 255, 255), 2)

        giou_ = giou(gt, pr) * 10
        giou_loss.append(giou_)
        cv2.putText(new_img, 'giou: ' + str(giou_), (500, 150), font, 1.2,
                    (255, 255, 255), 2)

        bbd_ = bbd(gt, pr)
        bbd_loss.append(bbd_)
        cv2.putText(new_img, 'TSB: ' + str(bbd_), (500, 200), font, 1.2,
                    (255, 255, 255), 2)

        cv2.namedWindow("image")
        cv2.imshow('image', new_img)
        cv2.waitKey (1)
        video.write(new_img)

    video.release()
    cv2.destroyAllWindows()

    lower = bbd_loss.index(min(bbd_loss))
    print(iou_loss[lower])
    plt.plot([lower, lower], [0, 15], color='#ffb6b9', linestyle='--')
    co = '\\times{10}^{-4}'
    coe = 'L2 Loss' + '$%s$' % co

    scatter_show(l2_loss, 0, coe)
    scatter_show(iou_loss, 1, 'IoU Loss$%s$15' % '\\times')
    scatter_show(giou_loss, 2, 'GIoU Loss$%s$10' % '\\times')
    scatter_show(bbd_loss, 3, 'SB Loss')
    plt.annotate('The best\nposition',
                 color='#4EAC5B',
                 weight='bold',
                 xy=(lower, iou_loss[lower] + 5),
                 ha='right',
                 bbox=dict(boxstyle='round,pad=0.5',
                           fc='yellow',
                           ec='k',
                           lw=1,
                           alpha=0.4),
                 xytext=(lower + 3, iou_loss[lower] + 8),
                 arrowprops=dict(color='#4EAC5B',
                                 arrowstyle="->",
                                 connectionstyle="angle3,angleA=90,angleB=0"))

    plt.legend(loc='upper right', bbox_to_anchor=(0.8, 0.97), fontsize=14)
    for doty in np.arange(5, 35, 5):
        dotx = [0, 1250]
        plt.plot(dotx, [doty, doty],
                 color='#C3C3C3',
                 linestyle='--',
                 linewidth=0.9)
    font2 = {
        'family': 'Times New Roman',
        'weight': 'normal',
        'size': 14,
    }
    plt.xlabel('Steps', font2)
    plt.ylabel('Loss', font2)
    plt.ylim(0, 35)
    plt.xlim(0, 1250)
    plt.savefig('area_maze.pdf', dpi=600, format='pdf')
    plt.show()

    pass
