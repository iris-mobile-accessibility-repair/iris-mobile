# encoding: utf-8
import os
import shutil
import csv
import cv2
import get_color_set

class_types = []
issue_class_list = []
def readFileName(filePath):
    name = os.listdir(filePath)
    return name

def createFolder(folderPath):
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)

def get_color_issueInfo(txt):
    color_info = []
    tempTxt = (txt.split("foreground color of ")[1]).split(" and an estimated background color of ")
    foreColor = tempTxt[0]
    backColor = tempTxt[1].split('.')[0]
    color_info.append(foreColor)
    color_info.append(backColor)
    return color_info

def rewriteTXT(APKname, APKPath, activeName, txtPath, rewrite_txtPath, out_csv, false_xml_scv, nonIssue_xml_scv):
    with open(txtPath, "r") as f:  # 打开文件
        lis = []
        lists = []
        tempLists = []
        id_or_bounds = ""
        for line in f:
            lis.append(line)
        # print(lis)
        for li in lis:
            li = li.split("\n")
            lists.append(li[0])
        # print(lists)
        n = -1
        n_contrast_type = ""
        n_id_or_bounds = ""
        id_or_bounds_List = []
        for list in lists:
            if list != "":
                tempLists.append(list)
            else:
                # print(tempLists)
                if tempLists[0] == 'Text contrast' or tempLists[0] == 'Image contrast':
                    # active_name
                    contrast_type = tempLists[0]
                    id_or_bounds = tempLists[1]
                    color_info = get_color_issueInfo(tempLists[2])
                    id_or_bounds_List.append(id_or_bounds)
                    if n == -1:
                        n_contrast_type = contrast_type
                        n_id_or_bounds = id_or_bounds
                        # id_or_bounds_List.append(n_id_or_bounds)
                        n = n + 1
                    elif contrast_type == n_contrast_type and id_or_bounds == n_id_or_bounds:
                        n = n + 1
                    else:
                        n = -1
                    raletive_class = fingRaletiveClass(APKPath, activeName, id_or_bounds, n, id_or_bounds_List)[0]
                    raletive_xml = fingRaletiveClass(APKPath, activeName, id_or_bounds, n, id_or_bounds_List)[1]
                    class_types.append(raletive_class)

                    csv.writer(open(out_csv, 'a')).writerow(
                        (APKname, activeName, contrast_type, id_or_bounds, raletive_class))

                    csv.writer(open(false_xml_scv, 'a')).writerow(
                        (APKname, activeName, contrast_type, id_or_bounds, raletive_class, raletive_xml, color_info))

                    # csv.writer(open(nonIssue_xml_scv, 'a')).writerow(
                    #     (APKname, activeName, nonIssue_class, nonIssueXML))

                    for tempList in tempLists:
                        with open(rewrite_txtPath, "a") as f1:
                            f1.write(tempList)
                            f1.write("\n")
                    with open(rewrite_txtPath, "a") as f1:
                        f1.write("\n")

                tempLists = []

        # print(tempLists)
        if tempLists != []:
            if tempLists[0] == 'Text contrast' or tempLists[0] == 'Image contrast':
                for tempList in tempLists:
                    with open(rewrite_txtPath, "a") as f1:
                        f1.write(tempList)
                        f1.write("\n")
        tempLists = []

        # print id_or_bounds_List
        # print activeName
        nonIssueXML_List = fingRaletiveClass(APKPath, activeName, id_or_bounds, n, id_or_bounds_List)[2]
        nonIssueClass_List = fingRaletiveClass(APKPath, activeName, id_or_bounds, n, id_or_bounds_List)[3]

        for index in range(len(nonIssueXML_List)):
            csv.writer(open(nonIssue_xml_scv, 'a')).writerow((APKname, activeName, nonIssueClass_List[index], nonIssueXML_List[index]))
            # print(nonIssueXML_List[index])
            # print(nonIssueClass_List[index])


def fingRaletiveClass(APKPath, activeName, id_or_bounds, n, id_or_bounds_List):
    laydoutPath = os.path.join(APKPath, 'layouts')
    XMLName = activeName + ".xml"
    TXTName = activeName + ".txt"
    XMLPath = os.path.join(laydoutPath, XMLName)
    copyPath = os.path.join(laydoutPath, "xmlTOtxt")
    createFolder(copyPath)
    classTag = ""
    falseXML_List = []
    nonIssueXML_List = []
    nonIssueClass_List = []
    if os.path.exists(XMLPath):
        shutil.copy(XMLPath, copyPath)
        TOtxt_xmlPath = os.path.join(copyPath, XMLName)
        TOtxt_txtPath = os.path.join(copyPath, TXTName)
        os.rename(TOtxt_xmlPath, TOtxt_txtPath)

        # classTag = getClass(TOtxt_txtPath, id_or_bounds)

        falseXML_List = getFalseXML(TOtxt_txtPath, id_or_bounds, n)[0]
        classTag = getFalseXML(TOtxt_txtPath, id_or_bounds, n)[1]
        nonIssueXML_List = getNonIssueXML(TOtxt_txtPath, id_or_bounds_List)[0]
        nonIssueClass_List = getNonIssueXML(TOtxt_txtPath, id_or_bounds_List)[1]
        # print(nonIssue_class)

    return classTag, falseXML_List , nonIssueXML_List, nonIssueClass_List

def getFalseXML(TOtxt_txtPath, id_or_bounds, n):
    raletive_xml = ""
    classTag = ""
    falseXML_list = []
    f = open(TOtxt_txtPath, "r")
    allTXT = f.read()
    allTXT = allTXT.split("<node")
    for txt in allTXT:
        if txt.find(id_or_bounds) == -1:
            continue
        else:
            if txt.startswith("<"):
                continue
            falseXML = "<node" + txt
            falseXML_list.append(falseXML)
            # print(falseXML)
            txt = txt.split("class=\"")
            txt[1] = txt[1].split("\"")
            classTag = txt[1][0]
    # print(classTag)
    # print (falseXML_list)
    # print (n,len(falseXML_list))
    if len(falseXML_list) != 0:
        raletive_xml = falseXML_list[n]
        # print (raletive_xml)

    return raletive_xml, classTag

def getNonIssueXML(TOtxt_txtPath, id_or_bounds_List):
    nonIssueXML = ""
    nonIssue_class = ""
    nonIssueXML_List = []
    nonIssueClass_List = []
    id_or_bounds_List_Temp = list(set(id_or_bounds_List))
    # print (id_or_bounds_List_Temp)
    f = open(TOtxt_txtPath, "r")
    allTXT = f.read()
    allTXT = allTXT.split("<node")
    for txt in allTXT:
        tap = 0
        for id_or_bounds in id_or_bounds_List_Temp:
            if txt.find(id_or_bounds) != -1:
                tap = 1
                break

        if tap == 1 or txt.find("class=\"") == -1:
            continue
        # if txt.startswith("<"):
        #     break
        xmlTxt = txt
        txt = txt.split("class=\"")
        txt[1] = txt[1].split("\"")
        if txt[1][0].endswith("Layout") or txt[1][0].endswith("Group"):
            continue
        nonIssueXML = "<node" + xmlTxt
        nonIssue_class = txt[1][0]
        nonIssueXML_List.append(nonIssueXML)
        nonIssueClass_List.append(nonIssue_class)
        # print(nonIssue_class)
        # print(nonIssueXML)
    # print id_or_bounds_List_Temp
    return nonIssueXML_List, nonIssueClass_List

def splitContrast(resultPath, outputsPath):
    if not os.path.exists(resultPath):
        createFolder(resultPath)
    APKnames = readFileName(outputsPath)
    # print(APKnames)
    out_csv = os.path.join(resultPath, 'classLog.csv')
    false_xml_scv = os.path.join(resultPath, 'false_xmlLog.csv')
    nonIssue_xml_scv = os.path.join(resultPath, 'nonIssue_xml_scv.csv')
    if not os.path.exists(out_csv):
        csv.writer(open(out_csv, 'a')).writerow(('apk_name', 'active_name', 'contrast_type', 'id_or_bounds', 'raletive_class'))
    if not os.path.exists(false_xml_scv):
        csv.writer(open(false_xml_scv, 'a')).writerow(('apk_name', 'active_name', 'contrast_type', 'id_or_bounds', 'raletive_class', 'raletive_xml', 'color_info'))
    if not os.path.exists(nonIssue_xml_scv):
        csv.writer(open(nonIssue_xml_scv, 'a')).writerow(('apk_name', 'active_name', 'raletive_class', 'raletive_xml'))

    for APKname in APKnames:
        print(APKname)
        rePath = os.path.join(resultPath, APKname)
        createFolder(rePath)

        APKPath = os.path.join(outputsPath, APKname)
        issuesPath = os.path.join(APKPath, "issues")
        if not os.path.exists(issuesPath):
            continue

        activeNames = readFileName(issuesPath)
        for activeName in activeNames:
            activePath = os.path.join(issuesPath, activeName)
            if activeName.endswith('.zip'):
                continue
            txtNames = readFileName(activePath)
            for txtName in txtNames:
                # print(txtName)
                if txtName.endswith(".txt"):
                    txtPath = os.path.join(activePath, txtName)
                    rewrite_txtPath = os.path.join(rePath, txtName)
                    #createFolder(rewrite_txtPath)
                    rewriteTXT(APKname, APKPath, activeName, txtPath, rewrite_txtPath, out_csv, false_xml_scv, nonIssue_xml_scv)

    issue_class_types = os.path.join(resultPath, 'issue_class_types.txt')
    for index in range(len(list(set(class_types)))):
        with open(issue_class_types, "a") as f1:
            if list(set(class_types))[index] == '':
                continue
            f1.write(list(set(class_types))[index])
            f1.write("\n")
            issue_class_list.append(list(set(class_types))[index])
    # print issue_class_list



def get_components(resultPath, outputsPath, scv_path, type_XML):
    # scv_path = os.path.join(resultPath, 'test.csv')
    raletive_class = "classnameNULL"
    with open(scv_path, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        column = [row for row in reader]
    id_is_null = 0
    apk_name_temp = ''
    act_temp = ''
    for index in range(len(column)):
        # if column[index]["apk_name"] == "de.p72b.bonitur":
        #     print column[index]
        apk_name = column[index]["apk_name"]
        print apk_name
        act = column[index]["active_name"]
        result_folder = os.path.join(resultPath, apk_name)
        components_path = os.path.join(result_folder, act, type_XML)
        if not os.path.exists(components_path):
            os.makedirs(components_path)
        screenshot_path0 = os.path.join(outputsPath, apk_name, 'screenshot')
        if not os.path.exists(screenshot_path0):
            continue
        if os.listdir(screenshot_path0) == []:
            continue
        screenshot_path = os.path.join(screenshot_path0, act)
        if not os.path.exists(screenshot_path):
            continue
        if not os.path.isdir(screenshot_path):
            img = cv2.imread(os.path.join(screenshot_path0, act))
        else:
            for file in os.listdir(screenshot_path):
                if file.endswith(".png") and not file.endswith("_thumbnail.png"):
                    img = cv2.imread(os.path.join(screenshot_path, file))
        # if os.listdir(screenshot_path)[0].endswith("_thumbnail.png"):
        #     # print os.path.join(screenshot_path, os.listdir(screenshot_path)[1])
        #     img = cv2.imread(os.path.join(screenshot_path, os.listdir(screenshot_path)[1]))
        # else:
        #     img = cv2.imread(os.path.join(screenshot_path, os.listdir(screenshot_path)[0]))

        # print img
        if column[index]["raletive_xml"] == '':
            continue
        raletive_xml = column[index]["raletive_xml"]
        if column[index]["raletive_class"] != '':
            raletive_class = column[index]["raletive_class"]
            #hhhhhhhhhhhhhhh
            if raletive_class not in issue_class_list:
                continue

        if apk_name != apk_name_temp or act != act_temp:
            apk_name_temp = apk_name
            act_temp = act
            id_is_null = 0
        id_is_null = id_is_null + 1

        if not raletive_xml == '':
            if raletive_xml.find("bounds=\"") == -1:
                continue
            bound = raletive_xml.split("bounds=\"")[1].split("\"")[0]
            class_N = raletive_class.split(".")[2]
            # print class_N
            y0 = int(bound.split(',')[1].split(']')[0])
            y1 = int(bound.split(',')[2].split(']')[0])
            x0 = int(bound.split(',')[0].split('[')[1])
            x1 = int(bound.split(',')[1].split('[')[1])
            component_name = str(id_is_null) + '_' + class_N
            try:
                print (x0,x1,y0,y1)
                cropped = img[y0:y1, x0:x1]
                # print cropped
                if cropped.size !=0:
                    cv2.imwrite(os.path.join(components_path, component_name + '.png'), cropped)
            except TypeError:
                pass
            except UnboundLocalError:
                pass


def get_components_inOneFolder(resultPath, outputsPath, scv_path, type_XML):
    # scv_path = os.path.join(resultPath, 'test.csv')
    raletive_class = "classnameNULL"
    with open(scv_path, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        column = [row for row in reader]
    id_is_null = 0
    SNUM = 1
    apk_name_temp = ''
    act_temp = ''
    for index in range(len(column)):
        # if column[index]["apk_name"] == "de.p72b.bonitur":
        #     print column[index]
        apk_name = column[index]["apk_name"]
        print apk_name
        act = column[index]["active_name"]
        result_folder = os.path.join(resultPath, "A_components_outputs", type_XML)
        if not os.path.exists(result_folder):
            os.makedirs(result_folder)
        screenshot_path0 = os.path.join(outputsPath, apk_name, 'screenshot')
        if os.listdir(screenshot_path0) == []:
            continue
        screenshot_path = os.path.join(screenshot_path0, act)
        for file in os.listdir(screenshot_path):
            if file.endswith(".png") and not file.endswith("_thumbnail.png"):
                img = cv2.imread(os.path.join(screenshot_path, file))
        # if os.listdir(screenshot_path)[0].endswith("_thumbnail.png"):
        #     # print os.path.join(screenshot_path, os.listdir(screenshot_path)[1])
        #     img = cv2.imread(os.path.join(screenshot_path, os.listdir(screenshot_path)[1]))
        # else:
        #     img = cv2.imread(os.path.join(screenshot_path, os.listdir(screenshot_path)[0]))

        # print img
        if column[index]["raletive_xml"] == '':
            continue
        raletive_xml = column[index]["raletive_xml"]
        if column[index]["raletive_class"] != '':
            raletive_class = column[index]["raletive_class"]
            #hhhhhhhhhhhhhhh
            if raletive_class not in issue_class_list:
                continue

        if apk_name != apk_name_temp or act != act_temp:
            apk_name_temp = apk_name
            act_temp = act
            id_is_null = 0
        id_is_null = id_is_null + 1

        if not raletive_xml == '':
            if raletive_xml.find("bounds=\"") == -1:
                continue
            bound = raletive_xml.split("bounds=\"")[1].split("\"")[0]
            class_N = raletive_class.split(".")[2]
            # print class_N
            y0 = int(bound.split(',')[1].split(']')[0])
            y1 = int(bound.split(',')[2].split(']')[0])
            x0 = int(bound.split(',')[0].split('[')[1])
            x1 = int(bound.split(',')[1].split('[')[1])
            component_name = str(SNUM) + '_' +apk_name + '_' + act + '_' + str(id_is_null) + '_' + class_N

            try:
                print (x0,x1,y0,y1)
                cropped = img[y0:y1, x0:x1]
                # print cropped
                if cropped.size !=0:
                    cv2.imwrite(os.path.join(result_folder, component_name + '.png'), cropped)
                    SNUM = SNUM + 1
            except TypeError:
                pass
            except UnboundLocalError:
                pass

def get_components_classFolder(resultPath, outputsPath, scv_path, type_XML):
    # scv_path = os.path.join(resultPath, 'test.csv')
    raletive_class = "classnameNULL"
    with open(scv_path, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        column = [row for row in reader]
    id_is_null = 0
    classNum = {}
    for cl in issue_class_list:
        classNum[cl] = 1
    apk_name_temp = ''
    act_temp = ''
    for index in range(len(column)):
        # if column[index]["apk_name"] == "de.p72b.bonitur":
        #     print column[index]
        apk_name = column[index]["apk_name"]
        print apk_name
        act = column[index]["active_name"]
        result_folder = os.path.join(resultPath, "A_components_class", type_XML)

        screenshot_path0 = os.path.join(outputsPath, apk_name, 'screenshot')
        if os.listdir(screenshot_path0) == []:
            continue
        screenshot_path = os.path.join(screenshot_path0, act)
        if os.path.exists(screenshot_path):
            for file in os.listdir(screenshot_path):
                if file.endswith(".png") and not file.endswith("_thumbnail.png"):
                    img = cv2.imread(os.path.join(screenshot_path, file))

        # print img
        if column[index]["raletive_xml"] == '':
            continue
        raletive_xml = column[index]["raletive_xml"]
        if column[index]["raletive_class"] != '':
            raletive_class = column[index]["raletive_class"]
            #hhhhhhhhhhhhhhh
            if raletive_class not in issue_class_list:
                continue

        result_classFolder = os.path.join(result_folder, raletive_class)
        if not os.path.exists(result_classFolder):
            os.makedirs(result_classFolder)

        if apk_name != apk_name_temp or act != act_temp:
            apk_name_temp = apk_name
            act_temp = act
            id_is_null = 0
        id_is_null = id_is_null + 1

        if not raletive_xml == '':
            if raletive_xml.find("bounds=\"") == -1:
                continue
            bound = raletive_xml.split("bounds=\"")[1].split("\"")[0]
            class_N = raletive_class.split(".")[2]
            # print class_N
            y0 = int(bound.split(',')[1].split(']')[0])
            y1 = int(bound.split(',')[2].split(']')[0])
            x0 = int(bound.split(',')[0].split('[')[1])
            x1 = int(bound.split(',')[1].split('[')[1])
            component_name = str(classNum[raletive_class]) + '_' +apk_name + '_' + act + '_' + str(id_is_null) + '_' + class_N

            try:
                print (x0,x1,y0,y1)
                cropped = img[y0:y1, x0:x1]
                # print cropped
                if cropped.size !=0:
                    cv2.imwrite(os.path.join(result_classFolder, component_name + '.png'), cropped)
                    classNum[raletive_class] = classNum[raletive_class] + 1
            except TypeError:
                pass
            except UnboundLocalError:
                pass

    for li in os.listdir(result_folder):
        os.rename(os.path.join(result_folder, li), os.path.join(result_folder, li + "_" + str(classNum[li] - 1)))


def get_components_APKFolder(resultPath, outputsPath, scv_path, type_XML):
    class_successNum = {}
    for cl in issue_class_list:
        class_successNum[cl.split(".")[2]] = 0
    class_successNum["total"] = 0
    class_failNum = {}
    for cl in issue_class_list:
        class_failNum[cl.split(".")[2]] = 0
    class_failNum["total"] = 0
    if type_XML == "IssueXML":
        color_contrast_path = os.path.join(resultPath, 'color_contrast.csv')
        if not os.path.exists(color_contrast_path):
            csv.writer(open(color_contrast_path, 'a')).writerow(
                ('apk_name', 'active_name', 'raletive_class', 'id_or_bounds', 'xbot_colorSet', 'getColor'))
    # scv_path = os.path.join(resultPath, 'test.csv')
    raletive_class = "classnameNULL"
    with open(scv_path, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        column = [row for row in reader]
    successNum = 0
    failNum = 0
    id_is_null = 0
    SNUM = 1
    apk_name_temp = ''
    act_temp = ''
    for index in range(len(column)):
        # if column[index]["apk_name"] == "de.p72b.bonitur":
        #     print column[index]
        apk_name = column[index]["apk_name"]
        # print apk_name
        act = column[index]["active_name"]
        result_folder = os.path.join(resultPath, apk_name, type_XML)

        screenshot_path0 = os.path.join(outputsPath, apk_name, 'screenshot')
        # if os.listdir(screenshot_path0) == []:
            # continue
        screenshot_path = os.path.join(screenshot_path0, act)
        if not os.path.exists(screenshot_path):
            continue
        if not os.path.isdir(screenshot_path):
            img = cv2.imread(os.path.join(screenshot_path0, act))
        else:
            for file in os.listdir(screenshot_path):
                if file.endswith(".png") and not file.endswith("_thumbnail.png"):
                    img = cv2.imread(os.path.join(screenshot_path, file))

        # print img
        if column[index]["raletive_xml"] == '':
            continue
        raletive_xml = column[index]["raletive_xml"]
        if column[index]["raletive_class"] != '':
            raletive_class = column[index]["raletive_class"]
            #hhhhhhhhhhhhhhh
            if raletive_class not in issue_class_list:
                continue

        # result_classFolder = os.path.join(result_folder, raletive_class)
        if not os.path.exists(result_folder):
            os.makedirs(result_folder)

        if apk_name != apk_name_temp:
            apk_name_temp = apk_name
            act_temp = act
            SNUM = 1
            id_is_null = 0
        elif act != act_temp:
            act_temp = act
            id_is_null = 0
        id_is_null = id_is_null + 1

        if not raletive_xml == '':
            if raletive_xml.find("bounds=\"") == -1:
                continue
            bound = raletive_xml.split("bounds=\"")[1].split("\"")[0]
            class_N = raletive_class.split(".")[2]
            # print class_N
            y0 = int(bound.split(',')[1].split(']')[0])
            y1 = int(bound.split(',')[2].split(']')[0])
            x0 = int(bound.split(',')[0].split('[')[1])
            x1 = int(bound.split(',')[1].split('[')[1])
            component_name = str(SNUM) + '_' +apk_name + '_' + act + '_' + str(id_is_null) + '_' + class_N

            try:
                print (x0,x1,y0,y1)
                cropped = img[y0:y1, x0:x1]
                # print cropped
                if cropped.size !=0:
                    cv2.imwrite(os.path.join(result_folder, component_name + '.png'), cropped)
                    if type_XML == "IssueXML":
                        id_or_bounds = column[index]["id_or_bounds"]
                        xbot_colorSet = column[index]["color_info"]
                        # print id_or_bounds
                        getColor = get_color_set.get_colorSet(os.path.join(result_folder, component_name + '.png'))
                        # print getColor
                        csv.writer(open(color_contrast_path, 'a')).writerow(
                            (apk_name, act, class_N, id_or_bounds, xbot_colorSet, getColor))

                        # print xbot_colorSet, str(getColor)
                        # type(xbot_colorSet) = str
                        if xbot_colorSet == str(getColor) or xbot_colorSet == str(getColor[::-1]):
                            class_successNum["total"] = class_successNum["total"] + 1
                            class_successNum[class_N] = class_successNum[class_N] + 1
                        else:
                            class_failNum["total"] = class_failNum["total"] + 1
                            class_failNum[class_N] = class_failNum[class_N] + 1
                    SNUM = SNUM + 1
            except TypeError:
                pass
            except UnboundLocalError:
                pass

    if type_XML == "IssueXML":
        issue_class_types = os.path.join(resultPath, 'color_successRatio.txt')
        with open(issue_class_types, "a") as f1:
            f1.write("success:\n")
            for cla in class_successNum:
                f1.write(cla + ": " + str(class_successNum[cla]))
                f1.write("\n")
            f1.write("\n")
            f1.write("fail:\n")
            for cla in class_successNum:
                f1.write(cla + ": " + str(class_failNum[cla]))
                f1.write("\n")


def get_components_activity(resultPath, outputsPath, scv_path):
    issue_class_list = ["android.widget.Button", "android.widget.TextView", "android.widget.ImageView",
                        "android.widget.ImageButton", "android.widget.EditText"]
    # scv_path = os.path.join(resultPath, 'test.csv')
    raletive_class = "classnameNULL"
    with open(scv_path, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        column = [row for row in reader]
    id_is_null = 0
    for index in range(len(column)):
        apk_name = column[index]["apk_name"]
        # print apk_name
        act = column[index]["active_name"]
        result_folder = os.path.join(resultPath, "A_components_activity")

        screenshot_path0 = os.path.join(outputsPath, apk_name, 'screenshot')
        # if os.listdir(screenshot_path0) == []:
        # continue
        screenshot_path = os.path.join(screenshot_path0, act)
        if not os.path.exists(screenshot_path):
            continue
        if not os.path.isdir(screenshot_path):
            img = cv2.imread(os.path.join(screenshot_path0, act))
        else:
            for file in os.listdir(screenshot_path):
                if file.endswith(".png") and not file.endswith("_thumbnail.png"):
                    img = cv2.imread(os.path.join(screenshot_path, file))

        # print img
        if column[index]["raletive_xml"] == '':
            continue
        raletive_xml = column[index]["raletive_xml"]
        if column[index]["raletive_class"] != '':
            raletive_class = column[index]["raletive_class"]
            # hhhhhhhhhhhhhhh
            if raletive_class not in issue_class_list:
                continue

        # result_classFolder = os.path.join(result_folder, raletive_class)
        if not os.path.exists(result_folder):
            os.makedirs(result_folder)

        if not raletive_xml == '':
            if raletive_xml.find("bounds=\"") == -1:
                continue
            bound = raletive_xml.split("bounds=\"")[1].split("\"")[0]
            class_N = raletive_class.split(".")[2]
            # print class_N
            y0 = int(bound.split(',')[1].split(']')[0])
            y1 = int(bound.split(',')[2].split(']')[0])
            x0 = int(bound.split(',')[0].split('[')[1])
            x1 = int(bound.split(',')[1].split('[')[1])
            component_name = apk_name + '_' + act + '_' + str(id_is_null) + '_' + class_N

            try:
                print (x0, x1, y0, y1)
                cropped = img[y0:y1, x0:x1]
                # print cropped
                if cropped.size != 0:
                    if not os.path.exists(os.path.join(result_folder, act.split('.')[len(act.split('.')) - 1], class_N)):
                        os.makedirs(os.path.join(result_folder, act.split('.')[len(act.split('.')) - 1], class_N))
                    cv2.imwrite(os.path.join(result_folder, act.split('.')[len(act.split('.')) - 1], class_N, component_name + '.png'), cropped)
                    id_is_null = id_is_null + 1
            except TypeError:
                pass
            except UnboundLocalError:
                pass