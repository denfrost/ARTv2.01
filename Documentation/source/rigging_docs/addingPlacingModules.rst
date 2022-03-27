##########################
Adding and Placing Modules
##########################

    :Date: |today|
    :Author: **Jeremy Ernst**

When you first launch the Rig Creator, two things will happen. A UI will appear and there will be a control object in
your viewport. This control object is the root module of the rig, and every rig needs to have this, so it is
automatically created. During this phase, you will be adding modules to define your character, as well as placing them.


See :doc:`Rig Creation Tools <../rigCreationTools>` to get a more in-depth explanation of the tools of the Rig Creator.


Adding a Module
----------------

To add a module, click on the desired module button in the "Rig Modules" section.

.. image:: /images/rig_modules.gif

This will bring up a new dialog for settings the parent bone of this module, as well as giving the module an optional
prefix and/or suffix. Some modules, like the arms and legs, have additional options.

.. figure:: /images/addModule.png
    :width: 553px
    :height: 410px

    The Add Module UI.

    +-------+----------------------------------------------------------------------+
    | #     | Description                                                          |
    +=======+======================================================================+
    | 1     | optional: adds a prefix to the module                                |
    +-------+----------------------------------------------------------------------+
    | 2     | optional: adds a suffix to the module                                |
    +-------+----------------------------------------------------------------------+
    | 3     | preview of the module name                                           |
    +-------+----------------------------------------------------------------------+
    | 4     | Extra options that may appear for certain modules.                   |
    +-------+----------------------------------------------------------------------+
    | 5     | Create button: Adds the module with the current settings.            |
    +-------+----------------------------------------------------------------------+
    | 6     | Search for a particular joint in the list of potential parent joints.|
    +-------+----------------------------------------------------------------------+
    | 7     | List of all potential parent joints based off installed modules.     |
    +-------+----------------------------------------------------------------------+

Once you have the information filled out, add the module by clicking "Create".

.. note:: You can change these settings in the "Installed Modules" section of the UI at any time.


Placing a Module
----------------

As soon as a module has been added, nodes will be added to the scene, and a widget will be added to the UI under the
"Installed Modules" section. Each module comes with a simple rig, which will be referred to as Joint Movers. Each module
also comes with proxy geometry, which can be used for quickly prototyping characters without having a model.

There are two types of joint movers: **Global** and **Offset**. What you see when you first add a module, are the
global movers. These are the yellow controls.

**Global movers** act like normal FK. Manipulating one will also affect any children of that "joint".

.. note:: At this stage, there are not any actual joints, just representations. The skeleton gets built after this
          phase.

.. image:: /images/global_movers.gif

Global movers can be translated, rotated, and scaled. Scaling is the fastest way to change the bone lengths, rather than
trying to translate each global mover.

**Offset movers** are the light blue controls, and can be viewed by toggling their visibility in the toolbar.

.. figure:: /images/toggle_offset.gif
    :width: 546px
    :height: 51px

    Visibility Toggles on the Rig Creator toolbar.

    +------------------------------------+-----------------------------------------+
    | Icon                               | Description                             |
    +====================================+=========================================+
    | .. image:: /images/globalMover.png | Global Mover visibility toggle          |
    +------------------------------------+-----------------------------------------+
    | .. image:: /images/offsetMover.png | Offset Mover visibility toggle          |
    +------------------------------------+-----------------------------------------+
    | .. image:: /images/meshMover.png   | Mesh Mover visibility toggle            |
    +------------------------------------+-----------------------------------------+

Offset movers only affect their joint. No children of that joint are affected. Offset movers are good for fine-tuning a
joint's position. I usually get my global movers roughed in first, then use offset movers to finesse the position of the
joint.

.. image:: /images/offset_movers.gif

.. note:: If "Aim Mode" is on, which it is by default, moving an offset mover will orient the parent so that it stays
          aligned properly. See :doc:`Rig Creation Tools <../rigCreationTools>` to learn more about aim mode.

There is a third type of mover, but it does not affect joints. The pink controls are called **Mesh Movers**, and only
affect the proxy geometry. These can be used to thin or thicken a proxy mesh to better represent the character ( as
well as be re-positioned if needed). These are found by toggling their visibility on the toolbar.

.. image:: /images/mesh_movers.gif

.. seealso:: :doc:`Rig Creation Tools <../rigCreationTools>` to learn about tools that help with module placement.


Editing a Module's Settings
---------------------------

Whenever a module is added, a widget for that module will appear in the UI, which can be used to change any settings the
module has. This includes changing what the parent joint is, as well as changing the module name. Some modules, like
the arm, have many settings that can be adjusted.

.. figure:: /images/module_settings.gif
    :width: 371px
    :height: 346px

    Click on the arrow at the top left to expand that module's widget, and begin editing settings.

Some settings will not take effect until you click on "Apply Settings". These are usually settings that add or remove
joints in the module.

.. image:: /images/apply_changes.gif

.. note:: The right-click context menu on the settings widget has options for copying, pasting, and resetting settings
          as well.

Mirroring a Module
------------------

The easiest way to mirror a module is by right clicking on the module's settings widget, and choosing "Create Mirror
of this Module".

.. image:: /images/mirror_a_module.png

This will bring up a dialog to add a prefix and suffix to the new module, and then automatically create the module with
the same settings as the source, and mirror transformations over. It will also figure out the correct parent bone for
the mirrored module.

.. image:: /images/mirroring_module.gif

When a module is mirrored, a link is made between the two modules. This allows the system to know that these modules can
mirror transformations. You will also note that the mirror module is specified in the settings widget:

.. image:: /images/mirror_module_widget.png

When two modules are linked as mirrors, a new right-click option is available. You can right click on a module to mirror
its transformations over to its mirror module.

.. image:: /images/mirror_transformations_menu.png

You can also create a module as normal, and manually specify the mirror module, by using the settings widget.

.. figure:: /images/mirror_module_manual.png
    :width: 341px
    :height: 135px

    Click on the "Mirror Module" button to specify a mirror for this module.


Duplicating a Module
--------------------

To duplicate a module, right click on the module's settings widget, and choose "Duplicate this Module":

.. image:: /images/duplicate_module.png

This is very useful when using chain or joint modules.

.. figure:: /images/duplicating_example.gif
    :width: 1307px
    :height: 675px

    In this example, I've created a joint for one of the pouches. I then duplicate that module to quickly place the
    next joint for the pouch. If I wanted to mirror these pouches to the other side, I could then create mirrors from
    the duplicates.

Deleting a Module
-----------------

To delete a module, right click on the module's settings widget, and choose "Delete Module".

.. image:: /images/delete_module.png

.. note:: If there were modules parented under a bone within the deleted module, they will be reparented to the root.

Physique Editor
---------------

If using the proxy geometry to prototype characters is something you wish to do, there is a tool called the Physique
Editor that can alter the proxy geometry to better fit the type of character you're building.

This tool can be found under the menu bar, under the Tools menu:

.. image:: /images/physique_editor_menu.png

See :doc:`Rig Creation Tools <../rigCreationTools>` to learn more about the Physique Editor.
