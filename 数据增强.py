import numpy as np
import cv2



pic = cv2.imread('01.jpg') #读入图片

h_pic = cv2.flip(pic, 1)#水平翻转
cv2.imshow('overturn-h', h_pic)


v_pic = cv2.flip(pic, 0)#垂直翻转
cv2.imshow('overturn-v', v_pic)


hv_pic = cv2.flip(pic, -1)#水平垂直翻转
cv2.imshow('overturn-hv', hv_pic)
cv2.waitKey(100000)
