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
point_size = 2
pan_color = (144 / 255, 238 / 255, 144 / 255, 0.5)
grid_color = (192 / 255, 192 / 255, 192 / 255, 0.5)


def get_colorbar(num):
    cm = matplotlib.cm.get_cmap('rainbow')
    colors = [cm(1. * i / num) for i in range(num)]
    xy = range(num)
    colorlist = [colors[x] for x in xy]
    return colorlist


def random_samples():
    height = 150
    width = 150
    img = np.ones((height, width, 3), np.uint8) * 255
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.imshow(img)
    ax.axis([0, width, 0, height])
    center = np.array([width // 2, height // 2 - 5], dtype='int32')
    gt_width = 80
    gt_height = 80
    bl = np.copy(center) - gt_width // 2
    rec_center = []
    rect = patches.Rectangle(bl,
                             gt_width,
                             gt_height,
                             linewidth=3,
                             edgecolor='#FFA500',
                             facecolor='none',
                             alpha=1)
    ax.add_patch(rect)
    pr_bl = np.copy(bl)
    pr_bl[0] += gt_width
    pr_bl[1] -= 20
    pr_rect = patches.Rectangle(pr_bl,
                                20,
                                20,
                                linewidth=3,
                                edgecolor='r',
                                facecolor='none',
                                alpha=1)
    ax.add_patch(pr_rect)
    start = pr_bl + 10
    end = center
    turn = 0
    step_length = gt_height + 20
    maze_points = maze(start, end, step_length)
    colors = get_colorbar(len(maze_points))
    loss_colors = []
    for i in range(len(maze_points)):
        # for i in range(5):
        points = maze_points[i]
        plt.scatter(points[:, 0],
                    points[:, 1],
                    c=colors[i],
                    s=point_size,
                    alpha=0.6)
        _ = np.array(colors[i])
        _ = np.tile(_, (len(points),1))
        loss_colors.append(_)
    centers = np.array([center, start])
    plt.scatter(centers[:, 0],
                centers[:, 1],
                s=point_size * 6,
                color='green',
                marker='o',
                edgecolor='black',
                alpha=0.5)
    font2 = {
        'family': 'Times New Roman',
        'weight': 'normal',
        'size': 10,
    }
    plt.xlabel('x', font2)
    plt.ylabel('y', font2)
    # plt.ylim(0, 35)
    # plt.xlim(0, 1250)
    plt.savefig('maze.pdf', dpi=600, format='pdf')






    gt_box = np.append(center + [-gt_width // 2, -gt_height // 2],
                       center + [gt_width // 2, gt_height // 2])
    pr_box = []
    for points in maze_points:
        bl = points + [-10, -10]
        ur = points + [10, 10]
        _ = np.ones((len(points), 4))
        _[:, 0:2] = bl
        _[:, 2:] = ur
        pr_box.append(_)
    return gt_box, pr_box, loss_colors, maze_points




def maze(start, end, step_length):
    maze_end = True
    maze_points = []
    while maze_end:
        maze = []
        turn = 1
        for i in range(4):
            points = np.ones((step_length + 1, 2), dtype='int32')
            if end in points:
                maze_end = False
                break
            if i == 0:
                points[:, 0] = start[0]
                points[:, 1] = [
                    j for j in range(start[1], start[1] + step_length + 1)
                ]
                pass
            elif i == 1:
                points[:, 1] = start[1]
                points[:, 0] = [
                    j
                    for j in range(start[0], start[0] - (step_length + 1), -1)
                ]
            elif i == 2:
                step_length -= point_size
                if step_length <= 0:
                    maze_end = False
                    break

                points = np.ones((step_length + 1, 2), dtype='int32')
                points[:, 0] = start[0]
                points[:, 1] = [
                    j
                    for j in range(start[1], start[1] - (step_length + 1), -1)
                ]

            else:
                points[:, 1] = start[1]
                points[:, 0] = [
                    j for j in range(start[0], start[0] + (step_length + 1))
                ]
                step_length -= point_size
                if step_length <= 0:
                    maze_end = False
                    break

            start = points[-1]
            maze_points.append(points)
    point = maze_points[-1][-1]
    points = np.ones((2, 2))
    points[0] = point + np.array([0, -1])
    points[1] = point + np.array([1, -1])
    maze_points.append(points)
    maze_points = np.array(maze_points)

    return np.array(maze_points)


def get_loss(pr_box, gt_box, loss_colors, loss_name):

    _loss = []
    all_colors = []
    for i in range(len(pr_box)):
        boxes = pr_box[i]
        colors = loss_colors[i]
        for j in range(len(boxes)):
            box = boxes[j]
            color = colors[j]
            if loss_name == 'iou':
                _loss.append(loss.iou_loss(box, gt_box))
            elif loss_name == 'sb':
                _loss.append(loss.SB(box, gt_box))
            else:
                _loss.append(loss.giou(box, gt_box))
            all_colors.append(color)
    return np.array(_loss), np.array(all_colors)


def plot_loss(x, y, z, colors, name):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, c=colors, s=point_size, alpha=0.5)

    ax.xaxis._axinfo["grid"]['color'] = grid_color
    ax.yaxis._axinfo["grid"]['color'] = grid_color
    ax.zaxis._axinfo["grid"]['color'] = grid_color
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel(name + ' Loss')
    ax.figure.savefig(name + '_maze_loss.pdf', dpi=600, format='pdf')


if __name__ == "__main__":
    gt_box, pr_box, loss_colors, maze_points = random_samples()
    iou, iou_color = get_loss(pr_box, gt_box, loss_colors, 'iou')
    sb, sb_color = get_loss(pr_box, gt_box, loss_colors, 'sb')
    giou, giou_color = get_loss(pr_box, gt_box, loss_colors, 'giou')
    all_points=[]
    for points in maze_points:
        for point in points:
            all_points.append(point)
    all_points=np.array(all_points)
    x = all_points[:, 0]
    y = all_points[:, 1]
    plot_loss(x, y, iou, iou_color.tolist(), 'IoU')
    plot_loss(x, y, sb, sb_color.tolist(), 'SB')
    plot_loss(x, y, giou, giou_color.tolist(), 'GIoU')


    plt.show()
