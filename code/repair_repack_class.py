# encoding: utf-8

import os
import shutil
import commands
import time

import nonIssueColorSet
import change_color_class

import harmonizationTs2
import get_clickableID2
import colorSet
import main

# path of work
results_folder = "/IRIS/iris-mobile"
# path of reference DB
resultPath = '/IRIS/iris-mobile/refDB'
# path of output of Xbot
outputsPath = '/IRIS/Xbot-main/main-folder/results/outputs'
apksEditSet = {}
colorChanged = {}
imageidsSet = {}
idStyleSet = {}


def decompile(eachappPath, decompileAPKPath):
    print "decompiling..."
    cmd = "apktool d {0} -f -o {1}".format(eachappPath, decompileAPKPath)
    os.system(cmd)

def recompile(decompileAPKPath, repackagedAppPath, recompileAPKName):
    print "recompile..."
    cmd = "apktool b {0} -o {1}".format(decompileAPKPath, os.path.join(repackagedAppPath, recompileAPKName))
    # print cmd
    output = commands.getoutput(cmd)
    return output


def de_re_pack(apk_path, apkname, results_folder, ColorSet, outputsPath):
    idS = []
    recompileAPKName = apkname + ".apk"
    decompilePath = os.path.join(results_folder, "apktool", apkname)
    repackagedAppPath = os.path.join(results_folder, "repackaged")

    if not os.path.exists(decompilePath):
        os.makedirs(decompilePath)

    if not os.path.exists(repackagedAppPath):
        os.makedirs(repackagedAppPath)

    decompile(apk_path, decompilePath)

    # Iris2

    # outputsPath = outputsPath
    # outputsPath = '/home/zyx/Desktop/Xbot-main/main-folder/results/outputs'
    act_T_Alpha = harmonizationTs2.get_bestT_Alpha(apkname, outputsPath)
    print "act_T_Alpha"
    print act_T_Alpha
    clickableIds, clickableIdsInAct = get_clickableID2.getClickableID(apkname, outputsPath)
    print 'clickableIds'
    print clickableIds
    # Iris2

    print "change_color"
    ids_location_inOneAPK = change_color_class.get_id_inOneAPK(os.path.join(resultPath, apkname), apkname, outputsPath)
    # print ids_location_inOneAPK[1]
    ids_bounds_inOneAPK = change_color_class.findInString(decompilePath, ids_location_inOneAPK[1])
    stringText = ids_bounds_inOneAPK[3]
    print "stringText"
    print stringText
    id_bound_colorSet = ids_bounds_inOneAPK[0]
    print "id_bound_colorSet"
    print id_bound_colorSet
    stringText = ids_bounds_inOneAPK[3]

    if id_bound_colorSet != {}:
        nonIssueColorAct = {}
        for act in ids_location_inOneAPK[2]:
            nonIssueColorAct[act] = ColorSet
            # nonIssueColorAct[act] = nonIssueColorSet.get_nonIssueColorSet_activity(resultPath, act)

        colorToChange = change_color_class.find_colorToChange_self(resultPath, apkname, id_bound_colorSet, act_T_Alpha)
        # print ids_inOneAPK
        colorToChange_self = colorToChange[0]
        print "colorToChange_self"
        print colorToChange_self

        colorToChange_class = {}

        editTextId = change_color_class.changeLayout_decompileAPK(decompilePath, id_bound_colorSet, colorToChange[0], nonIssueColorAct, colorToChange_class, act_T_Alpha)
        print "colorToChange_Layout"
        colorToChange0 = editTextId[1]
        print colorToChange0
        # print editTextId[2]
        print 'imageId_Name'
        imageId_Name = editTextId[4]
        print imageId_Name
        Manifest = change_color_class.changeManifestF_decompileAPK(decompilePath, id_bound_colorSet, stringText)
        if editTextId[2] != {} or Manifest != {}:
            if editTextId[2] != {}:
                print editTextId[2]
            else:
                print Manifest
            # colorName_colorNew
            # print editTextId[3]
            changeStyle = change_color_class.changeStyle_decompileAPK(decompilePath, editTextId[2], editTextId[5], editTextId[4], id_bound_colorSet,
                                                   colorToChange[0], nonIssueColorAct, editTextId[3], Manifest, colorToChange_class, act_T_Alpha)
            print 'colorToChange_final'
            colorToChange0 = changeStyle[0]
            print colorToChange0
            if editTextId[2] != {}:
                print "id_style"
                for et in editTextId[2]:
                    idS.append(editTextId[2][et][0])
                idS = list(set(idS))
                print idS
            imageId_Name = changeStyle[2]
            print "imageId_Name2"
            print imageId_Name

        # id_conponent_bound
        ids_location = ids_location_inOneAPK[4]
        print ids_location_inOneAPK[4]
        imageId_NameF = {}
        for imageIdName in imageId_Name:
            if imageIdName in ids_location_inOneAPK[4]:
                imageId_NameF[ids_location_inOneAPK[4][imageIdName]] = (
            imageId_Name[imageIdName][0], imageId_Name[imageIdName][1], imageIdName[0], imageIdName[1])
            else:
                for il in ids_location_inOneAPK[4]:
                    if imageIdName[0] == il[0]:
                        imageId_NameF[ids_location_inOneAPK[4][il]] = (
                            imageId_Name[imageIdName][0], imageId_Name[imageIdName][1], imageIdName[0], imageIdName[1])
                    break
        print imageId_NameF

        imageids = change_color_class.changeImages_decompileAPK(decompilePath, id_bound_colorSet, imageId_NameF, clickableIds)
        print imageids
        for imageid in imageids:
            colorToChange0[imageid] = "image"

        for eid in ids_location_inOneAPK[4]:
            if eid[0] in editTextId[0]:
                if eid[0] in colorToChange0:
                    del colorToChange0[eid[0]]
                # editTextId[0].append(ids_location_inOneAPK[4][eid])
                # editTextId[0].remove(eid[0])
                if eid[0] in idS:
                    idS.remove(eid[0])
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
                if stringText[eid[0]] in idS:
                    idS.append(ids_location_inOneAPK[4][eid])
                    idS.remove(stringText[eid[0]])
            if eid[0] in ids_location_inOneAPK[5] and eid[0] in colorToChange0:
                colorToChange0[ids_location_inOneAPK[5][eid[0]]] = colorToChange0[eid[0]]
                del colorToChange0[eid[0]]
            if eid[0] in ids_location_inOneAPK[5] and eid[0] in idS:
                idS.append(ids_location_inOneAPK[5][eid[0]])
                idS.remove(eid[0])
        print colorToChange0

        colorToChange_self = change_color_class.find_colorToChange_self(resultPath, apkname, id_bound_colorSet, act_T_Alpha)[0]
        print colorToChange_class
        recompile(decompilePath, repackagedAppPath, recompileAPKName)


def startRepkg(results_folder):
    # createDB
    main.createDB(outputsPath, resultPath)
    ColorSet = nonIssueColorSet.get_nonIssueColorSet_activity2(resultPath)
    # ColorSet = colorSet.ColorSet
    # nonIssueColorClass = nonIssueColorSet.get_nonIssueColorSet_class(change_color_class.resultPath)
    # print nonIssueColorClass
    for apk in os.listdir(os.path.join(results_folder, "apks")):
        if not apk.endswith(".apk"):
            continue
        apkname = apk.split(".apk")[0]
        de_re_pack(os.path.join(results_folder, "apks", apk), apkname, results_folder, ColorSet, outputsPath)
        os.remove(os.path.join(results_folder, "apks", apk))

time_start = time.time()
startRepkg(results_folder)
time_end = time.time()
time_c = time_end - time_start #运行所花时间
print('time cost', time_c, 's')
