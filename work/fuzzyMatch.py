# encoding: utf-8
import os
from fuzzywuzzy import fuzz
# print fuzz.token_set_ratio("AAAaaaa", "aaaaAAA")

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
            print (file, fuzz.token_set_ratio(actName, fileT), fileT)
            similarAct.append(file)
    return similarAct


print getSimilarStr('ActivitySettings')