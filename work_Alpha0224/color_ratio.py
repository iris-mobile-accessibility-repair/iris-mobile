# encoding: utf-8
import math
from colorsys import rgb_to_hsv
import get_color_set
import colorSet_reference
import cv2

# # colors = dict((
# # ((196, 2, 51), "RED"),
# # ((255, 165, 0), "ORANGE"),
# # ((255, 205, 0), "YELLOW"),
# # ((0, 128, 0), "GREEN"),
# # ((0, 0, 255), "BLUE"),
# # ((127, 0, 255), "VIOLET"),
# # ((0, 0, 0), "BLACK"),
# # ((255, 255, 255), "WHITE"),))
# colors = dict((
# ((60, 179, 113), "RED"),
# ((115, 211, 156), "ORANGE"),
# ((0, 153, 204), "YELLOW"),
# ((116, 212, 157), "GREEN"),
# ((115, 211, 156), "BLUE"),
# ((115, 211, 156), "VIOLET"),
# ((0, 0, 0), "BLACK"),
# ((255, 255, 255), "WHITE"),))
# def to_hsv(color):
#     """ converts color tuples to floats and then to hsv """
#     return rgb_to_hsv(*[x/255.0 for x in color])
#
# def color_dist(c1, c2):
#     """ returns the squared euklidian distance between two color vectors in hsv space """
#     return sum((a-b)**2 for a, b in zip(to_hsv(c1), to_hsv(c2)))
# def min_color_diff(color_to_match, colors):
#     """ returns the `(distance, color_name)` with the minimal distance to `colors`"""
#     return min((color_dist(color_to_match, test), colors[test]) for test in colors)
#
# color_to_match = (255,255,0)
# # print to_hsv(color_to_match)
# print min_color_diff(color_to_match, colors)

# def HSVDistance(hsv_1,hsv_2):
#     H_1,S_1,V_1 = hsv_1
#     H_2,S_2,V_2 = hsv_2
#     R=100
#     angle=30
#     h = R * math.cos(angle / 180 * math.pi)
#     r = R * math.sin(angle / 180 * math.pi)
#     x1 = r * V_1 * S_1 * math.cos(H_1 / 180 * math.pi);
#     y1 = r * V_1 * S_1 * math.sin(H_1 / 180 * math.pi);
#     z1 = h * (1 - V_1);
#     x2 = r * V_2 * S_2 * math.cos(H_2 / 180 * math.pi);
#     y2 = r * V_2 * S_2 * math.sin(H_2 / 180 * math.pi);
#     z2 = h * (1 - V_2);
#     dx = x1 - x2;
#     dy = y1 - y2;
#     dz = z1 - z2;
#     return math.sqrt(dx * dx + dy * dy + dz * dz)


# def ColourDistance(rgb_1, rgb_2):
#     R_1, G_1, B_1 = rgb_1
#     R_2, G_2, B_2 = rgb_2
#     rmean = (R_1 + R_2) / 2
#     R = R_1 - R_2
#     G = G_1 - G_2
#     B = B_1 - B_2
#     return math.sqrt((2 + rmean / 256) * (R ** 2) + 4 * (G ** 2) + (2 + (255 - rmean) / 256) * (B ** 2))
#
# print HSVDistance(to_hsv((255,255,0)),to_hsv((127, 0, 255)))
# print min((HSVDistance(to_hsv(color_to_match), to_hsv(test)), colors[test]) for test in colors)
# print ColourDistance((255,255,0),(116, 212, 157))
# print min((ColourDistance(color_to_match, test), colors[test]) for test in colors)


def luminanace(rgb):
    rgb_lum = []
    for v in rgb:
        v = float(v) / 255
        if v <= 0.03928:
            v = v / 12.92
        else:
            v = math.pow(((v+0.055)/1.055), 2.4)
        rgb_lum.append(v)
    # print rgb_lum
    # print rgb_lum[0] * 0.2126 + rgb_lum[1] * 0.7152 + rgb_lum[2] * 0.0722
    return rgb_lum[0] * 0.2126 + rgb_lum[1] * 0.7152 + rgb_lum[2] * 0.0722 + 0.05
print (luminanace((255, 255, 255))) / (luminanace((0, 0, 255)))

def ratioNum(txt):
    if txt.find("greater than 4.50 for small text") != -1:
        colorRatio = 4.5
    else:
        colorRatio = 3
    return colorRatio

# print ratioNum("The item's text contrast ratio is 3.25. This ratio is based on an estimated foreground color of #008CFF and an estimated background color of #FAFAFA. Consider using a contrast ratio greater than 4.50 for small text, or 3.00 for large text.")
# Tname = "aaa"
# txt = "name=\"aaa\""
# if txt.startswith("name=\"%s\"" %Tname):
#     print "hhhh"

# sets = {"aa":"s","b":"s","c":"s"}
# sets2 = {"ff":"s"}
# for i in sets:
#     if i=='b':
#         sets['bbb'] = sets[i]
#         del sets[i]
# print sets
# print u'Depuis la France métropolitaine ou les DOM appelez au :'
# dictMerged1 = dict(list(sets.items()) + list(sets2.items()) )
# print dictMerged1


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

def ifFit(color1, color2, color3):
    class0Color1 = min(
        (color_dist(get_color_set.colorToRGB(color2), get_color_set.colorToRGB(col)), col, "class0") for col in colorSet_reference.colorTriple0)
    class1Color1 = min(
        (color_dist(get_color_set.colorToRGB(color2), get_color_set.colorToRGB(col)), col, "class1") for col in colorSet_reference.colorTriple1)
    classColor1 = min(class0Color1, class1Color1)
    print classColor1
    if color1 != '':
        class0Color0 = min(
            (color_dist(get_color_set.colorToRGB(color1), get_color_set.colorToRGB(col)), col, "class0") for col in colorSet_reference.colorTriple0)
        class1Color0 = min(
            (color_dist(get_color_set.colorToRGB(color1), get_color_set.colorToRGB(col)), col, "class1") for col in colorSet_reference.colorTriple1)
        classColor0 = min(class0Color0, class1Color0)
        print classColor0
    else:
        classColor0 = (1, '', classColor1[2])

    finalColor = ''

    if classColor0[1] != '' and classColor0[2] == classColor1[2] and \
            sub(colorSet_reference.colorTriples[classColor0[2]].index(classColor0[1]),
                colorSet_reference.colorTriples[classColor1[2]].index(classColor1[1])) <= 5:
        print classColor0[1]
        print colorSet_reference.colorTriples[classColor0[2]].index(classColor0[1])
        print classColor1[1]
        print colorSet_reference.colorTriples[classColor1[2]].index(classColor1[1])
        # finalColor = classColor0[1]
        finalColor = color1
    else:
        if get_color_set.con_contrast(classColor1[1], color3) >= 4.5:
            finalColor = classColor1[1]
        # if get_color_set.con_contrast(classColor1[1], color3) >= 4.5:
        #     finalColor = classColor1[1]
        else:
            # print get_color_set.con_contrast(classColor1[1], '#FAFAFA')
            locat = colorSet_reference.colorTriples[classColor1[2]].index(classColor1[1])
            subNum = locat
            addNum = locat
            for i in range(0, 13):
                subNum = subNum - 1
                if subNum > -1:
                    print subNum
                    print get_color_set.con_contrast(colorSet_reference.colorTriples[classColor1[2]][subNum], color3)
                    if get_color_set.con_contrast(colorSet_reference.colorTriples[classColor1[2]][subNum], color3) >= 4.5:
                        finalColor = colorSet_reference.colorTriples[classColor1[2]][subNum]
                        break
                addNum = addNum + 1
                if addNum < len(colorSet_reference.colorTriples[classColor1[2]]):
                    print addNum
                    print get_color_set.con_contrast(colorSet_reference.colorTriples[classColor1[2]][addNum], color3)
                    if get_color_set.con_contrast(colorSet_reference.colorTriples[classColor1[2]][addNum], color3) >= 4.5:
                        finalColor = colorSet_reference.colorTriples[classColor1[2]][addNum]
                        break

    if finalColor == '':
        if get_color_set.con_contrast("#000000", color3) >= 4.5:
            finalColor = "#000000"
        elif get_color_set.con_contrast("#FFFFFF", color3) >= 4.5:
            finalColor = "#FFFFFF"
    return finalColor

print ifFit('', '#67BD8B', '#73D39C')


# RGB渐变色
def get_multi_colors_by_rgb(begin_color, end_color, color_count):
    if color_count < 2:
        return []

    colors = []
    steps = [(end_color[i] - begin_color[i]) / (color_count - 1) for i in range(3)]
    for color_index in range(color_count):
        colors.append([int(begin_color[i] + steps[i] * color_index) for i in range(3)])

    return colors

# print get_multi_colors_by_rgb((255,0,0), (0,255,0), 13)






# check colorSet right or not
def checkColor(color1, color2):
    class0Color1 = min(
        (color_dist(get_color_set.colorToRGB(color2), get_color_set.colorToRGB(col)), col, "class0") for col in colorSet_reference.colorTriple0)
    class1Color1 = min(
        (color_dist(get_color_set.colorToRGB(color2), get_color_set.colorToRGB(col)), col, "class1") for col in colorSet_reference.colorTriple1)
    classColor1 = min(class0Color1, class1Color1)
    print classColor1

    class0Color0 = min(
        (color_dist(get_color_set.colorToRGB(color1), get_color_set.colorToRGB(col)), col, "class0") for col in colorSet_reference.colorTriple0)
    class1Color0 = min(
        (color_dist(get_color_set.colorToRGB(color1), get_color_set.colorToRGB(col)), col, "class1") for col in colorSet_reference.colorTriple1)
    classColor0 = min(class0Color0, class1Color0)
    print classColor0

    print sub(colorSet_reference.colorTriples[classColor0[2]].index(classColor0[1]),
              colorSet_reference.colorTriples[classColor1[2]].index(classColor1[1]))
    if classColor0[2] == classColor1[2] and sub(colorSet_reference.colorTriples[classColor0[2]].index(classColor0[1]),
                colorSet_reference.colorTriples[classColor1[2]].index(classColor1[1])) <= 1:
        return 1
    else:
        return 0

# print checkColor('#4E51A9', '#6C70EA')
# '#4E51A9', '#585BBE',   6C70EA

def get_backColor(img, bound):
    sp = img.shape  # 获取图片维度
    width = sp[0]  # 宽度
    height = sp[1]  # 高度
    # print width
    # print height
    a = bound.split('[')[1].split(',')[0]
    b = bound.split(',')[1].split(']')[0]
    yh = int(a) + 5
    xw = int(b) + 5
    if yh in range(height):
        if xw in range(width):
            print yh,xw
            backColor = get_color_set.colorToRGB((img[xw, yh, 2], img[xw, yh, 1], img[xw, yh, 0]))
    # print img[1,64]
    return backColor


def checkColorSet(colorSet, backColor):
    if checkColor(colorSet[1], backColor) == 1:
        return 1
    elif checkColor(colorSet[0], backColor) == 1:
        return 0
    else:
        return "error"

# img = cv2.imread('/home/zyx/Desktop/Xbot-main/main-folder/results/outputs1/qisas.maghribi/screenshot/qisas.maghribia.AboutApp/screenshot_1637955974398.png')
#
# backColor = get_backColor(img, '[13,89][1054,146]')
# colorSet = ['#D36022', '#FFFFFF']
# print checkColorSet(colorSet, backColor)
