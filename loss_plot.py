import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import axes3d


def zhexian():
    mpl.rcParams['legend.fontsize'] = 10

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    x = np.linspace(-4 * np.pi, 4 * np.pi, 100)
    y = np.linspace(-4 * np.pi, 4 * np.pi, 100)
    z=x**2+y**2

    ax.plot(x, y, z, label='parametric curve')
    ax.legend()

    plt.show()


def wireframe(fig):



    ax = fig.add_subplot(111, projection='3d')

    # Grab some test data.
    # X, Y, Z = axes3d.get_test_data(0.05)
    X = np.arange(0, 100, 1)
    Y = np.arange(0, 100, 1)
    X, Y = np.meshgrid(X, Y)
    Z = (X**2 + Y**2)
    test2(X, Y, Z, fig, 'autumn')

    # Plot a basic wireframe.
    ax.plot_wireframe(X,
                      Y,
                      Z,
                      rstride=10,
                      cstride=10,
                      color='#f5587b',
                      label='x^2+y^2')
    Z=X*Y
    test2(X, Y, Z, fig,'winter')
    ax.plot_wireframe(X,
                      Y,
                      Z,
                      rstride=10,
                      cstride=10,
                      color='#414141',
                      label='x*y')
    ax.legend()

    # plt.show()
    return fig


def surface(fig):

    ax = fig.gca(projection='3d')


    X = np.arange(0, 100, 1)
    Y = np.arange(0, 100, 1)
    X, Y = np.meshgrid(X, Y)
    Z = (X**2 + Y**2)



    # Plot the surface.
    surf = ax.plot_surface(X,
                        Y,
                        Z,
                        cmap='rainbow',
                        linewidth=0,
                        antialiased=False)

    # Customize the z axis.
    ax.set_zlim(-1.01, 1.01)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

def test():
    # 生成网格点坐标矩阵
    n = 1000
    x, y = np.meshgrid(np.linspace(-3, 3, n),
                    np.linspace(-3, 3, n))
    # 根据x,y 计算当前坐标下的z高度值
    z = (1-x/2 + x**5 + y**3) * np.exp(-x**2 -y**2)

    plt.figure('Contour', facecolor='lightgray')
    plt.title('Contour', fontsize=18)
    plt.xlabel('x', fontsize=14)
    plt.ylabel('y', fontsize=14)
    plt.tick_params(labelsize=10)
    plt.grid(linestyle=':')
    cntr = plt.contour(x, y, z, colors='black', linewidths=0.5)
    # cntr等高线对象绘制标注
    plt.clabel(cntr, inline_spacing=1, fmt='%.1f',
            fontsize=10)
    # 等高线填充颜色
    plt.contourf(x, y, z, 8, cmap='jet')

    plt.show()


def test2(X, Y, Z, fig, cmap):

    norm = plt.Normalize(Z.min(), Z.max())
    colors = cm.viridis(norm(Z))
    rcount, ccount, _ = colors.shape
    ax = fig.gca(projection='3d')
    # surf = ax.plot_surface(X,
    #                     Y,
    #                     Z,
    #                     rcount=rcount,
    #                     ccount=ccount,
    #                     facecolors=colors,
    #                     shade=False)
    # surf.set_facecolor((0, 0, 0, 0))
    surf = ax.plot_surface(X,
                           Y,
                           Z,
                           rstride=10,
                           cstride=10,
                           cmap=cmap,
                           linewidth=0,
                           antialiased=False)
    ax.legend()
    # plt.show()


if __name__ == "__main__":
    fig = plt.figure()
    wireframe(fig)
    # surface(fig)

    plt.show()


    pass