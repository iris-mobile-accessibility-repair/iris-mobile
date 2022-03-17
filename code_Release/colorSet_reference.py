# encoding: utf-8
import get_color_set

# 白色：rgb(255,255,255)
# 黑色：rgb(0,0,0)
# 红色：rgb(255,0,0)
# 绿色：rgb(0,255,0)
# 蓝色：rgb(0,0,255)
# 青色：rgb(0,255,255)
# 紫色：rgb(255,0,255)

colorClass = {
    'class1': [(0, 0, 0), (105, 105, 105), (169, 169, 169), (192, 192, 192),
               (220, 220, 220), (211, 211, 211), (245, 245, 245), (255, 250, 250), (255, 255, 255)],
    'class2': [(128, 0, 0), (139, 0, 0), (165, 42, 42), (178, 34, 34),
               (188, 143, 143), (205, 92, 92), (255, 0, 0), (240, 128, 128), (250, 128, 114),
               (255, 99, 71), (255, 69, 0), (255, 127, 80), (255, 160, 122)],
    'class3': [(160,82,45), (210,105,30), (255,140,0), (244,164,96), (205,133,63),
               (222,184,135), (210,180,140)]
}

# 生成渐变色列表
def create_list():
    color_list = []
    # 从赤道黄
    for g in range(0,255):
        color_list.append((255,g,0))

    # 从黄到绿
    for r in range(255,-1,-1):
        color_list.append((r,255,0))

    # 从绿到青
    for b in range(1,255):
        color_list.append((0,255,b))

    # 从青到蓝
    for g in range(255,-1,-1):
        color_list.append((0,g,255))

    # 从蓝到紫
    for r in range(1,255):
        color_list.append((r,0,255))

    # 从紫到红
    for g in range(255,-1,-1):
        color_list.append((255,0,g))
    return color_list

# print create_list()


colorTriples = {}
R = [140, 160, 180, 200, 220, 240,
     255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
     240, 220, 200, 180, 160, 140, 120, 100, 80, 60, 40, 20, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240,
     255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]

G = [0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240,
     255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
     255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
     240, 220, 200, 180, 160, 140, 120, 100, 80, 60, 40, 20, 0]

B = [0, 0, 0, 0, 0, 0,
     0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240,
     255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
     255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
     240, 220, 200, 180, 160, 140, 120, 100, 80, 60, 40, 20, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
RGB1 = [255, 240, 220, 200, 180, 160, 140, 120, 100, 80, 60, 40, 20, 0]

# R = [255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
#      240, 220, 200, 180, 160, 140, 120, 100, 80, 60, 40, 20, 0,
#      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#      0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240]
#
# G = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#      0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240,
#      255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
#      255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255]
#
# B = [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240,
#      255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
#      255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255, 255,
#      240, 220, 200, 180, 160, 140, 120, 100, 80, 60, 40, 20, 0,
#      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# RGB1 = [255, 240, 220, 200, 180, 160, 140, 120, 100, 80, 60, 40, 20, 0]

# colorTriples = [get_color_set.colorToRGB((i, j, k)) for i in R for j in G for k in B]
# print colorTriples
# colorTriple = [(R[i], G[i], B[i]) for i in range(len(R))]
# print colorTriple

colorTriple0 = [get_color_set.colorToRGB((R[i], G[i], B[i])) for i in range(len(R))]
colorTriple1 = [get_color_set.colorToRGB((RGB1[i], RGB1[i], RGB1[i])) for i in range(len(RGB1))]
colorTriples["class0"] = colorTriple0
colorTriples["class1"] = colorTriple1




# print colorTriples
# #
# color1 = '#73D39C'
# print get_color_set.colorToRGB(color1)
# sul = min((get_color_set.con_contrast(color1, col), col)for col in colorTriple0)
# print get_color_set.colorToRGB('#00FF64')
# print colorTriple0.index(sul[1])
# print colorTriple0[36]
# print colorTriple0[43]
#
#
# class0Color0 = min((get_color_set.con_contrast("#4F8DF5", col), col, "class0")for col in colorTriple0)
# class1Color0 = min((get_color_set.con_contrast("#4F8DF5", col), col, "class1")for col in colorTriple1)
# classColor0 = min(class0Color0, class1Color0)
# print classColor0[1]
# class0Color1 = min((get_color_set.con_contrast("#FFFFFF", col), col, "class0")for col in colorTriple0)
# class1Color1 = min((get_color_set.con_contrast("#FFFFFF", col), col, "class1")for col in colorTriple1)
# classColor1 = min(class0Color1, class1Color1)
# print classColor1[1]
#
# def sub(num1,num2):
#     if num1 > num2:
#         return num1 - num2
#     else:
#         return num2 - num1
#
# finalColor = ''
# if classColor0[2] == classColor1[2] and sub(colorTriples[classColor0[2]].index(classColor0[1]), colorTriples[classColor1[2]].index(classColor1[1])) <= 2:
#     finalColor = classColor0[1]
# else:
#     if get_color_set.con_contrast(classColor1[1], '#FAFAFA') >= 3:
#         finalColor = classColor1[1]
#     else:
#         # print get_color_set.con_contrast(classColor1[1], '#FAFAFA')
#         locat = colorTriples[classColor1[2]].index(classColor1[1])
#         subNum = locat
#         addNum = locat
#         for i in range(1, 7):
#             if subNum - i > -1:
#                 if get_color_set.con_contrast(colorTriples[classColor1[2]][subNum - i], '#FAFAFA') >= 3:
#                     finalColor = colorTriples[classColor1[2]][subNum - i]
#                     break
#             subNum = subNum - 1
#             if addNum + i < len(colorTriples[classColor1[2]]):
#                 print addNum
#                 print get_color_set.con_contrast(colorTriples[classColor1[2]][addNum + i], '#FAFAFA')
#                 if get_color_set.con_contrast(colorTriples[classColor1[2]][addNum + i], '#FAFAFA') >= 3:
#                     finalColor = colorTriples[classColor1[2]][addNum + i]
#                     break
#             addNum = addNum + 1
#
# if finalColor == '':
#     print "ooooooooo"
# else:
#     print finalColor