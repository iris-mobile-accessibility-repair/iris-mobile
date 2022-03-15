# encoding: utf-8
import math

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

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
# print (luminanace((255, 255, 255))) / (luminanace((0, 0, 255)))

def con_contrast(rgb1, rgb2):
    if isinstance(rgb1, tuple) and isinstance(rgb2, tuple):
        if luminanace(rgb1) < luminanace(rgb2):
            return luminanace(rgb2) / luminanace(rgb1)
        return luminanace(rgb1) / luminanace(rgb2)
    elif isinstance(rgb1, str) and isinstance(rgb2, str):
        if luminanace(colorToRGB(rgb1)) < luminanace(colorToRGB(rgb2)):
            return luminanace(colorToRGB(rgb2)) / luminanace(colorToRGB(rgb1))
        return luminanace(colorToRGB(rgb1)) / luminanace(colorToRGB(rgb2))

def get_dominant_colors(infile, num_colors):
    image = Image.open(infile)

    # 缩小图片，否则计算机压力太大
    small_image = image.resize((80, 80))
    result = small_image.convert("P", palette=Image.ADAPTIVE, colors=num_colors)

    # 找到主要的颜色
    result = result.convert('RGB')
    main_colors = result.getcolors()
    # print main_colors
    main_colors.sort(reverse=True)
    # print main_colors
    colors = []
    colors_Max = []
    colors_Max_01 = []
    num_Max_second_List = []
    num_Max_second_List_01 = []

    num_Max_List = main_colors[0][1]
    num_Max_List_01 = [float((main_colors[0][1])[i]) / 255 for i in range(3)]
    if len(main_colors) == 1:
        num_Max_second_List = main_colors[0][1]
        num_Max_second_List_01 = [float((main_colors[0][1])[i]) / 255 for i in range(3)]
    elif len(main_colors) > 1:
        num_Max_second_List = main_colors[1][1]
        num_Max_second_List_01 = [float((main_colors[1][1])[i]) / 255 for i in range(3)]

    for count, col in main_colors:
        # print([float(col[i])/255 for i in range(3)])#RGB转RGBA，可输出RGBA色号
        colors.append([float(col[i]) / 255 for i in range(3)])

    colors_Max.append(num_Max_List)
    colors_Max.append(num_Max_second_List)
    colors_Max_01.append(num_Max_List_01)
    colors_Max_01.append(num_Max_second_List_01)

    return colors, colors_Max, colors_Max_01

def get_dominant_nonIssueColors(imageFile, num_colors):
    num_Max_second_List = []
    num_Max_second_List_01 = []
    image = Image.open(imageFile)
    # 缩小图片，否则计算机压力太大
    small_image = image.resize((80, 80))
    result = small_image.convert("P", palette=Image.ADAPTIVE, colors=num_colors)

    # 找到主要的颜色
    result = result.convert('RGB')
    main_colors = result.getcolors()
    # print main_colors
    main_colors.sort(reverse=True)
    # print main_colors
    colors = []
    colors_Max = []
    colors_Max_01 = []

    for count, col in main_colors:
        # print([float(col[i])/255 for i in range(3)])#RGB转RGBA，可输出RGBA色号
        colors.append([float(col[i]) / 255 for i in range(3)])

    num_Max_List = main_colors[0][1]
    num_Max_List_01 = [float((main_colors[0][1])[i]) / 255 for i in range(3)]

    # print main_colors
    # print max((con_contrast(num_Max_List, main_colors[1][1]), main_colors[1][1]))
    if len(main_colors) == 1:
        maxContrast = 1
    elif len(main_colors) == 2:
        maxContrast = con_contrast(num_Max_List, main_colors[1][1])
    else:
        maxContrast = max((con_contrast(num_Max_List, main_colors[r][1]), main_colors[r][1]) for r in range(1, len(main_colors)-1))[0]
    if len(main_colors) == 1 or maxContrast < 4.5:
        colors_Max = []
        colors_Max_01 = []
        return colors, colors_Max, colors_Max_01
    else:
        for r in range(1, len(main_colors)-1):
            if con_contrast(num_Max_List, main_colors[r][1]) > 4.5:
                num_Max_second_List = main_colors[r][1]
                num_Max_second_List_01 = [float((main_colors[r][1])[i]) / 255 for i in range(3)]
                break

        colors_Max.append(num_Max_List)
        colors_Max.append(num_Max_second_List)
        colors_Max_01.append(num_Max_List_01)
        colors_Max_01.append(num_Max_second_List_01)
        if num_Max_second_List == []:
            colors_Max = []
            colors_Max_01 = []

    # colors:[[0.8392156862745098, 0.8431372549019608, 0.8431372549019608], [0.9803921568627451, 0.9803921568627451, 0.9803921568627451], [0.10980392156862745, 0.10980392156862745, 0.10980392156862745]]
    # colors_Max:[(214, 215, 215), (250, 250, 250)]
    # colors_Max_01:[[0.8392156862745098, 0.8431372549019608, 0.8431372549019608], [0.9803921568627451, 0.9803921568627451, 0.9803921568627451]]
        return colors, colors_Max, colors_Max_01

# (214, 215, 215) <-> #D6D7D7
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

def get_nonIssueColorSet(imageFile):
    colorSet = []
    # num_colors -> set to 20
    colorTuples = get_dominant_nonIssueColors(imageFile, 20)[1]
    # print colorTuples
    for colorTuple in colorTuples:
        colorSet.append(colorToRGB(colorTuple))
    return colorSet

def get_colorSet(imageFile):
    colorSet = []
    # num_colors -> set to 20
    colorTuples = get_dominant_colors(imageFile, 20)[1]
    for colorTuple in colorTuples:
        colorSet.append(colorToRGB(colorTuple))
    return colorSet

# imageFile = "/home/zyx/Desktop/result/com.arosbilataman.arabicriiwayat/IssueXML/" \
#             "1_com.arosbilataman.arabicriiwayat_com.arosbilataman.arabicriiwayat.RecipeDetail_1_TextView.png"
# print get_colorSet(imageFile)
#
# color = get_dominant_colors(imageFile, 20)
# plt.figure(dpi=150)
# plt.bar(range(len(color[2])), np.ones(len(color[2])), color=(color[2]))
# plt.xticks(range(len(color[2])), (range(len(color[2]))))
# plt.show()

#
# nonIsuueImagePath = "/home/zyx/Desktop/result000/sick.sick.fifty/nonIssueXML/2_sick.sick.fifty_sick.sick.fifty.NextActivity_2_ImageView.png"
# print get_nonIssueColorSet(nonIsuueImagePath)
# # print con_contrast('#030304', '#F3F3F3')
# print con_contrast((72, 80, 107), (4, 4, 5))
# print colorToRGB((72, 80, 107))
# print colorToRGB((4, 4, 5))

# print get_colorSet('/home/zyx/com.link.kuaiji/res/drawable-hdpi-v4/add_f1.png')
