import json
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from operator import itemgetter
small=32*32
medium=96*96

def generate_scale():
    with open('/media/yy/DATA/datasets/VOC/VOCdevkit/VOC2007/voc07.txt','r') as f:
        voc=f.readlines()
        bboxs=[]
        for i in voc:
            _,i=i.split(' ')
            i=(i.rstrip('\n')).split(',')

            for j in range(len(i)//5):
                xmin = int(i[0 * j])
                ymin = int(i[0 * j + 1])
                xmax = int(i[0 * j + 2])
                ymax = int(i[0 * j + 3])
                w=xmax-xmin
                h=ymax-ymin
                bboxs.append(w*h)

    return bboxs






def scale_plot1(bboxs):

    bboxs = np.array(bboxs)
    area = bboxs[:].astype(np.float32)
    area=np.sort(area)
    max_area=max(area)
    min_area=min(area)
    area = 24 * (area - min_area) / (max_area - min_area)
    area = np.around(area)
    norm_area_count = Counter(area)
    norm_area_count=list(zip(norm_area_count.keys(),norm_area_count.values()))


    y = []
    for i in norm_area_count:
        y.append(i[1])
    x=np.array(range(len(y)))/25+1/60
    plt.bar(x, y, width=1 / 30, color='#3DC7BE')
    # for i in range(len(x)):
    #     m=x[i]
    #     n=y[i]
    #     plt.text(m,n+200,n,ha='center',fontsize=6)
    plt.xlim(0,1)
    plt.locator_params(nbins=10)
    plt.xlabel('Normalized Area')
    plt.ylabel('Frequency')
    plt.title('Normalized Area Distribution')
    plt.show()


if __name__ == "__main__":
    bboxs=generate_scale()
    scale_plot1(bboxs)
