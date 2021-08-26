import numpy as np



def coco(txt):
    with open(txt,'r') as f:
        img_num=0
        bboxs_num=0
        for num, line in enumerate(f):
            img_num+=1
            annotation = line.strip().split()
            if annotation == []:
                continue
            image_path = annotation[0]
            image_name = image_path.split('/')[-1]
            bbox_data_gt = np.array(
                    [list(map(int, box.split(','))) for box in annotation[1:]])

            bbox_data_gt = bbox_data_gt.reshape(-1,5)
            bboxs_num += bbox_data_gt.shape[0]

    return [img_num, bboxs_num]


if __name__ == "__main__":

    voc = coco(
        '/media/yy/DATA/datasets/VOC/VOCdevkit/VOC2007/voc07train_val.txt')
    coco = coco(
        '/media/yy/Test/coco_upload/tensorflow-yolov3/data/dataset/voc07test.txt'
    )
    print(voc)
    print(coco)