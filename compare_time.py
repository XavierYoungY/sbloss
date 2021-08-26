import numpy as np
import cv2
import random
import loss
import time

NUM=10647




def generate_boxes():
    # xmin ymin xmax ymax
    boxes1=[]
    boxes2=[]
    for i in range(NUM):
        xmin = random.randint(1, 50)
        ymin = random.randint(1, 50)
        xmax = random.randint(51, 99)
        ymax = random.randint(51, 99)
        box1 = [xmin,ymin,xmax,ymax]
        boxes1.append(box1)

        xmin = random.randint(100, 150)
        ymin = random.randint(100, 150)
        xmax = random.randint(151, 199)
        ymax = random.randint(151, 199)
        box2 = [xmin, ymin, xmax, ymax]
        boxes2.append(box2)
    boxes1 = np.array(boxes1)
    boxes2 = np.array(boxes2)
    return boxes1, boxes2

def calculate_time():
    boxes1, boxes2 = generate_boxes()
    # for l2
    start=time.time()

    for i in range(NUM):
        box1=boxes1[i]
        box2=boxes2[i]
        l2_loss=loss.l2(box1,box2)

    end = time.time()
    print(end-start)

    start = time.time()

    for i in range(NUM):
        box1 = boxes1[i]
        box2 = boxes2[i]
        giou_loss = loss.giou(box1, box2)

    end = time.time()
    print(end - start)

    start = time.time()

    for i in range(NUM):
        box1 = boxes1[i]
        box2 = boxes2[i]
        sb_loss = loss.SB(box1, box2)

    end = time.time()
    print(end - start)


if __name__ == "__main__":
    calculate_time()