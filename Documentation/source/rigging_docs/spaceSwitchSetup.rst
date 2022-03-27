#########################
Setting up Control Spaces
#########################

    :Date: |today|
    :Author: **Jeremy Ernst**

***************
Creating Spaces
***************

To create a space, you must be in an unreferenced rig file (In the ARTv2 menu, choose Edit Rig and select the asset
to open that rig file without referencing).

There are two ways to access the tool for creating a space.

Using the ARTv2 Menu:
---------------------

    .. figure:: /images/create_space_menu.png
        :width: 488px
        :height: 318px

        Access the Create Space tool from the ARTv2 menu.

Using the Rig Creator UI:
-------------------------

    .. figure:: /images/create_space_creator.png
        :width: 554px
        :height: 296px

        Access the Create Space tool from the Rig Creator Interface.

How to Create a Space:
----------------------

    .. figure:: /images/space_switcher_create_ui.png
        :width: 351px
        :height: 206px

        Below are what each of the fields in the UI are for:

        +----------------+-----------------------------------------------------------------------------------------+
        | Field          | Description                                                                             |
        +================+=========================================================================================+
        | Control        | The control to create the space on. Use the add selection button or the picker list     |
        |                | button to add a control to the field.                                                   |
        +----------------+-----------------------------------------------------------------------------------------+
        | Space          | This is the object in the scene that represents the space. This could be another control|
        |                | or some object in the scene.                                                            |
        +----------------+-----------------------------------------------------------------------------------------+
        | Name           | This is the name of the space that is displayed to the animator.                        |
        +----------------+-----------------------------------------------------------------------------------------+
        | Type           | This is the type of constraint used when creating the space.                            |
        +----------------+-----------------------------------------------------------------------------------------+

To create a space, simply add a valid control to the control field using either the 'use selection' button or the
picker list. If you use the picker list, it will only display valid controls to pick from. If you use selection, and the
control is invalid, that information will be relayed.

Next, add an object that represents the space (usually another control). Then give the space a name. Finally, choose
the constraint type. For the majority of cases, this will be the default of "Translation and Rotation". That's it!

Demo:

    .. figure:: /images/create_space.gif
        :width: 582px
        :height: 525px

        In this example, a body space is being created on the left IK hand control using the default option of using
        both translation and rotation. Then, a body space is created on the FK head anim using only rotation, meaning
        the head control will only be oriented to the body control, but will still travel with the neck.


**********************
Creating Global Spaces
**********************

An even more efficient way to create spaces is to create global spaces. These are spaces that all controls will receive
(unless you specify controls to exclude). This is a very quick way to get your spaces setup. Furthermore, these global
space setups can be saved and loaded, saving even more time.

There again, are two ways to access this tool:

Using the ARTv2 Menu:
---------------------

    .. figure:: /images/create_global_space_menu.png
        :width: 488px
        :height: 318px

        Access the Create Global Spaces tool from the ARTv2 menu.


Using the Rig Creator UI:
-------------------------

    .. figure:: /images/create_global_space_creator.png
        :width: 554px
        :height: 296px

        Access the Create Global Spaces tool from the Rig Creator Interface.

To create a global space, first, click on the "Add Global Space" button to add an entry. Just like creating a normal
space, fill out the space name, and the space object. Optionally, add controls you want to exclude from getting the
global space.

    .. figure:: /images/create_global_space.gif
        :width: 399px
        :height: 526px

        Creating a global space and excluding some controls from receiving the global space.

You can right click on a global space to access a menu to remove the space.

    .. figure:: /images/remove_global_space.gif
        :width: 399px
        :height: 526px

        Remove a global space by right clicking on a space and choosing remove.

Lastly, the global space setup can be saved or loaded, which is useful for establishing standard setups for characters
on a project.

        +-----------------------------------+----------------------------------------------------------------------+
        | Icon                              | Description                                                          |
        +===================================+======================================================================+
        | .. image:: /images/icons/save.png | Save a template file of the global space setup.                      |
        +-----------------------------------+----------------------------------------------------------------------+
        | .. image:: /images/icons/load.png | Load a template file of a global space setup.                        |
        +-----------------------------------+----------------------------------------------------------------------+

****************
Renaming a Space
****************

To access the rename space tool, like the previous space tools, you can use either the ARTv2 menu or the rig creator
button.

    .. figure:: /images/rename_space.png
        :width: 488px
        :height: 318px

        Access the Rename Space tool from the ARTv2 menu.

    .. figure:: /images/rename_space_creator.png
        :width: 480px
        :height: 342px

        Access the Rename Space tool from the Rig Creator icon.

Renaming a space is pretty straight-forward. Select the control with the space you want to rename, choose the space you
want to rename, and supply a new name.

****************
Deleting a Space
****************

Deleting a space is just like renaming a space and the tool can be accessed from the same two locations: the menu or the
rig creator interface.

        +------------------------------------------------+-------------------------------------------------------------+
        | Icon                                           | Description                                                 |
        +================================================+=============================================================+
        | .. image:: /images/icons/edit_remove_space.png | Launches the "remove space" tool.                           |
        +------------------------------------------------+-------------------------------------------------------------+




*************************
Scripting Space Creation
*************************
You can also script space creation.
To do this, you will want to import the SpaceSwitcher module, and run the CreateSpace class, like this:

    .. code-block:: python

                    # create a space named left_hand for the weapon_jnt_anim control. The object that represents this
                    # space is the ik_hand_l_anim. Create this as a translation-only space.
                    import Tools.Animation.ART_SpaceSwitcher as space_switch
                    space_switch.CreateSpace("left_hand", "weapon_jnt_anim", "ik_hand_l_anim", "translation")

Let's break these four arguments down:

        +---------------------+---------+------------------------------------------------------------------------+
        | Positional Argument | Type    | Description                                                            |
        +=====================+=========+========================================================================+
        | space_name          | string  | The name for the space.                                                |
        +---------------------+---------+------------------------------------------------------------------------+
        | control             | string  | The name of the control to receive the space.                          |
        +---------------------+---------+------------------------------------------------------------------------+
        | space               | string  | The name of the object that represents the space.                      |
        +---------------------+---------+------------------------------------------------------------------------+
        | space_type          | string  | (optional) (default = parent) Type of constraint to use.               |
        +---------------------+---------+------------------------------------------------------------------------+

We can create another space for our weapon_jnt_anim, but this one will use the default constraint type of parent.

    .. code-block:: python

        space_switch.CreateSpace("r hand", "weapon_jnt_anim", "ik_hand_r_anim")

.. tip::
    It is best practice to put the code for setting up your space switching controls into the post-script of the build
    process. That way, whenever you build or rebuild the rig, your spaces get setup automatically.


Example post-script for setting up simple spaces:

    .. code-block:: python

        # setup some space-switching capabilities for the weapon control and the ik hand controls.
        import Tools.Animation.ART_SpaceSwitcher as space_switch
        space_switch.CreateSpace("l hand", "weapon_jnt_anim", "weapon_jnt_l_anim")
        space_switch.CreateSpace("r hand", "weapon_jnt_anim", "weapon_jnt_r_anim")

        space_switch.CreateSpace("body", "ik_hand_l_anim", "torso_body_anim")
        space_switch.CreateSpace("head", "ik_hand_l_anim", "fk_head_anim")

        space_switch.CreateSpace("body", "ik_hand_r_anim", "torso_body_anim")
        space_switch.CreateSpace("head", "ik_hand_r_anim", "fk_head_anim")





You can also script the creation of global spaces. However, this does take having used the UI at least once to save out
a template file. With a template file saved out though, you can add a singular call to your post-script to have the
global spaces created automatically during the build process.

    .. code-block:: python

        # Build global spaces based on a previously saved out template file.
        import Tools.Animation.ART_SpaceSwitcher as space_switch
        space_switch.CreateGlobalSpaces("C:/ARTv2/User/Global Space Templates/my_template.spaces")

