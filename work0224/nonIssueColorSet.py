# encoding: utf-8
import os

from fuzzywuzzy import fuzz

import get_color_set

# import get_results

# resultPath = "/home/zyx/Desktop/result000"
apkNonIssueColorSet = {}
issue_class_list = ["android.widget.Button", "android.widget.TextView", "android.widget.ImageView", "android.widget.ImageButton", "android.widget.EditText", "android.widget.View",
                    'android.widget.CheckBox']

# resultPath = "G:/1103/result"
resultPath = "/home/zyx/Desktop/result"
actPath = os.path.join(resultPath, "A_components_activity")
def spiltStr(str):
    if str.upper().find('ACTIVITY') != -1:
        str = str.upper().replace('ACTIVITY', '')
    elif str.upper().find('ACT') != -1:
        str = str.upper().replace('ACT', '')
    return str

def getSimilarStr(actName):
    similarAct = []
    actName = spiltStr(actName)
    for file in os.listdir(actPath):
        # print file
        fileT = file
        fileT = spiltStr(fileT)
        # print fileT
        if fuzz.token_set_ratio(actName, fileT) > 60:
            # print (file, fuzz.token_set_ratio(actName, fileT), fileT)
            similarAct.append(file)
    return similarAct


def get_nonIssueColorSet(resultPath, apkName):
    nonIssueImage_path = os.path.join(resultPath, apkName, "nonIssueXML")
    classColorSet = {}
    # for cl in get_results.issue_class_list:
    for cl in issue_class_list:
        classColorSet[cl.split(".")[2]] = []
    if not os.path.exists(nonIssueImage_path):
        return classColorSet
    for image in os.listdir(nonIssueImage_path):
        if not image.endswith('.png'):
            continue
        colorSet = get_color_set.get_nonIssueColorSet(os.path.join(nonIssueImage_path, image))
        classTag = (image.split("_")[len(image.split("_")) - 1]).split('.')[0]
        if 'android.widget.' + classTag not in issue_class_list:
            classTag = 'TextView'
        if colorSet != []:
            # print classTag
            classColorSet[classTag].append(colorSet)
    apkNonIssueColorSet[apkName] = classColorSet
    return classColorSet

def get_allNonIssueColorSet(resultPath):
    for apk in os.listdir(resultPath):
        print apk
        if not os.path.exists(os.path.join(resultPath, apk, "nonIssueXML")):
            continue
        print get_nonIssueColorSet(resultPath, apk)
    return apkNonIssueColorSet

# print get_allNonIssueColorSet(resultPath)
# print get_nonIssueColorSet(resultPath, "sick.sick.fifty")

def get_nonIssueColorSet_class(resultPath):
    nonIssueImage_classPath = os.path.join(resultPath, "A_components_class", "nonIssueXML")
    classColorSet = {}
    # for cl in get_results.issue_class_list:
    for cl in issue_class_list:
        classColorSet[cl.split(".")[2]] = []
    if not os.path.exists(nonIssueImage_classPath):
        return classColorSet
    for file in os.listdir(nonIssueImage_classPath):
        fileT = file
        classTag = (fileT.split(".")[2]).split('_')[0]
        for image in os.listdir(os.path.join(nonIssueImage_classPath, file)):
            if not image.endswith('.png'):
                continue
            colorSet = get_color_set.get_nonIssueColorSet(os.path.join(nonIssueImage_classPath, file, image))
            if colorSet != []:
                classColorSet[classTag].append(colorSet)
    return classColorSet

# print get_nonIssueColorSet_class("/home/zyx/Desktop/result")

def get_nonIssueColorSet_activity(resultPath, act):
    classColorSet = {}
    # print act
    similarActList = getSimilarStr(act)
    # for cl in get_results.issue_class_list:
    for cl in issue_class_list:
        classColorSet[cl.split(".")[2]] = []
    # print act
    # print similarActList
    for similarAct in similarActList:

        nonIssueImage_classPath = os.path.join(resultPath, "A_components_activity", similarAct)

        if not os.path.exists(nonIssueImage_classPath):
            return classColorSet
        for file in os.listdir(nonIssueImage_classPath):
            for image in os.listdir(os.path.join(nonIssueImage_classPath, file)):
                if not image.endswith('.png'):
                    continue
                colorSet = get_color_set.get_nonIssueColorSet(os.path.join(nonIssueImage_classPath, file, image))
                if colorSet != []:
                    classColorSet[file].append(colorSet)
    # print classColorSet
    return classColorSet

# print get_nonIssueColorSet_activity("/home/zyx/Desktop/result", "AboutActivity")