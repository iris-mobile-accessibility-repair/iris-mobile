# encoding: utf-8
import math

import numpy as np

import get_color_set
import colorSet_reference
from colorsys import rgb_to_hsv

def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v

def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b

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
    
# r = 180
# g = 235
# b = 250
# r = 255
# g = 255
# b = 255
# print(rgb2hsv(r, g, b))
#
# # h = 360
# # s = 0.8
# # v = 1.0
# h = 0
# s = 0
# v = 0.5
# print(hsv2rgb(h, s, v))
# print(colorToRGB(hsv2rgb(h, s, v)))
# print(colorToRGB("#B4EBFA"))




def to_hsv(color):
    return rgb_to_hsv(*[x/255.0 for x in color])

def color_dist(c1, c2):
    return sum((a-b)**2 for a, b in zip(to_hsv(c1), to_hsv(c2)))

def min_color_diff( color_to_match, colorList):
    return min((color_dist(color_to_match, get_color_set.colorToRGB(test)), test)for test in colorList)

def sub(num1,num2):
    if num1 > num2:
        return num1 - num2
    else:
        return num2 - num1

def get_changeColor2(color1, color2, color3, ratio):
    class0Color1 = min(
        (color_dist(get_color_set.colorToRGB(color2), get_color_set.colorToRGB(col)), col, "class0") for col in colorSet_reference.colorTriple0)
    class1Color1 = min(
        (color_dist(get_color_set.colorToRGB(color2), get_color_set.colorToRGB(col)), col, "class1") for col in colorSet_reference.colorTriple1)
    classColor1 = min(class0Color1, class1Color1)
    print(classColor1[2])
    vG = 0.01
    (r, g, b) = colorToRGB(color2)
    (h, s, v) = rgb2hsv(r, g, b)
    print(h, s, v)
    finalColor = ''
    if classColor1[2] == "class1":
        # print(colorToRGB(hsv2rgb(h, s, v-0.1)))

        subNum = v
        addNum = v
        while 1 == 1:
            subNum = subNum - vG
            if subNum >= 0:
                if get_color_set.con_contrast(colorToRGB(hsv2rgb(h, s, subNum)), color3) >= 4.5:
                    finalColor = colorToRGB(hsv2rgb(h, s, subNum))
                    break
            addNum = addNum + vG
            if addNum <= 1:
                if get_color_set.con_contrast(colorToRGB(hsv2rgb(h, s, addNum)), color3) >= 4.5:
                    finalColor = colorToRGB(hsv2rgb(h, s, addNum))
                    break
            if subNum < 0 and addNum > 1:
                break
    elif classColor1[2] == "class0":
        sG = float(1/3)
        # print(float(sG*2))
        tag1 = 0
        tag2 = 0
        if s >= 0 and s < sG:
            tag1 = 0
            tag2 = sG
        elif s >= sG and s < sG * 2:
            tag1 = sG
            tag2 = sG * 2
        elif s >= sG * 2 and s <= 1:
            tag1 = sG * 2
            tag2 = 1
        subNum = s
        addNum = s
        while 1 == 1:
            subNum = subNum - vG
            if subNum >= tag1:
                # print((h, subNum, v))
                # print(get_color_set.con_contrast(colorToRGB(hsv2rgb(h, subNum, v)), color3))
                if get_color_set.con_contrast(colorToRGB(hsv2rgb(h, subNum, v)), color3) >= 4.5:
                    finalColor = colorToRGB(hsv2rgb(h, subNum, v))
                    break
            addNum = addNum + vG
            if addNum <= tag2:
                # print((h, addNum, v))
                # print(get_color_set.con_contrast(colorToRGB(hsv2rgb(h, addNum, v)), color3))
                if get_color_set.con_contrast(colorToRGB(hsv2rgb(h, addNum, v)), color3) >= 4.5:
                    finalColor = colorToRGB(hsv2rgb(h, addNum, v))
                    break
            # print(subNum, addNum)
            if subNum < tag1 and addNum > tag2:
                # break
                # h
                for i in range(1, 31):
                    if i < 31:
                        if h < i:
                            hT = 360 + h - i
                        else:
                            hT = h - i
                        # print(get_color_set.con_contrast(colorToRGB(hsv2rgb(hT, s, v)), color3))
                        if get_color_set.con_contrast(colorToRGB(hsv2rgb(hT, s, v)), color3) >= 4.5:
                            finalColor = colorToRGB(hsv2rgb(hT, s, v))
                            break
                    if i < 31:
                        # print(get_color_set.con_contrast(colorToRGB(hsv2rgb((h + i) % 360, s, v)), color3))
                        if get_color_set.con_contrast(colorToRGB(hsv2rgb((h + i) % 360, s, v)), color3) >= 4.5:
                            finalColor = colorToRGB(hsv2rgb((h + i) % 360, s, v))
                            # print(colorToRGB(hsv2rgb((h + i) % 360, s, v)))
                            break
                if finalColor != '':
                    break

                # change h,s
                for i in range(1, 31):
                    if i < 31:
                        if h < i:
                            hT = 360 + h - i
                        else:
                            hT = h - i

                        subNum1 = s
                        addNum1 = s
                        while 1 == 1:
                            subNum1 = subNum1 - vG
                            if subNum1 >= tag1:
                                # print(get_color_set.con_contrast(colorToRGB(hsv2rgb(hT, subNum1, v)), color3))
                                if get_color_set.con_contrast(colorToRGB(hsv2rgb(hT, subNum1, v)), color3) >= 4.5:
                                    finalColor = colorToRGB(hsv2rgb(hT, subNum1, v))
                                    break
                            addNum1 = addNum1 + vG
                            if addNum1 <= tag2:
                                # print(get_color_set.con_contrast(colorToRGB(hsv2rgb(hT, addNum1, v)), color3))
                                if get_color_set.con_contrast(colorToRGB(hsv2rgb(hT, addNum1, v)), color3) >= 4.5:
                                    finalColor = colorToRGB(hsv2rgb(hT, addNum1, v))
                                    break
                            if subNum1 < tag1 and addNum1 > tag2:
                                break
                    if i < 31:
                        subNum1 = s
                        addNum1 = s
                        while 1 == 1:
                            subNum1 = subNum1 - vG
                            if subNum1 >= tag1:
                                # print(get_color_set.con_contrast(colorToRGB(hsv2rgb((h + i) % 360, subNum1, v)), color3))
                                if get_color_set.con_contrast(colorToRGB(hsv2rgb((h + i) % 360, subNum1, v)), color3) >= 4.5:
                                    finalColor = colorToRGB(hsv2rgb((h + i) % 360, subNum1, v))
                                    break
                            addNum1 = addNum1 + vG
                            if addNum1 <= tag2:
                                # print(get_color_set.con_contrast(colorToRGB(hsv2rgb((h + i) % 360, addNum1, v)), color3))
                                if get_color_set.con_contrast(colorToRGB(hsv2rgb((h + i) % 360, addNum1, v)), color3) >= 4.5:
                                    finalColor = colorToRGB(hsv2rgb((h + i) % 360, addNum1, v))
                                    break
                            if subNum1 < tag1 and addNum1 > tag2:
                                break
                if finalColor != '':
                    break

                # V
                subNumV = v
                addNumV = v
                for i in range(1, 33):
                    subNumV = subNumV - vG
                    if subNumV >= 0:
                        if get_color_set.con_contrast(colorToRGB(hsv2rgb(h, s, subNumV)), color3) >= 4.5:
                            finalColor = colorToRGB(hsv2rgb(h, s, subNumV))
                            break
                    addNumV = addNumV + vG
                    if addNumV <= 1:
                        if get_color_set.con_contrast(colorToRGB(hsv2rgb(h, s, addNumV)), color3) >= 4.5:
                            finalColor = colorToRGB(hsv2rgb(h, s, addNumV))
                            break
                    if subNumV < 0 and addNumV > 1:
                        break

                break

    if finalColor == '':
        if get_color_set.con_contrast("#000000", color3) >= 4.5:
            finalColor = "#000000"
        elif get_color_set.con_contrast("#FFFFFF", color3) >= 4.5:
            finalColor = "#FFFFFF"

    print('finalColor')
    print(finalColor)
    return finalColor
    # if color1 != '':
    #     class0Color0 = min(
    #         (color_dist(get_color_set.colorToRGB(color1), get_color_set.colorToRGB(col)), col, "class0") for col in colorSet_reference.colorTriple0)
    #     class1Color0 = min(
    #         (color_dist(get_color_set.colorToRGB(color1), get_color_set.colorToRGB(col)), col, "class1") for col in colorSet_reference.colorTriple1)
    #     classColor0 = min(class0Color0, class1Color0)
    #     # print classColor0[1]
    # else:
    #     classColor0 = (1, '', classColor1[2])
    #
    # finalColor = ''
    # if classColor0[1] != '' and classColor0[2] == classColor1[2] and get_color_set.con_contrast(classColor0[1], color3) >= 4.5 and \
    #         sub(colorSet_reference.colorTriples[classColor0[2]].index(classColor0[1]),
    #             colorSet_reference.colorTriples[classColor1[2]].index(classColor1[1])) <= 13:
    #     finalColor = classColor0[1]
    # else:
    #     if get_color_set.con_contrast(classColor1[1], color3) >= 4.5:
    #         finalColor = classColor1[1]
    #     else:
    #         # print get_color_set.con_contrast(classColor1[1], '#FAFAFA')
    #         locat = colorSet_reference.colorTriples[classColor1[2]].index(classColor1[1])
    #         subNum = locat
    #         addNum = locat
    #         for i in range(0, 13):
    #             subNum = subNum - 1
    #             if subNum > -1:
    #                 # print subNum
    #                 # print get_color_set.con_contrast(colorSet_reference.colorTriples[classColor1[2]][subNum], color3)
    #                 if get_color_set.con_contrast(colorSet_reference.colorTriples[classColor1[2]][subNum], color3) >= 4.5:
    #                     finalColor = colorSet_reference.colorTriples[classColor1[2]][subNum]
    #                     break
    #             addNum = addNum + 1
    #             if addNum < len(colorSet_reference.colorTriples[classColor1[2]]):
    #                 # print addNum
    #                 # print get_color_set.con_contrast(colorSet_reference.colorTriples[classColor1[2]][addNum], color3)
    #                 if get_color_set.con_contrast(colorSet_reference.colorTriples[classColor1[2]][addNum], color3) >= 4.5:
    #                     finalColor = colorSet_reference.colorTriples[classColor1[2]][addNum]
    #                     break
    #
    # if finalColor == '':
    #     if get_color_set.con_contrast("#000000", color3) >= 4.5:
    #         finalColor = "#000000"
    #     elif get_color_set.con_contrast("#FFFFFF", color3) >= 4.5:
    #         finalColor = "#FFFFFF"
    # # else:
    # #     print finalColor
    # return finalColor

HueTemplates = {
    "i" : [(0.00, 0.05)],
    "V" : [(0.00, 0.26)],
    "L" : [(0.00, 0.05), (0.25, 0.22)],
    "mirror_L": [(0.00, 0.05), (-0.25, 0.22)],
    "I" : [(0.00, 0.05), (0.50, 0.05)],
    "T" : [(0.25, 0.50)],
    "Y" : [(0.00, 0.26), (0.50, 0.05)],
    "X" : [(0.00, 0.26), (0.50, 0.26)],
}



def get_S_T(s):
    sG = float(1 / 3)
    # print(float(sG*2))
    tag1 = 0
    if s >= 0 and s < sG:
        tag1 = 0
    elif s >= sG and s < sG * 2:
        tag1 = 1
    elif s >= sG * 2 and s <= 1:
        tag1 = 2
    return tag1

#圆弧距：在hue圆上的角度差
def deg_distance(a, b):
    d1 = np.abs(a - b)
    d2 = np.abs(360-d1)
    d = np.minimum(d1, d2)
    return d
#是否在区域内
def in_border(h,center,width):
    return deg_distance(h,center)<width/2
#区域外的h，计算最近边界的圆弧距
def dist_to_border(h,border):
    H1=deg_distance(h,border[0])
    H2=deg_distance(h,border[1])
    H_dist2bdr = np.minimum(H1,H2)
    return H_dist2bdr

def judgeSimiClass(color1, color2):
    class0Color1 = min(
        (color_dist(get_color_set.colorToRGB(color2), get_color_set.colorToRGB(col)), col, "class0") for col in
        colorSet_reference.colorTriple0)
    class1Color1 = min(
        (color_dist(get_color_set.colorToRGB(color2), get_color_set.colorToRGB(col)), col, "class1") for col in
        colorSet_reference.colorTriple1)
    classColor1 = min(class0Color1, class1Color1)
    # print classColor1[1]

    class0Color0 = min(
        (color_dist(get_color_set.colorToRGB(color1), get_color_set.colorToRGB(col)), col, "class0") for col in
        colorSet_reference.colorTriple0)
    class1Color0 = min(
        (color_dist(get_color_set.colorToRGB(color1), get_color_set.colorToRGB(col)), col, "class1") for col in
        colorSet_reference.colorTriple1)
    classColor0 = min(class0Color0, class1Color0)
    # print classColor0[1]

    if classColor0[2] == classColor1[2]:
        return 1
    else:
        return 0

def ifSimi(color1, color2):
    tag = 0
    class0Color1 = min(
        (color_dist(get_color_set.colorToRGB(color2), get_color_set.colorToRGB(col)), col, "class0") for col in colorSet_reference.colorTriple0)
    class1Color1 = min(
        (color_dist(get_color_set.colorToRGB(color2), get_color_set.colorToRGB(col)), col, "class1") for col in colorSet_reference.colorTriple1)
    classColor1 = min(class0Color1, class1Color1)
    # print classColor1[1]

    class0Color0 = min(
        (color_dist(get_color_set.colorToRGB(color1), get_color_set.colorToRGB(col)), col, "class0") for col in
        colorSet_reference.colorTriple0)
    class1Color0 = min(
        (color_dist(get_color_set.colorToRGB(color1), get_color_set.colorToRGB(col)), col, "class1") for col in
        colorSet_reference.colorTriple1)
    classColor0 = min(class0Color0, class1Color0)
    # print classColor0[1]


    finalColor = ''
    if classColor0[2] == classColor1[2] and \
            sub(colorSet_reference.colorTriples[classColor0[2]].index(classColor0[1]),
                colorSet_reference.colorTriples[classColor1[2]].index(classColor1[1])) <= 5:
        tag = 1
    return tag

def get_colorInDB(color2, color_simi, best_T,betst_alpha):
    final_color = ''
    simiS = []
    (r0, g0, b0) = colorToRGB(color2)
    (h0, s0, v0) = rgb2hsv(r0, g0, b0)
    # print color2
    # print color_simi
    print(h0, s0, v0)
    tagS0 = get_S_T(s0)
    for co in color_simi:
        if judgeSimiClass(co, color2) == 0:
            continue
        (r, g, b) = colorToRGB(co)
        (h, s, v) = rgb2hsv(r, g, b)
        if get_S_T(s) == tagS0:
            if abs(h - h0) < 60 or (360 - abs(h - h0)) < 60:
                simiS.append(co)
                # print co
    print(simiS)
    if simiS != []:
        # 1.distence！！！
        # delete
        if best_T == 'N':
            colorConsider1 = min(
                (color_dist(get_color_set.colorToRGB(color2), get_color_set.colorToRGB(cor)), cor) for cor in simiS)
            print(colorConsider1[1])
            final_color = colorConsider1[1]

        # 2.muban T
        else:
            colorDistSet = []
            for co in simiS:
                (r, g, b) = colorToRGB(co)
                (h, s, v) = rgb2hsv(r, g, b)
                print(h)

                borderSet = []
                for t in HueTemplates[best_T]:
                    bT = 0
                    center = t[0]*360 + betst_alpha #中心位置
                    width = t[1]*360 #宽度
                    border = [center - width/2,center + width/2]  #起止位置
                    if center - width/2 < 0:
                        borderSet.append((360 + (center - width/2), 360))
                        borderSet.append((0, center + width/2))
                        bT = 1
                    if center + width/2 > 360:
                        borderSet.append(((center - width/2), 360))
                        borderSet.append((0, center + width/2 - 360))
                        bT = 1
                    if bT ==0:
                        borderSet.append((center - width/2,center + width/2))
                print(borderSet)
                # temp_dist = dist_to_border(h, border)
                inBorders = 0
                for bor in borderSet:
                    if bor[0] <= h and bor[1] >= h and ifSimi(co, color2) == 1:
                        colorDistSet.append((0, co))
                        inBorders = 1
                        break
                if inBorders == 0:
                    miniDistance = 360
                    for bor in borderSet:
                        d0 = abs(h - bor[0])
                        miniDistance = min(d0, miniDistance)
                        d1 = abs(h - bor[1])
                        miniDistance = min(d1, miniDistance)
                    if ifSimi(co, color2) == 1:
                        colorDistSet.append((miniDistance, co))
            if colorDistSet != []:
                print(colorDistSet)
                colorConsider2 = min(colorDistSet)
                # print(colorConsider2[1])
                final_color = colorConsider2[1]
    print(final_color)
    return final_color

# get_changeColor2('', '#00A750', '#EAE8E8', 4.5)
#
# color_simi = ['#FFFFFF', '#000000', '#00793A', '#00852F']
# color2 = '#00A750'
# best_T = 'X'
# betst_alpha = 34
# # get_colorInDB(color2, color_simi)
# get_colorInDB(color2, color_simi, best_T,betst_alpha)



# get_changeColor2('', '#AD6F52', '#FFFFFF', 4.5)
#
# color_simi = ['#1D2203', '#B71C1C', '#E61831', '#D5253A', '#5E2646', '#0A0801', '#1F0912', '#C70A4C', '#050204', '#E3154B', '#E6006A', '#990000', '#CC0000', '#060104', '#3D3A1A', '#C50A0A', '#161C02', '#926736', '#E21830', '#3C3A19', '#6B4924', '#181E01', '#252911', '#D14124', '#CE0000', '#CD322E', '#200912', '#D1245E', '#5E3D1D', '#B30000', '#981919', '#D81B60']
#
# color2 = '#AD6F52'
# best_T = 'X'
# betst_alpha = 14
# # get_colorInDB(color2, color_simi)
# get_colorInDB(color2, color_simi, best_T,betst_alpha)