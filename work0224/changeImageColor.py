# encoding: utf-8
import os

import cv2
from PIL import Image

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

def transparence2white(imgPath, newColor):
    img = cv2.imread(imgPath, -1)
    sp=img.shape # 获取图片维度
    width=sp[0] # 宽度
    height=sp[1] # 高度
    colorsN = {}
    # print img
    num0 = 0
    num = 1
    for yh in range(height):
        for xw in range(width):
            color_d = img[xw, yh]  # 遍历图像每一个点，获取到每个点4通道的颜色数据
            cd = str(color_d).split(' ')
            if '' in cd:
                cd.remove('')
            if len(cd) == 3:
                break
            if(color_d[3]!=0): # 最后一个通道为透明度，如果其值为0，即图像是透明
                num = num + 1
            else:
                num0 = num0 + 1
    # print num0, num
    main_colors = get_dominant_colors(imgPath, 10)
    if num > num0 or len(main_colors) == 1:
        # print get_dominant_colors(imgPath, 10)
        oldColor = colorToRGB((main_colors[0])[1])
    else:
        oldColor = colorToRGB((main_colors[1])[1])
    # print oldColor

    for yh in range(height):
        for xw in range(width):
            color_d = img[xw, yh]  # 遍历图像每一个点，获取到每个点4通道的颜色数据
            cd = str(color_d).split(' ')
            if '' in cd:
                cd.remove('')
            if len(cd) == 3:
                if color_d[0] in range(colorToRGB(oldColor)[2]-10,colorToRGB(oldColor)[2]+10) and (color_d[1] in range(colorToRGB(oldColor)[1]-10,colorToRGB(oldColor)[1]+10)) \
                    and (color_d[2] in range(colorToRGB(oldColor)[0]-10,colorToRGB(oldColor)[0]+10)):
                    img[xw, yh] = [colorToRGB(newColor)[2], colorToRGB(newColor)[1], colorToRGB(newColor)[0]]
                # print img[xw,yh]
            elif(color_d[3]!=0): # 最后一个通道为透明度，如果其值为0，即图像是透明
                # print img[xw,yh]
                if color_d[0] in range(colorToRGB(oldColor)[2]-10,colorToRGB(oldColor)[2]+10) and (color_d[1] in range(colorToRGB(oldColor)[1]-10,colorToRGB(oldColor)[1]+10)) \
                    and (color_d[2] in range(colorToRGB(oldColor)[0]-10,colorToRGB(oldColor)[0]+10)):
                    img[xw, yh] = [colorToRGB(newColor)[2], colorToRGB(newColor)[1], colorToRGB(newColor)[0], color_d[3]]
                # print img[xw,yh]
    return img

# imgPath = '/home/zyx/Desktop/work/apktool0/com.trueway.nagaxking.trueway/res/drawable/ic_contact_pick.png'
# img = transparence2white(imgPath, '#505050')
# cv2.imwrite(imgPath, img)
# print colorToRGB((51, 51, 51))

# imgPath = 'G:\\1103\work\\apktool01\jp.co.hateblo.bomberhead_lab.e_alcohol_calendar2\\res\drawable\\tekisuto.png'
# img = transparence2white(imgPath, '#E46C0A')
# cv2.imwrite(imgPath, img)


# print colorToRGB((50, 50, 50))ic_add_image
# print colorToRGB('#FFA000')ic_add_note
# print get_dominant_colors('/home/zyx/Desktop/work2/apktool/de.rampro.activitydiary_134/res/drawable-hdpi/ic_add_note.png', 10)

# decom_Path = '/home/zyx/decompile/de.rampro.activitydiary_134'
# for drawablesFloder in os.listdir(os.path.join(decom_Path, "res")):
#     if not drawablesFloder.startswith("drawable"):
#         continue
#     # print valuesFloder
#     imageName = 'ic_add_image.png'
#     if imageName in os.listdir(os.path.join(decom_Path, "res", drawablesFloder)):
#         imgPath = os.path.join(decom_Path, "res", drawablesFloder, imageName)
#         img = transparence2white(imgPath, '#800000')
#         cv2.imwrite(imgPath, img)