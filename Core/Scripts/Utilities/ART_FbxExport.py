import sys
import os
import json

import maya.standalone as std
import maya.cmds as cmds
import maya.mel as mel

std.initialize(name='python')

if sys.argv[3] == "z":
    # set up axis to z
    cmds.upAxis(ax='z')



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def fbx_export():

    # log some basic info about incoming data
    sys.stdout.write("\n\n")
    sys.stdout.write("Opening File:\n")
    sys.stdout.write(str(sys.argv[1]))
    sys.stdout.write("\n\n")
    sys.stdout.write("Export Data File:\n\n")
    sys.stdout.write(str(sys.argv[2]))
    sys.stdout.write("\n\n")

    # open the maya file
    cmds.file(str(sys.argv[1]), open=True, ignoreVersion=True, force=True, prompt=False)

    cmds.loadPlugin("ARTv2_Stretchy_IK")
    currentMode = cmds.evaluationManager(q=True, mode=True)[0]
    cmds.evaluationManager(mode="off")

    # load data back into dict format
    f = open(str(sys.argv[2]), 'r')
    sys.stdout.write(str(f))
    data = json.load(f)
    f.close()

    # the data is a dictionary of characters and their export information. That data might look like:
    # character: [[seq1 data], [seq2 data]]
    # we need to go through each character's data, go through each sequence, and export that sequence out
    for character in data:
        sequences = data.get(character)
        sys.stdout.write("\n\n")
        sys.stdout.write(str(sequences))
        sys.stdout.write("\n")
        sys.stdout.write(str(len(sequences)))
        sys.stdout.write("\n")

        # sequence data as follows [0-6]:
        # Export Meshes? Export Morphs? Export Attrs? Which Morphs? Which Attrs? Pre Script? Path? Post Script? Path?
        # Sequence data [7] as follows:
        # [character, export?, fbxPath, start, end, fps, rotation interp, sample rate, root export]

        # loop through each sequence in the sequence data
        for sequence in sequences:

            # open file
            cmds.file(str(sys.argv[1]), open=True, ignoreVersion=True, force=True, prompt=False)

            exportMesh = sequence[0]
            exportMorphs = sequence[1]
            exportAttrs = sequence[2]
            morphTargets = sequence[3]
            customAttrs = sequence[4]
            preScript = sequence[5]
            postScript = sequence[6]
            sequenceInfo = sequence[7]

            # PRE-SCRIPT
            if preScript[0]:
                sys.stdout.write("\nExecuting Pre-Script...\n")
                status = executeScript(preScript[1])

                if status:
                    sys.stdout.write("\nPre-Script successfully executed!\n")
                else:
                    sys.stdout.write("\nPre-Script NOT successfully executed :( \n")

            # if this sequence is marked for export
            if sequenceInfo[1] is True:

                euler = False
                quat = True

                # get the outputPath
                filePath = sequenceInfo[2]

                # get the start and end frame
                startFrame = float(sequenceInfo[3])
                endFrame = float(sequenceInfo[4])
                cmds.playbackOptions(min=startFrame, max=endFrame, ast=startFrame, aet=endFrame)
                cmds.refresh()

                # get the fps
                fps = sequenceInfo[5]
                sys.stdout.write("\n\n" + str(fps) + "\n\n")
                cmds.currentUnit(time=str(fps))
                cmds.refresh()

                # get the rotation interpolation
                interp = sequenceInfo[6]
                if interp == "Quaternion Slerp":
                    euler = False
                    quat = True
                if interp == "Independent Euler-Angle":
                    euler = True
                    quat = False

                # set the fbx export flags
                setExportFlags(startFrame, endFrame, euler, quat)

                # get the sample rate
                sample = int(sequenceInfo[7])

                # get the root export option
                rootExport = sequenceInfo[8]

                # build selection of what to export
                toExport = []

                # rename joints if override data is present
                refs = cmds.ls(type='reference')
                for i in refs:
                    rFile = cmds.referenceQuery(i, f=True)
                    cmds.file(rFile, importReference=True)

                if cmds.objExists(character + ":ART_RIG_ROOT.exportOverrides"):
                    connections = cmds.listConnections(character + ":ART_RIG_ROOT.exportOverrides")
                    if connections is not None:
                        attrs = cmds.listAttr(connections[0], ud=True)

                        for attr in attrs:
                            value = cmds.getAttr(connections[0] + "." + attr)

                            if cmds.objExists(character + ":" + attr):
                                cmds.rename(character + ":" + attr, character + ":" + value)

                # EXPORT MESHES
                if exportMesh:
                    # get meshes
                    if cmds.objExists(character + ":ART_RIG_ROOT"):
                        if cmds.objExists(character + ":ART_RIG_ROOT.LOD_0_Meshes"):
                            meshes = cmds.listConnections(character + ":ART_RIG_ROOT.LOD_0_Meshes")

                            for mesh in meshes:
                                toExport.append(mesh)

                # EXPORT MORPHS
                if exportMorphs:
                    for each in morphTargets:
                        if cmds.objExists(each):
                            if (each.partition(":")[0]) == character:
                                conns = cmds.listConnections(each, type="mesh")
                                if conns is not None:
                                    toExport.extend(conns)

                # SKELETON
                skeleton = [character + ":root"]
                skeleton.extend(reversed(cmds.listRelatives(character + ":root", type='joint', allDescendents=True)))
                toExport.append(skeleton[0])

                sys.stdout.write("\n")
                sys.stdout.write(str(skeleton))
                sys.stdout.write("\n")

                # bake skeleton and blendshapes (using sample rate)
                # cmds.select(clear=True)
                # if exportMorphs:
                #     cmds.select(morphTargets, add=True)

                # bake down animation onto skeleton and blendshapes
                # cmds.bakeResults(simulation=True, sampleBy=sample, time=(startFrame, endFrame))

                # run euler filter and fix tangents
                cmds.select(skeleton)
                cmds.filterCurve()
                cmds.selectKey()
                cmds.keyTangent(itt="linear", ott="linear")

                # deal with custom attrs (deleting if user chose not to export)
                standardAttrs = ["translateX", "translateY", "translateZ", "rotateX", "rotateY", "rotateZ",
                                 "scaleX", "scaleY", "scaleZ", "visibility"]
                if exportAttrs:
                    available_attrs = cmds.listAttr(skeleton[0], keyable=True)
                    for attr in available_attrs:
                        if attr not in standardAttrs:
                            if (character + ":" + attr) not in customAttrs:
                                sys.stdout.write("\n\n")
                                sys.stdout.write("Removing Attr:")
                                sys.stdout.write(str(attr))
                                sys.stdout.write("\n\n")

                                # remove the attribute from the root
                                cmds.deleteAttr(skeleton[0], at=attr)

                # Root Export Options
                sys.stdout.write("\n\n" + str(rootExport) + "\n\n")
                if rootExport != "Export Root Animation":
                    if rootExport == "Zero Root":
                        sys.stdout.write("\nZeroing Out Root Animation\n")
                        cmds.cutKey(skeleton[0])
                        attrs = ["translate", "rotate", "scale"]
                        for attr in attrs:
                            try:
                                cmds.disconnectAttr(character + ":driver_root." + attr, character + ":root." + attr)
                            except Exception, e:
                                sys.stdout.write("\n" + str(e) + "\n")

                        for zeroAttr in [".tx", ".ty", ".tz", ".rx", ".ry", ".rz"]:
                            cmds.setAttr(character + ":root" + zeroAttr, 0)

                    if rootExport == "Zero Root, Keep World Space":
                        sys.stdout.write("\nZeroing Out Root Animation, Keeping World Space on rest of rig\n")
                        # first, find children that need to be locked in place and create a locator for each
                        rootConnections = cmds.listRelatives(skeleton[0], children=True, type="joint")
                        lockNodes = []
                        locators = []

                        for conn in rootConnections:
                            lockNodes.append(conn)
                        constraints = []

                        for lockNode in lockNodes:
                            loc = cmds.spaceLocator(name=lockNode + "_loc")[0]
                            locators.append(loc)
                            constraint = cmds.parentConstraint(lockNode, loc)[0]
                            constraints.append(constraint)

                            sys.stdout.write("Locking down " + lockNode + " to zero out root.")
                            sys.stdout.write("\n")

                        # then bake the locators
                        cmds.select(clear=True)
                        for lockNode in lockNodes:
                            cmds.select(lockNode + "_loc", add=True)

                        cmds.bakeResults(simulation=True, sb=sample, time=(float(startFrame), float(endFrame)))
                        cmds.delete(constraints)

                        # reverse the constraints so the bones are constrained to the locator
                        boneConstraints = []
                        for lockNode in lockNodes:
                            con = cmds.parentConstraint(lockNode + "_loc", lockNode)[0]
                            boneConstraints.append(con)

                        # disconnect attrs on root bone
                        attrs = ["translate", "rotate", "scale"]
                        for attr in attrs:
                            try:
                                cmds.disconnectAttr(character + ":driver_root." + attr, character + ":root." + attr)
                            except Exception, e:
                                sys.stdout.write("\n" + str(e) + "\n")

                        # cut keys on the root bone
                        cmds.cutKey(skeleton[0])
                        cmds.setAttr(skeleton[0] + ".tx", 0)
                        cmds.setAttr(skeleton[0] + ".ty", 0)
                        cmds.setAttr(skeleton[0] + ".tz", 0)
                        cmds.setAttr(skeleton[0] + ".rx", 0)
                        cmds.setAttr(skeleton[0] + ".ry", 0)
                        cmds.setAttr(skeleton[0] + ".rz", 0)

                        # bake bones now in world space
                        cmds.select(clear=True)
                        for lockNode in lockNodes:
                            cmds.select(lockNode, add=True)

                        cmds.bakeResults(simulation=True, sb=sample, time=(float(startFrame), float(endFrame)))
                        cmds.delete(boneConstraints)

                        # run an euler filter
                        cmds.select(skeleton)
                        cmds.filterCurve()

                # POST - SCRIPT
                if postScript[0]:
                    sys.stdout.write("\nExecuting Post Script...\n")

                    status = executeScript(postScript[1])

                    if status:
                        sys.stdout.write("\nPost-Script successfully executed!\n")
                    else:
                        sys.stdout.write("\nPost-Script NOT successfully executed :( \n")

                # EXPORT FBX
                cmds.select(toExport)

                try:
                    mel.eval("FBXExport -f \"" + filePath + "\" -s")
                except:
                    cmds.warning("no path specified..")

    cmds.evaluationManager(mode=currentMode)

    # close mayapy
    os.remove(str(sys.argv[2]))
    std.uninitialize()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def setExportFlags(startFrame, endFrame, euler=False, quat=True):

    # in 2015, if oneClick isn't loaded, it will throw up an error
    try:
        cmds.loadPlugin("OneClick.mll")
        sys.stdout.write("Loaded OneClick plugin.")
        sys.stdout.write("\n")
    except Exception, e:
        sys.stderr.write("unable to load OneClick plugin.")
        sys.stderr.write("\n")

    try:
        cmds.loadPlugin("fbxmaya.mll")
        sys.stdout.write("Loaded FBX plugin.")
        sys.stdout.write("\n")
    except Exception, e:
        sys.stderr.write("unable to load FBX plugin.")
        sys.stderr.write("\n")

    # Mesh
    mel.eval("FBXExportSmoothingGroups -v true")
    mel.eval("FBXExportHardEdges -v false")
    mel.eval("FBXExportTangents -v false")
    mel.eval("FBXExportInstances -v false")
    mel.eval("FBXExportInAscii -v true")
    mel.eval("FBXExportSmoothMesh -v false")

    # Animation
    mel.eval("FBXExportBakeComplexAnimation -v true")
    mel.eval("FBXExportBakeComplexStart -v " + str(startFrame))
    mel.eval("FBXExportBakeComplexEnd -v " + str(endFrame))
    mel.eval("FBXExportReferencedAssetsContent -v true")
    mel.eval("FBXExportBakeComplexStep -v 1")
    mel.eval("FBXExportUseSceneName -v false")
    mel.eval("FBXExportFileVersion -v FBX201400")

    if euler:
        mel.eval("FBXExportQuaternion -v euler")

    if quat:
        mel.eval("FBXExportQuaternion -v quaternion")

    mel.eval("FBXExportShapes -v true")
    mel.eval("FBXExportSkins -v true")
    mel.eval("FBXExportUpAxis z")

    # garbage we don't want
    # Constraints
    mel.eval("FBXExportConstraints -v false")

    # Cameras
    mel.eval("FBXExportCameras -v false")

    # Lights
    mel.eval("FBXExportLights -v false")

    # Embed Media
    mel.eval("FBXExportEmbeddedTextures -v false")

    # Connections
    mel.eval("FBXExportInputConnections -v false")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def executeScript(scriptPath):

    sourceType = ""
    status = False

    if scriptPath.find(".py") != -1:
        sourceType = "python"

    if scriptPath.find(".mel") != -1:
        sourceType = "mel"

    # MEL
    if sourceType == "mel":
        try:
            command = ""
            # open the file, and for each line in the file, add it to our command string.
            f = open(scriptPath, 'r')
            lines = f.readlines()
            for line in lines:
                command += line

            import maya.mel as mel
            mel.eval(command)

            # save the file
            cmds.file(save=True, type="mayaAscii")
            status = True
        except:
            pass

    # PYTHON
    if sourceType == "python":
        try:
            execfile("" + scriptPath + "")

            # save the file
            cmds.file(save=True, type="mayaAscii")
            status = True
        except:
            pass

    return status


fbx_export()
