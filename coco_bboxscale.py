import json
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from operator import itemgetter
small=32*32
medium=96*96

def generate_scale():
    with open('/media/yy/DATA/datasets/COCO/annotations/instances_train2017.json','r') as f:
        bbox_instances = json.load(f)
        images=bbox_instances['images']
        image_info={}
        for image in images:
            image_id=image['id']
            image_info[image_id] = [
                image['width'], image['height'],
                image['width'] * image['height']
            ]

        anns = bbox_instances['annotations']
        bboxs = []
        for i in anns:
            bbox = i['bbox']
            # x y w h
            scale = bbox[2] * bbox[3]
            bbox.append(scale)
            if scale <= small:
                bbox.append('small')
            elif scale <= medium:
                bbox.append('medium')
            else:
                bbox.append('large')
            image_id = i['image_id']
            image=image_info[image_id]
            bbox.append(scale/image[2])
            bboxs.append(bbox[2:])
    with open('bbox_scale.json', 'w') as f:
        json.dump(bboxs, f)

def scale_plot1():
    with open('bbox_scale.json', 'r') as f:
        bboxs=json.load(f)
        bboxs = np.array(bboxs)
        area = bboxs[:, 2].astype(np.float32)
        area=np.sort(area)
        max_area=max(area)
        min_area=min(area)

        area = 24 * (area - min_area) / (max_area - min_area)
        area = np.around(area)

        
        norm_area_count = Counter(area)
        norm_area_count=list(zip(norm_area_count.keys(),norm_area_count.values()))

        # norm_area_count = sorted(norm_area_count.items(),
        #                          key=lambda d: d[1],
        #                          reverse=True)
        y = []
        for i in norm_area_count:
            # _ = str(i[1]/1000)+'k'
            y.append(i[1])
        x=np.array(range(len(y)))/25+1/60
        plt.bar(x, y, width=1 / 30, color='#3DC7BE')
        yname=range(600000)
        yname = yname[0:600000:100000]
        ynames=[]
        for name in yname:
            ynames.append(str(name//1000)+'k')
        plt.yticks(yname, ynames)

        # for i in range(len(x)):
        #     m=x[i]
        #     n=y[i]
        #     plt.text(m,n+200,n,ha='center',fontsize=6)
        plt.xlim(0,1)
        plt.locator_params(nbins=10)
        plt.xlabel('Normalized Area')
        plt.ylabel('Frequency')
        plt.title('Normalized Area Distribution')
        plt.subplots_adjust(left=0.12, right=0.84, top=0.86, bottom=0.35)
        plt.savefig('scale.pdf', dpi=600, format='pdf')
        plt.show()


def cdf_plot():
    with open('bbox_scale.json', 'r') as f:
        bboxs = json.load(f)
        bboxs = np.array(bboxs)
        area = bboxs[:,4].astype(np.float32)

        area = np.around(area, decimals=3)
        norm_area_count = Counter(area)
        y = []
        for i in norm_area_count:
            y.append([i, norm_area_count[i]])
        y = sorted(y, key=itemgetter(0))
        y = np.array(y)
        x = y[:, 0]
        area = y[:, 1]
        y=np.zeros(len(area)+1)
        for i in range(len(y)):
            if i==0:
                y[0]=0
            else:
                y[i] = y[i-1] + area[i-1]
        max_num=max(y)
        y = y / max_num
        x = np.array(range(len(y))) /(len(y)-1)


        plt.plot(x,y)
        plt.xlim(0, 1)
        plt.ylim(0, 1)
        plt.locator_params(nbins=10)
        plt.subplots_adjust(top=.7,right=.93)
        plt.grid()
        plt.show()


def sml_plot():
    with open('bbox_scale.json', 'r') as f:
        bboxs = json.load(f)
        bboxs = np.array(bboxs)
        size=bboxs[:,3]
        size_count=Counter(size)
        x=size_count.keys()
        y=size_count.values()
        plt.bar(x,y)
        plt.show()
        pass


if __name__ == "__main__":
    # generate_scale()
    scale_plot1()
    # sml_plot()
    # cdf_plot()
