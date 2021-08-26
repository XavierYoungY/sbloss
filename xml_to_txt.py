#!/usr/bin/evn python
#coding:utf-8
import os
import sys
import xml.etree.ElementTree as ET
import glob

PRE_DEFINE_CATEGORIES = {"aeroplane": 0, "bicycle": 1, "bird": 2, "boat": 3,
                         "bottle": 4, "bus": 5, "car": 6, "cat": 7, "chair": 8,
                         "cow": 9, "diningtable": 10, "dog": 11, "horse": 12,
                         "motorbike": 13, "person": 14, "pottedplant": 15,
                         "sheep": 16, "sofa": 17, "train":18 , "tvmonitor":19}
def get_imlist(file):
    imlist=[]
    with open(file,'r') as file:
        for line in file:
            imlist.append(line.strip('\n'))
    print(imlist)
    return imlist
def get_impath(trainlist,im_dir):
    #trainlist = get_imlist(file)
    impath = []
    for im in trainlist:
        im1 = im + '.jpg'
        find_im1 = os.path.join(im_dir,im1)
        impath.append(find_im1)
    print(impath)
    return impath
def pick_xml(trainlist,xml_dir):
    #trainlist = get_imlist(file)
    xml_list=[]
    for im in trainlist:
        xml_label = im + '.xml'
        xml_file = os.path.join(xml_dir, xml_label)
        xml_list.append(xml_file)
    print(xml_list)
    return xml_list
#def get(root, name):
# vars = root.findall(name)
# return vars
def parse_xml(xml_list,file_txt):
    f_w = open(file_txt, 'a+')
    for xml_f in xml_list:
        im_name = os.path.basename(xml_f)[:-4]+'.jpg'
        tree = ET.parse(xml_f)
        root = tree.getroot()
        print(im_name)
        #f_w.write(im_name+' ')
        categories = PRE_DEFINE_CATEGORIES
        imbbox = []
        for obj in root.iter('object'):
            category = obj.find('name').text
            category_id = categories[category]
            bndbox = obj.find('bndbox')
            xmin = bndbox.find('xmin').text
            ymin = bndbox.find('ymin').text
            xmax = bndbox.find('xmax').text
            ymax = bndbox.find('ymax').text
            #print coodrnation
            bbox = str(xmin)+','+str(ymin)+','+str(xmax)+','+str(ymax)+','+str(category_id)
            imbbox.append(bbox)
        imbboxs=",".join(imbbox)
        #print(imbboxs)
        im_info="/media/yy/DATA/datasets/VOC/VOCdevkit/VOC2007/JPEGImages/"+im_name+" "+imbboxs
        f_w.write(im_info+"\n")
        #f_w.write(str(xmin)+','+str(ymin)+','+str(xmax)+','+str(ymax)+',')
        #f_w.write(str(category_id)+",")
        #f_w.write("\n")








root_path = "/media/yy/DATA/datasets/VOC/VOCdevkit/VOC2007"
file_txt = "voc07test.txt"
xml_dir = os.path.join(root_path, 'Annotations')

#xml_list = os.listdir(os.path.join(root_path, 'Annotations'))

#print(xml_list)
im_lables_dir = "/media/yy/DATA/datasets/VOC/VOCdevkit/VOC2007/ImageSets/Main"  #train or test image name
image_dir = "/media/yy/DATA/datasets/VOC/VOCdevkit/VOC2007/JPEGImages"

#trainval data
train_im = os.path.join(im_lables_dir, 'trainval.txt')
test_im = os.path.join(im_lables_dir, 'test.txt')
trainlist = get_imlist(train_im)
testlist = get_imlist(test_im)

im_path = get_impath(trainlist,image_dir)
# xml_list = pick_xml(trainlist,xml_dir)
xml_list = pick_xml(testlist,xml_dir)
parse_xml(xml_list,file_txt)
