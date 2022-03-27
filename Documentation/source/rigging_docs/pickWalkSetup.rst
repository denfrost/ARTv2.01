###################
Custom Pick-Walking
###################

Setting up Pick-Walking
-----------------------

For learning about the pick-walking tools and how to setup pick-walking with the interface, see
:doc:`Custom Pick-Walking <../animation_docs/pickwalker>`


Scripting Pick-Walking Setup
----------------------------
Once you have a template file, you can script the pick-walk setup rather easily.

.. code-block:: python

    import Tools.Animation.ART_PickWalkSetup as pick_walk
    inst = pick_walk.ART_PickWalk("my_character", "C:\\test.pickWalk", False)

    # load a pick-walk template
    inst.load_template()

The arguments here are:

    +---------------------+---------+------------------------------------------------------------------------+
    | Keyword Argument    | Type    | Description                                                            |
    +=====================+=========+========================================================================+
    | character           | string  | The name of the character (or namespace if in a referenced file).      |
    +---------------------+---------+------------------------------------------------------------------------+
    | template_file       | string  | The file path of the template file to load or save.                    |
    +---------------------+---------+------------------------------------------------------------------------+
    | strip_namespace     | bool    | Whether or not to strip namespaces when loading a template.            |
    |                     |         | Valid only if the template was saved from a referenced rig.            |
    +---------------------+---------+------------------------------------------------------------------------+

.. tip:: Add a call to the load_template method in your post-script to always have pick-walking setup everytime a rig
         build is done!

.. seealso:: :doc:`ART_PickWalkSetup Technical Documentation <../technical_docs/animation/setupPickWalk>`


Pick-Walking Under-the-hood
---------------------------

When you setup pick-walking, what's happening under-the-hood is a series of attributes and connections being made that
work in tandem with the rig pick-walking hotkeys you can bind in the ARTv2 Hotkey Editor.

There are four possible attributes that can be added for pick-walking: pickWalkUp, pickWalkDown, pickWalkLeft, and
pickWalkRight. These attributes are message attributes that will connect to the control for pick-walking in the
direction.

Let's take a look at an fk_lowerarm_anim control in the attribute editor.

.. figure:: /images/pick_walk_attrs.png
    :width: 549px
    :height: 252px

    The attributes for pick-walking up and down showing their connections to the corresponding control.

As you can see, there are two attributes for pick-walking setup by default. Pick-walking up connects to our
fk_upperarm_anim control, and pick-walking down to the fk_hand_anim control.

If we take a look at one of the hotkey scripts for pick-walking, you can see that it get's the selection, checks if a
specific pickwalk attribute exists, and then gets te connections to that attribute. Once it has the control connected
to that attribute, it selects it.

.. code-block:: python

    selection = cmds.ls(sl=True)
    if len(selection) > 0:
        attrs = cmds.listAttr(selection[-1], ud=True)
        if attrs is not None:
            if "pickWalkUp" in attrs:
                connections = cmds.listConnections(selection[-1] + ".pickWalkUp")
                if connections is not None:
                    cmds.select(cmds.listConnections(selection[-1] + ".pickWalkUp")[0])
