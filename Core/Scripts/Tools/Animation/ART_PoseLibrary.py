"""
This file contains classes for handling saving and loading of poses.
"""
import os
import sys
import json
import datetime
import math
from functools import partial
import webbrowser

import maya.cmds as cmds
import maya.OpenMaya as openMaya
import maya.api.OpenMaya as api
import maya.OpenMayaUI as mui

# noinspection PyUnresolvedReferences
from ThirdParty.Qt import QtGui, QtCore, QtWidgets
import Utilities.utils as utils
import Utilities.interfaceUtils as interfaceUtils

# To deal with the change between Maya 2016 and Maya 2017's PyQt version, try importing different versions of shiboken.
try:
    import shiboken as shiboken
except ImportError:
    import shiboken2 as shiboken


# Globals
windowName = "pyARTv2_PoseLibraryWin"
windowTitle = "Pose Library"

windowName_cp = "pyARTv2_CreatePoseWin"
windowTitle_cp = "Create New Pose"

# get the directory path of the tools
settings = QtCore.QSettings("Epic Games", "ARTv2")
toolsPath = settings.value("toolsPath")
iconsPath = settings.value("iconPath")
scriptPath = settings.value("scriptPath")
projectPath = settings.value("projectPath")

# load the stylesheets
STYLE = interfaceUtils.get_style_sheet("artv2_style")
MENU_STYLE = interfaceUtils.get_style_sheet("menu")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class ART_CreatePose(object):
    """
    Class for creating a pose asset.
    """

    def __init__(self, pose_name, pose_location, controls, viewport=None, image=None, partial_pose=False):

        super(ART_CreatePose, self).__init__()

        # build the full path for the pose file
        full_path = utils.returnNicePath(pose_location, pose_name)

        # store variables
        self.pose_path = full_path
        self.controls = controls
        self.status = False
        self.image = image

        # determine if this is an overwrite
        self.overwrite = False
        file_writable = True

        if os.path.exists(self.pose_path + ".v2pose"):
            self.overwrite = True

            file_writable = os.access(self.pose_path + ".v2pose", os.W_OK)

        if file_writable is False:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("File is not writable. Aborting operation.")
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            msgBox.exec_()
            return

        # create image if one wasn't passed in
        if image is None:
            # use API to grab image from view
            newView = mui.M3dView()
            mui.M3dView.getM3dViewFromModelEditor(viewport, newView)

            # read the color buffer from the view, and save the MImage to disk
            self.thumbnail = openMaya.MImage()
            newView.readColorBuffer(self.thumbnail, True)
            self.thumbnail.writeToFile(full_path + ".png", 'png')

        # pose data stored in dict
        self.pose = {}

        # get user
        user = ""
        for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
            user = os.environ.get(name)
        self.pose["creator"] = user

        # get date
        now = datetime.datetime.now()
        self.pose["date"] = str(now.month) + "/" + str(now.day) + "/" + str(now.year)

        # store whether this was a partial pose
        self.pose["partial"] = partial_pose

        # write pose
        self._write_pose()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _write_pose(self):

        # get data and write pose
        pose_written = self._get_pose_data()

        if pose_written is True:
            self.status = True

        # if status was false, report and delete image if it was created.
        if pose_written is not True:
            self.status = False

            if self.image is None:
                if self.overwrite is False:
                    os.remove(self.pose_path + ".png")

            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Errors occurred and pose was not saved.")
            msgBox.setDetailedText(str(pose_written))
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            msgBox.exec_()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _get_pose_data(self):

        pose = {}

        for control in self.controls:
            # get world matrix
            worldMatrix = cmds.getAttr(control + ".worldMatrix")

            # get keyable attributes in channel box
            attrs = cmds.listAttr(control, keyable=True)

            # add space
            if cmds.objExists(control + ".space"):
                attrs.append("space")

            # for each attr, get value
            attr_data = {}
            if attrs is not None:
                for attr in attrs:
                    attr_value = cmds.getAttr(control + "." + attr)
                    attr_data[attr] = attr_value

            # add to pose dict
            nice_name = control.partition(":")[2]
            pose[nice_name] = [attr_data, worldMatrix]

        self.pose["controls"] = pose
        pose_written = self._write_pose_data()
        return pose_written

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _write_pose_data(self):

        try:
            f = open(self.pose_path + ".v2pose", 'w')

            # dump the data with json
            json.dump(self.pose, f, sort_keys=True, indent=4)
            f.close()
        except Exception, e:
            return e

        return True


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class ART_LoadPose(object):
    """
    Class for loading poses. Requires the pose file to load, the load operation( All Controls, Selected Controls,
    Mirror, Mirror Selected, the space (Local Space or World Space), the namespace of the rig to operate on, and,
    optionally, a mirror axis.
    """

    def __init__(self, pose_location, operation, space, character, axis="X", offset=None):

        super(ART_LoadPose, self).__init__()

        self.character = character
        self.operation = operation
        self.space = space

        operations = {
            "All Controls": {"Local Space": self.load_pose_local, "World Space": self.load_pose_world},
            "Selected Controls": {"Local Space": partial(self.load_pose_local, selection=cmds.ls(sl=True)),
                                  "World Space": partial(self.load_pose_world, selection=cmds.ls(sl=True))},
            "Mirror": {"Local Space": partial(self.load_pose_mirror, local=True, mirror_axis=axis),
                       "World Space": partial(self.load_pose_mirror, local=False, mirror_axis=axis)},
            "Mirror Selected": {"Local Space": partial(self.load_pose_mirror, local=True, mirror_axis=axis,
                                                       selection=cmds.ls(sl=True)),
                                "World Space": partial(self.load_pose_mirror, local=False, mirror_axis=axis,
                                                       selection=cmds.ls(sl=True))},
            "Offset": {"Local Space": partial(self.load_pose_offset, offset_control=offset)}
                      }

        if self.operation in operations.keys():
            if self.space in operations.get(self.operation):
                spaces = operations.get(self.operation)
                func = spaces.get(self.space)
                func(pose=pose_location)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def load_pose_local(self, pose, selection=None):
        """
        Load the pose using the attribute values stored in the pose.
        :param pose: the pose file on disk
        :param selection: whether or not to load the pose on selected controls. If None, then it will load on all.
        """

        controls = self._return_pose_data(pose)[0]
        if selection is None:
            # iterate through controls and apply data
            for control in controls:
                control_data = controls.get(control)
                attribute_data = control_data[0]
                self._apply_local_pose(control, attribute_data)
        else:
            failed = []
            for each in selection:
                nice_name = each.partition(":")[2]
                control_data = controls.get(nice_name)
                if control_data is not None:
                    attribute_data = control_data[0]
                    self._apply_local_pose(nice_name, attribute_data)
                else:
                    failed.append(nice_name)
            if len(failed) > 0:
                for each in failed:
                    cmds.warning(each + " has no data in pose.")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def load_pose_world(self, pose, selection=None):
        """
        Load the pose by calculating new attributes to set on the controls by using the stored worldMatrix for the
        controls, ensuring the controls load exactly as the pose was saved, regardless of spaces.
        :param pose: the pose file on disk
        :param selection: whether or not to load the pose on selected controls. If None, then it will load on all.
        """

        # first, call on load pose local, so attributes get set
        self.load_pose_local(pose, selection)

        # open the pose file
        controls = self._return_pose_data(pose)[0]

        progress_bar = interfaceUtils.ProgressBar("Loading Pose", interfaceUtils.getMainWindow())
        progress_bar.setRange(0, 15)
        progress_bar.show()
        QtWidgets.QApplication.processEvents()

        if selection is None:
            for i in range(15):
                for control in controls:
                    control_data = controls.get(control)
                    matrix = control_data[1]
                    self._apply_world_pose(control, matrix)
                progress_bar.setValue(progress_bar.getValue() + 1)

        else:
            for i in range(15):
                for each in selection:
                    nice_name = each.rpartition(":")[2]
                    control_data = controls.get(nice_name)
                    if control_data is not None:
                        matrix = control_data[1]
                        self._apply_world_pose(nice_name, matrix)
                progress_bar.setValue(progress_bar.getValue() + 1)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def load_pose_mirror(self, pose, selection=None, local=False, mirror_axis="X"):
        """
        Loads the mirror of the pose.
        :param pose: the pose file on disk
        :param selection: whether or not to load the pose on selected controls. If None, then it will load on all.
        :param local: whether to load in local space or world space.
        :param mirror_axis: the axis to mirror on.
        """

        progress_bar = interfaceUtils.ProgressBar("Loading Mirrored Pose", interfaceUtils.getMainWindow())
        progress_bar.setRange(0, 8)
        progress_bar.show()
        QtWidgets.QApplication.processEvents()

        temp_pose = None

        # capture current pose
        if selection is not None:
            temp_dir = utils.returnFriendlyPath(cmds.internalVar(userTmpDir=True))
            ART_CreatePose("temp", temp_dir, selection, viewport=None, image="test")
            temp_pose = utils.returnNicePath(temp_dir, "temp.v2pose")
        progress_bar.setValue(progress_bar.getValue() + 1)

        # load the pose from the library and apply it
        self.load_pose_local(pose, selection)
        progress_bar.setValue(progress_bar.getValue() + 1)

        # open the pose file and get the data
        pose_data = self._return_pose_data(pose)
        controls = pose_data[0]
        partial_pose = pose_data[1]

        if partial_pose:
            selection = []
            for control in controls:
                selection.append(self.character + ":" + control)

        mirror_data = self._generate_mirror_data(local, mirror_axis, controls, selection)
        return_data = self._iterate_mirror_controls(mirror_data.keys(), mirror_data, controls, selection)
        completed = return_data[0]
        failed = return_data[1]
        progress_bar.setValue(progress_bar.getValue() + 1)

        # one final check
        # if selection is None:
        for i in range(5):
            for ctrl in completed:
                invert_data = self._get_invert_axis(ctrl)
                try:
                    self._set_mirror_transforms(ctrl, mirror_data.get(ctrl), invert_data[0], invert_data[1],
                                                invert_data[2])
                except ValueError:
                    pass
            progress_bar.setValue(progress_bar.getValue() + 1)

        cmds.delete("pose_mirror_grp")

        if selection is not None:
            cmds.select(clear=True)
            for each in failed:
                cmds.select(each, add=True)
            if temp_pose is not None:
                ART_LoadPose(temp_pose, "Selected Controls", "Local Space", self.character, "X")
            try:
                os.remove(temp_pose)
            except IOError:
                pass
            except WindowsError:
                pass
            except OSError:
                pass
            except TypeError:
                pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def load_pose_offset(self, pose, offset_control):
        """
        Takes the given offset_control as a position to load the pose from. For example, if the character is now moved
        away from the world origin, and you want to load a pose on the character in that new position, you could
        select the body control (can be any control) and load pose with offset, which will load the pose in the position
        and orientation of the selected/given control.

        :param pose: the pose file on disk.
        :param offset_control: the control to load the pose in the position and orientation of.
        """

        # store offset control matrix
        offset_matrix = cmds.getAttr(offset_control + ".worldMatrix")

        # open the pose file and get the data
        data = self._return_pose_data(pose)
        controls = data[0]
        partial_pose = data[1]

        if partial_pose is True:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("This is a partial pose. While loading offset poses is technically supported,"
                           " it will likely not give the results expected. Continue?")
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.addButton("Yes", QtWidgets.QMessageBox.YesRole)
            msgBox.addButton("No", QtWidgets.QMessageBox.NoRole)
            ret = msgBox.exec_()
            if ret == 1:
                return

        progress_bar = interfaceUtils.ProgressBar("Loading Offset Pose", interfaceUtils.getMainWindow())
        progress_bar.setRange(0, 13)
        progress_bar.show()
        QtWidgets.QApplication.processEvents()

        # load pose
        self.load_pose_local(pose)

        # create group at offset control's transforms
        offset_group = cmds.group(empty=True, name="offset_pose_group")
        current_offset_matrix = cmds.getAttr(offset_control + ".worldMatrix")
        cmds.xform(offset_group, ws=True, m=current_offset_matrix)

        # create locators for controls
        locators = self._create_offset_locators(controls, offset_group)
        progress_bar.setValue(progress_bar.getValue() + 1)

        # move offset group to stored offset control position
        new_pose_data = self._move_offset_locators(locators, offset_matrix, offset_group)

        # calculate the new values for each control based on the new world matrix
        completed, failed = self._iterate_world_pose(controls, new_pose_data)
        progress_bar.setValue(progress_bar.getValue() + 1)

        # one final check
        for i in range(10):
            for ctrl in completed:
                if ctrl in new_pose_data.keys():
                    if api.MMatrix(cmds.getAttr(ctrl + ".worldMatrix")) != api.MMatrix(new_pose_data.get(ctrl)):
                        matrix = api.MMatrix(new_pose_data.get(ctrl))
                        self._calculate_and_set_local_values(ctrl, matrix)
            progress_bar.setValue(progress_bar.getValue() + 1)

        # delete offset group
        cmds.delete(offset_group)
        for locator in locators:
            if cmds.objExists(locator):
                cmds.delete(locator)

        # report
        if len(failed) > 0:
            for each in failed:
                cmds.warning("Failed to set data for: " + each)

        progress_bar.setValue(progress_bar.getValue() + 1)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _apply_local_pose(self, control, attrData):

        for attribute in attrData:
            value = attrData.get(attribute)
            if cmds.objExists(self.character + ":" + control + "." + attribute):
                try:
                    cmds.setAttr(self.character + ":" + control + "." + attribute, value)
                    cmds.setKeyframe(self.character + ":" + control + "." + attribute)
                except RuntimeError:
                    pass

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _apply_world_pose(self, control, matrix):

        # apply world matrix data
        if cmds.objExists(self.character + ":" + control):
            if not api.MMatrix(cmds.getAttr(self.character + ":" + control + ".worldMatrix")) == api.MMatrix(matrix):

                # get parent inverse matrix of control
                parentMatrix = api.MMatrix(
                    cmds.getAttr(self.character + ":" + control + ".parentInverseMatrix"))
                controlMatrix = api.MMatrix(matrix)
                newMatrix = controlMatrix * parentMatrix

                # get transformation matrix and translate/rotate values
                transform_matrix = api.MTransformationMatrix(newMatrix)
                translates = transform_matrix.translation(api.MSpace.kWorld)
                rotates = transform_matrix.rotation()
                angles = [math.degrees(angle) for angle in (rotates.x, rotates.y, rotates.z)]

                # set values
                count = 0
                for attr in ["translateX", "translateY", "translateZ"]:
                    keyable_attrs = cmds.listAttr(self.character + ":" + control, k=True, locked=False)
                    if attr in keyable_attrs:
                        try:
                            cmds.setAttr(self.character + ":" + control + "." + attr, translates[count])
                            cmds.setKeyframe(self.character + ":" + control + "." + attr)
                        except RuntimeError:
                            cmds.warning("could not apply data on " + self.character + ":" + control)
                    count += 1

                count = 0
                for attr in ["rotateX", "rotateY", "rotateZ"]:
                    keyable_attrs = cmds.listAttr(self.character + ":" + control, k=True, locked=False)
                    if attr in keyable_attrs:
                        try:
                            cmds.setAttr(self.character + ":" + control + "." + attr, angles[count])
                            cmds.setKeyframe(self.character + ":" + control + "." + attr)
                        except RuntimeError:
                            cmds.warning("could not apply data on " + self.character + ":" + control)
                    count += 1

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _calculate_and_set_local_values(self, control, matrix):

        inverse_matrix = api.MMatrix(cmds.getAttr(control + ".parentInverseMatrix"))
        local_matrix = matrix * inverse_matrix
        xform_matrix = api.MTransformationMatrix(local_matrix)

        translates = xform_matrix.translation(api.MSpace.kWorld)
        rotation = xform_matrix.rotation()
        rotates = [math.degrees(angle) for angle in (rotation.x, rotation.y, rotation.z)]

        for attr in [["translateX", translates[0]], ["translateY", translates[1]],
                     ["translateZ", translates[2]], ["rotateX", rotates[0]], ["rotateY", rotates[1]],
                     ["rotateZ", rotates[2]]]:

            try:
                cmds.setAttr(control + "." + attr[0], attr[1])
                cmds.setKeyframe(control + "." + attr[0])
            except Exception, e:
                print e

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _construct_mirror_matrix(self, control, matrix, invertX, invertY, invertZ):

        matrix = api.MMatrix(matrix)

        if invertX:
            matrix.setElement(0, 0, -matrix[0])
            matrix.setElement(0, 1, -matrix[1])
            matrix.setElement(0, 2, -matrix[2])
        if invertY:
            matrix.setElement(1, 0, -matrix[4])
            matrix.setElement(1, 1, -matrix[5])
            matrix.setElement(1, 2, -matrix[6])
        if invertZ:
            matrix.setElement(2, 0, -matrix[8])
            matrix.setElement(2, 1, -matrix[9])
            matrix.setElement(2, 2, -matrix[10])

        parent_matrix = api.MMatrix(cmds.getAttr(control + ".parentInverseMatrix"))
        local_matrix = matrix * parent_matrix
        xform_matrix = api.MTransformationMatrix(local_matrix)

        translates = xform_matrix.translation(api.MSpace.kWorld)
        rotation = xform_matrix.rotation()
        rotates = [math.degrees(angle) for angle in (rotation.x, rotation.y, rotation.z)]

        return [translates, rotates]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _create_offset_locators(self, pose_data, offset_group):

        locators = []
        for control in pose_data.keys():
            control_data = pose_data.get(control)
            matrix = control_data[1]

            locator = cmds.spaceLocator(name=control + "_pose_locator")[0]
            cmds.setAttr(locator + ".visibility", 0)
            cmds.xform(locator, ws=True, m=matrix)

            if cmds.objExists(self.character + ":" + control + ".sourceModule"):
                if cmds.getAttr(self.character + ":" + control + ".sourceModule") != "root":
                    cmds.parent(locator, offset_group)
                else:
                    if control.find("root_anim") != -1:
                        cmds.parent(locator, offset_group)
            locators.append(locator)

        return locators

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _generate_mirror_data(self, local, mirror_axis, pose_controls, selection):

        mirror_data = {}
        locators, controls = [], []

        mirror_group = self._create_mirror_group(local, selection)

        for each in pose_controls:
            if selection is not None:
                if self.character + ":" + each in selection:
                    controls.append(each)
            else:
                if cmds.objExists(self.character + ":" + each):
                    controls.append(each)

        # Now, go through the controls, creating a locator with the control's matrix data
        for control in controls:
            control_data = pose_controls.get(control)
            matrix = control_data[1]
            locator = cmds.spaceLocator(name=control + "_pose_locator")[0]
            cmds.xform(locator, ws=True, m=matrix)
            cmds.parent(locator, mirror_group)
            locators.append(locator)

        # mirror the mirror_group
        cmds.setAttr(mirror_group + ".scale" + mirror_axis, -1)

        # Add entries to the new mirror_data dictionary with the locator's matrix data and the attribute data
        for control in controls:
            control_data = pose_controls.get(control)
            attribute_data = control_data[0]
            mirror_control = self.character + ":" + control

            if cmds.objExists(self.character + ":" + control + ".mirror"):
                connections = cmds.listConnections(self.character + ":" + control + ".mirror")
                if connections is not None:
                    mirror_control = connections[0]

            # set the raw attribute data on the mirror control
            for attribute in attribute_data:
                value = attribute_data.get(attribute)
                if cmds.objExists(mirror_control + "." + attribute):
                    try:
                        cmds.setAttr(mirror_control + "." + attribute, value)
                    except RuntimeError:
                        pass

            # store the locator matrix with the mirror control
            locator = control + "_pose_locator"
            new_matrix = cmds.getAttr(locator + ".worldMatrix")
            mirror_data[mirror_control] = new_matrix

        return mirror_data

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _create_mirror_group(self, local, selection):

        mirror_group = cmds.group(empty=True, name="pose_mirror_grp")
        if local is True:
            if selection is None:
                cmds.delete(cmds.parentConstraint(self.character + ":mirror_origin", mirror_group)[0])
            if selection is not None:
                # find highest common parent that is a core control (doesn't have mirrors)
                parent = self._get_common_parent(selection)

                bone_matrix = api.MMatrix(cmds.getAttr(self.character + ":" + parent + ".worldMatrix"))
                origin_matrix = api.MMatrix(cmds.getAttr(self.character + ":mirror_origin.parentInverseMatrix"))
                local_matrix = bone_matrix * origin_matrix
                xform_matrix = api.MTransformationMatrix(local_matrix)

                translates = xform_matrix.translation(api.MSpace.kWorld)
                rotation = xform_matrix.rotation()
                rotates = [math.degrees(angle) for angle in (rotation.x, rotation.y, rotation.z)]

                cmds.setAttr(mirror_group + ".translateX", translates[0])
                cmds.setAttr(mirror_group + ".translateY", translates[1])
                cmds.setAttr(mirror_group + ".translateZ", translates[2])
                cmds.setAttr(mirror_group + ".rotateZ", rotates[2])

        return mirror_group

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _get_common_parent(self, controls):

        parents = []

        for each in controls:
            control_node = cmds.listConnections(each + ".controlClass")
            rig_module_node = cmds.listConnections(control_node[0] + ".parentModule")
            parent_module_bone = cmds.getAttr(rig_module_node[0] + ".parentModuleBone")
            if parent_module_bone not in parents:
                parents.append(parent_module_bone)

        num_parents = []
        for parent_bone in parents:
            full_path = cmds.listRelatives(self.character + ":" + parent_bone, f=True)[0]
            relatives = full_path.split("|")
            num_parents.append([parent_bone, len(relatives)])

        return min(num_parents)[0]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _get_invert_axis(self, control):

        invertX = False
        invertY = False
        invertZ = False

        if cmds.objExists(control + ".invertX"):
            invertX = cmds.getAttr(control + ".invertX")
            invertY = cmds.getAttr(control + ".invertY")
            invertZ = cmds.getAttr(control + ".invertZ")

        return [invertX, invertY, invertZ]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _iterate_mirror_controls(self, controls, mirror_data, data_controls, selection):

        completed, skipped, failed = [], [], []

        if selection is None:
            for each in controls:
                base_name = each.rpartition(":")[2]
                if base_name in data_controls.keys():
                    skipped.append(each)

        elif selection is not None:
            for each in selection:
                base_name = each.rpartition(":")[2]
                if base_name in data_controls.keys():
                    skipped.append(each)

        uniques = []
        while len(skipped) > 0:
        # for i in range(10):
            for ctrl in skipped:
                # check to see if the control is in a mirror module, but does not have a mirror control
                if cmds.objExists(ctrl + ".unique"):
                    index = skipped.index(ctrl)
                    skipped.pop(index)
                    completed.append(ctrl)
                    uniques.append(ctrl)
                    continue

                invert_data = self._get_invert_axis(ctrl)
                control_parents = utils.find_parent_controls(ctrl)

                if control_parents is None:
                    completed.append(ctrl)
                    index = skipped.index(ctrl)
                    skipped.pop(index)
                    continue

                if len(control_parents) == 0:
                    completed.append(ctrl)

                if selection is not None:
                    for parent in control_parents:
                        if parent not in selection:
                            completed.append(parent)

                # check to see if all of the control's parents are in the completed list
                result = all(elem in completed for elem in control_parents)
                if result is True:
                    try:
                        self._set_mirror_transforms(ctrl, mirror_data.get(ctrl), invert_data[0], invert_data[1],
                                                    invert_data[2])
                    except ValueError:
                        failed.append(ctrl)
                    finally:
                        completed.append(ctrl)
                        index = skipped.index(ctrl)
                        skipped.pop(index)

        # if the control was in a mirror module, but did not have a mirror control, do not try to do mirror operations
        # on that control!
        for each in uniques:
            if each in completed:
                index = completed.index(each)
                completed.pop(index)

        return [completed, failed]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _iterate_world_pose(self, original_pose_data, new_pose_data):

        skipped = []
        completed = []
        failed = []

        for each in new_pose_data.keys():
            base_name = each.rpartition(":")[2]
            if base_name in original_pose_data.keys():
                skipped.append(each)

        while len(skipped) > 0:
            for ctrl in skipped:
                control_parents = utils.find_parent_controls(ctrl)
                if len(control_parents) == 0:
                    completed.append(ctrl)
                for parent in control_parents:
                    if parent not in new_pose_data.keys():
                        completed.append(parent)
                result = all(elem in completed for elem in control_parents)
                if result is True:
                    try:
                        matrix = api.MMatrix(new_pose_data.get(ctrl))
                        self._calculate_and_set_local_values(ctrl, matrix)
                    except ValueError:
                        failed.append(ctrl)
                    finally:
                        completed.append(ctrl)
                        index = skipped.index(ctrl)
                        skipped.pop(index)

        return [completed, failed]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _move_offset_locators(self, locators, offset_matrix, offset_group):

        cmds.xform(offset_group, ws=True, m=offset_matrix)
        cmds.refresh(force=True)

        # store the locator matrix with the control
        new_pose_data = {}
        for locator in locators:
            matrix = api.MMatrix(cmds.getAttr(locator + ".worldMatrix"))
            control = self.character + ":" + locator.partition("_pose_locator")[0]
            new_pose_data[control] = matrix

        return new_pose_data

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _return_pose_data(self, pose_file):

        f = open(pose_file, 'r')
        data = json.load(f)
        f.close()
        pose_data = data.get("controls")
        partial_pose = data.get("partial")
        return [pose_data, partial_pose]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _set_mirror_transforms(self, control, matrix, invertX, invertY, invertZ):

        transform_data = self._construct_mirror_matrix(control, matrix, invertX, invertY, invertZ)

        for attr in [["translateX", transform_data[0][0]], ["translateY", transform_data[0][1]],
                     ["translateZ", transform_data[0][2]], ["rotateX", transform_data[1][0]],
                     ["rotateY", transform_data[1][1]], ["rotateZ", transform_data[1][2]]]:
            try:
                if cmds.getAttr(control + "." + attr[0]) != attr[1]:
                    cmds.setAttr(control + "." + attr[0], attr[1])
            except RuntimeError:
                pass


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class ART_CreatePoseUI(QtWidgets.QMainWindow):
    """
    Interface for creating and saving a pose.
    """
    def __init__(self, inst, parent=None):

        super(ART_CreatePoseUI, self).__init__(parent)

        self.currentSelection = cmds.ls(sl=True)

        # build the UI
        self.parent_inst = inst
        self._build_interface()

        # re-select
        cmds.select(self.currentSelection)

        # auto-select same directory selected in pose library
        selected = self.parent_inst.directory_tree.selectedItems()

        if len(selected) > 0:
            path = selected[0].data(0, QtCore.Qt.UserRole)[1]
            iterator = QtWidgets.QTreeWidgetItemIterator(self.directory_tree)
            items = []

            while iterator.value():
                items.append(iterator.value())
                iterator += 1

            for item in items:
                self.directory_tree.collapseItem(item)
                self.directory_tree.setItemSelected(item, False)
                if item.data(0, QtCore.Qt.UserRole)[1] == path:
                    self.directory_tree.setItemSelected(item, True)
                    self.directory_tree.scrollToItem(item)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _build_interface(self):

        if cmds.window(windowName_cp, exists=True):
            cmds.deleteUI(windowName_cp, wnd=True)

        self.window_icon = QtGui.QIcon(os.path.join(iconsPath, "System/logo.png"))
        self.setWindowIcon(self.window_icon)
        self.setStyleSheet(STYLE)

        # set the window size
        self.setMinimumSize(QtCore.QSize(440, 410))
        self.setMaximumSize(QtCore.QSize(440, 410))

        # size policies
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setSizePolicy(mainSizePolicy)

        # set qt object name
        self.setObjectName(windowName_cp)
        self.setWindowTitle(windowTitle_cp)

        # create the main widget
        self.mainWidget = QtWidgets.QFrame()
        self.mainWidget.setObjectName("dark")
        self.setCentralWidget(self.mainWidget)

        # create the mainLayout
        self.mainLayout = QtWidgets.QHBoxLayout(self.mainWidget)

        # column 1: vbox with tree widget and push button
        column_1_layout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(column_1_layout)

        self.directory_tree = QtWidgets.QTreeWidget()
        self.directory_tree.setMinimumHeight(360)
        self.directory_tree.setMaximumHeight(360)
        self.header_text = os.path.basename(projectPath)
        header = QtWidgets.QTreeWidgetItem([self.header_text + ":"])
        self.directory_tree.setHeaderItem(header)
        self.directory_tree.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        tree_header = self.directory_tree.header()
        tree_header.setMinimumSectionSize(300)
        column_1_layout.addWidget(self.directory_tree)
        populate_tree(self.directory_tree)

        add_new_folder_button = QtWidgets.QPushButton("Add New Folder")
        add_new_folder_button.setMinimumHeight(25)
        add_new_folder_button.setMaximumHeight(25)
        add_new_folder_button.setObjectName("settings")
        column_1_layout.addWidget(add_new_folder_button)
        add_new_folder_button.clicked.connect(self._add_new_project_directory)

        spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        column_1_layout.addItem(spacer)

        # column 2: vbox with lineEdit for path, viewport, pose name label, line edit for pose name, label for # of
        # controls, spacer, and a button for creating the pose

        column_2_layout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(column_2_layout)

        self.pose_path = QtWidgets.QLineEdit(os.path.basename(projectPath) + "/")
        self.pose_path.setEnabled(False)
        column_2_layout.addWidget(self.pose_path)
        self.viewport_widget = ViewportWidget(200, 200, self)

        column_2_layout.addWidget(self.viewport_widget)

        self.pose_name = QtWidgets.QLineEdit()
        self.pose_name.setObjectName("light")
        self.pose_name.setPlaceholderText("Enter pose name..")
        column_2_layout.addWidget(self.pose_name)

        create_pose_select_btn = QtWidgets.QPushButton("Create Pose for Selected Controls")
        create_pose_select_btn.setMinimumHeight(48)
        create_pose_select_btn.setMaximumHeight(48)
        create_pose_select_btn.setObjectName("settings")
        column_2_layout.addWidget(create_pose_select_btn)
        create_pose_select_btn.clicked.connect(partial(self._create_pose, True))

        create_pose_btn = QtWidgets.QPushButton("Create Pose")
        create_pose_btn.setMinimumHeight(48)
        create_pose_btn.setMaximumHeight(48)
        create_pose_btn.setObjectName("settings")
        column_2_layout.addWidget(create_pose_btn)
        create_pose_btn.clicked.connect(self._create_pose)

        # update pose path if item in tree widget is selected
        self.directory_tree.itemSelectionChanged.connect(partial(update_path, self.directory_tree,
                                                                 self.pose_path,
                                                                 self.pose_name))

        # restore window position
        winSettings = QtCore.QSettings("ARTv2", "CreatePose")
        self.restoreGeometry(winSettings.value("geometry"))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # noinspection PyMissingOrEmptyDocstring
    def closeEvent(self, event):

        # store window positions
        winSettings = QtCore.QSettings("ARTv2", "CreatePose")
        winSettings.setValue("geometry", self.saveGeometry())

        try:
            self.viewport_widget.setParent(None)
            self.viewport_widget.close()
        except Exception, e:
            print e

        QtWidgets.QMainWindow.closeEvent(self, event)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _add_new_project_directory(self):

        selected = self.directory_tree.selectedItems()
        if len(selected) == 0:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Must select a project or an existing project directory to add a new directory to.")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.setDefaultButton(QtWidgets.QMessageBox.Ok)
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.exec_()
            return

        # simple UI for user to add new Group
        if cmds.window("ART_CreatePose_AddNewGrpUI", exists=True):
            cmds.deleteUI("ART_CreatePose_AddNewGrpUI", wnd=True)

        # launch a UI to get the name information
        self.addNewGrpWin = QtWidgets.QMainWindow(self)

        # size policies
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # create the main widget
        self.addNewGrpWin_mainWidget = QtWidgets.QWidget()
        self.addNewGrpWin.setCentralWidget(self.addNewGrpWin_mainWidget)

        # set qt object name
        self.addNewGrpWin.setObjectName("ART_CreatePose_AddNewGrpUI")
        self.addNewGrpWin.setWindowTitle("Add New Directory")

        # create the mainLayout for the rig creator UI
        self.addNewGrpWin_mainLayout = QtWidgets.QVBoxLayout(self.addNewGrpWin_mainWidget)
        self.addNewGrpWin_mainLayout.setContentsMargins(0, 0, 0, 0)

        self.addNewGrpWin.resize(310, 153)
        self.addNewGrpWin.setSizePolicy(mainSizePolicy)
        self.addNewGrpWin.setMinimumSize(QtCore.QSize(310, 153))
        self.addNewGrpWin.setMaximumSize(QtCore.QSize(310, 153))

        # add background image/QFrame for first page
        self.addNewGrpWin_frame = QtWidgets.QFrame()
        self.addNewGrpWin_mainLayout.addWidget(self.addNewGrpWin_frame)
        self.addNewGrpWin_frame.setMinimumSize(QtCore.QSize(310, 153))
        self.addNewGrpWin_frame.setMaximumSize(QtCore.QSize(310, 153))

        # create vertical layout
        self.addNewGrpWin_vLayout = QtWidgets.QVBoxLayout(self.addNewGrpWin_frame)

        label = QtWidgets.QLabel("Adding directory to:")
        self.addNewGrpWin_vLayout.addWidget(label)

        # project path widget
        self.addNewGrpWin_parentDir = QtWidgets.QLineEdit()
        self.addNewGrpWin_parentDir.setEnabled(False)
        self.addNewGrpWin_vLayout.addWidget(self.addNewGrpWin_parentDir)

        # set project path to selected directory structure (if possible)
        selected = self.directory_tree.selectedItems()
        if len(selected) > 0:
            item_data = selected[0].data(0, QtCore.Qt.UserRole)

            if item_data[0] == "folder":
                full_path = item_data[1]
                partial_path = full_path.split(self.header_text)[1]
                partial_path = utils.returnFriendlyPath(partial_path)
                self.addNewGrpWin_parentDir.setText(self.header_text + partial_path)

        # directory name layout/widgets
        dir_layout = QtWidgets.QHBoxLayout()
        self.addNewGrpWin_vLayout.addLayout(dir_layout)

        label2 = QtWidgets.QLabel("Directory Name:")
        dir_layout.addWidget(label2)

        self.addNewGrpWinLineEdit = QtWidgets.QLineEdit()
        self.addNewGrpWinLineEdit.setPlaceholderText("Enter a directory name")
        self.addNewGrpWinLineEdit.setMinimumWidth(185)
        self.addNewGrpWinLineEdit.setMaximumWidth(185)
        dir_layout.addWidget(self.addNewGrpWinLineEdit)

        # add group button
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)

        self.addNewGrpWin_AddButton = QtWidgets.QPushButton("Create New Directory")
        self.addNewGrpWin_vLayout.addWidget(self.addNewGrpWin_AddButton)
        self.addNewGrpWin_AddButton.setFont(font)
        self.addNewGrpWin_AddButton.setMinimumHeight(40)
        self.addNewGrpWin_AddButton.setObjectName("settings")
        self.addNewGrpWin_AddButton.clicked.connect(self._create_new_directory)

        # show the ui
        self.addNewGrpWin.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _create_new_directory(self):

        # get name from lineEdit
        dir_name = self.addNewGrpWinLineEdit.text()
        if len(dir_name) == 0:
            cmds.warning("No valid Directory name entered.")
            return

        # make sure there are no naming conflicts
        selectedProject = self.addNewGrpWin_parentDir.text()
        selectedProject = selectedProject.partition(self.header_text + "/")[2]
        item_names = selectedProject.split("/")

        project = os.path.join(projectPath, selectedProject)
        existingGroups = os.listdir(project)

        if dir_name in existingGroups:
            cmds.warning("Directory with that name already exists. Aborting..")
            return

        # make the directory
        path = os.path.join(project, dir_name)
        os.makedirs(path)

        # close the ui
        self.addNewGrpWin.close()

        # repopulate
        populate_tree(self.directory_tree)

        # expand project to show new directory
        for each in item_names:
            items = self.directory_tree.findItems(each, QtCore.Qt.MatchRecursive)
            for item in items:
                self.directory_tree.setItemExpanded(item, True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _create_pose(self, partial_pose=False):

        # full pose or selection?
        if partial_pose is False:
            cmds.select(clear=True)

        character = self.parent_inst.character_combo_box.currentText()
        controls = get_controls(character, partial_pose)

        # validate path
        path = self.pose_path.text()
        if path == os.path.basename(projectPath) + "/":
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Save pose in root projects directory?")
            msgBox.setIcon(QtWidgets.QMessageBox.Question)
            msgBox.addButton("Yes", QtWidgets.QMessageBox.YesRole)
            msgBox.addButton("No", QtWidgets.QMessageBox.NoRole)
            ret = msgBox.exec_()
            if ret == 1:
                return

        # validate name
        if self.pose_name.text() == "":
            cmds.warning("Must enter a name for the pose.")
            return
        pose_dir = self.pose_path.text().partition(os.path.basename(projectPath) + "/")[2]
        pose_location = utils.returnNicePath(projectPath, pose_dir)
        files = os.listdir(pose_location)
        poses = []

        for each in files:
            if os.path.splitext(utils.returnNicePath(pose_location, each))[1] == ".v2pose":
                poses.append(each)

        pose_name = self.pose_name.text()
        if pose_name + ".v2pose" in poses:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Overwrite existing pose?")
            msgBox.setIcon(QtWidgets.QMessageBox.Question)
            msgBox.addButton("Yes", QtWidgets.QMessageBox.YesRole)
            msgBox.addButton("No", QtWidgets.QMessageBox.NoRole)
            ret = msgBox.exec_()
            if ret == 1:
                return

        # validate controls
        if len(controls) - 1 == 0:
            warning_string = "No controls in pose. Either select nothing to save all controls or select controls" \
                             "and retry."
            cmds.warning(warning_string)
            return

        # pass info to instance of ART_CreatePose
        pose_inst = ART_CreatePose(pose_name, pose_location, controls, viewport=self.viewport_widget.viewport,
                                   partial_pose=partial_pose)
        if pose_inst.status is True:
            self.parent_inst.get_poses()
            self.close()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# noinspection PyMissingOrEmptyDocstring
class ART_PoseLibraryUI(QtWidgets.QMainWindow):
    """
    Interface for displaying saved poses and loading them.
    """
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def __init__(self, parent=None):

        super(ART_PoseLibraryUI, self).__init__(parent)

        self.rows = 4
        self.columns = 4
        self.poses = []

        self._build_interface()
        self._populate_characters()

        # Populate the UI, selecting a default pose path if the attribute exists on the character.
        self._select_default_pose_path()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _build_interface(self):

        if cmds.window(windowName, exists=True):
            cmds.deleteUI(windowName, wnd=True)

        self.window_icon = QtGui.QIcon(os.path.join(iconsPath, "System/logo.png"))
        self.setWindowIcon(self.window_icon)
        self.setStyleSheet(STYLE)

        self.setMinimumSize(QtCore.QSize(644, 590))
        self.setMaximumSize(QtCore.QSize(644, 590))

        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setSizePolicy(mainSizePolicy)

        self.setObjectName(windowName)
        self.setWindowTitle(windowTitle)

        self.main_widget = QtWidgets.QFrame()
        self.main_widget.setObjectName("dark")
        self.setCentralWidget(self.main_widget)

        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)

        # create the menu bar
        self.menu_bar = QtWidgets.QMenuBar()
        self.menu_bar.setMaximumHeight(25)
        self.main_layout.addWidget(self.menu_bar)

        help_menu = self.menu_bar.addMenu("Help")
        help_menu.addAction("Hotkeys", self._show_hotkeys)
        help_menu.addAction("Help", self._show_help)

        # Create the top section layout, which will have two columns.
        # The first column will contain a VBoxLayout with two rows
        top_frame = QtWidgets.QFrame()
        top_frame.setObjectName("border")
        self.main_layout.addWidget(top_frame)

        top_section_layout = QtWidgets.QHBoxLayout()
        top_frame.setLayout(top_section_layout)

        column1_layout = QtWidgets.QVBoxLayout()
        top_section_layout.addLayout(column1_layout)

        row1_layout = QtWidgets.QHBoxLayout()
        column1_layout.addLayout(row1_layout)

        row2_layout = QtWidgets.QHBoxLayout()
        column1_layout.addLayout(row2_layout)

        # The first row in this first column will contain widgets for selecting which character to operate on and
        # which space to load the pose in.
        character_label = QtWidgets.QLabel("Character: ")
        character_label.setMinimumWidth(125)
        character_label.setMaximumWidth(125)
        row1_layout.addWidget(character_label)

        self.character_combo_box = QtWidgets.QComboBox()
        self.character_combo_box.setMinimumWidth(137)
        self.character_combo_box.setMaximumWidth(137)
        self.character_combo_box.setObjectName("light")
        row1_layout.addWidget(self.character_combo_box)
        self.character_combo_box.currentIndexChanged.connect(self._select_default_pose_path)
        tooltip = "Which character the poses will load onto."
        self.character_combo_box.setToolTip(tooltip)

        spacer = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        row1_layout.addItem(spacer)

        space_label = QtWidgets.QLabel("Space: ")
        space_label.setMinimumWidth(62)
        space_label.setMaximumWidth(62)
        row1_layout.addWidget(space_label)

        self.space_combo_box = QtWidgets.QComboBox()
        self.space_combo_box.setMinimumWidth(137)
        self.space_combo_box.setMaximumWidth(137)
        self.space_combo_box.setObjectName("light")
        row1_layout.addWidget(self.space_combo_box)
        self.space_combo_box.addItem("Local Space")
        self.space_combo_box.addItem("World Space")
        tooltip = "Local space will load the pose using the attribute values stored.\n\n"
        tooltip += "World space will load the pose by calculating the correct values\nin world space. "
        tooltip += "This is useful for poses that may have been saved\nwith controls in a space other than default.\n\n"
        tooltip += "Using this for mirroring, will either mirror on the character (local)\nor about the origin (world)."
        self.space_combo_box.setToolTip(tooltip)

        # The second row in this first column will contain widgets for the default pose location and the load operation.
        location_label = QtWidgets.QLabel("Default Pose Location: ")
        location_label.setMinimumWidth(125)
        location_label.setMaximumWidth(125)
        row2_layout.addWidget(location_label)

        self.default_pose_loc = QtWidgets.QLineEdit()
        self.default_pose_loc.setMinimumWidth(137)
        self.default_pose_loc.setMaximumWidth(137)
        self.default_pose_loc.setObjectName("light")
        self.default_pose_loc.setEnabled(False)
        tooltip = "Right click on a directory in the directory tree to set that\ndirectory as the default pose location"
        tooltip += " for that character.\n\nEvery time you open the pose library, it will automatically\n"
        tooltip += "open that location."
        self.default_pose_loc.setToolTip(tooltip)
        row2_layout.addWidget(self.default_pose_loc)

        spacer = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        row2_layout.addItem(spacer)

        operation_label = QtWidgets.QLabel("Operate on: ")
        operation_label.setMinimumWidth(62)
        operation_label.setMaximumWidth(62)
        row2_layout.addWidget(operation_label)

        self.operation_combo_box = QtWidgets.QComboBox()
        self.operation_combo_box.setMinimumWidth(137)
        self.operation_combo_box.setMaximumWidth(137)
        self.operation_combo_box.setObjectName("light")
        tooltip = "Change if the pose will load on selected controls or all controls."
        self.operation_combo_box.setToolTip(tooltip)
        row2_layout.addWidget(self.operation_combo_box)

        self.operation_combo_box.addItem("All Controls")
        self.operation_combo_box.addItem("Selected Controls")

        # The second column of this top section contains the button for adding a new pose.
        add_pose_btn = QtWidgets.QPushButton("Add New Pose")
        add_pose_btn.setMinimumSize(QtCore.QSize(97, 56))
        add_pose_btn.setMaximumSize(QtCore.QSize(97, 56))
        add_pose_btn.setObjectName("settings")
        top_section_layout.addWidget(add_pose_btn)
        add_pose_btn.clicked.connect(self._add_new_pose)

        # The bottom section of the interface also has two columns. One will be for browsing directories,
        # the other for displaying the poses in that directory.
        bottom_section_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(bottom_section_layout)

        # The first column will have a search bar and a directory tree widget. The search bar will search through the
        #  directories.
        tree_layout = QtWidgets.QVBoxLayout()
        bottom_section_layout.addLayout(tree_layout)

        self.tree_search = QtWidgets.QLineEdit()
        self.tree_search.setPlaceholderText("Search..")
        self.tree_search.setMinimumWidth(130)
        self.tree_search.setMaximumWidth(130)
        tree_layout.addWidget(self.tree_search)
        self.tree_search.setObjectName("light")

        self.directory_tree = QtWidgets.QTreeWidget()
        self.directory_tree.setMinimumSize(QtCore.QSize(130, 398))
        self.directory_tree.setMaximumSize(QtCore.QSize(130, 398))
        self.header_text = os.path.basename(projectPath)
        header = QtWidgets.QTreeWidgetItem([self.header_text + ":"])
        self.directory_tree.setHeaderItem(header)
        tree_layout.addWidget(self.directory_tree)
        self.rows = populate_tree(self.directory_tree, ignoreFiles=True)
        self.directory_tree.itemSelectionChanged.connect(self.get_poses)
        self.directory_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.directory_tree.customContextMenuRequested.connect(self._tree_widget_menu)

        # Hook up the search bar to the self.search function.
        self.tree_search.editingFinished.connect(partial(self._search, self.directory_tree, self.tree_search))

        # The second column will have a search bar for searching poses that are currently displayed, and a large
        # scroll area for displaying the poses as buttons.
        pose_layout = QtWidgets.QVBoxLayout()
        bottom_section_layout.addLayout(pose_layout)

        self.pose_search = QtWidgets.QLineEdit()
        self.pose_search.setPlaceholderText("Search Poses..")
        self.pose_search.setMinimumWidth(200)
        self.pose_search.setMaximumWidth(200)
        self.pose_search.setObjectName("light")
        pose_layout.addWidget(self.pose_search)

        self.scroll_contents = QtWidgets.QFrame()
        self.scroll_contents.setObjectName("lightnoborder")
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setObjectName("light")
        self.scroll_area.setMinimumSize(QtCore.QSize(466, 398))
        self.scroll_area.setMaximumSize(QtCore.QSize(466, 398))
        pose_layout.addWidget(self.scroll_area)

        self.status_bar = QtWidgets.QStatusBar(self)
        pose_layout.addWidget(self.status_bar)
        self.setStatusBar(self.status_bar)

        self.pose_search.editingFinished.connect(self._filter_poses)

        self.scroll_layout = QtWidgets.QGridLayout()
        self.scroll_layout.setHorizontalSpacing(0)
        self.scroll_layout.setVerticalSpacing(5)

        # restore window position
        artv2_settings = QtCore.QSettings("ARTv2", "PoseLibrary")
        self.restoreGeometry(artv2_settings.value("geometry"))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # noinspection PyMissingOrEmptyDocstring
    def eventFilter(self, obj, event):

        if event.type() == QtCore.QEvent.Enter:
            self.status_bar.showMessage(obj.statusTip())
        if event.type() == QtCore.QEvent.Leave:
            self.status_bar.clearMessage()

        return event.accept()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _update_thumbnail_closeEvent(self, event):

        try:
            self.update_viewport.setParent(None)
            self.update_viewport.close()
        except Exception, e:
            print e

        event.accept()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def closeEvent(self, event):

        # store window positions
        winSettings = QtCore.QSettings("ARTv2", "PoseLibrary")
        winSettings.setValue("geometry", self.saveGeometry())

        QtWidgets.QMainWindow.closeEvent(self, event)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _tree_widget_menu(self, pos):

        menu = QtWidgets.QMenu()
        menu.setStyleSheet(MENU_STYLE)
        character = self.character_combo_box.currentText()
        icon = QtGui.QIcon(os.path.join(iconsPath, "System/modelPose.png"))
        menu.addAction(icon, "Set as default pose location for " + character, partial(self._set_default_location,
                                                                                      character, pos))
        menu.exec_(self.directory_tree.viewport().mapToGlobal(pos))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _set_default_location(self, character, pos):

        item = self.directory_tree.itemAt(pos)
        path = item.data(0, QtCore.Qt.UserRole)[1]
        self.default_pose_loc.setText(path)

        if cmds.objExists(character + ":ART_RIG_ROOT"):
            if not cmds.objExists(character + ":ART_RIG_ROOT.defaultPosePath"):
                cmds.addAttr(character + ":ART_RIG_ROOT", ln="defaultPosePath", dt="string")
            cmds.setAttr(character + ":ART_RIG_ROOT.defaultPosePath", json.dumps(path), type="string")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _select_default_pose_path(self):

        character = self.character_combo_box.currentText()
        if cmds.objExists(character + ":ART_RIG_ROOT.defaultPosePath"):
            path = json.loads(cmds.getAttr(character + ":ART_RIG_ROOT.defaultPosePath"))
            self.default_pose_loc.setText(path)

            iterator = QtWidgets.QTreeWidgetItemIterator(self.directory_tree)
            items = []
            while iterator.value():
                items.append(iterator.value())
                iterator += 1

            for item in items:
                self.directory_tree.collapseItem(item)
                self.directory_tree.setItemSelected(item, False)
                if item.data(0, QtCore.Qt.UserRole)[1] == path:
                    self.directory_tree.setItemSelected(item, True)
                    self.directory_tree.scrollToItem(item)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _search(self, treeWidget, lineEdit):

        iterator = QtWidgets.QTreeWidgetItemIterator(treeWidget)
        items = []
        while iterator.value():
            items.append(iterator.value())
            iterator += 1

        for item in items:
            item.setSelected(False)
            treeWidget.setItemHidden(item, True)

        treeWidget.collapseAll()
        text = lineEdit.text()

        if len(text) > 0:
            for each in items:
                parents = []
                if text.lower() in each.text(0).lower():
                    self._find_tree_parents(each, parents)
                    for parent in parents:
                        treeWidget.setItemHidden(parent, False)
                    treeWidget.setItemHidden(each, False)
                    treeWidget.scrollToItem(each)

        if len(text) == 0:
            for item in items:
                item.setSelected(False)
                treeWidget.setItemHidden(item, False)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _filter_poses(self):

        search_term = self.pose_search.text()
        if len(search_term) > 0:
            poses = []
            for each in self.poses:
                posePath = each[0]
                poseName = os.path.splitext(os.path.basename(posePath))[0]
                if search_term in poseName:
                    poses.append([each[0], each[1]])

            self._clear_layout(self.scroll_layout)
            self._populate_poses(poses)

        else:
            self._clear_layout(self.scroll_layout)
            self._populate_poses(self.poses)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _find_tree_parents(self, item, return_list):

        parent = item.parent()
        if parent is not None:
            return_list.append(parent)
            self._find_tree_parents(parent, return_list)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def get_poses(self):
        """
        Get the poses on disk for the selected folder in the tree widget, and populate the pose library with the
        buttons for the poses.
        :return:
        """
        # Create the necessary rows and columns in the grid layout to hold our poses.
        for r in range((self.rows + 2)/4):
            for c in range(4):
                widget = QtWidgets.QLabel("")
                widget.setMinimumSize(QtCore.QSize(100, 100))
                widget.setMaximumSize(QtCore.QSize(100, 100))
                self.scroll_layout.setColumnMinimumWidth(c, 111)
                self.scroll_layout.setRowMinimumHeight(r, 111)
                self.scroll_layout.addWidget(widget, r, c)

        self._clear_layout(self.scroll_layout)

        selected = self.directory_tree.selectedItems()

        if len(selected) > 0:
            selected = selected[0]
            data = selected.data(0, QtCore.Qt.UserRole)
            folder = utils.returnFriendlyPath(data[1])

            # Locate pose files in the selected directory (and all sub-directories).
            self.poses = []

            for root, directories, files in os.walk(folder):
                for each in files:
                    location = os.path.join(root, each)

                    if os.path.splitext(location)[1] == ".v2pose":

                        # Verify that the pose has an icon file present. If so, add the pose and icon to our list.
                        icon = location.replace(".v2pose", ".png")
                        if os.path.exists(utils.returnNicePath(location, icon)):
                            pose_file = location
                            icon_file = icon
                            self.poses.append([pose_file, icon_file])

        self._populate_poses(self.poses)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _populate_poses(self, poses):

        # Loop through the incoming poses, and add them to the grid layout.
        count = 0
        for pose in poses:
            btn = self._create_pose_button(pose[0], pose[1])
            self.scroll_layout.setColumnMinimumWidth(count % self.columns, 111)
            self.scroll_layout.setRowMinimumHeight(count / self.columns, 111)
            self.scroll_layout.addWidget(btn, count / self.columns, count % self.columns)
            count += 1

        # Fill empty space with a spacer to keep spacing between pose buttons consistent.
        if count % self.columns > 0:
            for i in range(self.columns - (count % self.columns)):

                spacer = QtWidgets.QSpacerItem(111, 111, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
                self.scroll_layout.setColumnMinimumWidth((count % self.columns) + i, 111)
                self.scroll_layout.setRowMinimumHeight(count / self.columns, 111)
                self.scroll_layout.addItem(spacer, count / self.columns, (count % self.columns) + i)

        spacer = QtWidgets.QSpacerItem(111, 111, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.scroll_layout.addItem(spacer, self.scroll_layout.rowCount() + 1, 0)

        self.scroll_contents.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_contents)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _create_pose_button(self, pose_path, icon_path):

        btn = QtWidgets.QPushButton()
        btn.setMinimumSize(QtCore.QSize(100, 100))
        btn.setMaximumSize(QtCore.QSize(100, 100))
        image = QtGui.QIcon(icon_path)
        btn.setIconSize(QtCore.QSize(96, 96))
        btn.setIcon(image)
        btn.setObjectName("pose")
        btn.setProperty("path", pose_path)
        btn.clicked.connect(partial(self._load_pose, btn))
        btn.installEventFilter(self)

        # Read the pose file data so the info contained can be added to the tooltip.
        f = open(pose_path, 'r')
        data = json.load(f)
        f.close()

        # Build the tooltip for the pose button.
        status_string = "Pose Name: " + os.path.splitext(os.path.basename(pose_path))[0] + "    "
        status_string += "\n\nCreated By: " + data.get("creator") + "    "
        status_string += "\nEdited On: " + data.get("date") + "    "
        status_string += "\nContains " + str(len(data.get("controls"))) + " controls"
        btn.setStatusTip(status_string)

        btn.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        btn.customContextMenuRequested.connect(partial(self._pose_button_menu, btn))

        return btn

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _pose_button_menu(self, btn, pos):

        rename_icon = QtGui.QIcon(os.path.join(iconsPath, "System/edit.png"))
        delete_icon = QtGui.QIcon(os.path.join(iconsPath, "System/removeModule.png"))
        capture_icon = QtGui.QIcon(os.path.join(iconsPath, "System/capture.png"))
        mirror_local_icon = QtGui.QIcon(os.path.join(iconsPath, "System/mirror.png"))
        offset_pose_icon = QtGui.QIcon(os.path.join(iconsPath, "System/offset_pose.png"))

        menu = QtWidgets.QMenu()
        menu.setStyleSheet(MENU_STYLE)

        mirror_poseX_action = menu.addAction(mirror_local_icon, "Mirror pose (X)", partial(self._load_pose_mirror, btn,
                                                                                           "X"))

        status_string = "Loads a mirrored version of the pose. Use the 'Space' drop-down menu to change " \
                        "how the mirrored pose is loaded."
        mirror_poseX_action.hovered.connect(partial(self._show_status_tip, status_string))

        mirror_poseY_action = menu.addAction(mirror_local_icon, "Mirror pose (Y)", partial(self._load_pose_mirror, btn,
                                                                                           "Y"))

        status_string = "Loads a mirrored version of the pose. Use the 'Space' drop-down menu to change " \
                        "how the mirrored pose is loaded."
        mirror_poseY_action.hovered.connect(partial(self._show_status_tip, status_string))

        mirror_poseZ_action = menu.addAction(mirror_local_icon, "Mirror pose (Z)", partial(self._load_pose_mirror, btn,
                                                                                           "Z"))

        status_string = "Loads a mirrored version of the pose. Use the 'Space' drop-down menu to change " \
                        "how the mirrored pose is loaded."
        mirror_poseZ_action.hovered.connect(partial(self._show_status_tip, status_string))

        offset_action = menu.addAction(offset_pose_icon, "Load pose with offset", partial(self._load_pose_offset, btn))
        status_string = "Loads the pose at the location and orientation of the selected control. See the Help menu" \
                        "for more details and examples."
        offset_action.hovered.connect(partial(self._show_status_tip, status_string))

        menu.addSeparator()

        update_thumbnail = menu.addAction(capture_icon, "Update thumbnail", partial(self._update_thumbnail_ui, btn))
        status_string = "Re-capture the thumbnail for this pose."
        update_thumbnail.hovered.connect(partial(self._show_status_tip, status_string))

        rename_action = menu.addAction(rename_icon, "Rename pose", partial(self._rename_pose, btn))
        status_string = "Rename this pose."
        rename_action.hovered.connect(partial(self._show_status_tip, status_string))

        delete_action = menu.addAction(delete_icon, "Delete pose", partial(self._delete_pose, btn))
        status_string = "Permanently delete this pose."
        delete_action.hovered.connect(partial(self._show_status_tip, status_string))

        menu.exec_(btn.mapToGlobal(pos))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _show_status_tip(self, status_string):

        self.status_bar.showMessage(status_string, 3500)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _show_help(self):

        html_file = os.path.join(toolsPath, "Documentation\\build\\poseLibrary.html")
        webbrowser.get().open('file://' + os.path.realpath(html_file))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _show_hotkeys(self):

        window = QtWidgets.QMainWindow(interfaceUtils.getMainWindow())
        window.setWindowTitle("Pose Library Hotkeys")
        window.setMinimumSize(QtCore.QSize(300, 300))
        window.setMaximumSize(QtCore.QSize(300, 300))
        window.setStyleSheet(STYLE)

        widget = QtWidgets.QLabel()
        widget.setMinimumSize(QtCore.QSize(300, 300))
        widget.setMaximumSize(QtCore.QSize(300, 300))

        img_path = utils.returnFriendlyPath(os.path.join(iconsPath, "Help/tooltips/pose_lib_hotkeys.png"))
        pixmap = QtGui.QPixmap(img_path)
        widget.setPixmap(pixmap)

        window.setCentralWidget(widget)
        window.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _update_thumbnail_ui(self, btn):

        pose_path = btn.property("path")
        icon_path = pose_path.replace(".v2pose", ".png")

        window = QtWidgets.QMainWindow(interfaceUtils.getMainWindow())
        window.setMinimumSize(QtCore.QSize(250, 300))
        window.setMaximumSize(QtCore.QSize(250, 300))
        window.setStyleSheet(STYLE)
        window.closeEvent = self._update_thumbnail_closeEvent

        main_widget = QtWidgets.QFrame()
        main_widget.setObjectName("dark")
        window.setCentralWidget(main_widget)

        layout = QtWidgets.QVBoxLayout(main_widget)

        self.update_viewport = ViewportWidget(200, 200, None)
        layout.addWidget(self.update_viewport)

        save_button = QtWidgets.QPushButton("Save and Close")
        save_button.setMinimumHeight(48)
        save_button.setMaximumHeight(48)
        save_button.setObjectName("settings")
        save_button.clicked.connect(partial(self._update_thumbnail, self.update_viewport, window, icon_path))
        layout.addWidget(save_button)

        window.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _update_thumbnail(self, viewport, window, icon_path):
        cmds.refresh(force=True)
        newView = mui.M3dView()
        mui.M3dView.getM3dViewFromModelEditor(viewport.viewport, newView)

        # read the color buffer from the view, and save the MImage to disk
        self.thumbnail = openMaya.MImage()
        newView.readColorBuffer(self.thumbnail, True)
        try:
            self.thumbnail.writeToFile(icon_path, 'png')
        except RuntimeError:
            raise RuntimeError("Unable to write to file. Make sure file is not read-only.")

        window.close()
        self.get_poses()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _rename_pose(self, btn):

        pose_path = btn.property("path")
        icon_path = pose_path.replace(".v2pose", ".png")

        new_name, ok = QtWidgets.QInputDialog.getText(self, "Rename Pose", "New Name:")

        if ok and new_name:
            directory = os.path.dirname(pose_path)

            try:
                os.rename(pose_path, os.path.join(directory, new_name + ".v2pose"))
                os.rename(icon_path, os.path.join(directory, new_name + ".png"))
            except EnvironmentError:
                error_type, value, traceback = sys.exc_info()
                interfaceUtils.display_error(value, traceback)

        self.get_poses()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _delete_pose(self, btn):

        pose_path = btn.property("path")
        icon_path = pose_path.replace(".v2pose", ".png")

        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Question)
        msg_box.setText("Are you sure you want to delete this pose?")
        msg_box.addButton("Yes", QtWidgets.QMessageBox.YesRole)
        msg_box.addButton("No", QtWidgets.QMessageBox.NoRole)
        ret = msg_box.exec_()

        if ret == 1:
            return

        try:
            os.remove(pose_path)
            os.remove(icon_path)
        except EnvironmentError:
            error_type, value, traceback = sys.exc_info()
            interfaceUtils.display_error(value, traceback)

        self.get_poses()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _clear_layout(self, layout):

        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self._clear_layout(child.layout())

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _add_new_pose(self):

        if cmds.window(windowName_cp, exists=True):
            cmds.deleteUI(windowName_cp, wnd=True)

        inst = ART_CreatePoseUI(self, interfaceUtils.getMainWindow())
        inst.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _populate_characters(self):

        characters = utils.returnCharacterModules()
        count = 0
        for character in characters:
            name = cmds.getAttr(character + ".namespace")
            self.character_combo_box.addItem(name)
            self.character_combo_box.setItemData(count, character)
            count += 1

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _load_pose(self, button):

        operation = self.operation_combo_box.currentText()
        space = self.space_combo_box.currentText()

        mods = cmds.getModifiers()
        # ctrl
        if (mods & 4) > 0:
            operation = "Selected Controls"

        # shift
        if (mods & 1) > 0:
            space = "World Space"

        character = self.character_combo_box.currentText()
        pose_file = button.property("path")

        ART_LoadPose(pose_file, operation, space, character)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _load_pose_mirror(self, button, axis):

        character = self.character_combo_box.currentText()
        pose_file = button.property("path")

        operation = "Mirror"
        if self.operation_combo_box.currentText() == "Selected Controls":
            operation = "Mirror Selected"

        space = self.space_combo_box.currentText()

        mods = cmds.getModifiers()
        # ctrl
        if (mods & 4) > 0:
            operation = "Mirror Selected"

        # shift
        if (mods & 1) > 0:
            space = "World Space"

        ART_LoadPose(pose_file, operation, space, character, axis)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _load_pose_offset(self, button):

        character = self.character_combo_box.currentText()
        pose_file = button.property("path")
        operation = "Offset"
        space = "Local Space"

        # get selected control and validate
        selection = cmds.ls(sl=True)
        if len(selection) > 0:
            controls = get_controls(character)
            if selection[0] in controls:
                ART_LoadPose(pose_file, operation, space, character, "X", offset=selection[0])
            else:
                raise RuntimeError("No valid control selected.")
        else:
            raise RuntimeError("No control selected.")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class ViewportWidget(QtWidgets.QFrame):
    """
    Widget for showing and embedding a maya viewport. Also contains controls for changing the background color.
    """

    def __init__(self, width, height, parent=None):
        super(ViewportWidget, self).__init__(parent)

        self.setMinimumSize(width + 50, height + 10)
        self.setMaximumSize(width + 50, height + 10)
        self.setObjectName("dark")
        self.setStyleSheet(STYLE)

        layout = QtWidgets.QHBoxLayout(self)
        column_1_layout = QtWidgets.QVBoxLayout()
        layout.addLayout(column_1_layout)
        column_2_layout = QtWidgets.QVBoxLayout()
        layout.addLayout(column_2_layout)

        # model editor
        self.viewport = cmds.modelEditor(dl="default", da="smoothShaded", hud=False, gr=False, dtx=True, sdw=True,
                                         j=False, ca=False, lt=False, nc=False, m=False)

        self.viewport_widget = interfaceUtils.getMayaName(self.viewport)
        self.viewport_widget.setObjectName("border")
        self.viewport_widget.setEnabled(False)
        self.viewport_widget.setMinimumSize(width - 4, height - 4)
        self.viewport_widget.setMaximumSize(width - 4, height - 4)
        column_1_layout.addWidget(self.viewport_widget)

        blue_background_button = QtWidgets.QPushButton()
        blue_background_button.setMinimumSize(QtCore.QSize(20, 20))
        blue_background_button.setMaximumSize(QtCore.QSize(20, 20))
        blue_background_button.setObjectName("blue")
        column_2_layout.addWidget(blue_background_button)
        blue_background_button.clicked.connect(partial(self._change_background, "imagePlanePose"))

        brown_background_button = QtWidgets.QPushButton()
        brown_background_button.setMinimumSize(QtCore.QSize(20, 20))
        brown_background_button.setMaximumSize(QtCore.QSize(20, 20))
        brown_background_button.setObjectName("brown")
        column_2_layout.addWidget(brown_background_button)
        brown_background_button.clicked.connect(partial(self._change_background, "imagePlanePose2"))

        purple_background_button = QtWidgets.QPushButton()
        purple_background_button.setMinimumSize(QtCore.QSize(20, 20))
        purple_background_button.setMaximumSize(QtCore.QSize(20, 20))
        purple_background_button.setObjectName("purple")
        column_2_layout.addWidget(purple_background_button)
        purple_background_button.clicked.connect(partial(self._change_background, "imagePlanePose3"))

        green_background_button = QtWidgets.QPushButton()
        green_background_button.setMinimumSize(QtCore.QSize(20, 20))
        green_background_button.setMaximumSize(QtCore.QSize(20, 20))
        green_background_button.setObjectName("green")
        column_2_layout.addWidget(green_background_button)
        green_background_button.clicked.connect(partial(self._change_background, "imagePlanePose4"))

        spacer = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        column_2_layout.addItem(spacer)

        # create and attach thumbnail camera
        self._create_camera("imagePlanePose")
        self.viewport_widget.show()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _create_camera(self, img):

        self.camera = cmds.camera(name="thumbnail_camera")[0]
        cmds.parentConstraint("persp", self.camera)
        cmds.setAttr(self.camera + ".v", 0)
        cmds.lockNode(self.camera, lock=True)

        cmds.modelEditor(self.viewport, edit=True, camera=self.camera, av=True)

        # turn on anti-aliasing and ambient occlusion
        if cmds.getAttr("hardwareRenderingGlobals.ssaoEnable") == 0:
            cmds.setAttr("hardwareRenderingGlobals.ssaoEnable", 1)
        cmds.setAttr("hardwareRenderingGlobals.ssaoAmount", 2)
        if cmds.getAttr("hardwareRenderingGlobals.multiSampleEnable") == 0:
            cmds.setAttr("hardwareRenderingGlobals.multiSampleEnable", 1)

        # add image plane with image
        img_path = utils.returnFriendlyPath(os.path.join("System/backgrounds", img + ".png"))
        imagePlanePath = utils.returnFriendlyPath(os.path.join(iconsPath, img_path))
        self.imagePlane = cmds.imagePlane(fn=imagePlanePath, c=self.camera, lt=self.camera, sia=False)
        cmds.setAttr(self.imagePlane[1] + ".depth", 3000)
        cmds.setAttr(self.imagePlane[1] + ".sizeX", 2)
        cmds.setAttr(self.imagePlane[1] + ".sizeY", 2)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # noinspection PyMissingOrEmptyDocstring
    def closeEvent(self, event):

        if cmds.objExists("thumbnail_camera*"):
            children = cmds.listRelatives("thumbnail_camera*", children=True)
            if len(children) > 0:
                for each in children:
                    cmds.lockNode(each, lock=False)
            cmds.lockNode("thumbnail_camera*", lock=False)
            cmds.delete("thumbnail_camera*")
            if cmds.objExists(self.imagePlane[0]):
                cmds.delete(self.imagePlane[0])

        QtWidgets.QFrame.closeEvent(self, event)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _change_background(self, img):

        for node in [self.imagePlane[0], self.camera]:
            cmds.lockNode(node, lock=False)
            cmds.delete(node)

        self._create_camera(img)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def update_path(widget, lineEdit, altWidget=None):
    """
    Updates the given lineEdit widget with the with a directory path from the given widget's selected items.

    :param widget: Usually a tree widget, but the widget to query the selected directory from.
    :param lineEdit: Which lineEdit widget to update with the directory path
    :param altWidget: A secondary lineEdit widget to display only the file name.
    """

    selected = widget.selectedItems()
    if len(selected) > 0:
        selected = selected[0]
        item_type = selected.data(0, QtCore.Qt.UserRole)

        path = item_type[1].partition(os.path.basename(projectPath))[2]
        path = utils.returnFriendlyPath(path)

        if item_type[0] == "folder":
            lineEdit.setText(os.path.basename(projectPath) + path + "/")

        if item_type[0] == "file":
            file_data = path.rpartition("/")
            path_name = file_data[0]
            file_name = os.path.splitext(file_data[2])[0]

            lineEdit.setText(os.path.basename(projectPath) + path_name + "/")
            if altWidget is not None:
                altWidget.setText(file_name)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def populate_tree(widget, ignoreFiles=False):
    """
    Find all projects on disk (using the project path setting) and add each project to the tree widget with the
    sub-folders of that project.

    """

    widget.clear()

    # if the project path doesn't exist on disk, create it
    if not os.path.exists(projectPath):
        os.makedirs(projectPath)

    # get a list of the existing folders in projects
    existingProjects = os.listdir(projectPath)
    folders = []

    # find out which returned items are directories
    for each in existingProjects:
        if os.path.isdir(utils.returnFriendlyPath(os.path.join(projectPath, each))):
            folders.append(each)

    items = []
    populate_project_tree(widget, projectPath, items)

    if ignoreFiles is False:
        for each in items:
            file_name = os.path.splitext(each[1])[0]
            file_item = QtWidgets.QTreeWidgetItem(each[2], [file_name])
            file_item.setData(0, QtCore.Qt.UserRole, ["file", each[0]])
            icon_path = utils.returnNicePath(iconsPath, 'System/file.png')
            file_item.setIcon(0, QtGui.QIcon(icon_path))

    return len(items)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def populate_project_tree(widget, directory, item_list, parent_item=None):
    """
    Populates the given treeWidget (widget) with the items in the given directory.

    :param widget: The tree widget to populate.
    :param directory: Directory to crawl through and gather all sub directories and files.
    :param item_list: A list passed in that gets populated with directory items that are files only.
    :param parent_item: The parent QTreeWidgetItem that the created QTreeWidgetItem will get parented under.
    """

    # creating some lists for filtering folders and files
    banned = [".mayaSwatches"]
    file_filter = [".v2pose"]

    # get items in passed in directory
    sub_items = os.listdir(directory)
    for each in sub_items:

        # if the item is a directory (not a file), check for children
        if os.path.isdir(os.path.join(directory, each)):
            if not parent_item:
                if each not in banned:
                    folder_item = QtWidgets.QTreeWidgetItem(widget, [each])
                    folder_item.setData(0,
                                        QtCore.Qt.UserRole,
                                        ["folder", utils.returnFriendlyPath(os.path.join(directory, each))])
                    icon_path = utils.returnNicePath(iconsPath, 'System/folder.png')
                    folder_item.setIcon(0, QtGui.QIcon(icon_path))
                    populate_project_tree(widget, utils.returnFriendlyPath(os.path.join(directory, each)), item_list,
                                          folder_item)
            else:
                if each not in banned:
                    folder_item = QtWidgets.QTreeWidgetItem(parent_item, [each])
                    folder_item.setData(0, QtCore.Qt.UserRole,
                                        ["folder", utils.returnFriendlyPath(os.path.join(directory, each))])
                    icon_path = utils.returnNicePath(iconsPath, 'System/folder.png')
                    folder_item.setIcon(0, QtGui.QIcon(icon_path))

                    populate_project_tree(widget, utils.returnFriendlyPath(os.path.join(directory, each)), item_list,
                                          folder_item)

        # if the item is a file, add the item to the tree widget
        if os.path.isfile(os.path.join(directory, each)):
            if os.path.splitext(each)[1] in file_filter:
                item_list.append([os.path.join(directory, each), each, parent_item])


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def get_controls(character, partial_pose=False):
    """
    Gets the controls for the given character.

    :param character: Which character/namespace to gather data for.
    :param partial_pose: Whether or not to return all controls or only controls that match the selection.
    :return: returns a list of controls for the character.
    """

    selection = cmds.ls(sl=True)

    return_controls = []
    character_controls = []

    if cmds.objExists(character + ":" + "ART_RIG_ROOT"):
        modules = cmds.listConnections(character + ":ART_RIG_ROOT.rigModules")

        if modules is not None:
            for mod in modules:
                controls = cmds.listConnections(mod + ".controls")

                if controls is not None:
                    for control in controls:
                        # get all attrs on the controlNode
                        attrs = cmds.listAttr(control, ud=True)

                        # loop through attrs, getting connections
                        for attr in attrs:
                            connections = cmds.listConnections(control + "." + attr, source=False)
                            if connections is not None:
                                character_controls.extend(connections)

    if len(selection) > 0:
        for each in selection:
            if each in character_controls:
                return_controls.append(each)

    if partial_pose is False:
        if len(selection) == 0:
            for each in character_controls:
                return_controls.append(each)
        return_controls.append(character + ":" + "rig_settings")

    return return_controls


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def run():
    """ runs the pose library interface."""

    if cmds.window(windowName, exists=True):
        cmds.deleteUI(windowName, wnd=True)

    gui = ART_PoseLibraryUI(interfaceUtils.getMainWindow())
    gui.show()
    return gui
