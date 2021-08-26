import json
import matplotlib.pyplot as plt
import operator
from matplotlib.pyplot import MultipleLocator
import numpy as np


def adjust_axes(r, t, fig, axes):
    # get text width for re-scaling
    bb = t.get_window_extent(renderer=r)
    text_width_inches = bb.width / fig.dpi
    # get axis width in inches
    current_fig_width = fig.get_figwidth()
    new_fig_width = current_fig_width + text_width_inches
    propotion = new_fig_width / current_fig_width
    # get axis limit
    x_lim = axes.get_xlim()
    axes.set_xlim([x_lim[0], x_lim[1] * propotion])


def draw_plot_func(dictionary, n_classes, window_title, plot_title, x_label,
                   output_path, to_show, plot_color, true_p_bar):
   
    sorted_keys = list(dictionary.keys())
    sorted_values = list(dictionary.values())

    #
    if true_p_bar != "":
        """
     Special case to draw in (green=true predictions) & (red=false predictions)
    """
        fp_sorted = []
        tp_sorted = []
        for key in sorted_keys:
            fp_sorted.append(dictionary[key] - true_p_bar[key])
            tp_sorted.append(true_p_bar[key])
        plt.barh(range(n_classes),
                 fp_sorted,
                 align='center',
                 color='crimson',
                 label='False Predictions')
        plt.barh(range(n_classes),
                 tp_sorted,
                 align='center',
                 color='forestgreen',
                 label='True Predictions',
                 left=fp_sorted)
        # add legend
        plt.legend(loc='lower right')
        """
     Write number on side of bar
    """
        fig = plt.gcf()  # gcf - get current figure
        axes = plt.gca()
        r = fig.canvas.get_renderer()
        for i, val in enumerate(sorted_values):
            fp_val = fp_sorted[i]
            tp_val = tp_sorted[i]
            fp_str_val = " " + str(fp_val)
            tp_str_val = fp_str_val + " " + str(tp_val)
            # trick to paint multicolor with offset:
            #   first paint everything and then repaint the first number
            t = plt.text(val,
                         i,
                         tp_str_val,
                         color='forestgreen',
                         va='center',
                         fontweight='bold')
            plt.text(val,
                     i,
                     fp_str_val,
                     color='crimson',
                     va='center',
                     fontweight='bold')
            if i == (len(sorted_values) - 1):  # largest bar
                adjust_axes(r, t, fig, axes)
    else:
        plt.barh(range(n_classes), sorted_values, color=plot_color)
        """
     Write number on side of bar
    """
        fig = plt.gcf()  # gcf - get current figure
        axes = plt.gca()
        r = fig.canvas.get_renderer()
        for i, val in enumerate(sorted_values):
            str_val = " " + str(val)  # add a space before
            if val < 1.0:
                str_val = " {0:.2f}".format(val)
            t = plt.text(val,
                         i,
                         str_val,
                         color=plot_color,
                         va='center',
                         fontweight='bold')
            # re-set axes to show number inside the figure
            if i == (len(sorted_values) - 1):  # largest bar
                adjust_axes(r, t, fig, axes)
    # set window title
    fig.canvas.set_window_title(window_title)
    # write classes in y axis
    tick_font_size = 12
    plt.yticks(range(n_classes), sorted_keys, fontsize=tick_font_size)
    """
   Re-scale height accordingly
  """
    init_height = fig.get_figheight()
    # comput the matrix height in points and inches
    dpi = fig.dpi
    height_pt = n_classes * (tick_font_size * 1.4)  # 1.4 (some spacing)
    height_in = height_pt / dpi
    # compute the required figure height
    top_margin = 0.15  # in percentage of the figure height
    bottom_margin = 0.05  # in percentage of the figure height
    figure_height = height_in / (1 - top_margin - bottom_margin)
    # set new height
    if figure_height > init_height:
        fig.set_figheight(figure_height)

    # set plot title
    plt.title(plot_title, fontsize=14)
    # set axis titles
    # plt.xlabel('classes')
    plt.xlabel(x_label, fontsize='large')
    # adjust size of window
    fig.tight_layout()
   
    fig.savefig(output_path)
    

if __name__ == "__main__":

    path1 = '/media/yy/File/Link to yolo/tensorflow-yolov3/mAP/yolo_map.json'
    path2 = '/media/yy/File/Link to yolo/yolov3-myIOU/mAP/myiou_map.json'

    with open(path1,'r') as f1:
        ori=json.load(f1)
        keys1 = list(ori.keys())
        values1 = list(ori.values())

    with open(path2, 'r') as f2:
        my = json.load(f2)
        keys2 = list(my.keys())
        values2 = list(my.values())


    window_title = "mAP"
    plot_title = "mAP"
    x_label = "Average Precision"
    output_path = "./mAP.png"
    to_show = True
    plot_color = 'royalblue'


    draw_plot_func(ori, len(keys1), window_title, plot_title, x_label,
                    output_path, to_show, plot_color, "")

    plot_color = 'darkorange'
    draw_plot_func(my, len(keys1), window_title, plot_title, x_label,
                   output_path, to_show, plot_color, "")

    plt.show()
