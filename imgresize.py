import cv2
import numpy as np
import matplotlib.pyplot as plt
import os



def img_resize(imgname):

    #读取原始图像
    img = cv2.imread(imgname)
    size=img.shape[0]*img.shape[1]//2

    #图像取样
    r1 = cv2.pyrDown(img)

    r2 = cv2.pyrDown(r1)
    r3 = cv2.pyrDown(r2)
    r6 = cv2.pyrDown(r3)

    r4=cv2.pyrUp(img)
    r5 = cv2.pyrUp(r4)




    imgname=imgname.rstrip('.jpg')+'_'
    #显示图像
    cv2.imshow('UP2', r5)
    cv2.imwrite(imgname + 'UP2' + '.jpg', r5)
    cv2.imshow('UP1', r4)
    cv2.imwrite(imgname + 'UP1' + '.jpg', r4)


    cv2.imshow('PyrDown1', r1)
    cv2.imwrite(imgname + 'PyrDown1' + '.jpg', r1)
    cv2.imshow('PyrDown2', r2)
    cv2.imwrite(imgname + 'PyrDown2' + '.jpg', r2)
    cv2.imshow('PyrDown3', r3)
    cv2.imwrite(imgname + 'PyrDown3' + '.jpg', r3)




    cv2.waitKey(500)
    cv2.destroyAllWindows()



def read_directory(directory_name):
    array_of_img = []  # this if for store all of the image data
    # this loop is for read each image in this foder,directory_name is the foder name with images.
    for filename in os.listdir(directory_name):
        #print(filename) #just for test
        #img is used to store the image data
        img = directory_name + "/" + filename
        array_of_img.append(img)

    return array_of_img


if __name__ == "__main__":
    rootdir = '/media/yy/DATA/datasets/VOC/VOCdevkit/VOC2007/test'

    array_of_img = read_directory(rootdir)
    for img in array_of_img:
        img_resize(img)

    pass
