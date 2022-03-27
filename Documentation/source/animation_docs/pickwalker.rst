###################
Custom Pick-Walking
###################

    :Date: |today|
    :Author: **Jeremy Ernst**

You can setup custom pick-walking between controls in your rig. To do this, open the Pick-Walking tool under the ARTv2
menu, found here:

.. image:: /images/pick_walk_menu.png


Pick-walk Interface Overview
----------------------------

.. image:: /images/pickWalkUI.png

.. figure:: /images/pick_walk_tools.png
    :width: 323px
    :height: 290px

    The left side of the UI features some tools for module control visibility and settings.

    +--------+-----------------------------------------------------------------------------------------+
    | Number | Description                                                                             |
    +========+=========================================================================================+
    | 1      | If you have multiple characters, choose which one whose modules you want to view here.  |
    +--------+-----------------------------------------------------------------------------------------+
    | 2      | List of modules for the character (#1)                                                  |
    +--------+-----------------------------------------------------------------------------------------+
    | 3      | With modules selected, you can use this to select the settings node for those modules.  |
    +--------+-----------------------------------------------------------------------------------------+
    | 4      | With modules selected, you can use this to hide the controls of those modules.          |
    +--------+-----------------------------------------------------------------------------------------+
    | 5      | With modules selected, you can use this to show the controls of those modules.          |
    +--------+-----------------------------------------------------------------------------------------+

.. figure:: /images/pick_walk_setup.png
    :width: 556px
    :height: 267px

    The right side of the UI contains the widgets used for creating the pick-walking relationships.

    +--------+-----------------------------------------------------------------------------------------+
    | Number | Description                                                                             |
    +========+=========================================================================================+
    | 1      | The source control. Select a control and click this button to load the selection as the |
    |        | source control. This is the control that you will be setting pick-walking up on.        |
    +--------+-----------------------------------------------------------------------------------------+
    | 2      | The pick-walk up object. With a selection, click this button to load that selection     |
    |        | as the pick-walk up object for the source control.                                      |
    +--------+-----------------------------------------------------------------------------------------+
    | 3      | The pick-walk down object. With a selection, click this button to load that selection   |
    |        | as the pick-walk down object for the source control.                                    |
    +--------+-----------------------------------------------------------------------------------------+
    | 4      | The pick-walk left object. With a selection, click this button to load that selection   |
    |        | as the pick-walk left object for the source control.                                    |
    +--------+-----------------------------------------------------------------------------------------+
    | 5      | The pick-walk right object. With a selection, click this button to load that selection  |
    |        | as the pick-walk right object for the source control.                                   |
    +--------+-----------------------------------------------------------------------------------------+

Setting up Pick-Walking
-----------------------

Select a control you want to set pick-walking up on, and click on the middle button. Controls get built with some amount
of pick-walking setup by default. If a control has any pick-walking setup already, you should see other button's text
change to the name of those pick-walk controls.

For example, if I load the fk_upperarm control, you will see the top and bottom buttons populate, showing you that if
you pick-walk up, you will move to the fk_clavicle control, and if you pick-walk down, you will move to the
fk_lowerarm_control.

.. figure:: /images/populate_pickwalk_source.gif
    :width: 1136px
    :height: 359px

    Loading the FK upperarm control, we can see the default pick-walk relationships that are setup.

To add or change a pick-walking relationship, select the control you want to pick-walk to, and then click on the button
that corresponds to that direction.

.. figure:: /images/populate_pickwalk_targets.gif
    :width: 1136px
    :height: 359px

    In this example, I want to have pick-walking down while the FK hand control is selected move to my IK hand control.
    I can also change an existing relationship in the same way. Here, I change the pick-walk right control to be the
    top pinky finger joint, and then add a pick-walk left for the top thumb joint.

.. note:: Setting up pick-walking up to another control does not automatically setup pick-walking for that control's
          opposite direction to go back to that original control. These assumptions are not made, and if you want
          that behavior, you must explicitly create it for both controls.


Saving and Loading Pick-Walk Templates
--------------------------------------

In the pick-walk interface, under the File menu, you will find the ability to save and load templates. Saving is rather
straight forward, but loading has some options to cover.

.. figure:: /images/load_pick_walk_template.png
    :width: 436px
    :height: 228px

    Load pick-walk template options.

    +--------+-----------------------------------------------------------------------------------------+
    | Number | Description                                                                             |
    +========+=========================================================================================+
    | 1      | The pickwalk file to load (*.pickWalk)                                                  |
    +--------+-----------------------------------------------------------------------------------------+
    | 2      | If the pickWalk file was saved out from a referenced rig, the file will have namespaces |
    |        | in it. If it does, check "Strip Namespaces" if you are loading them onto a different    |
    |        | character, or a character with no namespaces. Usually this will not be the case, and    |
    |        | this can be left unchecked.                                                             |
    +--------+-----------------------------------------------------------------------------------------+
    | 3      | The character you want to load the pickWalk template onto.                              |
    +--------+-----------------------------------------------------------------------------------------+


Using the Pick-Walking
----------------------

You will notice that by default, using Maya's built in pick-walk hotkeys do not recognize these relationships you've
setup. To actually use the pick-walking, you must use the ARTv2 Hotkey Editor, and assign keys to the rig pick-walking
functions.

Start by opening the Hotkey Editor:

.. image:: /images/hotkey_editor_menu.png

Navigate to the Rig Pick-Walking section, and then assign keys as you see fit. If you simply want to overwrite Maya's
pick-walking, just assign the arrow keys accordingly. If you want to preserve Maya's default pick-walking, you could add
a modifier, like CTRL, to the rig pick-walking.

.. image:: /images/pick_walk_hotkeys.png


.. note:: Append pick-walking is adding the pick-walked control to your current selection. For example, in a typical FK
          arm setup, if I append pick-walk down from the FK upperarm, instead of just selecting the FK lowerarm control,
          it will add that control to my selection, so that I have both the upperarm and lowerarm selected. This is very
          useful when dealing with chains, like fingers!



