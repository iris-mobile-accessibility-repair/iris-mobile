# encoding: utf-8
import os
import get_results

# outputsPath = '/home/zyx/Desktop/Xbot-main-analyze/main-folder/results/outputs'
# resultPath = "/home/zyx/Desktop/result000"
outputsPath = '/home/zyx/Desktop/Xbot-main/main-folder/results/outputs'
resultPath = "/home/zyx/Desktop/result"


if __name__ == "__main__":
    get_results.splitContrast(resultPath, outputsPath)
    false_xml_scv = os.path.join(resultPath, 'false_xmlLog.csv')
    nonIssue_xml_scv = os.path.join(resultPath, 'nonIssue_xml_scv.csv')

    #result_folder = os.path.join(resultPath, apk_name)
    #components_path = os.path.join(result_folder, act, type_XML)
    get_results.get_components(resultPath, outputsPath, false_xml_scv, "IssueXML")
    get_results.get_components(resultPath, outputsPath, nonIssue_xml_scv, "nonIssueXML")
    # #
    # # #result_folder = os.path.join(resultPath, "A_components_outputs", type_XML)
    # # get_results.get_components_inOneFolder(resultPath, outputsPath, false_xml_scv, "IssueXML")
    # # get_results.get_components_inOneFolder(resultPath, outputsPath, nonIssue_xml_scv, "nonIssueXML")
    # #
    # # #result_classFolder = os.path.join(result_folder, raletive_class)
    # get_results.get_components_classFolder(resultPath, outputsPath, false_xml_scv, "IssueXML")
    # get_results.get_components_classFolder(resultPath, outputsPath, nonIssue_xml_scv, "nonIssueXML")


    # get_components_APKFolder
    get_results.get_components_APKFolder(resultPath, outputsPath, false_xml_scv, "IssueXML")
    get_results.get_components_APKFolder(resultPath, outputsPath, nonIssue_xml_scv, "nonIssueXML")

    get_results.get_components_activity(resultPath, outputsPath, nonIssue_xml_scv)
