import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

#将画布分为3*3,并且将画布定位到第一个axis系中
height = 150
width = 150
img = np.ones((height, width, 3), np.uint8) * 255
fig = plt.figure()
ax = fig.add_subplot(111)
ax.imshow(img)
center = np.array([width // 2, height // 2 - 5],dtype='int32')
gt_width = 80
gt_height = 80
bl = np.copy(center) - gt_width//2
rec_center=[]
rect = patches.Rectangle(bl,
                            gt_width,
                            gt_height,
                            linewidth=3,
                            edgecolor='#60B683',
                            facecolor='none',
                            alpha=1)
ax.add_patch(rect)
ax.axis([0, width, 0, height])
ax.add_patch(patches.Rectangle((0, 0), 2, 3))
ax.set_title("patches.Rectangle((0, 0), 2, 3)")
plt.show()