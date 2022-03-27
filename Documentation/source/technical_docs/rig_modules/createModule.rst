#################
Extending ARTv2
#################

.. topic:: Overview

    This page details the steps in creating your own module derived from the base class. The sections are presented in
    the order you should write your module.

    :Date: |today|
    :Author: **Jeremy Ernst**


.. contents::
    :depth: 3


IDE and Style Guide
###################

The preferred IDE for developing ARTv2 modules is `PyCharm <https://www.jetbrains.com/pycharm/>`_,
since we can specify our code style and inspections in the settings.
Below are the settings used for code style and inspections to set in PyCharm.

To access the settings in PyCharm, go to File -> Settings (or hit Ctrl+Alt+s). On the left, find Editor, then Code
Style.


.. image:: /images/pyCharm_codeStyle_0.png

Now, go to the Python section under Code Style. These are the settings for each of those tabs:


.. image:: /images/pyCharm_codeStyle_1.png

.. image:: /images/pyCharm_codeStyle_2.png


For Inspections, browse in the settings to Editor -> Inspections. There are two sections in here we will edit:
General and Python.

For General, items that have changed are denoted in blue text:

.. image:: /images/pyCharm_inspections_0.png

For Python, items that have changed are denoted in blue text:

.. image:: /images/pyCharm_inspections_1.png



Creating a Custom Module
#######################

Create an Icon
**************

To begin creating a module, the very first thing you'll want to do is create the icon for the module so it shows up
in the UI. To do so, browse to ARTv2/Core/Icons/System and open moduleIcons.psd in Photoshop. Every module needs two
icons: the standard icon and the hover-state icon. The photoshop file is setup to easily accommodate this.

Standard icon for the Torso module:

.. image:: /images/torso.png

Hover icon for the Torso module:

.. image:: /images/hover_torso.png

Your icons will be saved as a png in ARTv2/Core/Icons/Modules. The syntax is moduleName.png and hover_moduleName.png.


Create the Python File
***********************

In the ARTv2/Core/Scripts/Modules folder, add a new python file for your module following the existing naming
conventions (ART_moduleName.py)

To get started on the class, open ART_Head.py and copy from the docstring down to right before the class definition.
This will save time instead of having to write all this from scratch. If you have any new file attributes, update the
docstring with that information. Most likely, the import statements won't need to change, so let's skip down to the
file attributes and redefine these for our module.

.. image:: /images/fileAttrs.png

File Attributes:

.. code-block:: rest

    *icon: relative path to the standard icon we created ("Modules/moduleName.png").

    *search: search terms, separated by a ":", that you want your module to be found by ("joint:leaf").

    *className: the name of the module class, following the naming conventions ("ART_Head").

    *jointMover: the relative path to the joint mover file (Hasn't been created yet, we'll come back to this).

    *baseName: when a module is created, the user can specify a prefix and suffix which wrap the base name.
     For example, if our baseName is "head", the module name will be ("optionalPrefix") + "head" + ("optionalSuffix").

    *rigs: a list of the rigs this module will build (for example, ["FK::IK"]).

    *fbxImport: a list of the available options when import motion onto the rig from an FBX,
     (for example, ["None", "FK", "IK", "Both"]). "None" should always be an option.

    *matchData: if the module has more than one rig type, you may want to add the ability to match between rig types.
      This attribute allows you to specify whether or not the module can match (first argument in list) and if so,
      what are the match options (a list of strings). For example: [True, ["Match FK to IK", "Match IK to FK"] ].
      If you do not want your module to have the ability to match, you would simply have [False, None]

    *controlTypes: this will make sense much later, but this is a list of the attributes you will create on the
      network node that hold your different rig controls, and a label for what type of control those attributes
      contain. For example: [["fkControls", "FK"]] means that on the module network node, there is an attribute called
      fkControls that holds a list of the rig controls, and those controls are of type FK. This is used by the select
      controls tool (ART_SelectControlsUI.py).

At this point, your file should look something like this:

.. image:: /images/yourModule_1.png

If at this point, you were to launch the Rig Creator under the ART 2.0 menu, you should see your module now in the
module list (just don't click on it yet!)


Defining the Module Class
*************************

**Steps**:

    #. Update docstring.
    #. Update base class init arguments.

.. code-block:: rest

    Once again, it's probably easiest to just open a module like ART_Head.py and copy the class definition and the
    "__init__". All modules should inherit from ART_RigModule as there is a ton of functionality in there that you'll
    get for free. This guide assumes you will be inheriting from ART_RigModule.

.. image:: /images/headModule.png

|
.. code-block:: rest

    All you really need to change here is any docstring info, and the call to the base class "__init__", replacing
    the first two arguments with your module's information. Those first two arguments are: moduleName and moduleType.
    The moduleType is the same string you defined for your className at the top of the file. The moduleName is the name
    the network node will be given on creation. (For example: "ART_Head_Module", "ART_Head"). The network node will
    store all our module's attributes and connections. Maya will automatically add a number to the end of the moduleName
    if a node of the same name already exists, which is what we want. Usually, the syntax for the moduleName is
    simply the moduleType + "_Module".


Add Attributes
**************

**Steps**:

    #. Add Created_Bones attribute and set its default value
    #. Add baseName attribute and set its value to baseName (var)
    #. Add canAim attribute and set its value depending on whether you want
       your module to be able to have "aim mode" functionality.
    #. Add aimMode attribute and set its default value to False.
       (This is whether or not the module is currently in aimMode.)
    #. Add any additional attributes your module will need.

.. code-block:: rest

    The next function we need to implement will add any attributes we need to our module's network node.
    These are things like: can this module aim? how many spine joints? etc.

    The base class handles the creation of the network node, so if you were to launch the Rig Creator, and add your
    module, there would be a network node in the scene with your defined moduleName. There are some generic attributes
    that are always added by the base class, but this function will add attributes we want to track for our module.

If you were to try and create your module now, you would still get errors, but a network node with your defined attrs
should be created:

    .. image:: /images/networkNode_attrs.png



There are four attributes you must add for your module, as the tools will be looking for them.

.. image:: /images/addAttrs.png

.. code-block:: rest

    For Created_Bones, you will set the value to be whatever your default joint mover configuration will be:
    "joint_01::joint_02::joint_03::" (ART_Chain). Since we haven't built our joint mover yet, this may change,
    but know that you'll need to revisit this attribute so the default value is equal to your default joint mover
    configuration.

    baseName is pretty self-explanatory. For canAim, if you want this module to have "aim mode" functionality, set this
    to True. You can leave aimMode set to False by default regardless.

    Any additional attributes you know you'll need, you'll want to add them in this function. This is anything that your
    settings UI will have options for, like number of toes, or number of neck joints, etc.

Skeleton Settings UI
********************

**Steps**:

    #. Call on base class method to get basic structure
    #. Add Mirror Module info (if applicable)
    #. Add Current Parent info (Always)
    #. Add Change Name and Change Parent buttons (Always)
    #. Add Mirror Module button (if applicable)
    #. Add Bake Offsets button (Always)
    #. Add any custom widgets needed for your module.

.. code-block:: rest

    It's best to reference another module's implementation when writing this function. You'll likely be able to
    copy/paste quite a bit from another module for steps 1-6. If you're writing a module that does not support
    mirroring, open up ART_Head to copy/paste from for those first six steps. If your module can mirror, open
    up ART_Leaf.

.. image:: /images/skelSettings_chain.png

Open up ART_Chain.py and look at skeletonSettings_UI to view the code that created the above interface in the image.

.. image:: /images/skelSettings.png


Building the Joint Mover
************************

**Steps**:

    1. Build the joint mover geometry in a similar style to the existing joint movers.
    2. Create the global mover curve object and color it yellow. *(".overrideColor", 17)*
    3. Create the offset mover curve object (usually duplicate the global, and scale down) and color it light blue.
       *(".overrideColor", 18)*
    4. Create the geometry mover curve object (usually duplicate the offset, and scale down) and color it light pink.
       *(".overrideColor", 20)*
    5. Name the joint mover curve objects according to the naming convention (list below)
    6. Create a group node for each global mover that is in the same space as the mover control. Name these according to
       the naming convention.
    7. Create the LRA node (pull from an existing file, making sure material names are unaffected) and the LRA group.
    8. Setup the hierarchy of movers.
    9. Set geometry to referenced, check naming, check materials, finalize hierarchy.


The next step is to create the joint mover. There are a few basic rules when creating a joint mover for a module.
It's best to look at an existing joint mover file to review how they're setup.
When building the joint mover, try to adhere to the aesthetic that has been defined by the existing joint movers. The
first step is to build the mesh that will be our proxy geometry.

    .. code-block:: rest

           The geometry has a style to it that also uses two materials that you can see from an existing file.
           proxy_shader_black and proxy_shader_tan. Your geometry should also use those material names with those exact
           colors. It may be easiest to open an existing file and copy/paste the materials into your current working
           file. Make sure to also follow the naming convention for the geometry.

           In this example, I am building the chain module. For now, I will completely build out one link of the
           chain and deal with the other links later.

    .. image:: /images/proxy_geo.png

After we have our geometry built with the correct naming and the materials assigned with the correct names and
colors, the next step is to build the global mover curve object. This can be as simple or complex as you want. In the
chain module, I'll just use a simple circle.

    .. code-block:: rest

            As noted in the steps, the global mover has to be a specific color. You can achieve this with selecting
            the object and simply running:
                cmds.setAttr(cmds.ls(sl = True)[0] + ".overrideEnabled", True)
                cmds.setAttr(cmds.ls(sl = True)[0] + ".overrideColor", 17)
            Also, the naming convention is controlName + "_mover", so for this link of the chain, it will be
            "chain_01_mover".
            One important thing I should note is that you should make sure your pivot on the control is where you
            want it! For this chain control, the pivot will actually be at the origin, right at the head of the chain.

    .. image:: /images/global_mover.png

Now we need to create the offset mover, which is simply as easy as duplicating our global mover and scaling the CVs in.

    .. code-block:: rest

            As noted in the steps, the offset mover has to be a specific color. You can achieve this with selecting
            the object and simply running:
                cmds.setAttr(cmds.ls(sl = True)[0] + ".overrideEnabled", True)
                cmds.setAttr(cmds.ls(sl = True)[0] + ".overrideColor", 18)
            Also, the naming convention is controlName + "_mover_offset", so for this link of the chain, it will be
            "chain_01_mover_offset".

    .. image:: /images/offset_mover.png

The last mover control is for the proxy geo itself, so the user can move, rotate, and scale the proxy geo itself,
which doesn't actually affect the joint position at all, it's just for aesthetics. Again, duplicate the offset mover
and scale the CVs in to quickly create this mover.

    .. code-block:: rest

            As noted in the steps, the geo mover has to be a specific color. You can achieve this with selecting
            the object and simply running:
                cmds.setAttr(cmds.ls(sl = True)[0] + ".overrideEnabled", True)
                cmds.setAttr(cmds.ls(sl = True)[0] + ".overrideColor", 20)
            Also, the naming convention is controlName + "_mover_geo", so for this link of the chain, it will be
            "chain_01_mover_geo".

    .. image:: /images/geo_mover.png

Now we can setup the hierarchy of our movers. For the global mover, create an empty group that is in the same space as
the global mover control. This can be achieved by creating an empty group, point and orient constraining the group to
the global mover, and deleting the constraints. The name of the group will be controlName + "_mover_grp". At this
point, make sure that the orientation of your group is what you want your control to be. For instance, if you want
rotateX to be your twist axis, make sure to adjust the group orientation to address this. For this chain control, I
wanted Z to be my pitch axis, Y to be my yaw axis, and X to be my roll axis, so I needed to adjust the rotate values
until this was the case.

    .. image:: /images/mover_group.png

Now that the group orientation is as desired, go ahead and parent the global mover to the global mover group. Then
parent the offset mover to the global mover. Then parent the geo mover to the offset mover, and lastly, parent the
proxy_geo to the geo mover. Your hierarchy should look like this:

    .. image:: /images/mover_hierarchy.png

Select the global mover (not the mover group) and freeze transforms on translate, rotate, and scale. Now our movers
have the correct orientation that we want and we can move onto the next step.

    .. image:: /images/mover_hierarchy.gif

The next step for the joint mover is to add the LRA control (local rotation axis) to display the orientation of the
"joint". To do this, I usually will open another joint mover file, and copy an existing LRA control, and then go back
to this scene and paste it, like so:

    .. image:: /images/lra_control.gif

We'll need to unlock the translate and rotate channels on the LRA control (using the channel control) in order to be
able to properly set the space of the control for the next step. Now you can point/orient constrain the lra to the
global mover control and delete the constraints. The display of the LRA should match the true orientation of the
global mover.

    .. image:: /images/lra_control2.gif

Just like the global mover, we need to create a group node for the LRA control. The naming for the LRA control is
controlName_lra, while the group will be controlName_lra_grp. Point/orient constrain the newly created group to the
LRA control and remove the constraints. Name the group correctly, then parent the LRA under the group. The group will
be parented under the offset control, so that your hierarchy looks like this:

    .. image:: /images/lra_hierarchy.png

Real quick, since we copy/pasted our LRA control into this scene, let's make sure the materials are still named
correctly. As you can see, they have "pasted__" in the name, so let's remove those prefixes from the materials before
continuing.

    .. image:: /images/lra_mats.png

We also need to lock down the LRA control's translate and rotate channels again, as we don't want the user to be able
to directly manipulate this control, as it is just for visualization.
|
|
|
|
For each joint in your module, you would need to repeat all of these steps. Each joint's "mover" group would then get
parented under its parent's global mover. For the chain module, if the joint mover had 3 links in the chain, this is
what that would look like:

    .. image:: /images/chain_module_hierarchy.png

Another thing we need to do real quick is set our proxy geo and LRA geo to be referenced by enabling overrideEnabled
and setting the display type to reference. You can use this script to easily achieve this:

.. code-block:: python

    #select a piece of geometry, then run this to set that geometry to be referenced.
    cmds.setAttr(cmds.ls(sl = True)[0] + ".overrideEnabled", True)
    cmds.setAttr(cmds.ls(sl = True)[0] + ".overrideDisplayType", 2)

Lastly, we need to add a mover_grp as the very top group node to our joint mover. Simply create an empty group, name
it mover_grp, and parent your top-most global mover group underneath. It should look like this:

    .. image:: /images/mover_grp.png

This concludes the basic guideline to creating a joint mover for your module. Definitely take a look at existing
joint mover files and their applyModuleChanges functions to see how other modules are set up.



Add Joint Movers to Outliner
****************************

The function you will need to implement in your module class to get your joint movers showing up in the outliner, is
addJointMoverToOutliner. The chain module actually was probably the most complicated, as the range of joints you can
add is 2 to 99, so being able to dynamically add onto the joint mover and have it update in the outliner properly was
tricky. The main gist though is that you get the top level index of the outliner widget:

.. code-block:: python

    index = self.rigUiInst.treeWidget.topLevelItemCount()

Then, you want to add a top level item to the outliner for your module that doesn't represent a given joint mover, but
rather a 'folder' for your module joint movers.

.. code-block:: python

    # Add the module to the tree widget in the outliner tab of the rig creator UI
    self.outlinerWidgets[self.name + "_treeModule"] = QtWidgets.QTreeWidgetItem(self.rigUiInst.treeWidget)
    self.rigUiInst.treeWidget.topLevelItem(index).setText(0, self.name)
    foreground = QtGui.QBrush(QtGui.QColor(255, 255, 255))
    self.outlinerWidgets[self.name + "_treeModule"].setForeground(0, foreground)

Breaking down each line, the first line is adding an entry to our self.outlinerWidgets dictionary that contains a
QTreeWidgetItem, with the parent being the outliner tree widget. The second line is setting the text of that
QTreeWidgetItem to the module name. The third line is simply setting a color, that the fourth line then sets as the
foreground.

After your top-most item is added, it's time to start adding your joint movers. The process is similar to the above,
whereas you will create a new QTreeWidgetItem, give it the name of your joint mover, and give it a parent from the
self.outlinerWidgets dictionary of your choosing.

.. code-block:: python

    self.outlinerWidgets[yourJointName] = QtWidgets.QTreeWidgetItem(theParentTreeWidgetItemYouWant)
    self.outlinerWidgets[yourJointName].setText(yourJointNamex)

Then there are three functions in the base class you can use to add buttons next to the joint mover entry in the
outliner, as seen here:

    .. image:: /images/outlinerButtons.png

These functions are:

.. code-block:: python

    self.createGlobalMoverButton(yourJointName, self.outlinerWidgets[yourJointName], self.rigUiInst)
    self.createOffsetMoverButton(yourJointName, self.outlinerWidgets[yourJointName], self.rigUiInst)
    self.createMeshMoverButton(yourJointName, self.outlinerWidgets[yourJointName], self.rigUiInst)

You do not need to create a button for all 3 mover types if you do not want to. There are some movers, like the root,
that doesn't have a mesh mover. That covers adding the joint movers to the outliner, initially at least. We'll need to
implement a way to update the outliner when the module settings change, and different joint movers need to be added or
removed. Before doing that, the next step I recommend is implementing self.applyModuleChanges, which gets called when
changes to the module have been made via the skeleton settings UI.




Toggle Button State
*******************

This simple function enables or disables the Apply Changes button. It gets called on by whatever spin box, check box,
or other skeleton settings UI element you want, that needs to have those changes applied.

.. code-block:: python

    self.numJoints.valueChanged.connect(self.toggleButtonState)

The function is very simple (and really should be in the base class, but the apply button is currently created in each
rig module, and the base class doesn't know about the apply button.)

.. code-block:: python

    state = self.applyButton.isEnabled()
    if state == False:
        self.applyButton.setEnabled(True)




Apply Module Changes
********************

The purpose of this function is to update the joint movers based on new settings in the skeleton settings UI. In the
case of the chain module, this means the number of joints in the chain has increased or decreased, and we need to update
the scene to reflect that. Other modules mean doing different things, like deleting the joint mover and importing a new
one (in the case of changing the leg or arm side, etc).

There is a checklist of sorts though. You should make sure you hit all of these things in your implementation.

**Steps**:

    1. First, you should check for any dependencies your module may have, like if there are any modules whose parent is
       this module. use self.checkForDependencies() to get a list returned, and self.fixDependencies() to deal with them.
    2. Then, take care of any joint mover changes in the scene. Reference other implementations of this method to see
       how other modules handle this.
    3. Update any attribute values on the module's network node to reflect the new changes in the UI.
    4. If the number of joints have changed, you will need to rebuild the string for the Created_Bones attribute.
        .. code-block:: python

            attrString = ""
            for bone in createdJoints:
                attrString += bone + "::"
            cmds.setAttr(networkNode + ".Created_Bones", lock=False)
            cmds.setAttr(networkNode + ".Created_Bones", attrString, type="string", lock=True)
    5. Reset the apply changes button to be disabled.
    6. Update the outliner (will cover next) and update the bone count. Update bone count is in base class and just
       needs to be called.

Here is the full method implementation for the chain module:

.. code-block:: python

    def applyModuleChanges(self, moduleInst):
        networkNode = self.returnNetworkNode

        # get prefix/suffix
        name = self.groupBox.title()
        prefix = name.partition(baseName)[0]
        suffix = name.partition(baseName)[2]

        if len(prefix) > 0:
            if prefix.find("_") == -1:
                prefix = prefix + "_"
        if len(suffix) > 0:
            if suffix.find("_") == -1:
                suffix = "_" + suffix

        # create list of the new created bones
        createdJoints = []

        # get current number of chain joints value
        currentNum = int(cmds.getAttr(networkNode + ".numJoints"))

        # get new number of chain joints value
        newNumJoints = self.numJoints.value()

        if newNumJoints != currentNum:
            # look for any attached modules
            attachedModules = self.checkForDependencies()
            if len(attachedModules) > 0:
                self.fixDependencies(attachedModules)

        if newNumJoints > currentNum:
            # add more chain segments
            for i in range((newNumJoints - currentNum)):
                self.addChainSegment(True)

        if newNumJoints < currentNum:
            # remove chain segments
            for i in range((currentNum - newNumJoints)):
                self.removeChainSegment()

        # update numJoints value
        cmds.setAttr(networkNode + ".numJoints", lock=False)
        cmds.setAttr(networkNode + ".numJoints", newNumJoints, lock=True)

        # build attrString
        for i in range(newNumJoints):
            if i < 9:
                createdJoints.append(prefix + "chain_0" + str(i + 1) + suffix)
            else:
                createdJoints.append(prefix + "chain_" + str(i + 1) + suffix)

        attrString = ""
        for bone in createdJoints:
            attrString += bone + "::"

        cmds.setAttr(networkNode + ".Created_Bones", lock=False)
        cmds.setAttr(networkNode + ".Created_Bones", attrString, type="string", lock=True)

        # reset button
        self.applyButton.setEnabled(False)

        # update outliner
        self.updateOutliner(currentNum)
        self.updateBoneCount()

        # clear selection
        cmds.select(clear=True)




Updating Outliner
*****************

When settings change and the outliner needs to be updated to reflect the addition of new joint movers within a module or
the removal, self.updateOutliner() is used to make these changes.

The way the majority of modules are setup, during the addJointMoverToOutliner method, is that every possible joint mover
for that module is initially added, and if that joint isn't being used, the QTreeWidgetItem is hidden. For example, in
a hand, all of the fingers are added at creation, and if the metacarpals are not being used, those items in the outliner
just get hidden, as they are also hidden in the viewport.

The chain module was a bit different, as I didn't want to initially add 99 entries for every possible chain, so its
implementation was different, and is probably a special case.

Here is a typical implementation:

.. code-block:: python

   def updateOutliner(self):

        # whenever changes are made to the module settings, update the outliner to show the new or removed movers

        # PELVIS

        if not self.pelvisCB.isChecked():
            self.outlinerWidgets[self.originalName + "_pelvis"].setHidden(True)
        else:
            self.outlinerWidgets[self.originalName + "_pelvis"].setHidden(False)

        # SPINE
        numSpine = self.numSpine.value()
        if numSpine == 2:
            self.outlinerWidgets[self.originalName + "_spine_03"].setHidden(True)
            self.outlinerWidgets[self.originalName + "_spine_04"].setHidden(True)
            self.outlinerWidgets[self.originalName + "_spine_05"].setHidden(True)
        if numSpine == 3:
            self.outlinerWidgets[self.originalName + "_spine_03"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_spine_04"].setHidden(True)
            self.outlinerWidgets[self.originalName + "_spine_05"].setHidden(True)
        if numSpine == 4:
            self.outlinerWidgets[self.originalName + "_spine_03"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_spine_04"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_spine_05"].setHidden(True)
        if numSpine == 5:
            self.outlinerWidgets[self.originalName + "_spine_03"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_spine_04"].setHidden(False)
            self.outlinerWidgets[self.originalName + "_spine_05"].setHidden(False)

So what is happening here is just looking at the number of spine bones value as well as the 'include pelvis' value
and either showing or hiding the QTreeWidgets to match those settings. That's it! Call this at the end of your
applyModuleChanges function.




Updating Settings UI
********************

The one problem right now is that if you were to relaunch the UI, the settings displayed would be at their default
creation values. We need to have the UI read from the network node to fill the UI with the correct values.
This is done in a function called self.updateSettingsUI() and is called at the end of the skeletonSettingsUI method.

.. code-block:: python

    # Populate the settings UI based on the network node attributes
    self.updateSettingsUI()

The method itself is pretty simple. Get the attribute values off of a network node, and use those values to set
the UI values.

.. code-block:: python

    def updateSettingsUI(self):
        # this function will update the settings UI when the UI is launched based on the network node settings in the
        # scene
        networkNode = self.returnNetworkNode
        numJoints = cmds.getAttr(networkNode + ".numJoints")

        # update UI elements
        self.numJoints.setValue(numJoints)

        # apply changes
        self.applyButton.setEnabled(False)

In the case of the chain, there is only one value (as of writing this) to update in the UI, so this is a super simply
method.




Aim Mode Setup
**************

Whether or not you implement aim mode is up to you and the behavior you want for your module. Implementing this method
is very straight-forward. For the chain module, this is the implementation:

.. code-block:: python

    def aimMode_Setup(self, state):

        # get attributes needed
        name = self.groupBox.title()
        prefix = name.partition(baseName)[0]
        suffix = name.partition(baseName)[2]

        if len(prefix) > 0:
            if prefix.find("_") == -1:
                prefix = prefix + "_"
        if len(suffix) > 0:
            if suffix.find("_") == -1:
                suffix = "_" + suffix

        networkNode = self.returnNetworkNode
        numJoints = cmds.getAttr(networkNode + ".numJoints")

        # setup aim vector details per side
        aimVector = [1, 0, 0]
        aimUp = [0, 1, 0]

        # if passed in state is True:
        if state:

            # setup aim constraints
            for i in range(int(numJoints)):
                x = i + 2
                if i < 9:
                    mover = prefix + "chain_0" + str(i + 1) + suffix
                else:
                    mover = prefix + "chain_" + str(i + 1) + suffix
                if x < 9:
                    master = prefix + "chain_0" + str(x) + suffix
                else:
                    master = prefix + "chain_" + str(x) + suffix

                if cmds.objExists(master + "_lra"):
                    cmds.aimConstraint(master + "_lra", mover + "_mover_offset", aimVector=aimVector, upVector=aimUp,
                                       wut="objectrotation", wu=[0, 1, 0], worldUpObject=master + "_mover_end", mo=True)

        # if passed in state is False:
        if not state:
            cmds.select(name + "_mover_grp", hi=True)
            aimConstraints = cmds.ls(sl=True, exactType="aimConstraint")

            for constraint in aimConstraints:
                cmds.lockNode(constraint, lock=False)
                cmds.delete(constraint)

            self.bakeOffsets()
            cmds.select(clear=True)

If the passed in state is True, aim mode is setup. This happens automatically on module creation if the method has been
implemented. If the passed in state is False, all aim constraints are deleted. On the chain module, any time the
applyModuleChanges function is called, I first set aim mode to False, removing existing aim constraints, then set it to
True, at the very end of the applyModuleChanges method.


Pin Module
**********
Pin Module should be setup on every module, as it is highly likely that its functionality is desired. What it does, is
pins the module in place in 3D space so that the parent module no longer affects its position. It accomplishes this by
simply creating a space locator and matching the position and rotation of the top level group of the module, then
constraining said group to itself. The method also handles removing the pinning setup.

.. image:: /images/pinModules.png

There are two attributes that get added if they don't already exist, which are used to track the constraint node used
and the locator used for the pin operation. These attributes are message attributes that directly connect to those
nodes.

.. code-block:: python

    def pinModule(self, state):

        networkNode = self.returnNetworkNode
        topLevelMover = self.name + "_01_mover"

        # create a locator if state is true that will pin the module in place.
        if state:
            if cmds.getAttr(networkNode + ".pinned") is True:
                return
            loc = cmds.spaceLocator()[0]
            cmds.setAttr(loc + ".v", False, lock=True)
            constraint = cmds.parentConstraint(topLevelMover, loc)[0]
            cmds.delete(constraint)
            const = cmds.parentConstraint(loc, topLevelMover)[0]
            attrs = cmds.listAttr(topLevelMover, keyable=True)

            for attr in attrs:
                try:
                    cmds.setAttr(topLevelMover + "." + attr, keyable=False, lock=True)
                except Exception:
                    pass

            # add attributes to our network node that will allow us to track our constraint and locator for pinning.
            if not cmds.objExists(networkNode + ".pinConstraint"):
                cmds.addAttr(networkNode, ln="pinConstraint", keyable=True, at="message")
            if not cmds.objExists(networkNode + ".pinLocator"):
                cmds.addAttr(networkNode, ln="pinLocator", keyable=True, at="message")

            cmds.connectAttr(const + ".message", networkNode + ".pinConstraint")
            cmds.connectAttr(loc + ".message", networkNode + ".pinLocator")

        if not state:
            attrs = cmds.listAttr(topLevelMover, keyable=True)
            for attr in attrs:
                try:
                    cmds.setAttr(topLevelMover + "." + attr, lock=True)
                except Exception:
                    pass

            # delete the locator and constrint connected to the respective attributes to disable pinning.
            connections = cmds.listConnections(networkNode + ".pinConstraint")
            if connections is not None:
                for connection in connections:
                    cmds.delete(connection)
            connections = cmds.listConnections(networkNode + ".pinLocator")
            if connections is not None:
                for connection in connections:
                    cmds.delete(connection)

        cmds.select(clear=True)

If you are trying to unpin a module, the function simply lists the connections to those two message attributes and
deletes them.

Testing the Joint Mover
***********************

At this point, before you move further, the following functions should really be tested to make sure your module doesn't
need any special treatment.

**Test the Following**:

    1. Test copy/paste and reset settings on your module. This is found in the right click menu in the skeleton settings
       UI. The chain module needed some special attention here due to the addition of being able to change the proxy
       geometry and the control shapes.

       .. image:: /images/contextMenu.gif

    2. Test deleting your module, found in the right click menu in the skeleton settings UI.
    3. Test creating a mirror of your module if you've set it up to be able to mirror. If you need to do anything extra,
       there is a function you can use besides overriding called createMirrorModule_custom, which gets run after the
       base class function.
    4. Test mirroring transformations on your mirrored module. If you find the base class function isn't quite mirroring
       your transformations correctly, you can override it or do some stuff post by using mirrorTransformations_Custom.
       That method gets run after the base class mirror transformations and allows you to do any small tweaks to the
       mirroring you may need.
    5. Lastly, test templates. There is no reason they shouldn't work, but in case you're doing something unique in your
       module the templates currently don't account for, it's good to find that out now and address it before moving
       forward.

       .. image:: /images/templates.png

Skin Proxy Geo
**************

Rig Building
************

Control Picker
**************

Switch Modes
************

Import FBX
**********

Setting up Pickwalking
**********************



