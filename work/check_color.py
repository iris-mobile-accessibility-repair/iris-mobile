# encoding: utf-8
from colorsys import rgb_to_hsv

import cv2

import get_color_set
import colorSet_reference

def colorToRGB(value):
    digit = list(map(str, range(10))) + list("ABCDEF")
    if isinstance(value, tuple):
        string = '#'
        for i in value:
            a1 = i // 16
            a2 = i % 16
            string += digit[a1] + digit[a2]
        return string
    elif isinstance(value, list):
        string = '#'
        for i in value:
            a1 = i // 16
            a2 = i % 16
            string += digit[a1] + digit[a2]
        return string
    elif isinstance(value, str):
        a1 = digit.index(value[1]) * 16 + digit.index(value[2])
        a2 = digit.index(value[3]) * 16 + digit.index(value[4])
        a3 = digit.index(value[5]) * 16 + digit.index(value[6])
        return (a1, a2, a3)

def color_dist(c1, c2):
    return sum((a-b)**2 for a, b in zip(to_hsv(c1), to_hsv(c2)))

def to_hsv(color):
    return rgb_to_hsv(*[x/255.0 for x in color])

def min_color_diff( color_to_match, colorList):
    return min((color_dist(color_to_match, get_color_set.colorToRGB(test)), test)for test in colorList)

def sub(num1,num2):
    if num1 > num2:
        return num1 - num2
    else:
        return num2 - num1

def checkColor(color1, color2):
    class0Color1 = min(
        (color_dist(get_color_set.colorToRGB(color2), get_color_set.colorToRGB(col)), col, "class0") for col in colorSet_reference.colorTriple0)
    class1Color1 = min(
        (color_dist(get_color_set.colorToRGB(color2), get_color_set.colorToRGB(col)), col, "class1") for col in colorSet_reference.colorTriple1)
    classColor1 = min(class0Color1, class1Color1)
    # print classColor1

    class0Color0 = min(
        (color_dist(get_color_set.colorToRGB(color1), get_color_set.colorToRGB(col)), col, "class0") for col in colorSet_reference.colorTriple0)
    class1Color0 = min(
        (color_dist(get_color_set.colorToRGB(color1), get_color_set.colorToRGB(col)), col, "class1") for col in colorSet_reference.colorTriple1)
    classColor0 = min(class0Color0, class1Color0)
    # print classColor0
    #
    # print sub(colorSet_reference.colorTriples[classColor0[2]].index(classColor0[1]),
    #           colorSet_reference.colorTriples[classColor1[2]].index(classColor1[1]))
    if classColor0[2] == classColor1[2] and sub(colorSet_reference.colorTriples[classColor0[2]].index(classColor0[1]),
                colorSet_reference.colorTriples[classColor1[2]].index(classColor1[1])) <= 1:
        return 1
    else:
        return 0

# print checkColor('#4E51A9', '#6C70EA')
# '#4E51A9', '#585BBE',   6C70EA
# print checkColor('#8B4513', '#955423')


def get_backColor(img, bound):
    sp = img.shape  # 获取图片维度
    width = sp[0]  # 宽度
    height = sp[1]  # 高度
    # print width
    # print height
    # print bound
    a = bound.split('[')[1].split(',')[0]
    b = bound.split(',')[1].split(']')[0]
    a1 = bound.split('[')[2].split(',')[0]
    b1 = bound.split(',')[2].split(']')[0]
    imgW = int(a1) - int(a)
    yh = int(a) + 10
    xw = int(b1) - 10
    yh1 = int(a1) - 10
    xw1 = int(b) + 10
    if yh in range(height):
        if xw in range(width):
            # print yh,xw
            backColor = colorToRGB((img[xw, yh, 2], img[xw, yh, 1], img[xw, yh, 0]))
    if yh1 in range(height):
        if xw1 in range(width):
            # print yh,xw
            backColor1 = colorToRGB((img[xw1, yh1, 2], img[xw1, yh1, 1], img[xw1, yh1, 0]))
    # print img[1,64]
    if checkColor(backColor, backColor1):
        # print backColor
        return backColor
    else:
        backColor = ''
        return backColor

def checkColorSet(img, colorSet, bound):
    backColor = get_backColor(img, bound)
    # print backColor
    if backColor == '':
        return "error"
    if checkColor(colorSet[1], backColor) == 1:
        return 1
    elif checkColor(colorSet[0], backColor) == 1:
        return 0
    else:
        return "error"

# img = cv2.imread('/home/zyx/Desktop/Xbot-main2/main-folder/results/outputs/com.fullsix.android.labanquepostale.accountaccess/screenshot/com.fullsix.android.labanquepostale.accountaccess.activities.AccountsListActivity/screenshot_1640599664295.png')
# bound = '[147,505][879,568]'
# colorSet = ['#7997CB', '#FFFFFF']
# print checkColorSet(img, colorSet, bound)