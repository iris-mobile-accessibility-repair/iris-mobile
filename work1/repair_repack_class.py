# encoding: utf-8

import os
import shutil
import commands
import nonIssueColorSet
import change_color_class

results_folder = "/home/zyx/Desktop/work0"
apksEditSet = {}

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


def de_re_pack(apk_path, apkname, results_folder):
    recompileAPKName = apkname + ".apk"
    decompilePath = os.path.join(results_folder, "apktool", apkname)
    repackagedAppPath = os.path.join(results_folder, "repackaged")

    if not os.path.exists(decompilePath):
        os.makedirs(decompilePath)

    if not os.path.exists(repackagedAppPath):
        os.makedirs(repackagedAppPath)

    decompile(apk_path, decompilePath)

    print "change_color"
    ids_location_inOneAPK = change_color_class.get_id_inOneAPK(os.path.join(change_color_class.resultPath, apkname), apkname)
    # print ids_location_inOneAPK[1]
    ids_bounds_inOneAPK = change_color_class.findInString(decompilePath, ids_location_inOneAPK[1])
    stringText = ids_bounds_inOneAPK[3]
    id_bound_colorSet = ids_bounds_inOneAPK[0]
    print id_bound_colorSet
    stringText = ids_bounds_inOneAPK[3]

    if id_bound_colorSet != {}:
        nonIssueColorAct = {}
        for act in ids_location_inOneAPK[2]:
            nonIssueColorAct[act] = nonIssueColorSet.get_nonIssueColorSet_activity(change_color_class.resultPath, act)

        colorToChange = change_color_class.find_colorToChange_self(change_color_class.resultPath, apkname, id_bound_colorSet)
        # print ids_inOneAPK
        print colorToChange[0]

        editTextId = change_color_class.changeLayout_decompileAPK(decompilePath, id_bound_colorSet, colorToChange[0], nonIssueColorAct)
        print editTextId[1]
        # print editTextId[2]
        Manifest = change_color_class.changeManifestF_decompileAPK(decompilePath, id_bound_colorSet, stringText)
        if editTextId[2] != {} or Manifest != {}:
            if editTextId[2] != {}:
                print editTextId[2]
            else:
                print Manifest
            # colorName_colorNew
            # print editTextId[3]
            changeStyle = change_color_class.changeStyle_decompileAPK(decompilePath, editTextId[2], editTextId[5], editTextId[4], id_bound_colorSet,
                                                   colorToChange[0], nonIssueColorAct, editTextId[3], Manifest)
            print changeStyle[0]

        for eid in ids_location_inOneAPK[4]:
            if eid[0] in editTextId[0]:
                editTextId[0].append(ids_location_inOneAPK[4][eid])
                editTextId[0].remove(eid[0])
            if eid[0] in stringText:
                if stringText[eid[0]] in editTextId[0]:
                    editTextId[0].append(ids_location_inOneAPK[4][eid])
                    editTextId[0].remove(stringText[eid[0]])
        # print editTextId[0]
        null_id = ids_location_inOneAPK[3]
        for issueId in id_bound_colorSet:
            if issueId.startswith('[') and issueId.endswith(']'):
                null_id.append(issueId)
        # print null_id
        splitId = list(set(editTextId[0] + null_id))
        print splitId
        apksEditSet[apkname] = splitId

        recompile(decompilePath, repackagedAppPath, recompileAPKName)


def startRepkg(results_folder):
    # nonIssueColorClass = nonIssueColorSet.get_nonIssueColorSet_class(change_color_class.resultPath)
    # print nonIssueColorClass
    for apk in os.listdir(os.path.join(results_folder, "apks")):
        if not apk.endswith(".apk"):
            continue
        apkname = apk.split(".apk")[0]
        if not os.path.exists(os.path.join(change_color_class.resultPath, apkname)):
            continue
        de_re_pack(os.path.join(results_folder, "apks", apk), apkname, results_folder)
        os.remove(os.path.join(results_folder, "apks", apk))

startRepkg(results_folder)
print apksEditSet