# encoding: utf-8
import change_color_class
import os
import nonIssueColorSet


pathDir1 = os.listdir('G:\\1103\work\\apktool01')
pathDir2 = os.listdir('G:\\1103\work\\apktool11')
pathDir3 = os.listdir('G:\\1103\work0\\apktool')

def getRatio(APKName):
    if APKName in pathDir1:
        outputsPath = 'G:/1103/Xbot-main/main-folder/results/outputs0'
        HOME_PATH = 'G:/1103/work/apktool01'
    elif APKName in pathDir2:
        outputsPath = 'G:/1103/Xbot-main/main-folder/results/outputs1'
        HOME_PATH = 'G:/1103/work/apktool11'
    elif APKName in pathDir3:
        outputsPath = 'G:/1103/Xbot-main/main-folder/results/outputs'
        HOME_PATH = 'G:/1103/work0/apktool'
    ids_location_inOneAPK = change_color_class.get_id_inOneAPK(os.path.join(change_color_class.resultPath, APKName), APKName, outputsPath)
    # print ids_location_inOneAPK[1]
    ids_bounds_inOneAPK = change_color_class.findInString(os.path.join(HOME_PATH, APKName), ids_location_inOneAPK[1])
    stringText = ids_bounds_inOneAPK[3]
    print "stringText"
    print stringText
    id_bound_colorSet = ids_bounds_inOneAPK[0]
    print "id_bound_colorSet"
    print id_bound_colorSet
    stringText = ids_bounds_inOneAPK[3]

    nonIssueColorAct = {}
    for act in ids_location_inOneAPK[2]:
        nonIssueColorAct[act] = nonIssueColorSet.get_nonIssueColorSet_activity(change_color_class.resultPath, act)

    colorToChange = change_color_class.find_colorToChange_self(change_color_class.resultPath, APKName, id_bound_colorSet)[0]
    # print ids_inOneAPK
    print "colorToChange_self"
    print colorToChange

    colorToChange_class = {}

    editTextId = change_color_class.changeLayout_decompileAPK(os.path.join(HOME_PATH, APKName), id_bound_colorSet, colorToChange,
                                           nonIssueColorAct, colorToChange_class)
    print "colorToChange_Layout"
    colorToChange0 = editTextId[1]
    print colorToChange0
    print 'imageId_Name'
    imageId_Name = editTextId[4]
    print imageId_Name
    Manifest = change_color_class.changeManifestF_decompileAPK(os.path.join(HOME_PATH, APKName), id_bound_colorSet, stringText)
    if editTextId[2] != {} or Manifest != {}:
        if editTextId[2] != {}:
            print editTextId[2]
        else:
            print Manifest
        # colorName_colorNew    list(set(editId)), colorToChange, id_style, colorName_colorNew, imageId_Name, imageId_style
        # decom_Path, id_style, imageId_style, imageId_Name, id_bound_colorSet, colorToChange, nonIssueColorAct, colorName_colorNew
        print editTextId[3]
        changeStyle = change_color_class.changeStyle_decompileAPK(os.path.join(HOME_PATH, APKName), editTextId[2], editTextId[5],
                                               editTextId[4], id_bound_colorSet, colorToChange, nonIssueColorAct,
                                               editTextId[3], Manifest, colorToChange_class)
        print 'colorToChange_final'
        colorToChange0 = changeStyle[0]
        print colorToChange0
        imageId_Name = changeStyle[2]
        print "imageId_Name2"
        print imageId_Name

    # print editTextId[0]  decom_Path, id_style, id_bound_colorSet, colorToChange, nonIssueColorAct
    # print editTextId[0]

    # id_conponent_bound
    print ids_location_inOneAPK[4]
    imageId_NameF = {}
    for imageIdName in imageId_Name:
        if imageIdName not in ids_location_inOneAPK[4]:
            for im in ids_location_inOneAPK[4]:
                if im[0] == imageIdName[0]:
                    imageId_NameF[ids_location_inOneAPK[4][im]] = (
                        imageId_Name[imageIdName][0], imageId_Name[imageIdName][1], im[0], im[1])
        else:
            imageId_NameF[ids_location_inOneAPK[4][imageIdName]] = (
            imageId_Name[imageIdName][0], imageId_Name[imageIdName][1], imageIdName[0], imageIdName[1])
    print imageId_NameF
    for eid in ids_location_inOneAPK[4]:
        if eid[0] in editTextId[0]:
            if eid[0] in colorToChange0:
                del colorToChange0[eid[0]]
            # editTextId[0].append(ids_location_inOneAPK[4][eid])
            # editTextId[0].remove(eid[0])
        if eid[0] in stringText:
            if stringText[eid[0]] in editTextId[0]:
                if stringText[eid[0]] in colorToChange0:
                    del colorToChange0[eid[0]]
                editTextId[0].append(ids_location_inOneAPK[4][eid])
                editTextId[0].remove(stringText[eid[0]])
            ########
            if stringText[eid[0]] in colorToChange0:
                colorToChange0[ids_location_inOneAPK[4][eid]] = colorToChange0[stringText[eid[0]]]
                del colorToChange0[stringText[eid[0]]]
        if eid[0] in ids_location_inOneAPK[5] and eid[0] in colorToChange0:
            colorToChange0[ids_location_inOneAPK[5][eid[0]]] = colorToChange0[eid[0]]
            del colorToChange0[eid[0]]
    print colorToChange0

    colorToChange_self = change_color_class.find_colorToChange_self(change_color_class.resultPath, APKName, id_bound_colorSet)[0]
    print colorToChange_class

    # print editTextId[0]
    null_id = ids_location_inOneAPK[3]
    for issueId in id_bound_colorSet:
        if issueId.startswith('[') and issueId.endswith(']'):
            null_id.append(issueId)
    # print null_id
    splitId = list(set(editTextId[0] + null_id))
    print splitId


    # com.beyzas.ravan???

    colorClassNum = {}
    colorClassNum["colorToChange_self"] = []
    colorClassNum["colorToChange_class"] = []
    colorClassNum["other"] = []
    for fid in colorToChange0:
        if fid in splitId:
            continue
        if fid in colorToChange_self:
            colorClassNum["colorToChange_self"].append(fid)
        elif fid in colorToChange_class:
            colorClassNum["colorToChange_class"].append(fid)
        else:
            colorClassNum["other"].append(fid)
    print colorClassNum
    selfN = len(colorClassNum["colorToChange_self"])
    classN = len(colorClassNum["colorToChange_class"])
    otherN = len(colorClassNum["other"])
    sumN = selfN + classN + otherN
    if sumN != 0:
        print float(selfN) / sumN, float(classN) / sumN, float(otherN) / sumN

    return splitId, colorClassNum, selfN, classN, otherN

# getRatio("com.link.kuaiji")
# getRatio("de.markusfisch.android.shadereditorF049D62A646B115791D9E7817EB7410EC9137880")

apksSplitId = {}
apksColorClass = {}
apksPartN = {}
selfS = 0
classS = 0
otherS = 0

for APKName in os.listdir("G:\\1103\work0\\apks0"):
    APKName = APKName.split('.apk')[0]
    print APKName
    splitId, colorClassNum, selfN, classN, otherN = getRatio(APKName)
    apksSplitId[APKName] = splitId
    apksColorClass[APKName] = colorClassNum["colorToChange_self"] + colorClassNum["colorToChange_class"] + colorClassNum["other"]
    apksPartN[APKName] = (selfN, classN, otherN)
    selfS = selfS + selfN
    classS = classS + classN
    otherS = otherS + otherN

print apksSplitId
print apksColorClass
print apksPartN

print selfS
print classS
print otherS