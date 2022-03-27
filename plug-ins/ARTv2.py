import os
import sys
import webbrowser

import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm

# maya 2016 and before vs maya 2017 and after
try:
    from PySide import QtCore
except:
    from PySide2 import QtCore


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def makeMyCustomUI():
    gMainWindow = mel.eval('$temp1=$gMainWindow')
    customMenu = cmds.menu("epicGamesARTv2Menu", label="A.R.T. 2.0", parent=gMainWindow)

    # ART
    cmds.menuItem(parent=customMenu, label="Animation Rigging Toolkit 2.0", bld=True, enable=False)

    cmds.menuItem(parent=customMenu, divider=True, dividerLabel="Rigging:")
    cmds.menuItem(parent=customMenu, label="Rig Creator", c=ART_characterRigCreator)
    cmds.menuItem(parent=customMenu, label="Open Rig File", c=ART_EditRig)

    edit_rig_menu = cmds.menuItem(parent=customMenu, label="Edit Rig..", subMenu=True)

    cmds.menuItem(parent=edit_rig_menu, divider=True, dividerLabel="Setup Space Switching:")
    cmds.menuItem(parent=edit_rig_menu, label="Create Space For Control", c=ART_CreateSpace)
    cmds.menuItem(parent=edit_rig_menu, label="Create Global Spaces", c=ART_CreateGlobalSpaces)
    cmds.menuItem(parent=edit_rig_menu, label="Rename a Space", c=ART_RenameSpace)
    cmds.menuItem(parent=edit_rig_menu, label="Delete a Space", c=ART_DeleteSpace)

    cmds.menuItem(parent=edit_rig_menu, divider=True, dividerLabel="Misc:")
    cmds.menuItem(parent=edit_rig_menu, label="Setup Pick-Walking", c=launchPickWalkUI)
    cmds.menuItem(parent=edit_rig_menu, label="Override Joint Names", c=launchOverrideJoints)

    cmds.menuItem(parent=edit_rig_menu, divider=True, dividerLabel="Export:")
    cmds.menuItem(parent=edit_rig_menu, label="Export Skel Meshes (FBX)", c=launchExportMeshes)

    cmds.menuItem(parent=customMenu, divider=True, dividerLabel="Animation:")
    cmds.menuItem(parent=customMenu, label="Add Rig For Animation", c=ART_AddRig)
    cmds.menuItem(parent=customMenu, label="Animation Tools", c=ART_LaunchAnimTools)

    cmds.menuItem(parent=customMenu, divider=True, dividerLabel="Misc:")
    cmds.menuItem(parent=customMenu, label="Settings", c=launchSettings)
    cmds.menuItem(parent=customMenu, label="Hotkey Editor", c=launchHotkeyEditor)
    cmds.menuItem(parent=customMenu, label="Run Batch Script", c=launchBatcher)
    cmds.menuItem(parent=customMenu, label="Check For Updates", c=ART_Update)
    # cmds.menuItem(parent=customMenu, label="Report an Issue", c=ART_Report)

    cmds.menuItem(parent=customMenu, divider=True, dividerLabel="UE4:")
    cmds.menuItem(parent=customMenu, label="UE4 Live Link", c=launchLiveLink)

    cmds.menuItem(parent=customMenu, divider=True, dividerLabel="Help")
    cmds.menuItem(parent=customMenu, label="Technical Documentation", c=ART_TechDocs)

    ART_writeStyleSheets()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def ART_writeStyleSheets(*args):
    settings = QtCore.QSettings("Epic Games", "ARTv2")
    scriptPath = settings.value("scriptPath")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def ART_CreateSpace(*args):
    ART_writeStyleSheets()
    import Tools.Animation.Interfaces.ART_SpaceSwitcherUI as ssui
    reload(ssui)
    ssui.create_space(None, None)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def ART_CreateGlobalSpaces(*args):
    ART_writeStyleSheets()
    import Tools.Animation.Interfaces.ART_SpaceSwitcherUI as ssui
    reload(ssui)
    ssui.create_global_spaces()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def ART_RenameSpace(*args):
    ART_writeStyleSheets()
    import Tools.Animation.Interfaces.ART_SpaceSwitcherUI as ssui
    reload(ssui)

    control = None
    selection = cmds.ls(sl=True)
    if len(selection) > 0:
        if cmds.objExists(selection[0] + ".follow"):
            control = selection[0]

    ssui.rename_space(control)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def ART_DeleteSpace(*args):
    ART_writeStyleSheets()
    import Tools.Animation.Interfaces.ART_SpaceSwitcherUI as ssui
    reload(ssui)

    control = None
    selection = cmds.ls(sl=True)
    if len(selection) > 0:
        if cmds.objExists(selection[0] + ".follow"):
            control = selection[0]

    ssui.delete_space(control)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def ART_characterRigCreator(*args):
    ART_writeStyleSheets()
    import Tools.Rigging.ART_RigCreatorUI as ART_RigCreatorUI
    reload(ART_RigCreatorUI)
    ART_RigCreatorUI.createUI()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def ART_EditRig(*args):
    ART_writeStyleSheets()
    import Tools.Rigging.ART_EditRigUI as ART_EditRigUI
    reload(ART_EditRigUI)
    ART_EditRigUI.run()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def ART_AddRig(*args):
    ART_writeStyleSheets()
    import Tools.Rigging.ART_EditRigUI as ART_EditRigUI
    reload(ART_EditRigUI)
    ART_EditRigUI.runAdd()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def ART_LaunchAnimTools(*args):
    ART_writeStyleSheets()
    import Tools.Animation.ART_AnimationUI as ART_AnimationUI
    reload(ART_AnimationUI)
    ART_AnimationUI.run()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def launchSettings(*args):
    ART_writeStyleSheets()
    import Tools.System.ART_Settings as ART_Settings
    reload(ART_Settings)
    ART_Settings.run()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def launchHotkeyEditor(*args):

    ART_writeStyleSheets()
    import Tools.System.ART_HotkeyEditor as ART_HotkeyEditor
    reload(ART_HotkeyEditor)
    ART_HotkeyEditor.run()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def launchPickWalkUI(*args):

    ART_writeStyleSheets()
    import Tools.Animation.Interfaces.ART_PickWalkSetupUI as ART_PickWalkSetupUI
    reload(ART_PickWalkSetupUI)
    ART_PickWalkSetupUI.run()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def launchOverrideJoints(*args):

    ART_writeStyleSheets()
    import Tools.Rigging.Interfaces.ART_OverrideJointNames_UI as ojn
    reload(ojn)
    ojn.run()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def launchExportMeshes(*args):

    ART_writeStyleSheets()

    if cmds.objExists("root"):
        if cmds.objExists("JointMover"):
            if cmds.objExists("ART_RIG_ROOT"):
                import Tools.Rigging.ART_RigCreatorUI as ART_RigCreatorUI
                reload(ART_RigCreatorUI)
                inst = ART_RigCreatorUI.createUI()

                from Tools.Rigging import ART_ExportMeshes
                reload(ART_ExportMeshes)
                ART_ExportMeshes.ART_ExportMeshes(inst)
                return

    cmds.warning("File contains no ARTv2 asset.")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def launchBatcher(*args):

    ART_writeStyleSheets()
    import Tools.System.ART_Batcher as ART_Batcher
    reload(ART_Batcher)
    ART_Batcher.art_batcher_ui()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def launchLiveLink(*args):

    version = cmds.about(version=True)
    plugin = "MayaLiveLinkPlugin2018.mll"

    if "2016" in version:
        plugin = "MayaLiveLinkPlugin2016.mll"
    if "2017" in version:
        plugin = "MayaLiveLinkPlugin2017.mll"

    try:
        cmds.loadPlugin(plugin)
        cmds.loadPlugin("MayaLiveLinkUI")
    except Exception:
        cmds.warning("No Maya Live Link plugin installed.")
        cmds.warning("See: https://docs.unrealengine.com/en-us/Engine/Animation/Live-Link-Plugin")
        return

    mel.eval("MayaLiveLinkUI;")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def unbind_mesh(*args):

    selection = pm.ls(sl=True)
    if selection:
        if isinstance(selection[0], pm.nodetypes.Transform):
            children = selection[0].getChildren()
            for child in children:
                shape = child.getShape()
                skin_cluster = mel.eval('findRelatedSkinCluster ' + child.nodeName())
                if skin_cluster:
                    pm.PyNode(skin_cluster).envelope.set(0)

        else:
            pm.warning("please select a group containing meshes.")
    else:
        pm.warning("please select a group containing meshes.")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def rebind_mesh(*args):

    selection = pm.ls(sl=True)
    if selection:
        mel.eval("BakeAllNonDefHistory")
        if isinstance(selection[0], pm.nodetypes.Transform):
            children = selection[0].getChildren()
            for child in children:
                shape = child.getShape()
                history = [n for n in shape.history(il=1, pdo=True) if not isinstance(n, pm.nodetypes.GeometryFilter)]
                if history:
                    pm.warning("Non-deformer history found. Skin weights may be affected.")
                skin_cluster = mel.eval('findRelatedSkinCluster ' + child.nodeName())
                if skin_cluster:
                    pm.PyNode(skin_cluster).envelope.set(1)

        else:
            pm.warning("please select a group containing meshes.")
    else:
        pm.warning("please select a group containing meshes.")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def _mesh_compare(grp, namespace):
    from maya import OpenMaya

    group_node = pm.PyNode(grp)
    meshes = group_node.getChildren()

    for mesh in meshes:
        if pm.objExists(namespace + ":" + mesh.nodeName()):
            _copy_weights(mesh, namespace + ":" + mesh.nodeName())
        else:
            OpenMaya.MGlobal_displayError("Mesh does not exist: {0}".format(namespace + ":" + mesh.nodeName()))


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def transfer_weights(*args):

    result = cmds.promptDialog(
        title='Transfer Weights',
        message='Namespace:',
        button=['OK', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel')

    if result == 'OK':
        namespace = cmds.promptDialog(query=True, text=True)
        grp = cmds.ls(sl=True)[0]

        _mesh_compare(grp, namespace)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def _copy_weights(source, target):
    skin_cluster = mel.eval('findRelatedSkinCluster ' + source)
    if skin_cluster:
        influences = cmds.skinCluster(skin_cluster, q=True, wi=True)
        max_influences = cmds.skinCluster(skin_cluster, q=True, mi=True)

        cmds.select(influences)
        new_skin = cmds.skinCluster(cmds.ls(sl=True), target, tsb=True, mi=max_influences)[0]
        cmds.copySkinWeights(ss=skin_cluster, ds=new_skin, noMirror=True)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def make_outline_meshes(*args):


    selection = pm.ls(sl=True)
    if selection:
        if isinstance(selection[0], pm.nodetypes.Transform):

            group = pm.group(name="meshes_outline", empty=True)
            material = pm.shadingNode("lambert", asShader=True, name="outline_material")
            shader = pm.sets(renderable=True, noSurfaceShader=True, empty=True, name="outlineSurfaceShader")
            material.outColor.connect(shader.surfaceShader)

            children = selection[0].getChildren()
            for child in children:
                outline = child.duplicate(name=child.nodeName() + "_outline")[0]
                outline.setParent(group)
                outline.getShape().displayColors.set(0)
                pm.sets(shader, edit=True, forceElement=[outline])

                _copy_weights(child.nodeName(), outline.nodeName())

            mel.eval('MLdeleteUnused;')


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def ART_Update(*args):
    ART_writeStyleSheets()
    import Tools.System.Interfaces.ART_UpdaterUI as ART_Updater
    reload(ART_Updater)
    ART_Updater.run()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def ART_Report(*args):
    ART_writeStyleSheets()
    import Tools.System.ART_Reporter as ART_Reporter
    ART_Reporter.run()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def ART_TechDocs(*args):
    settings = QtCore.QSettings("Epic Games", "ARTv2")
    toolsPath = settings.value("toolsPath")
    html_file = os.path.join(toolsPath, "Documentation\\build\\index.html")
    webbrowser.get().open('file://' + os.path.realpath(html_file))


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def removeMyCustomUI():
    cmds.deleteUI("epicGamesARTv2Menu")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Function for allowing user to browse to Maya Tools directory location
def epicToolsInstall_UI():
    if cmds.window("epicToolsInstall_UI", exists=True):
        cmds.deleteUI("epicToolsInstall_UI")

    window = cmds.window("epicToolsInstall_UI", w=300, h=100, title="Epic Games Tools Install", mnb=False, mxb=False)

    mainLayout = cmds.columnLayout(w=300, h=100)
    formLayout = cmds.formLayout(w=300, h=100)

    text = cmds.text(
        label="ERROR: Could not find ARTv2 directory.\n Please locate folder using the \'Browse\' button.", w=300)
    cancelButton = cmds.button(label="Cancel", w=140, h=50, c=cancel)
    browseButton = cmds.button(label="Browse", w=140, h=50, c=browse)

    cmds.formLayout(formLayout, edit=True, af=[(text, 'left', 10), (text, 'top', 10)])
    cmds.formLayout(formLayout, edit=True, af=[(cancelButton, 'left', 5), (cancelButton, 'top', 50)])
    cmds.formLayout(formLayout, edit=True, af=[(browseButton, 'right', 5), (browseButton, 'top', 50)])

    cmds.showWindow(window)
    cmds.window(window, edit=True, w=300, h=100)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# if user cancels out of UI setup
def cancel(*args):
    cmds.deleteUI("epicToolsInstall_UI")
    cmds.warning("Maya Tools will not be setup")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# function to browse to MayaTools location on disk
def browse(*args):
    # browser to tools directory
    mayaToolsDir = cmds.fileDialog2(dialogStyle=2, fileMode=3)[0]
    # confirm that this is actually the maya tools directory
    if os.path.basename(mayaToolsDir) != "ARTv2":
        cmds.warning("Selected directory is not valid. Please locate the ARTv2 directory.")

    else:
        cmds.deleteUI("epicToolsInstall_UI")

        # create file that contains this path
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        settings.setValue("toolsPath", os.path.normpath(mayaToolsDir))
        settings.setValue("scriptPath", os.path.normpath(mayaToolsDir + "/Core/Scripts"))
        settings.setValue("iconPath", os.path.normpath(mayaToolsDir + "/Core/Icons"))
        settings.setValue("projectPath", os.path.normpath(mayaToolsDir + "/Projects"))

        # run setup
        epicTools()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# check to see if tools exist
def epicTools():
    settings = QtCore.QSettings("Epic Games", "ARTv2")
    toolsPath = settings.value("toolsPath")
    scriptPath = settings.value("scriptPath")
    iconPath = settings.value("iconPath")
    projectPath = settings.value("projectPath")

    if toolsPath is None:
        epicToolsInstall_UI()

    if os.path.exists(toolsPath):
        paths = [returnFriendlyPath(scriptPath),
                 returnFriendlyPath(os.path.join(scriptPath, os.path.normpath("Utilities"))),
                 returnFriendlyPath(os.path.join(scriptPath, os.path.normpath("Tools"))),
                 returnFriendlyPath(os.path.join(scriptPath, os.path.normpath("RigModules"))),
                 returnFriendlyPath(os.path.join(scriptPath, os.path.normpath("ThirdParty")))]

        defaultPaths = [returnFriendlyPath(os.path.join(toolsPath, os.path.normpath("Core/Scripts"))),
                        returnFriendlyPath(os.path.join(toolsPath, os.path.normpath("Core/Scripts/Utilities"))),
                        returnFriendlyPath(os.path.join(toolsPath, os.path.normpath("Core/Scripts/Tools"))),
                        returnFriendlyPath(os.path.join(toolsPath, os.path.normpath("Core/Scripts/RigModules"))),
                        returnFriendlyPath(os.path.join(toolsPath, os.path.normpath("Core/Scripts/ThirdParty")))]

        # look in sys.path to see if path is in sys.path. if not, add it
        for path in defaultPaths:
            for sysPath in sys.path:
                # sysPath = returnFriendlyPath(sysPath)
                sysPath = os.path.normpath(sysPath).replace("\\", "/")
                if path == sysPath:
                    sys.path.remove(path)

        for path in paths:
            if path not in sys.path:
                sys.path.append(path)

        for path in sys.path:
            print path

    else:
        epicToolsInstall_UI()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# convenience function for returning an os friendly path
def returnFriendlyPath(path):
    nicePath = os.path.normpath(path).replace("\\", "/")
    return nicePath


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Initialize the script plug-in
def initializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "Jeremy Ernst", "1.0")
    status = mplugin.registerUI(makeMyCustomUI, removeMyCustomUI)

    # check for tools path
    epicTools()

    cmds.help(popupMode=True)
    return status


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Uninitialize the script plug-in
def uninitializePlugin(mobject):
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
