# encoding: utf-8
from operator import itemgetter
import os
import cv2
from PIL import Image
from colorsys import rgb_to_hsv
import changeImageColor

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

    return main_colors


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

def spiltTransparent(imgPath):
    img = cv2.imread(imgPath, -1)
    sp = img.shape  # 获取图片维度
    width = sp[0]  # 宽度
    height = sp[1]  # 高度
    num0 = 0
    num = 0
    for yh in range(height):
        for xw in range(width):
            color_d = img[xw, yh]  # 遍历图像每一个点，获取到每个点4通道的颜色数据
            if len(color_d) == 3:
                return 0
            if (color_d[3] != 0):  # 最后一个通道为透明度，如果其值为0，即图像是透明
                num = num + 1
            else:
                num0 = num0 + 1
    # print num0, num
    if num > num0:
        return 0
    else:
        return 1

def color_dist(c1, c2):
    return sum((a-b)**2 for a, b in zip(to_hsv(c1), to_hsv(c2)))
def to_hsv(color):
    return rgb_to_hsv(*[x/255.0 for x in color])

def spiltSame(colorT, main_colors):
    colorRemove = []
    for color in main_colors:
        if color[1][0] in range(colorT[1][0] - 10, colorT[1][0] + 10) and color[1][1] in range(colorT[1][1] - 10,
                                                                                               colorT[1][1] + 10) and \
                color[1][2] in range(colorT[1][2] - 10, colorT[1][2] + 10):
            if color != colorT:
                colorRemove.append(color)
        elif color[0] < 40:
            colorRemove.append(color)
    for c in colorRemove:
        main_colors.remove(c)
    return main_colors


# Judge single color
# necessary condition！！！
def imageCondition1(imgPath):
    re = 0
    main_colors = get_dominant_colors(imgPath, 10)
    # print main_colors
    if spiltTransparent(imgPath) == 1 and len(main_colors) != 1:
        del (main_colors[0])
    if len(main_colors) < 3:
        re = 1
    else:
        colorT = main_colors[0]
        main_colors0 = spiltSame(colorT, main_colors)
        # print main_colors0
        # print main_colors
        if len(main_colors) != 1:
            colorT = main_colors[1]
            main_colors1 = spiltSame(colorT, main_colors)
            # print main_colors1
            if len(main_colors0) < len(main_colors1):
                main_colors = main_colors0
            else:
                main_colors = main_colors1
            if len(main_colors) < 3:
                re = 1
            elif main_colors[2][0] < 15:
                re = 1
        else:
           re = 1
    # print main_colors
    return re, main_colors

# def spiltMainColors(imgPath):
#     # print spiltTransparent(imgPath)
#     main_colors = get_dominant_colors(imgPath, 10)
#     # print main_colors
#     if spiltTransparent(imgPath) == 1:
#         del (main_colors[0])
#     # print main_colors
#     condition1, spiltMainColors = imageCondition1(main_colors)
#     print spiltMainColors
#     return condition1

# # imgPath = '/home/zyx/Desktop/work/apktool01/com.darsh.galleryorganizer2/res/drawable-hdpi-v4/ic_add_white_24dp.png'
# imgPath = 'G:/1103/work/apktool0/com.link.kuaiji/res/drawable-hdpi-v4/add_f1.png'
# print imageCondition1(imgPath)[0]
# # print spiltMainColors(imgPath)
# # print colorToRGB('#67BD8B')
# # print colorToRGB((100, 189, 138))


# conponentClass
def imageCondition2(conponentClass):
    re = 0
    if conponentClass == 'ImageButton' or conponentClass == 'Button':
        re = 1
    return re

# print imageCondition2('ImageButton')

# position
def imageCondition3(bound):
    top = 250
    bottom = 1600
    re = 0
    if bound.split(',')[2].split(']')[0] < top or bound.split(',')[1].split(']')[0] > bottom:
        re = 1
    return re

# bound = '[891,1605][1038,1752]'
# print imageCondition3(bound)

# semantics
def imageCondition4(id, imageSourceName):
    re = 0
    semList = ['CLOSE', 'CANCEL', 'CLEAR', 'REMOVE', 'DELETE',
               'ADD', 'ABOUT', 'SHARE', 'SEARCH', 'MENU', 'FOLDER', 'SET',
               'UP', 'DOWN']
    if id.upper().find('BUTTON') != -1 or imageSourceName.upper().find('BTN') != -1:
        return 1
    for sem in semList:
        if id.upper().find(sem) != -1 or imageSourceName.upper().find(sem) != -1:
            return 1
    return re

# {'btnPhone': (['phone'], '#00DCFF')}
# print imageCondition4('setting', 'phone')

def judgeNeedChage(color_to_match, imageList):
    imageSort = []
    imageToChange = []
    for image in imageList:
        # print image
        # # print spiltMainColors(image)
        # print imageCondition1(image)[1]
        imageSort.append(min(
            (color_dist(colorToRGB(color_to_match), test[1]), test[0], image) for test in imageCondition1(image)[1]))
        # print imageSort
    # imageSort = [(0.007445290447416104, 4450), (0.369600824537783, 9999), (0.007445290447416104, 6400)]
    # 如果第一个条件相同 则按第二个条件排序
    imageSort = sorted(imageSort, key=lambda x: (x[0], -x[1]))
    # print imageSort
    imageToChange.append(imageSort[0][2])
    if len(imageSort) > 1:
        for i in range(1, len(imageSort)):
            if imageSort[i][0] == imageSort[0][0]:
                imageToChange.append(imageSort[i][2])
    return imageToChange

def changeSourceImage(decom_Path, imageId_NameF, id_bound_colorSet):
    imagesToChange = {}
    imagesToChangeB = {}
    imagesToChangeF = {}
    for bound in imageId_NameF:
        imagesToChangeB[bound] = []
        if imageId_NameF[bound][2] in imageId_NameF[bound][0]:
            imageNames = [imageId_NameF[bound][2]]
        else:
            imageNames = imageId_NameF[bound][0]
        # print imageNames
        for drawablesFloder in os.listdir(os.path.join(decom_Path, "res")):
            if not drawablesFloder.startswith("drawable"):
                continue
            # print drawablesFloder
            drawablePath = os.path.join(decom_Path, "res", drawablesFloder)
            for image in imageNames:
                if image + '.png' in os.listdir(drawablePath):
                    imagePath = os.path.join(drawablePath, image + '.png')
                    c1 = imageCondition1(imagePath)
                    c2 = imageCondition2(imageId_NameF[bound][3])
                    c3 = imageCondition3(bound)
                    c4 = imageCondition4(imageId_NameF[bound][2], image)
                    if c1 == 0:
                        continue
                    if c2 + c3 + c4 > 0:
                        imagesToChangeB[bound].append(imagePath)
                        imagesToChange[imagePath] = (id_bound_colorSet[imageId_NameF[bound][2]][0][0], imageId_NameF[bound][1])
    # for imageToChange in imagesToChange:
    #     img = changeImageColor.transparence2white(imageToChange, imagesToChange[imageToChange])
    #     cv2.imwrite('aaa.png', img)
    for boundItem in imagesToChangeB:
        imageList = imagesToChangeB[boundItem]
        if imageList == []:
            continue
        color_to_match = imagesToChange[imageList[0]][0]
        # print judgeNeedChage(color_to_match, imageList)
        imagesToC = judgeNeedChage(color_to_match, imageList)

        # print imagesToC
        for im in imagesToC:
            imagesToChangeF[im] = imagesToChange[im][1]
    # print imagesToChangeB
    # print imagesToChangeF
    # print imagesToChange
    return imagesToChangeF

# HOME_PATH = 'G:/1103/work/apktool01'
# APKName = "com.link.kuaiji"
# imageId_NameF = {'[540,1689][677,1794]': (['list_item', 'qq', 'list_item_divide'], '#000000', 'imageView2', 'ImageView'), '[415,1561][664,1679]': (['add_f1'], '#000000', 'i2', 'ImageView'), '[415,1676][664,1794]': (['add_f2'], '#000000', 'i1', 'ImageView'), '[0,87][158,161]': (['back'], '#3C3C3C', 'back', 'ImageView'), '[143,1689][280,1794]': (['list_item_divide_operate', 'upload', 'weibo2', 'list_item_divide'], '#000000', 'imageView1', 'ImageView')}
# id_bound_colorSet = {'qq': (['#73D39C', '#FFFFFF'], 3, 'LoginActivity', '', 'Text contrast'), 'weibo': (['#73D39C', '#FFFFFF'], 3, 'LoginActivity', '', 'Text contrast'), 'calander': (['#FFFFFF', '#73D39C'], 3, 'EntranceActivity', '', 'Text contrast'), 'imageView1': (['#73D39C', '#FFFFFF'], 3, 'LoginActivity', '', 'Image contrast'), 'imageView2': (['#73D39C', '#FFFFFF'], 3, 'LoginActivity', '', 'Image contrast'), 'i1': (['#67BD8B', '#73D39C'], 3, 'EntranceActivity', '', 'Image contrast'), '\xe8\xae\xb0\xe8\xb4\xa6': (['#45C01A', '#FFFFFF'], 3, 'EntranceActivity', 'TextView', 'Text contrast'), 'header_income_outcome': (['#FFFFFF', '#73D39C'], 3, 'EntranceActivity', '', 'Text contrast'), 'back': (['#FFFFFF', '#73D39C'], 3, 'RegisterActivity', '', 'Image contrast'), 'month': (['#3CB371', '#FFFFFF'], 3, 'EntranceActivity', '', 'Text contrast'), 'remindText': (['#FFFFFF', '#73D39C'], 3, 'EntranceActivity', '', 'Text contrast'), 'button2': (['#73D39C', '#FFFFFF'], 3, 'LoginActivity', '', 'Text contrast'), 'button1': (['#73D39C', '#FFFFFF'], 3, 'RegisterActivity', '', 'Text contrast'), 'time': (['#FFFFFF', '#73D39C'], 3, 'EntranceActivity', '', 'Text contrast'), 'year': (['#3CB371', '#FFFFFF'], 3, 'EntranceActivity', '', 'Text contrast'), 'editText2': (['#808080', '#FFFFFF'], 4.5, 'RegisterActivity', '', 'Text contrast'), 'textView2': (['#FFFFFF', '#3CB371'], 3, 'RegisterActivity', '', 'Text contrast'), 'textView1': (['#3CB371', '#FFFFFF'], 3, 'RegisterActivity', '', 'Text contrast'), 'editText1': (['#0099CC', '#FFFFFF'], 4.5, 'RegisterActivity', '', 'Text contrast'), 'editText3': (['#808080', '#FFFFFF'], 4.5, 'RegisterActivity', '', 'Text contrast'), 'i2': (['#73D39C', '#FFFFFF'], 3, 'EntranceActivity', '', 'Image contrast')}
#
# decom_Path = os.path.join(HOME_PATH, APKName)
#
#
# imagesToChangeF = changeSourceImage(decom_Path, imageId_NameF, id_bound_colorSet)
# # print imagesToChange
# print imagesToChangeF










imageList = ['/home/zyx/Desktop/work2/apktool/com.link.kuaiji/res/drawable-hdpi-v4/qq.png',
             '/home/zyx/Desktop/work2/apktool/com.link.kuaiji/res/drawable-hdpi-v4/list_item_divide.png',
             '/home/zyx/Desktop/work2/apktool/com.link.kuaiji/res/drawable-hdpi-v4/list_item.png']


# color_to_match = '#67BD8B'
# imageSort = []
# imageToChange = []
# for image in imageList:
#     # print image
#     # print spiltMainColors(image)
#     # print imageCondition1(image)[1]
#     imageSort.append(min((color_dist(colorToRGB(color_to_match), test[1]), test[0], image) for test in imageCondition1(image)[1]))
#     # print imageSort
# # imageSort = [(0.007445290447416104, 4450), (0.369600824537783, 9999), (0.007445290447416104, 6400)]
# # 如果第一个条件相同 则按第二个条件排序
# imageSort = sorted(imageSort, key=lambda x: (x[0], -x[1]))
# print imageSort
# imageToChange.append(imageSort[0][2])
# if len(imageSort) > 1:
#     for i in range(1, len(imageSort)):
#         if imageSort[i][0] == imageSort[0][0]:
#             imageToChange.append(imageSort[i][2])
# print imageToChange