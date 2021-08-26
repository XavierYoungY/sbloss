import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import axes3d
color = ['#348498', '#ff502f', '#005792']


def wireframe(x, y, z, color_, ax):


    # Plot a basic wireframe.
    ax.plot_wireframe(x,
                      y,
                      z,
                      rstride=10,
                      cstride=10,
                      color=color_)

    ax.legend()

def l1(x,y):
    z = 2 * abs(x + y)
    return z


def MSE(x,y):
    z=4*(x+y)**2
    return z

def bbd(x,y):
    inter = 0.25 * (x + y)**2
    enclose = 0.25 * 9 * (x + y)**2
    z = (4 * (x + y)**2 - inter) / enclose
    return z

def iou(x,y):
    inter_area=x*y
    enclose_area=9

if __name__ == "__main__":
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = np.arange(0, 100, 1)
    y = np.arange(0, 100, 1)
    x, y = np.meshgrid(x, y)
    z=l1(x, y)
    wireframe(x, y, z, color[2], ax)
    # z = MSE(x, y)
    # wireframe(x, y, z, color[0], ax)
    # z = bbd(x, y)
    # wireframe(x, y, z, color[1], ax)
    plt.show()
