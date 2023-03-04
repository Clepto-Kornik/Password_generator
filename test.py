import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
from matplotlib import patches
from PIL import Image
from IPython.display import clear_output
from pathlib import Path


# events occuring after mouse buttons are presed
def draw_line(event, x, y, flags, parameters):
    global xaddline, yaddline, xremoveline, yremoveline, ix, iy, draw, color, click, height, width, addline, removeline
    # left mouse button clicked
    if (event == 1):
        draw = True
        color = 255
        click = 1
        ix = x
        iy = y
    # right mouse button clicked
    if (event == 2):
        draw = True
        color = 0
        click = 2
        ix = x
        iy = y

    if (event == 0):
        if (draw == True):
            # drawing line for both buttons
            cv.line(img_tmp, pt1=(ix, iy), pt2=(x, y), color=(color, color, color), thickness=2)
            ix = x
            iy = y
            if (click == 1):  # left button
                for i in range(0, 5):
                    if (((ix + i) < width) and ((ix - i) >= 0)):
                        xaddline.append(ix + i)
                    if (((iy + i) < height) and ((iy - i) >= 0)):
                        yaddline.append(iy + i)
                    if (((ix - i) >= 0) and ((ix + i) < width)):
                        xaddline.append(ix - i)
                    if (((iy - i) >= 0) and ((iy + i) < height)):
                        yaddline.append(iy - i)
            elif (click == 2):  # right button
                for i in range(0, 5):
                    if (((ix + i) < width) and ((ix - i) >= 0)):
                        xremoveline.append(ix + i)
                    if (((iy + i) < height) and ((iy - i) >= 0)):
                        yremoveline.append(iy + i)
                    if (((ix - i) >= 0) and ((ix + i) < width)):
                        xremoveline.append(ix - i)
                    if (((iy - i) >= 0) and ((iy + i) < height)):
                        yremoveline.append(iy - i)

    # buttons are released
    if (event == 4 or event == 5):
        draw = False
        if (len(yaddline) > 0 and len(xaddline) > 0):
            n = min(len(yaddline), len(xaddline))
            addline = np.vstack((yaddline[:n], xaddline[:n])).T
        if (len(yremoveline) > 0 and len(xremoveline) > 0):
            n = min(len(yremoveline), len(xremoveline))
            removeline = np.vstack((yremoveline[:n], xremoveline[:n])).T


def rectangle(event, x, y, flags, parameters):
    global ix, iy, ix1, iy1, draw
    # left button presed for drawing rectangle
    if (event == 1):
        draw = True
        ix = x
        iy = y
    # button released - end of drawing rectangle
    if (event == 4):
        draw = False
        cv.rectangle(img_tmp, pt1=(ix, iy), pt2=(x, y), color=(0, 0, 255), thickness=2)
        ix1 = x
        iy1 = y


fileName = 'im_two.jpg'
img = cv.imread('im_two.jpg')[:, :, ::-1]
mask = np.zeros(img.shape[:2], np.uint8)
# GrabCut parameters
bgd_model = np.zeros((1, 65), np.float64)
fgd_model = np.zeros((1, 65), np.float64)
height = img.shape[:2][0]
width = img.shape[:2][1]

figure, ax = plt.subplots(1)
ax.imshow(img)  # show original image

draw = False
ix, iy, ix1, iy1 = -1, -1, -1, -1
img_tmp = img.copy()
original_img = img.copy()
# window for region selecting
cv.namedWindow('Select the region of interest')
cv.setMouseCallback('Select the region of interest', rectangle)

# loop for editing
while (True):
    cv.imshow('Select the region of interest', img_tmp)
    if cv.waitKey(20) & 0xFF == ord('q'):  # skiping to the next step
        break
cv.destroyAllWindows()
figure, ax = plt.subplots(1)

# rectangle parameters
if (ix1 < ix):
    ix1, ix = ix, ix1
if (iy1 < iy):
    iy1, iy = iy, iy1
# new rectangle parameters
width = abs(ix1 - ix)
height = abs(iy1 - iy)
xStart = ix
yStart = iy

# rectangle and foreground is shown
rect = patches.Rectangle((ix, iy), width, height, edgecolor='r', facecolor='none')
ax.imshow(img)
ax.add_patch(rect)
rect = (xStart, yStart, width, height)

cv.grabCut(img, mask, rect, bgd_model, fgd_model, 5, cv.GC_INIT_WITH_RECT)

mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
img = img * mask2[:, :, np.newaxis]
plt.imshow(img)

# loop for the algorithm - alows making changes
counter = 0
while (True):
    draw = False
    xaddline, yaddline, xremoveline, yremoveline, ix, iy, click = [], [], [], [], 0, 0, 0
    addline = []
    removeline = []
    img_tmp = img.copy()
    color = 50

    # after the first iteration replace the mask since it was converted from [0:3] to [0:1]
    if counter > 0:
        mask = mask_tmp.copy()

    # window for manualy selecting regions
    cv.namedWindow('Right button - remove and left button - keep')
    cv.setMouseCallback('Right button - remove and left button - keep', draw_line)

    while (True):
        cv.imshow('Right button - remove and left button - keep', img_tmp)
        if cv.waitKey(20) & 0xFF == ord('q'):  # skips to the next step
            break
    cv.destroyAllWindows()
    figure, ax = plt.subplots(1)

    # edit the mask for the algorithm based on manual changes
    if len(addline) > 0:
        mask[addline[:, 0], addline[:, 1]] = 1
    if len(removeline) > 0:
        mask[removeline[:, 0], removeline[:, 1]] = 0

    mask_tmp = mask.copy()
    mask, bgd_model, fgd_model = cv.grabCut(img, mask, None, bgd_model, fgd_model, 5, cv.GC_INIT_WITH_MASK)
    mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    img = original_img * mask[:, :, np.newaxis]
    counter = counter + 1

    # output
    plt.imshow(img)
    plt.show()
    if input('Do You want to make more changes? yes/no:\n') != 'yes':
        break
    clear_output(wait=True)

    plt.imshow(img)
    plt.show()

new_img = Image.fromarray(img)
path = Path('C:/Users/HP/Desktop/'.rsplit(".", 1)[0] + 'output.png')  # saving output image
new_img.save(path)

# transfer black as transparent and save new image
img = Image.open(path)
img = img.convert('RGBA')
datas = img.getdata()
mask_1D = mask.flatten()  # returns a copy of the array collapsed into one dimension
index = 0
new_data = []
for item in datas:
    if item[0] == 0 and item[1] == 0 and item[2] == 0 and mask_1D[index] == 0:
        new_data.append((255, 255, 255, 0))
    else:
        new_data.append(item)
    index = index + 1
img.putdata(new_data)
img.save(path)