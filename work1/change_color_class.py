# encoding: utf-8
import os
from colorsys import rgb_to_hsv

import cv2

import get_results
import nonIssueColorSet
import get_color_set
import colorSet_reference
import check_color

outputsPath = '/home/zyx/Desktop/Xbot-main/main-folder/results/outputs0'
resultPath = "/home/zyx/Desktop/result"
# HOME_PATH = "/home/zyx/decompile"
HOME_PATH = '/home/zyx/Desktop/work/apktool01'
APKName = "com.ADLS.steamproperty"
# APKName = "appinventor.ai_iraahooo.SAMYUKTHA_SALARY_CALCULATOR"

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

def ratioNum(txt):
    if txt.find("greater than 4.50 for small text") != -1:
        colorRatio = 4.5
    else:
        colorRatio = 3
    return colorRatio

def get_bounds(txt):
    bound = (txt.split("bounds=\"")[1]).split("\"")[0]
    return bound

def get_text(txt):
    if txt.find("text=\"") == -1:
        return ""
    # if txt.fing('title="@string/') != -1:
    #     text = (txt.split('title="@string/')[1]).split("\"")[0]
    if txt.find("text=\"@string/") != -1:
        text = (txt.split("text=\"@string/")[1]).split("\"")[0]
    else:
        text = (txt.split("text=\"")[1]).split("\"")[0]
    return text
def get_textCmponent(txt):
    if txt.find("class=\"") == -1:
        return ""
    compon = (txt.split("class=\"")[1]).split("\"")[0]
    return compon.split(".")[len(compon.split(".")) - 1]

def find_text_for_location(APKName, actName):
    bound_text = {}
    bound_id = {}
    layoutsPath = os.path.join(outputsPath, APKName, "layouts")
    if os.path.exists(layoutsPath):
        if (actName.split(".txt")[0] + '.xml') in os.listdir(layoutsPath):
            f = open(os.path.join(layoutsPath, (actName.split(".txt")[0] + '.xml')), "r")
            allTXT = f.read()
            allTXT = allTXT.split("<")
            for txt in allTXT:
                if txt.find("bounds") == -1:
                    continue
                if txt.find("text") != -1:
                    bound_text[get_bounds(txt)] = (get_text(txt), get_textCmponent(txt))
                if txt.find("resource-id") != -1:
                    id  = (txt.split("resource-id=\"")[1]).split("\"")[0]
                    if id.find(':id/') != -1:
                        bound_id[id.split(':id/')[1]] = (get_bounds(txt), get_textCmponent(txt))
                    elif id != '':
                        bound_id[id] = (get_bounds(txt), get_textCmponent(txt))
                # print get_text(txt)
    # print bound_id
    return bound_text, bound_id

def get_id_inOneAPK(APK_Path, APKName):
    null_id = []
    act_ids = {}
    ids_inOneAPK = {}
    stringBound = {}
    activity = []
    for file in os.listdir(APK_Path):
        if file.endswith(".txt"):
            img = ''
            imgTag = 0
            fileT = file
            bound_text_id = find_text_for_location(APKName, fileT.split(".xml")[0])
            bound_text = bound_text_id[0]
            bound_id = bound_text_id[1]
            pngFile = os.path.join(outputsPath, APKName, "screenshot", fileT.split(".txt")[0])
            if os.path.exists(pngFile):
                for fi in os.listdir(pngFile):
                    if fi.endswith(".png") and not fi.endswith("_thumbnail.png"):
                        img = cv2.imread(os.path.join(pngFile, fi))
                        imgTag = 1
                        # print bound_text
            with open(os.path.join(APK_Path, file), "r") as f:
                lis = []
                lists = []
                tempLists = []
                for line in f:
                    lis.append(line)
                # print(lis)
                for li in lis:
                    li = li.split("\n")
                    lists.append(li[0])
                # print(lists)
                id_or_bounds_List = {}
                for l in lists:
                    if l != "":
                        tempLists.append(l)
                    else:
                        # print(tempLists)
                        if tempLists[1].find(":id/") != -1:
                            id = tempLists[1].split(":id/")
                            issueColor = get_results.get_color_issueInfo(tempLists[2])
                            # print id[1]
                            # print tempLists[2]
                            # print issueColor
                            if issueColor[1] == issueColor[0] or tempLists[1].find('android:id/') != -1:
                                null_id.append(id[1])

                            #check colorSet
                            if imgTag == 1 and id[1] in bound_id and check_color.checkColorSet(img, issueColor, bound_id[id[1]][0]) == 0:
                                # print id[1]
                                issueColor1 = issueColor
                                issueColor = [issueColor1[1], issueColor1[0]]
                            #

                            colorRatio = ratioNum(tempLists[2])
                            id_or_bounds_List[id[1]] = issueColor
                            ids_inOneAPK[id[1]] = (issueColor, colorRatio, file.split('.')[len(file.split('.')) - 2], '', tempLists[0])
                            activity.append(file.split('.')[len(file.split('.')) - 2])
                        else:
                            issueColor = get_results.get_color_issueInfo(tempLists[2])
                            colorRatio = ratioNum(tempLists[2])
                            if tempLists[1].startswith("[") and tempLists[1] in bound_text:

                                # check colorSet
                                # print bound_text
                                if tempLists[1] in bound_text and check_color.checkColorSet(img, issueColor, tempLists[1]) == 0:
                                    # print bound_text[tempLists[1]][0]
                                    # print issueColor
                                    issueColor1 = issueColor
                                    issueColor = [issueColor1[1], issueColor1[0]]
                                #

                                # print tempLists[1]
                                # print bound_text[tempLists[1]]
                                if bound_text[tempLists[1]][0] == '' or bound_text[tempLists[1]][0].isspace():
                                    null_id.append(tempLists[1])

                                id_or_bounds_List[bound_text[tempLists[1]]] = issueColor
                                # print bound_text[tempLists[1]][1]
                                stringBound[bound_text[tempLists[1]]] = tempLists[1]
                                ids_inOneAPK[bound_text[tempLists[1]][0]] = (issueColor, colorRatio, file.split('.')[len(file.split('.')) - 2], bound_text[tempLists[1]][1], tempLists[0])
                                activity.append(file.split('.')[len(file.split('.')) - 2])
                            else:
                                # print tempLists[1]
                                id_or_bounds_List[tempLists[1]] = issueColor
                                ids_inOneAPK[tempLists[1]] = (issueColor, colorRatio, file.split('.')[len(file.split('.')) - 2], '', tempLists[0])
                                activity.append(file.split('.')[len(file.split('.')) - 2])
                        tempLists = []
                # id_or_bounds_List = list(set(id_or_bounds_List))
                # print list(set(id_or_bounds_List))
                act_ids[file.split(".txt")[0]] = id_or_bounds_List
    # print ids_inOneAPK
    return act_ids, ids_inOneAPK, list(set(activity)), list(set(null_id)), stringBound

# id_colorSet = get_id_inOneAPK(os.path.join(resultPath, APKName), APKName)
# print id_colorSet[1]

def find_color(formerColor, colorSet):
    color_simi = []
    for coPair in colorSet:
        if coPair == []:
            continue
        if formerColor[1] == coPair[0]:
            color_simi.append(coPair[1])
        elif formerColor[1] == coPair[1]:
            color_simi.append(coPair[0])
    return list(set(color_simi))

def find_colorSet(formerColor, colorSet):
    color_simi = []
    for cl in colorSet:
        for coPair in colorSet[cl]:
            if coPair == []:
                continue
            if formerColor[1] == coPair[0]:
                color_simi.append(coPair[1])
            elif formerColor[1] == coPair[1]:
                color_simi.append(coPair[0])
    return list(set(color_simi))

def find_colorSet_class(formerColor, colorSet, component_class):
    color_simi = []
    # print colorSet
    # print component_class
    for coPair in colorSet[component_class]:
        if coPair == []:
            continue
        if formerColor[1] == coPair[0]:
            color_simi.append(coPair[1])
        elif formerColor[1] == coPair[1]:
            color_simi.append(coPair[0])
    # print component_class
    # print list(set(color_simi))
    return list(set(color_simi))

def get_changeColor_self(resultPath, APKName, id_colorSet):
    colorChange = {}
    # id_colorSet = get_id_inOneAPK(os.path.join(resultPath, APKName), APKName)[1]
    # print id_colorSet
    nonIssueColor = nonIssueColorSet.get_nonIssueColorSet(resultPath, APKName)
    print "nonIssueColor"
    print nonIssueColor
    for idC in id_colorSet:
        color_simi = find_colorSet(id_colorSet[idC][0], nonIssueColor)
        # print id_colorSet[idC][0]
        # print color_simi
        if color_simi != []:
            # min((color_dist(color_to_match, colorToRGB(test)), test) for test in colorList)
            colorConsider1 = min((color_dist(get_color_set.colorToRGB(id_colorSet[idC][0][1]), get_color_set.colorToRGB(cor)), cor) for cor in color_simi)
            colorChange[idC] = (colorConsider1[1], id_colorSet[idC][0], id_colorSet[idC][1])
        else:
            colorChange[idC] = ('', id_colorSet[idC][0], id_colorSet[idC][1])
    return colorChange


def ifFit(color1, color2, color3, ratio):
    class0Color1 = min(
        (color_dist(get_color_set.colorToRGB(color2), get_color_set.colorToRGB(col)), col, "class0") for col in colorSet_reference.colorTriple0)
    class1Color1 = min(
        (color_dist(get_color_set.colorToRGB(color2), get_color_set.colorToRGB(col)), col, "class1") for col in colorSet_reference.colorTriple1)
    classColor1 = min(class0Color1, class1Color1)
    # print classColor1[1]
    if color1 != '':
        class0Color0 = min(
            (color_dist(get_color_set.colorToRGB(color1), get_color_set.colorToRGB(col)), col, "class0") for col in colorSet_reference.colorTriple0)
        class1Color0 = min(
            (color_dist(get_color_set.colorToRGB(color1), get_color_set.colorToRGB(col)), col, "class1") for col in colorSet_reference.colorTriple1)
        classColor0 = min(class0Color0, class1Color0)
        # print classColor0[1]
    else:
        classColor0 = (1, '', classColor1[2])

    finalColor = ''
    if classColor0[1] != '' and classColor0[2] == classColor1[2] and \
            sub(colorSet_reference.colorTriples[classColor0[2]].index(classColor0[1]),
                colorSet_reference.colorTriples[classColor1[2]].index(classColor1[1])) <= 5:
        finalColor = color1
    return finalColor


def find_colorToChange_self(resultPath, APKName, id_bound_colorSet):
    color_id = {}
    id_findInAct = []
    waitChangeColor_self = get_changeColor_self(resultPath, APKName, id_bound_colorSet)
    print "waitChangeColor_self"
    print waitChangeColor_self
    for wcolor_id in waitChangeColor_self:
        # print wcolor_id
        wcolor = waitChangeColor_self[wcolor_id]
        color1 = wcolor[0]
        color2 = wcolor[1][0]
        color3 = wcolor[1][1]
        ratio = wcolor[2]
        finalColor = ifFit(color1, color2, color3, ratio)
        if finalColor != '':
            color_id[wcolor_id] = finalColor
        else:
            id_findInAct.append(wcolor_id)

    return color_id, list(set(id_findInAct))

def get_changeColor(nonIssueColorAct, id_colorSet, componentClass, id):
    colorChange = {}
    # id_colorSet = get_id_inOneAPK(os.path.join(resultPath, APKName), APKName)[1]
    # print id_colorSet
    # print nonIssueColorAct
    color_simi = find_colorSet_class(id_colorSet[id][0], (nonIssueColorAct[id_colorSet[id][2]]), componentClass)
    # print componentClass
    # print nonIssueColorClass[componentClass]
    if color_simi != []:
        colorConsider1 = min((color_dist(get_color_set.colorToRGB(id_colorSet[id][0][1]), get_color_set.colorToRGB(cor)), cor) for cor in color_simi)
        colorChange[id] = (colorConsider1[1], id_colorSet[id][0], id_colorSet[id][1])
    else:
        colorChange[id] = ('', id_colorSet[id][0], id_colorSet[id][1])
    return colorChange


def find_colorToChange(nonIssueColorAct, id_colorSet, componentClass, id):
    color_id = {}
    waitChangeColor = get_changeColor(nonIssueColorAct, id_colorSet, componentClass, id)
    # print nonIssueColorAct[id_colorSet[id][2]]
    # print waitChangeColor
    for wcolor_id in waitChangeColor:
        # print wcolor_id
        wcolor = waitChangeColor[wcolor_id]
        color1 = wcolor[0]
        color2 = wcolor[1][0]
        color3 = wcolor[1][1]
        ratio = wcolor[2]
        finalColor = ifFit(color1, color2, color3, ratio)
        if finalColor != '':
            color_id[wcolor_id] = finalColor
        else:
            class0Color1 = min(
                (color_dist(get_color_set.colorToRGB(color2), get_color_set.colorToRGB(col)), col, "class0") for col in
                colorSet_reference.colorTriple0)
            class1Color1 = min(
                (color_dist(get_color_set.colorToRGB(color2), get_color_set.colorToRGB(col)), col, "class1") for col in
                colorSet_reference.colorTriple1)
            classColor1 = min(class0Color1, class1Color1)
            # print classColor1[1]
            if get_color_set.con_contrast(classColor1[1], color3) >= 4.5:
                finalColor = classColor1[1]
            else:
                # print get_color_set.con_contrast(classColor1[1], '#FAFAFA')
                locat = colorSet_reference.colorTriples[classColor1[2]].index(classColor1[1])
                subNum = locat
                addNum = locat
                for i in range(0, 13):
                    subNum = subNum - 1
                    if subNum > -1:
                        # print subNum
                        # print get_color_set.con_contrast(colorSet_reference.colorTriples[classColor1[2]][subNum], color3)
                        if get_color_set.con_contrast(colorSet_reference.colorTriples[classColor1[2]][subNum],
                                                      color3) >= 4.5:
                            finalColor = colorSet_reference.colorTriples[classColor1[2]][subNum]
                            break
                    addNum = addNum + 1
                    if addNum < len(colorSet_reference.colorTriples[classColor1[2]]):
                        # print addNum
                        # print get_color_set.con_contrast(colorSet_reference.colorTriples[classColor1[2]][addNum], color3)
                        if get_color_set.con_contrast(colorSet_reference.colorTriples[classColor1[2]][addNum],
                                                      color3) >= 4.5:
                            finalColor = colorSet_reference.colorTriples[classColor1[2]][addNum]
                            break
            if finalColor == '':
                if get_color_set.con_contrast("#000000", color3) >= 4.5:
                    finalColor = "#000000"
                elif get_color_set.con_contrast("#FFFFFF", color3) >= 4.5:
                    finalColor = "#FFFFFF"
            color_id[wcolor_id] = finalColor
    # print color_id
    return color_id


def get_id_txt(txt):
    id = ''
    if txt.find("android:id=\"@id/") != -1:
        id = (txt.split("android:id=\"@id/")[1]).split("\"")[0]
    elif txt.find("android:id=\"@android:id/") != -1:
        id = (txt.split("android:id=\"@android:id/")[1]).split("\"")[0]
    elif txt.find(":id=\"@id/") != -1:
        id = (txt.split(":id=\"@id/")[1]).split("\"")[0]
    elif txt.find(":id=\"@android:id/") != -1:
        id = (txt.split(":id=\"@android:id/")[1]).split("\"")[0]
    return id

def get_text_txt(txt):
    text =''
    # if txt.find("android:text=\"@string/") != -1:
    #     text = (txt.split("android:text=\"@string/")[1]).split("\"")[0]
    # elif txt.find("android:text=\"") != -1:
    #     text = (txt.split("android:text=\"")[1]).split("\"")[0]
    if txt.find(":text=\"") != -1:
        text = (txt.split(":text=\"")[1]).split("\"")[0]
    elif txt.find(":text=\"@string/") != -1:
        text = (txt.split(":text=\"@string/")[1]).split("\"")[0]
    elif txt.find(":title=\"@string/") != -1:
        text = (txt.split(":title=\"@string/")[1]).split("\"")[0]
    elif txt.find(":title=\"") != -1:
        text = (txt.split(":title=\"")[1]).split("\"")[0]
    return text

def get_title_txt(txt):
    title =''
    if txt.find(":title=\"") != -1:
        title = (txt.split(":title=\"")[1]).split("\"")[0]
    return title

def get_style_txt(txt):
    # android:textAppearance="@style/TextAppearance.AppCompat.Medium"
    style = ""
    if txt.find("=\"@style/") != -1:
        style = (txt.split("=\"@style/")[1]).split("\"")[0]
    return style

def get_color_styleTxt(txt):
    if txt.find("android:textColor") != -1:
        color = (txt.split("name=\"android:textColor\">")[1]).split("</item>")[0]
    return color

def get_stringText(txt):
    return (txt.split(">")[1]).split("</string")[0]

def get_componentClass(txt):
    class_list = ["Button", "TextView", "ImageView", "ImageButton", "EditText"]
    componentClass = txt.split(" ")[0]
    if componentClass in class_list:
        return componentClass
    else:
        return "TextView"

def get_Tag(txt):
    for t in txt.split(' '):
        if t.find(':id="') != -1:
            tagT = t.split(':id="')[0]
            break
        elif t.find(':text="') != -1:
            tagT = t.split(':text="')[0]
            break
    return tagT

def findInString(decom_Path, ids_inOneAPK):
    bounds_inOneAPK = {}
    stringText = {}
    for file in os.listdir(os.path.join(decom_Path, "res")):
        if not file.startswith("values"):
            continue
        if "strings.xml" in os.listdir(os.path.join(decom_Path, "res", file)):
            f = open(os.path.join(decom_Path, "res", file, "strings.xml"), "r")
            allTXT = f.read()
            allTXT = allTXT.split("<string ")
            for txt in allTXT:
                if not txt.startswith("name"):
                    continue
                if get_stringText(txt) in ids_inOneAPK or get_stringText(txt) in stringText:
                    stringName = (txt.split("name=\"")[1]).split("\"")[0]
                    if get_stringText(txt) in stringText:
                        bounds_inOneAPK[(txt.split("name=\"")[1]).split("\"")[0]] = bounds_inOneAPK[stringText[get_stringText(txt)]]
                        # stringText[get_stringText(txt)] = (stringText[get_stringText(txt)][0], stringText[get_stringText(txt)][1] + stringName + ',')
                    else:
                        stringText[get_stringText(txt)] = stringName
                        bounds_inOneAPK[stringName] = ids_inOneAPK[get_stringText(txt)]
                        del ids_inOneAPK[get_stringText(txt)]
    # print stringText
                    # print get_stringText(txt)
                    # print (txt.split("name=\"")[1]).split("\"")[0]
    # print ids_inOneAPK
    # print bounds_inOneAPK
    ids_bounds_inOneAPK = dict(list(ids_inOneAPK.items()) + list(bounds_inOneAPK.items()))
    # print ids_bounds_inOneAPK
    return ids_bounds_inOneAPK, ids_inOneAPK, bounds_inOneAPK, stringText

def solveTextContrast(id, txt, colorToChange, colorName_colorNew, id_style, nonIssueColorAct, id_bound_colorSet):
    # print id
    componentClass = get_componentClass(txt)
    if txt.find(":textColor=\"") != -1 or txt.find(":textColorLink=\"") != -1 or txt.find(":titleTextColor=\"") != -1:
        # print txt
        txt_temp1 = txt
        if txt.find(":textColor=\"") != -1:
            old_color = (txt_temp1.split(":textColor=\"")[1]).split("\"")[0]
            # print old_color
        if txt.find(":textColorLink=\"") != -1:
            old_color = (txt_temp1.split(":textColorLink=\"")[1]).split("\"")[0]
        elif txt.find(":titleTextColor=\"") != -1:
            old_color = (txt_temp1.split(":titleTextColor=\"")[1]).split("\"")[0]

        if id in colorToChange:
            txt = txt.replace(old_color, colorToChange[id])
        else:
            # print id
            colorToC = find_colorToChange(nonIssueColorAct, id_bound_colorSet, componentClass, id)
            # print colorToChange
            colorToChange[id] = colorToC[id]
            # print colorToChange
            txt = txt.replace(old_color, colorToChange[id])
        # print old_color
        if old_color.startswith('@color/'):
            colorName_colorNew[old_color.split('@color/')[1]] = colorToChange[id]
    elif txt.find("@style/") != -1:
        id_style[get_style_txt(txt)] = (id, componentClass)
    else:
        if id not in colorToChange:
            colorToC = find_colorToChange(nonIssueColorAct, id_bound_colorSet, componentClass, id)
            colorToChange[id] = colorToC[id]

        if txt.find("android:id=") != -1:
            txt = txt.split("android:id=")[0] + "android:textColor=\"" + colorToChange[
                id] + "\" " + "android:id=" + txt.split("android:id=")[1]
        elif txt.find("android:text=") != -1:
            txt = txt.split("android:text=")[0] + "android:textColor=\"" + \
                       colorToChange[id] + "\" " + "android:text=" + txt.split("android:text=")[1]
        else:
            tagT = get_Tag(txt)
            # print tagT
            txt = txt.split(id + '"')[0] + id + '" ' + tagT + ":textColor=\"" + \
                       colorToChange[id] + "\"" + \
                       txt.split(id + '"')[1]

    return txt, id_style, colorToChange

def solveImageContrast(id, txt, colorToChange, imageId_style, nonIssueColorAct, id_bound_colorSet, imageId_Name, id_class):
    # :tint =
    componentClass = get_componentClass(txt)
    id_class[id] = componentClass
    # if txt.find("app:tint=\"") != -1:
    #     txt_temp1 = txt
    #     old_color = (txt_temp1.split("app:tint=\"")[1]).split("\"")[0]
    #     if txt.find(":srcCompat=\"@drawable/") != -1:
    #         txt_temp1 = txt
    #         drawableName = (txt_temp1.split(":srcCompat=\"@drawable/")[1]).split("\"")[0]
    #         imageId_Name[id] = drawableName
    #
    #     if id not in colorToChange:
    #         # print id
    #         colorToC = find_colorToChange(nonIssueColorAct, id_bound_colorSet, componentClass, id)
    #         # print colorToChange
    #         colorToChange[id] = colorToC[id]
    #         # print colorToChange
    #     # print txt
    #     txt = txt.replace(old_color, colorToChange[id])
    #     # print txt
    if txt.find(":src=\"@drawable/") != -1:
        txt_temp1 = txt
        drawableName = (txt_temp1.split(":src=\"@drawable/")[1]).split("\"")[0]
        if id not in imageId_Name:
            imageId_Name[id] = []
        if drawableName not in imageId_Name[id]:
            imageId_Name[id].append(drawableName)
    elif txt.find(":srcCompat=\"@drawable/") != -1:
        txt_temp1 = txt
        drawableName = (txt_temp1.split(":srcCompat=\"@drawable/")[1]).split("\"")[0]
        if id not in imageId_Name:
            imageId_Name[id] = []
        if drawableName not in imageId_Name[id]:
            imageId_Name[id].append(drawableName)
    elif txt.find(":background=\"@drawable/") != -1:
        txt_temp1 = txt
        drawableName = (txt_temp1.split(":background=\"@drawable/")[1]).split("\"")[0]
        if id not in imageId_Name:
            imageId_Name[id] = []
        if drawableName not in imageId_Name[id]:
            imageId_Name[id].append(drawableName)
    elif txt.find("@style/") != -1:
        imageId_style[get_style_txt(txt)] = (id, componentClass, id_bound_colorSet[id][0])
    # for id in imageId_Name:
    #     if id not in colorToChange:
    #         colorToC = find_colorToChange(nonIssueColorAct, id_bound_colorSet, componentClass, id)
    #         colorToChange[id] = colorToC[id]
    #     imageId_Name[id] = (imageId_Name[id], colorToChange[id])
    return txt, colorToChange, imageId_Name, imageId_style, id_class


def changeLayout_decompileAPK(decom_Path, id_bound_colorSet, colorToChange, nonIssueColorAct):
    imageId_Name = {}
    editId = []
    id_style = {}
    id_class = {}
    imageId_style = {}
    colorName_colorNew = {}
    for id in id_bound_colorSet:
        if id_bound_colorSet[id][3] == 'EditText':
            # print id
            editId.append(id)
    for layoutFloder in os.listdir(os.path.join(decom_Path, "res")):
        if not layoutFloder.startswith("layout"):
            continue
        # print layoutFloder
        for xmlFile in os.listdir(os.path.join(decom_Path, "res", layoutFloder)):
            if xmlFile.endswith(".xml"):
                TXTFile = xmlFile.split(".xml")[0] + ".txt"
                os.rename(os.path.join(decom_Path, "res", layoutFloder, xmlFile),
                          os.path.join(decom_Path, "res", layoutFloder, TXTFile))

        for TXTFile in os.listdir(os.path.join(decom_Path, "res", layoutFloder)):
            allData = ""
            # print TXTFile
            if TXTFile.endswith(".txt"):
                f = open(os.path.join(decom_Path, "res", layoutFloder, TXTFile), "r")
                allTXT = f.read()
                allTXT = allTXT.split("<")
                for txt in allTXT:
                    # print txt
                    if txt.find(":id=") == -1 and txt.find(":text=") == -1 and txt != "" and txt.find(":title=") == -1:
                        allData += "<" + txt
                        continue
                    elif (get_id_txt(txt) in id_bound_colorSet) or (get_text_txt(txt) in id_bound_colorSet) or (get_title_txt(txt) in id_bound_colorSet):
                        if (get_id_txt(txt) in id_bound_colorSet) and (get_id_txt(txt) not in editId):
                            id = get_id_txt(txt)
                        elif get_text_txt(txt) in id_bound_colorSet and (get_text_txt(txt) not in editId):
                            id = get_text_txt(txt)
                        elif get_title_txt(txt) in id_bound_colorSet and (get_title_txt(txt) not in editId):
                            id = get_title_txt(txt)

                        txt0 = txt
                        if txt.startswith("EditText") or txt0.split(' ')[0].find("EditText") != -1:
                            editId.append(get_id_txt(txt))
                            allData += "<" + txt
                            continue
                        elif id_bound_colorSet[id][4] == 'Text contrast':
                            solution = solveTextContrast(id, txt, colorToChange, colorName_colorNew, id_style,
                                                  nonIssueColorAct, id_bound_colorSet)
                            txt = solution[0]
                            id_style = solution[1]
                            colorToChange = solution[2]
                            allData += "<" + txt
                        elif id_bound_colorSet[id][4] == 'Image contrast':
                            # print id
                            # print txt
                            solution = solveImageContrast(id, txt, colorToChange, imageId_style, nonIssueColorAct, id_bound_colorSet, imageId_Name, id_class)
                            txt = solution[0]
                            # id_style = solution[1]
                            colorToChange = solution[1]
                            imageId_Name = solution[2]
                            imageId_style = solution[3]
                            id_class = solution[4]
                            allData += "<" + txt

                    elif txt != '':
                        allData += "<" + txt
                # print allData

            with open(os.path.join(decom_Path, "res", layoutFloder, TXTFile), 'a+') as test:
                test.truncate(0)
            # f = open(os.path.join(decom_Path, "res", layoutFloder, TXTFile), "r")
            # allTXT0 = f.read()
            # print "hhh" + allTXT0
            with open(os.path.join(decom_Path, "res", layoutFloder, TXTFile), "w") as f:
                # print allData
                f.write(allData)

        for txtFile in os.listdir(os.path.join(decom_Path, "res", layoutFloder)):
            if txtFile.endswith(".txt"):
                xmlFile = txtFile.split(".txt")[0] + ".xml"
                os.rename(os.path.join(decom_Path, "res", layoutFloder, txtFile),
                          os.path.join(decom_Path, "res", layoutFloder, xmlFile))
    # print id_style
    # print id_class
    for id in imageId_Name:
        if id not in colorToChange:
            colorToC = find_colorToChange(nonIssueColorAct, id_bound_colorSet, id_class[id], id)
            colorToChange[id] = colorToC[id]
        imageId_Name[id] = (imageId_Name[id], colorToChange[id])
    print "imageId_Name"
    print imageId_Name
    print "imageId_style"
    print imageId_style
    return list(set(editId)), colorToChange, id_style, colorName_colorNew, imageId_Name, imageId_style

def get_colorName(txt):
    return txt.split('@color/')[1]

def get_styleName(txt):
    return (txt.split("name=\"")[1]).split("\"")[0]

def changeStyle_decompileAPK(decom_Path, id_style, imageId_style, imageId_Name, id_bound_colorSet, colorToChange, nonIssueColorAct, colorName_colorNew, Manifest):
    # colorName_colorNew = {}
    # if not os.path.exists(os.path.join(decom_Path, "res", "values")):
    styleXmlFile = "styles.xml"
    for valuesFloder in os.listdir(os.path.join(decom_Path, "res")):
        if not valuesFloder.startswith("values"):
            continue
        # print valuesFloder
        if styleXmlFile in os.listdir(os.path.join(decom_Path, "res", valuesFloder)):
            TXTFile = styleXmlFile.split(".xml")[0] + ".txt"
            os.rename(os.path.join(decom_Path, "res", valuesFloder, styleXmlFile),
                          os.path.join(decom_Path, "res", valuesFloder, TXTFile))

            allData = ""
            f = open(os.path.join(decom_Path, "res", valuesFloder, TXTFile), "r")
            allTXT = f.read()
            # print allTXT
            allTXT = allTXT.split("<style ")
            for txt in allTXT:
                # print txt
                if txt.startswith("name"):
                    if (get_styleName(txt) not in id_style) and (get_styleName(txt) not in imageId_style) and (get_styleName(txt) not in Manifest) and txt != '':
                        allData += "<style " + txt
                        continue
                    elif get_styleName(txt) in id_style:
                        if txt.find("android:textColor") == -1:
                            allData += "<style " + txt
                            continue
                        else:
                            txtT = txt
                            id_component = id_style[(txtT.split("name=\"")[1]).split("\"")[0]]
                            # print txt
                            colorNameT = get_color_styleTxt(txt)

                            if id_component[0] in colorToChange:
                                txt = txt.replace(colorNameT, colorToChange[id_component[0]])
                            else:
                                colorToC = find_colorToChange(nonIssueColorAct, id_bound_colorSet, id_component[1],
                                                              id_component[0])
                                # print colorToChange[id_component[0]]
                                colorToChange[id_component[0]] = colorToC[id_component[0]]
                                txt = txt.replace(colorNameT, colorToC[id_component[0]])
                            # print txt
                            if colorNameT.find('@color/') != -1:
                                colorName = get_colorName(colorNameT)
                                colorName_colorNew[colorName] = colorToChange[id_component[0]]

                            allData += "<style " + txt
                    elif get_styleName(txt) in imageId_style:
                        # if txt.find("srcCompat") == -1 and txt.find('background') == -1 and txt.find("srcCompat") == -1 and txt != '':
                        if txt.find('@drawable/') == -1 and txt != '':
                            allData += "<style " + txt
                            continue
                        else:
                            txtT = txt
                            draName = (txtT.split('@drawable/')[1]).split('<')[0]
                            if draName not in imageId_Name[imageId_style[get_styleName(txt)][0]][0]:
                                imageId_Name[imageId_style[get_styleName(txt)][0]][0].append(draName)
                    elif get_styleName(txt) in Manifest:
                        # print get_styleName(txt)
                        txtT = txt
                        id_component = Manifest[(txtT.split("name=\"")[1]).split("\"")[0]]
                        if id_component[0] not in colorToChange:
                            colorToC = find_colorToChange(nonIssueColorAct, id_bound_colorSet, id_component[1],
                                                          id_component[0])
                            # print colorToChange[id_component[0]]
                            colorToChange[id_component[0]] = colorToC[id_component[0]]
                        if txt.find('<item name=') != -1:
                            if txt.find('<item name="titleTextColor">') == -1:
                                txt0 = txt.split('</style>')
                                allData += '<style ' + txt0[0] + '\t' + '<item name="titleTextColor">' + colorToChange[
                                    id_component[0]] + '</item>' + '</style>' + '\n'
                            else:
                                txt0 = txt
                                colorNameT = (txt0.split('<item name="titleTextColor">')[1]).split('<')[0]
                                txt = txt.replace(colorNameT, colorToChange[id_component[0]])
                                allData += "<style " + txt
                        else:
                            txt = txt.split('/>')[0] + '>' + '\n\t' + '<item name="titleTextColor">' + colorToChange[
                                    id_component[0]] + '</item>' + '</style>' + '\n'
                            allData += "<style " + txt

                else:
                    allData += txt

            with open(os.path.join(decom_Path, "res", valuesFloder, TXTFile), 'a+') as test:
                test.truncate(0)
            with open(os.path.join(decom_Path, "res", valuesFloder, TXTFile), "w") as f:
                # print allData
                f.write(allData)

            xmlFile = TXTFile.split(".txt")[0] + ".xml"
            os.rename(os.path.join(decom_Path, "res", valuesFloder, TXTFile),
                              os.path.join(decom_Path, "res", valuesFloder, xmlFile))
    print "imageId_Name"
    print imageId_Name
    return colorToChange, colorName_colorNew, imageId_Name

def get_AppLable(txt):
    if txt.find(':label="@string/') != -1:
        return (txt.split(':label="@string/')[1]).split('"')[0]
    elif txt.find(':label="') != -1:
        return (txt.split(':label="')[1]).split('"')[0]

def get_theme(txt):
    return (txt.split(':theme="@style/')[1]).split('"')[0]

def changeManifestF_decompileAPK(decom_Path, id_bound_colorSet, stringText):
    id_style_ManifestF = {}
    ManifestXmlFile = 'AndroidManifest.xml'
    if ManifestXmlFile in os.listdir(decom_Path):
        f = open(os.path.join(decom_Path, ManifestXmlFile), "r")
        allTXT = f.read()
        allTXT = allTXT.split("<")
        for txt in allTXT:
            # print txt
            if txt.find(':label=') != -1 and txt.find(':theme=') != -1:
                id = get_AppLable(txt)
                if id in id_bound_colorSet:
                    id_style_ManifestF[get_theme(txt)] = (id, 'TextView')
                elif id in stringText:
                    id_style_ManifestF[get_theme(txt)] = (stringText[id], 'TextView')
    return id_style_ManifestF



ids_location_inOneAPK = get_id_inOneAPK(os.path.join(resultPath, APKName), APKName)
# print ids_location_inOneAPK[1]
ids_bounds_inOneAPK = findInString(os.path.join(HOME_PATH, APKName), ids_location_inOneAPK[1])
stringText = ids_bounds_inOneAPK[3]
print "stringText"
print stringText
id_bound_colorSet = ids_bounds_inOneAPK[0]
print "id_bound_colorSet"
print id_bound_colorSet
stringText = ids_bounds_inOneAPK[3]

nonIssueColorAct = {}
for act in ids_location_inOneAPK[2]:
    nonIssueColorAct[act] = nonIssueColorSet.get_nonIssueColorSet_activity(resultPath, act)

colorToChange = find_colorToChange_self(resultPath, APKName, id_bound_colorSet)[0]
# print ids_inOneAPK
print "colorToChange_self"
print colorToChange

editTextId = changeLayout_decompileAPK(os.path.join(HOME_PATH, APKName), id_bound_colorSet, colorToChange, nonIssueColorAct)
print "colorToChange_Layout"
print editTextId[1]
Manifest = changeManifestF_decompileAPK(os.path.join(HOME_PATH, APKName), id_bound_colorSet, stringText)
if editTextId[2] != {} or Manifest != {}:
    if editTextId[2] != {}:
        print editTextId[2]
    else:
        print Manifest
    # colorName_colorNew    list(set(editId)), colorToChange, id_style, colorName_colorNew, imageId_Name, imageId_style
    #decom_Path, id_style, imageId_style, imageId_Name, id_bound_colorSet, colorToChange, nonIssueColorAct, colorName_colorNew
    print editTextId[3]
    changeStyle = changeStyle_decompileAPK(os.path.join(HOME_PATH, APKName), editTextId[2], editTextId[5], editTextId[4], id_bound_colorSet, colorToChange, nonIssueColorAct, editTextId[3], Manifest)
    print 'colorToChange_final'
    print changeStyle[0]

# print editTextId[0]  decom_Path, id_style, id_bound_colorSet, colorToChange, nonIssueColorAct
# print editTextId[0]
print ids_location_inOneAPK[4]
for eid in ids_location_inOneAPK[4]:
    if eid[0] in editTextId[0]:
        editTextId[0].append(ids_location_inOneAPK[4][eid])
        editTextId[0].remove(eid[0])
    if eid[0] in stringText:
        if stringText[eid[0]] in editTextId[0]:
            editTextId[0].append(ids_location_inOneAPK[4][eid])
            editTextId[0].remove(stringText[eid[0]])
print editTextId[0]
null_id = ids_location_inOneAPK[3]
for issueId in id_bound_colorSet:
    if issueId.startswith('[') and issueId.endswith(']'):
        null_id.append(issueId)
print null_id
splitId = list(set(editTextId[0] + null_id))
print splitId

