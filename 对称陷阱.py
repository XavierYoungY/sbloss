import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
from math import cos, sin, pi
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.tri as mtri
import loss
from matplotlib import cm
from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle
point_size=10
pan_color = (144 / 255, 238 / 255, 144 / 255, 0.5)
grid_color = (192 / 255, 192 / 255, 192 / 255, 0.5)


def get_r_point(x0, y0, r):

    samples_num = 5000
    t = np.random.random(size=samples_num) * 2 * np.pi - np.pi
    x = r * np.cos(t)
    y = r * np.sin(t)

    i_set = np.arange(0, samples_num, 1)
    for i in i_set:
        len = np.sqrt(np.random.random())
        x[i] = x0 + x[i] * len
        y[i] = y0 + y[i] * len

    return x, y


def get_colorbar(num):
    cm = matplotlib.cm.get_cmap('tab20')
    colors = [cm(1. * i / num) for i in range(num)]
    xy = range(num)
    colorlist = [colors[x] for x in xy]
    return colorlist


def scatter_circle(center, r):
    x = center[0]
    y = center[1]
    x, y = get_r_point(x, y, r)
    sizes = point_size*np.ones(len(x))
    # colorbar = [i for i in range(100)]
    colorbar = get_colorbar(100)
    colors = []
    r_ = np.arange(0, r, r / 100)
    for i in range(len(x)):
        x_ = x[i] - center[0]
        y_ = y[i] - center[1]
        index = int((x_**2 + y_**2)**.5 / (r / 100))
        colors.append(colorbar[index])

    plt.scatter(x, y, c=colors, s=sizes, alpha=0.6, marker='3')
    font2 = {
        'family': 'Times New Roman',
        'weight': 'normal',
        'size': 10,
    }
    plt.xlabel('x', font2)
    plt.ylabel('y', font2)
    # plt.ylim(0, 35)
    # plt.xlim(0, 1250)
    plt.axis([0, 150, -13, 130])


    plt.savefig('symmetric_trap.pdf', dpi=600, format='pdf')
    return x, y, colors


def random_samples():
    height = 150
    width = 150
    img = np.ones((height, width, 3), np.uint8) * 255
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(img)
    center = (width // 2, height // 2 - 5)
    gt_width=40
    gt_height=74
    rect = patches.Rectangle(center,
                             gt_width,
                             -gt_height,
                             linewidth=3,
                             edgecolor='#67C4BD',
                             facecolor='none',
                             alpha=1)

    ax.add_patch(rect)
    pr_bl = np.array(center) + np.array([30, -30])
    pr_ur = np.array(center) + np.array([gt_width + 5, -(5 + gt_height)])
    w_h = pr_ur - pr_bl
    pr_rect = patches.Rectangle(pr_bl,
                                w_h[0],
                                w_h[1],
                                linewidth=3,
                                edgecolor='#F7C143',
                                facecolor='none',
                                ls='--',
                                alpha=1)
    ax.add_patch(pr_rect)
    ax.invert_yaxis()


    x, y, colors = scatter_circle(center, 50)
    gt_box = [
        center[0], center[1], center[0] + gt_width, center[1] + gt_height
    ]
    pr_br = [gt_box[2] + 5, gt_box[3] + 5]
    pr_box=[]
    for i in range(len(x)):
        box=[]
        box.append(x[i])
        box.append(y[i])
        box.append(pr_br[0])
        box.append(pr_br[1])
        pr_box.append(box)
    pr_box=np.array((pr_box))
    gt_box = np.array((gt_box))
    print('样本数量：'+str(len(x)))



    return pr_box, colors, gt_box, x, y


def get_loss(pr_box,gt_box):

    l2_loss=[]
    sb_loss=[]
    for box in pr_box:
        l2_loss.append(loss.l2(box,gt_box))
        sb_loss.append(loss.SB(box, gt_box))
    return np.array(l2_loss), np.array(sb_loss)


def plot_loss(x, y, z,colors,name):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, c=colors, s=point_size, alpha=0.5,marker='3')
    # make the panes transparent
    # ax.xaxis.set_pane_color(pan_color)
    # ax.yaxis.set_pane_color(pan_color)
    # ax.zaxis.set_pane_color(pan_color)
    # make the grid lines transparent
    ax.xaxis._axinfo["grid"]['color'] = grid_color
    ax.yaxis._axinfo["grid"]['color'] = grid_color
    ax.zaxis._axinfo["grid"]['color'] = grid_color
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel(name+' Loss')
    ax.figure.savefig(name+'loss.pdf', dpi=600, format='pdf')








if __name__ == "__main__":
    pr_box, colors, gt_box, x, y = random_samples()
    l2_loss, sb_loss = get_loss(pr_box, gt_box)
    plot_loss(x, y, l2_loss, colors,'L2')
    plot_loss(x, y, sb_loss, colors,'SB')


    # plt.colorbar()
    plt.show()
