
import os
import time

import maya.cmds as cmds
import maya.mel as mel
import Utilities.utils as utils

import Utilities.interfaceUtils as interfaceUtils
import Utilities.riggingUtils as riggingUtils
from ThirdParty.Qt import QtGui, QtCore, QtWidgets


class ART_BuildProgress_UI():
    """
    This class kicks off building all of the rigs for the modules. It displays an interface that shows progress and
    displays information about the rig build.

    It exports skin weights, rebuilds the skeleton in rig pose, imports skin weights, runs any pre-script,
    calls on each module's rig building code, sets up rig parenting and hierarchy, and finally runs any post-script.

        .. image:: /images/buildProgress.gif

    """

    def __init__(self, mainUI):
        """
        Instantiates the class, getting the QSettings and then calling on the function to build the UI for the tool.

        :param mainUI: The instance of the Rig Creator UI that this class was called from.

        .. seealso:: ART_BuildProgressUI.buildUI

        """

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.projectPath = settings.value("projectPath")
        self.iconsPath = settings.value("iconPath")

        self.mainUI = mainUI
        self.rigData = []
        self.warnings = 0
        self.errors = 0

        # build the UI
        if cmds.window("ART_BuildProgressWin", exists=True):
            cmds.deleteUI("ART_BuildProgressWin", wnd=True)

        self.buildUI()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildUI(self):
        """
        Builds the interface, which doesn't really have any user-interaction, but is there to display information
        about the progress of the rig build. There are two QProgressBars that show current module build progress and
        total build progress, then a QTextEdit which outputs information about what the build process is currently
        working on.

        After the interface is built, it sets the rig pose on the joints of each module.

        """

        # create the main window
        self.mainWin = QtWidgets.QMainWindow(interfaceUtils.getMainWindow())
        self.mainWin.setStyleSheet("background-color: rgb(0, 0, 0);, color: rgb(0,0,0);")

        self.style = interfaceUtils.get_style_sheet("artv2_style")
        self.mainWin.setStyleSheet(self.style)

        # create the main widget
        self.mainWidget = QtWidgets.QWidget()
        self.mainWin.setCentralWidget(self.mainWidget)

        # set qt object name
        self.mainWin.setObjectName("ART_BuildProgressWin")
        self.mainWin.setWindowTitle("Build Progress")
        window_icon = QtGui.QIcon(os.path.join(self.iconsPath, "System/logo.png"))
        self.mainWin.setWindowIcon(window_icon)

        # font
        headerFont = QtGui.QFont()
        headerFont.setPointSize(8)
        headerFont.setBold(True)

        # set size policy
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # create the mainLayout for the rig creator UI
        self.layout = QtWidgets.QVBoxLayout(self.mainWidget)

        self.mainWin.resize(500, 300)
        self.mainWin.setSizePolicy(mainSizePolicy)
        self.mainWin.setMinimumSize(QtCore.QSize(500, 300))
        self.mainWin.setMaximumSize(QtCore.QSize(500, 300))

        # create the QFrame for this page
        self.background = QtWidgets.QFrame()
        self.layout.addWidget(self.background)
        self.mainLayout = QtWidgets.QVBoxLayout(self.background)

        # build the progress bars:

        self.currentTask = QtWidgets.QProgressBar()
        self.mainLayout.addWidget(self.currentTask)
        self.currentTask.setRange(0, 100)
        self.currentTask.setTextVisible(True)
        self.currentTask.setValue(0)

        self.totalProgress = QtWidgets.QProgressBar()
        self.mainLayout.addWidget(self.totalProgress)
        self.totalProgress.setFormat("Total Progress..")
        self.totalProgress.setRange(0, 12)
        self.totalProgress.setTextVisible(True)
        self.totalProgress.setValue(0)

        # detailed information
        self.infoText = QtWidgets.QTextEdit()
        self.mainLayout.addWidget(self.infoText)
        self.infoText.setMinimumHeight(200)
        self.infoText.setMaximumHeight(200)
        self.infoText.setText("Starting Build Process..")
        self.infoText.setReadOnly(True)

        # show the window
        self.mainWin.show()

        QtWidgets.QApplication.processEvents()
        # start build
        self.setRigPose()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def exportWeights(self):
        """
        Exports all skin weights of meshes that have skinClusters to a .weights file (JSON). It also has
        functionality to deal with morph targets, making sure they are preserved when history on the meshes is deleted.

        .. seealso:: riggingUtils.export_skin_weights()

        """

        self.infoText.append("\n")
        self.infoText.append("|| EXPORTING SKIN WEIGHTS ||")

        # find meshes that are weighted
        weightedMeshes = []
        skinClusters = cmds.ls(type='skinCluster')

        for cluster in skinClusters:
            geometry = cmds.skinCluster(cluster, q=True, g=True)[0]
            geoTransform = cmds.listRelatives(geometry, parent=True)[0]
            weightedMeshes.append([geoTransform, cluster])

        # update progress bar
        numMeshes = len(weightedMeshes)
        self.currentTask.setRange(0, numMeshes)
        self.currentTask.setValue(0)

        # save out weights of meshes
        for mesh in weightedMeshes:
            filePath = utils.returnFriendlyPath(os.path.join(cmds.internalVar(utd=True), mesh[0] + ".WEIGHTS"))

            # export skin weights
            riggingUtils.export_skin_weights(filePath, mesh[0])

            # CHECK FOR MORPH TARGETS
            blendshapeList = []

            # find blendshapes
            skinCluster = riggingUtils.findRelatedSkinCluster(mesh[0])

            if skinCluster is not None:
                blendshapes = cmds.listConnections(skinCluster + ".input", source=True, type="blendShape")
                deleteShapes = []
                if blendshapes is not None:
                    for each in blendshapes:
                        attrs = cmds.listAttr(each, m=True, string="weight")
                        if attrs is not None:
                            for attr in attrs:

                                # if not, manually create shapes by toggling attrs and duplicating mesh
                                if not cmds.objExists(attr):
                                    cmds.setAttr(each + "." + attr, 1)
                                    dupe = cmds.duplicate(mesh[0])[0]

                                    # parent to world
                                    parent = cmds.listRelatives(dupe, parent=True)
                                    if parent is not None:
                                        cmds.parent(dupe, world=True)

                                    # rename the duplicate mesh to the blendshape name
                                    cmds.rename(dupe, attr)
                                    cmds.setAttr(each + "." + attr, 0)
                                    deleteShapes.append(attr)

                            # add the blendshape node name and its attrs to the master blendshape list
                            blendshapeList.append([each, attrs])

            # delete history of meshes
            cmds.delete(mesh[0], ch=True)

            # reapply blendshapes
            for item in blendshapeList:
                bshapeName = item[0]
                shapeList = item[1]

                i = 1
                for shape in shapeList:
                    if cmds.objExists(bshapeName):
                        cmds.blendShape(bshapeName, edit=True, t=(mesh[0], i, shape, 1.0))

                    else:
                        cmds.select([shape, mesh[0]], r=True)
                        cmds.blendShape(name=bshapeName)
                        cmds.select(clear=True)

            try:
                for each in deleteShapes:
                    cmds.delete(each)
            except:
                pass

            # update progress and info
            self.infoText.append("    Exported Skin Weights for " + mesh[0])
            curVal = self.currentTask.value()
            self.currentTask.setValue(curVal + 1)

        # update main progress bar
        self.totalProgress.setValue(1)
        self.infoText.append("\n")
        QtWidgets.QApplication.processEvents()

        # rebuild the skeleton in rig pose
        cmds.refresh()
        # self.rebuildSkeleton()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def setRigPose(self):
        """
        Sets the rig pose on each module's joints. Lastly, calls on ART_BuildProgressUI.exportWeights()

        ..seealso :: ART_BuildProgressUI.exportWeights()

        """

        # set rig pose
        self.infoText.append("Setting Rig Pose..")
        numMods = len(self.mainUI.moduleInstances) - 1

        self.currentTask.setRange(0, numMods)
        self.currentTask.setValue(0)

        for inst in self.mainUI.moduleInstances:
            if inst.name != "root":
                inst.setupForRigPose()
                inst.setReferencePose("rigPose")
                inst.cleanUpRigPose()
                curVal = self.currentTask.value()
                self.currentTask.setValue(curVal + 1)

        # update main progress bar
        self.totalProgress.setValue(2)
        QtWidgets.QApplication.processEvents()

        cmds.refresh()
        # self.exportWeights()
        self.preScript()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def rebuildSkeleton(self):
        """
        Rebuilds the skeleton in rig pose, meaning that all joint rotations will be zeroed in rig pose rather than
        model pose. This ensures clean rigging.

        Lastly, calls on ART_BuildProgressUI.importWeights() to reimport weighting back onto the meshes.

        .. seealso:: riggingUtils.buildSkeleton(), ART_BuildProgressUI.importWeights()

        """

        # rebuild the skeleton
        cmds.delete("root")

        self.infoText.append("Rebuilding Skeleton in Rig Pose..")

        # build skeleton from utils
        riggingUtils.buildSkeleton()

        # update main progress bar
        self.totalProgress.setValue(3)
        QtWidgets.QApplication.processEvents()

        # import weights
        cmds.refresh()
        # self.importWeights()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def importWeights(self):
        """
        Imports skin weights back onto the asset geometry after having rebuilt the skeleton in rig pose. Then calls
        on ART_BuildProgressUI.preScript().

        .. seealso:: ART_BuildProgressUI.preScript()

        """

        meshes = utils.findAllSkinnableGeo()

        self.currentTask.setRange(0, len(meshes))
        self.currentTask.setValue(0)
        self.infoText.append("\n")
        self.infoText.append("|| IMPORTING SKIN WEIGHTS ||")

        for mesh in meshes:
            filePath = utils.returnFriendlyPath(os.path.join(cmds.internalVar(utd=True), mesh + ".WEIGHTS"))

            if os.path.exists(filePath):
                riggingUtils.import_skin_weights(filePath, mesh, True)

                # update progress and info
                self.infoText.append("    Imported Skin Weights for " + mesh)
                curVal = self.currentTask.value()
                self.currentTask.setValue(curVal + 1)

                # remove skin file
                os.remove(filePath)

            else:
                # update progress and info
                self.infoText.setTextColor(QtGui.QColor(236, 217, 0))
                self.infoText.append("    Could not import weights for " + mesh)
                self.infoText.setTextColor(QtGui.QColor(255, 255, 255))
                self.warnings += 1

                curVal = self.currentTask.value()
                self.currentTask.setValue(curVal + 1)

        # update main progress bar
        self.totalProgress.setValue(5)
        QtWidgets.QApplication.processEvents()

        # call on the prescript
        cmds.refresh()
        self.preScript()

        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        #     def exportMeshes(self):
        #
        #         lodAttrs = utils.getLodData()
        #         exportData = utils.findExportMeshData()
        #
        #         self.currentTask.setRange(0, len(lodAttrs))
        #         self.currentTask.setValue(0)
        #
        #
        #         #save the file
        #         saveFile = cmds.file(q = True, sceneName = True)
        #
        #
        #         try:
        #             cmds.file(save = True)
        #         except Exception, e:
        #             cmds.error("Could not save file. Error: " + str(e))
        #             return
        #
        #
        #         #for each LOD
        #         for each in exportData:
        #             meshValue = each[1]
        #             pathValue = each[0]
        #             boneValue = each[2]
        #             poseData = each[3]
        #             utils.exportMesh(self.mainUI, meshValue, pathValue, boneValue, poseData)
        #
        #             #open the file
        #             cmds.file(saveFile, open = True, force = True)
        #
        #             #update UI
        #             self.infoText.setTextColor(QtGui.QColor(0,255,18))
        #             self.infoText.append("    SUCCESS: FBX file exported.")
        #             self.infoText.append("          " + str(pathValue))
        #             self.infoText.setTextColor(QtGui.QColor(255,255,255))
        #
        #             #update progress bar
        #             curVal = self.currentTask.value()
        #             self.currentTask.setValue(curVal + 1)
        #
        #         #update main progress bar
        #         self.totalProgress.setValue(7)
        #
        #         #run pre-script
        #         self.preScript()

        """
        Keeping this around for now, but currently it is not being used.
        Exporting is now done through edit rig -> Export Skeletal Meshes
        """

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def preScript(self):
        """
        If there is a pre-script to run, this will call on ART_BuildProgressUI.executeScript() to run the pre-script.
        Then it will call on ART_BuildProgressUI.buildRigs() to build each module's rigs.

        .. note:: Pre-Scipts are used if you ever want to do something to your character before the rig gets built.
                  An example usage would be adding IK joints for UE4 in a pre-script, as you don't want or need
                  controls for those IK joints, and setting up those constraints.

        .. seealso:: ART_BuildProgressUI.executeScript(), ART_BuildProgressUI.buildRigs()

        """

        self.infoText.append(" \n")

        # get pre-script path from character node, if it exists
        characterNode = utils.returnCharacterModule()
        if cmds.objExists(characterNode + ".preScriptPath"):
            scriptPath = cmds.getAttr(characterNode + ".preScriptPath")
            self.infoText.append("Executing Pre-Script..")
            self.infoText.append("    " + scriptPath)

            # try to execute the pre-script
            status = self.executeScript(scriptPath)
            if status:
                self.infoText.setTextColor(QtGui.QColor(0, 255, 18))
                self.infoText.append("    SUCCESS: Pre-Script Was Successfully Executed..")
                self.infoText.setTextColor(QtGui.QColor(255, 255, 255))

            if not status:
                self.infoText.setTextColor(QtGui.QColor(255, 0, 0))
                self.infoText.append("    FAILED: Pre-Script Was Not Successfully Executed..")
                self.infoText.setTextColor(QtGui.QColor(255, 255, 255))
                self.errors += 1
        else:
            self.infoText.setTextColor(QtGui.QColor(255, 255, 0))
            self.infoText.append("No Pre-Script To Run..")
            self.infoText.setTextColor(QtGui.QColor(255, 255, 255))

        # update main progress bar
        self.totalProgress.setValue(8)
        QtWidgets.QApplication.processEvents()

        # build rigs
        cmds.refresh()
        self.buildRigs()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def buildRigs(self):
        """
        First, create a driver skeleton which the rig will build upon, then calls on each module's buildCustomRig
        function, which will build the rig for that module, then sets up rig parenting and hiearchy once all modules
        are built.

        Lastly, calls on the function to execute a post script if one was given during publish.

        .. seealso:: riggingUtils.createDriverSkeleton(), ART_BuildProgressUI.postScript()

        """

        self.infoText.append(" \n")
        self.infoText.append("||  PREPARING TO BUILD CONTROL RIGS..  ||")

        # Update Current Task bar with num modules
        self.currentTask.setRange(0, len(self.mainUI.moduleInstances))
        self.currentTask.setValue(0)

        # create the driver skeleton
        riggingUtils.createDriverSkeleton()

        # Loop through modules, building rigs
        for inst in self.mainUI.moduleInstances:
            self.infoText.append(" \n")
            self.infoText.append("    Building: " + str(inst.name))

            # build module rigs
            try:
                inst.buildRig(self.infoText, self)
                cmds.refresh()
            except StandardError:
                import sys
                error_type, value, traceback = sys.exc_info()
                tb = utils.get_traceback(traceback)
                print tb
            finally:
                networkNode = inst.returnNetworkNode
                cmds.lockNode(networkNode, lock=True)

            # update progress bar
            curVal = self.currentTask.value()
            self.currentTask.setValue(curVal + 1)

        # =======================================================================
        # #Setup the rig parenting
        # =======================================================================
        time.sleep(2)
        self.infoText.append("Setting up rig parenting...")
        cmds.refresh()

        for data in self.rigData:
            createdConstraints = []

            if data[1] == "driver_root":
                pConst = cmds.pointConstraint("offset_anim", data[0], mo=True)[0]
                oConst = cmds.orientConstraint("offset_anim", data[0], mo=True)[0]
                if pConst not in createdConstraints:
                    createdConstraints.append(pConst)
                if oConst not in createdConstraints:
                    createdConstraints.append(oConst)

            else:
                # get the connections of the passed in parent bone
                connections = []
                for connection in cmds.listConnections(data[1], type="constraint", source=True, destination=False):
                    if connection not in connections:
                        connections.append(connection)
                for connection in connections:
                    driveAttrs = []
                    targetWeights = []

                    # get those constraint target attributes for each constraint connection
                    targets = cmds.getAttr(connection + ".target", mi=True)
                    if len(targets) >= 1:
                        for each in targets:
                            # get the names of the constraint targets
                            targetWeights.append(
                                    cmds.listConnections(connection + ".target[" + str(each) + "].targetWeight",
                                                         p=True)[0])
                            for targetWeight in targetWeights:
                                name = targetWeight.rpartition(".")[2]
                                name = name.rpartition("W")[0]
                                if name not in driveAttrs:
                                    driveAttrs.append(name)

                    # Setup constraint between the driveAttrs and the rigData[0] node
                    for attr in driveAttrs:
                        try:
                            const = cmds.parentConstraint(attr, data[0], mo=True)[0]
                            createdConstraints.append(const)
                        except StandardError, e:
                            print str(e)

                    # get the names of the constraint targets
                    for const in createdConstraints:
                        constraintAttrs = []
                        targets = cmds.getAttr(const + ".target", mi=True)
                        for each in targets:
                            constraintAttrs.append(
                                    cmds.listConnections(const + ".target[" + str(each) + "].targetWeight", p=True)[0])

                        # setup connections between the parent bone constraints and the newly created constraints
                        if len(constraintAttrs) > 0:
                            for i in range(len(constraintAttrs)):
                                try:
                                    cmds.connectAttr(targetWeights[i], constraintAttrs[i])
                                except StandardError:
                                    pass

        # =======================================================================
        # #setup pick-walking for the rig
        # =======================================================================
        time.sleep(2)
        self.infoText.append("Setting up default pick-walking...")

        # take all the top level nodes and setup pickwalking to their parent controls
        for inst in self.mainUI.moduleInstances:
            try:
                inst.setupPickWalking()
            except Exception:
                self.infoText.setTextColor(QtGui.QColor(255, 0, 0))
                self.infoText.append("#Error setting up pick-walking on " + str(inst.name))
                self.infoText.setTextColor(QtGui.QColor(255, 255, 255))
                self.errors += 1

        # =======================================================================
        # #create an uber settings node with proxy attributes
        # =======================================================================
        settings = cmds.group(empty=True, name="rig_settings")
        cmds.parent(settings, "rig_grp")

        keyable = cmds.listAttr(settings, keyable=True)
        for each in keyable:
            cmds.setAttr(settings + "." + each, keyable=False, lock=True, channelBox=False)

        settingNodes = []
        modules = cmds.listConnections("ART_RIG_ROOT.rigModules")
        for module in modules:
            modName = cmds.getAttr(module + ".moduleName")
            mod_settings = modName + "_settings"
            if cmds.objExists(mod_settings):
                settingNodes.append([modName, mod_settings])

        for each in settingNodes:
            name = each[0]
            node = each[1]

            attrs = cmds.listAttr(node, keyable=True)
            if attrs is not None:
                for attr in attrs:
                    attr_type = cmds.getAttr(node + "." + attr, type=True)
                    cmds.addAttr(settings, ln=name + "_" + attr, proxy=node + "." + attr, at=attr_type, keyable=True)

        # =======================================================================
        # #set the state on the main network node
        # =======================================================================
        if cmds.objExists("ART_RIG_ROOT.state"):
            cmds.setAttr("ART_RIG_ROOT.state", 2)

        # =======================================================================
        # #hide all joints
        # =======================================================================
        joints = cmds.ls(type="joint")
        for joint in joints:
            try:
                cmds.setAttr(joint + ".v", lock=False)
                cmds.setAttr(joint + ".v", 0, lock=True)
            except Exception:
                pass

        # =======================================================================
        # #remove unused skin influences to optimize scene
        # =======================================================================
        mel.eval("removeAllUnusedSkinInfs()")

        # =======================================================================
        # #build mirror table
        # =======================================================================
        time.sleep(2)
        self.infoText.append("Building mirror table...")
        utils.MirrorTable()

        # =======================================================================
        # #save the file
        # =======================================================================
        cmds.file(save=True, type="mayaAscii")

        # update main progress bar
        self.totalProgress.setValue(9)
        QtWidgets.QApplication.processEvents()

        # =======================================================================
        # #execute post script
        # =======================================================================
        cmds.refresh()
        self.postScript()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def postScript(self):
        """
        If there is a post-script to run, this will call on ART_BuildProgressUI.executeScript() to run the post-script.
        Then it will call on ART_BuildProgressUI.completeBuild() which wraps up the build process and alerts the user
        the build is done.

        .. note:: Post-Scipts are used if you ever want to do something to your character after the rig gets built.
                  An example usage would be adding custom rigging to joints or controls in the scene, setting up custom
                  relationships or set-driven keys, etc.

        .. seealso:: ART_BuildProgressUI.executeScript(), ART_BuildProgressUI.completeBuild()

        """

        self.infoText.append(" \n")

        # get pre-script path from character node, if it exists
        characterNode = utils.returnCharacterModule()
        if cmds.objExists(characterNode + ".postScriptPath"):
            scriptPath = cmds.getAttr(characterNode + ".postScriptPath")
            self.infoText.append("Executing Post-Script..")
            self.infoText.append("    " + scriptPath)

            # try to execute the pre-script
            status = self.executeScript(scriptPath)
            if status:
                self.infoText.setTextColor(QtGui.QColor(0, 255, 18))
                self.infoText.append("    SUCCESS: Post-Script Was Successfully Executed..")
                self.infoText.setTextColor(QtGui.QColor(255, 255, 255))

            if not status:
                self.infoText.setTextColor(QtGui.QColor(255, 0, 0))
                self.infoText.append("    FAILED: Post-Script Was Not Successfully Executed..")
                self.infoText.setTextColor(QtGui.QColor(255, 255, 255))
                self.errors += 1

        else:
            self.infoText.setTextColor(QtGui.QColor(255, 255, 0))
            self.infoText.append("No Post-Script To Run..")
            self.infoText.setTextColor(QtGui.QColor(255, 255, 255))

        # update main progress bar
        self.totalProgress.setValue(10)
        QtWidgets.QApplication.processEvents()

        # capture model pose for rig controls
        cmds.file(save=True, type="mayaAscii")
        self.completeBuild()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def completeBuild(self):
        """
        Locks down all network nodes, saves the scene, and alerts user that the rig build is complete.

        """

        self.infoText.append(" \n")
        self.infoText.append("Cleaning Up..")

        # save scene
        cmds.file(save=True, type="mayaAscii")

        # iterate total progress
        self.totalProgress.setValue(12)
        QtWidgets.QApplication.processEvents()

        # add build info
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)

        self.infoText.setFont(font)
        self.infoText.setTextColor(QtGui.QColor(0, 255, 18))
        self.infoText.append("\n\nPUBLISH COMPLETE!")

        font.setPointSize(8)
        font.setBold(False)
        self.infoText.setTextColor(QtGui.QColor(255, 255, 255))
        self.infoText.setFont(font)

        # get file name
        fileName = cmds.file(q=True, sceneName=True)
        iconPath = cmds.getAttr("ART_RIG_ROOT.iconPath")

        self.infoText.append("Assets Created:    ")
        self.infoText.append("    " + fileName)
        self.infoText.append("    " + iconPath)
        self.infoText.append(str(self.warnings) + " warnings")
        self.infoText.append(str(self.errors) + " errors")

        # tell user build is complete
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setText("Rig Build Complete!")
        msgBox.addButton("New Scene", QtWidgets.QMessageBox.YesRole)
        msgBox.addButton("Edit Rig", QtWidgets.QMessageBox.NoRole)
        ret = msgBox.exec_()

        if ret == 1:
            import Tools.Rigging.ART_RigCreatorUI as ART_RigCreatorUI
            ART_RigCreatorUI.createUI()
            cmds.refresh(force=True)
            cmds.dockControl("pyArtRigCreatorDock", e=True, r=True)

            if cmds.window("ART_PublishWin", exists=True):
                cmds.deleteUI("ART_PublishWin", wnd=True)

        else:

            # if the rigCreatorUI exists delete UI
            if cmds.dockControl("pyArtRigCreatorDock", q=True, exists=True):
                cmds.deleteUI("pyArtRigCreatorUi")
                cmds.deleteUI("pyArtRigCreatorDock", control=True)

            if cmds.window("ART_PublishWin", exists=True):
                cmds.deleteUI("ART_PublishWin", wnd=True)

            cmds.file(new=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def executeScript(self, scriptPath):
        """
        Takes a given script (mel or python) and runs it.

        :param scriptPath: location of the script to be evaluated and ran.

        :return: Whether or not the execution of the script failed or not.

        .. seealso:: ART_BuildProgressUI.preScript(), ART_BuildProgressUI.postScript()

        """

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
