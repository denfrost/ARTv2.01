import maya.cmds as cmds
import utils as utils
import json
import os
import subprocess
import tempfile
from functools import partial
from ThirdParty.Qt import QtGui, QtCore, QtWidgets


def find_characters():

    characterInfo = []

    allNodes = cmds.ls(type="network")
    characterNodes = []
    for node in allNodes:
        attrs = cmds.listAttr(node)
        if "rigModules" in attrs:
            characterNodes.append(node)

    # go through each node, find the character name, the namespace on the node, and the picker attribute
    for node in characterNodes:
        try:
            namespace = cmds.getAttr(node + ".namespace")
        except Exception:
            namespace = cmds.getAttr(node + ".name")

        characterInfo.append([node, namespace])

    return characterInfo


def batch_export(directory):

    settings = QtCore.QSettings("Epic Games", "ARTv2")
    toolsPath = settings.value("toolsPath")

    upAxis = cmds.upAxis(q=True, ax=True)

    directory = utils.returnFriendlyPath(directory)
    files = os.listdir(directory)
    files_to_export = []
    valid_types = [".ma", ".mb"]

    # get files to export
    for each in files:
        if os.path.isfile(os.path.join(directory, each)):
            if os.path.splitext(each)[1] in valid_types:
                if each.find("export_TEMP") == -1:
                    files_to_export.append(os.path.join(directory, each))

    # create a log file
    stdoutFile = os.path.join(directory, "export_log.txt")
    out = file(stdoutFile, 'w')

    # loop through files and export
    for f in files_to_export:

        cmds.file(f, o=True, force=True)

        # save copy of scene to temp location
        sourceFile = cmds.file(q=True, sceneName=True)
        filePath = os.path.dirname(sourceFile)
        tempFile = os.path.join(filePath, "export_TEMP.ma")

        cmds.file(rename=tempFile)
        cmds.file(save=True, type="mayaAscii", force=True)

        # construct characterData
        characters = find_characters()

        characterData = {}
        for character in characters:

            try:
                data = json.loads(cmds.getAttr(character[0] + ".fbxAnimData"))
                for d in data:
                    d[0] = False
                    d[1] = False

                characterData[character[1]] = data
            except:
                continue

        # pass tempFile and characterData to mayapy instance for processing
        mayapy = utils.getMayaPyLoc()
        if os.path.exists(mayapy):
            script = utils.returnFriendlyPath(os.path.join(toolsPath, "Core\Scripts\Utilities\ART_FbxExport.py"))

            # create a temp file with the json data
            with tempfile.NamedTemporaryFile(delete=False) as temp:
                json.dump(characterData, temp)
                temp.close()

            # open mayapy, passing in export file and character data
            subprocess.Popen(mayapy + ' ' + "\"" + script + "\"" + ' ' + "\"" + tempFile + "\"" + ' ' +
                             "\"" + temp.name + "\"" + ' ' + "\"" + upAxis + "\"", stdout=out, stderr=out)

    # close the output file (for logging)
    out.close()
