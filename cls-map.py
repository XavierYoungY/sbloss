import matplotlib.pyplot as plt
import pandas as pd
import xlrd
import numpy as np
import matplotlib.image as mpimg
import pylab as pl
colors = ["#EE66F8", "#fdc4b6", "#41b6e6"]
text_colors = ['#2b9464', '#E7475E']


def get_cls_names(map_over_clss):
    names = []
    for i in map_over_clss:
        name, _ = i.split(':')
        names.append(name)
    return names


def get_cls_map(map_over_clss):
    map_ = []
    for i in map_over_clss:
        name, _ = i.split(':')
        _ = round(float(_) * 100, 2)
        map_.append(_)
    return map_


if __name__ == "__main__":

    clss_map_path = 'VOC_clss_map.xlsx'

    excel = xlrd.open_workbook(clss_map_path)  #打开数据

    excel.sheet_names()  # 获取excel里的工作表sheet名称数组
    sheet = excel.sheet_by_index(0)  #根据下标获取对应的sheet表
    loss_names = sheet.row_values(0)
    cls_map = []
    for i in range(3):
        map_over_clss = sheet.col_values(i)[1:]
        names = get_cls_names(map_over_clss)
        cls_map.append(get_cls_map(map_over_clss))

    bar_width = 0.5
    for i in range(3):
        x = np.arange(len(cls_map[i])) + bar_width * i
        for _ in range(len(x)):
            x[_]+=1*_
        plt.bar(x,
                cls_map[i],
                label=loss_names[i],
                fc=colors[i],
                width=bar_width,
                alpha=1)


    text = []
    for i in range(20):
        _ = []
        for j in range(2):
            _.append(cls_map[j][i])
        text.append(max(_))
    for i in range(20):
        _=text[i]
        __ = str(round(cls_map[2][i] - _,1))
        if cls_map[2][i]>_:
            text[i] = '+' + __
        else:
            text[i] = __


    for i in range(20):
        if '+' in text[i]:
            color=text_colors[0]
        else:
            color=text_colors[1]
        plt.text(x[i] +   bar_width,
                 cls_map[2][i] + 0.65,
                 text[i],
                 ha='right',
                 fontsize=7,
                 color=color)

    for _ in range(len(x)):
        x[_] -= bar_width

    # for i in range(len(names)):
    #     names[i]=''

    plt.xticks(x, names, rotation=45, fontsize=8, ha="right")
    plt.xlabel('Categories')
    plt.ylabel('AP(%)')

    # plt.title('VOC ')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.01), frameon=False)
    plt.subplots_adjust(left=0.09, right=0.98, top=0.67, bottom=0.2)



    plt.savefig("cls-map.pdf", format="pdf")
    plt.savefig("cls-map.svg", format="svg")
    plt.show()