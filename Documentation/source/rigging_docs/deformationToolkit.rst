###################
Deformation Toolkit
###################

    :Date: |today|
    :Author: **Jeremy Ernst**

.. note:: If you're only using the proxy geometry at this point, you can skip right ahead to "Publishing the Rig".

This section will go over the deformation toolkit interface and the tools it includes. Let's start with the toolbar at
the top of the interface.


.. figure:: /images/deformation_toolkit_toolbar.png
    :width: 551px
    :height: 56px

    Deformation Toolkit toolbar

    +-----------------------------------------------+------------------------------------------------------------------+
    | Icon                                          | Description                                                      |
    +===============================================+==================================================================+
    | .. image:: /images/icons/paintWeights.png     | Puts the tool into Paint Skin Weights mode.                      |
    +-----------------------------------------------+------------------------------------------------------------------+
    | .. image:: /images/icons/addRemove.png        | Launches the Add or Remove Influences tool.                      |
    +-----------------------------------------------+------------------------------------------------------------------+
    | .. image:: /images/icons/mirrorWeights.png    | Launches Maya's Mirror Skin Weights options.                     |
    +-----------------------------------------------+------------------------------------------------------------------+
    | .. image:: /images/icons/importSkin.png       | Launches the Import Skin Weights tool.                           |
    +-----------------------------------------------+------------------------------------------------------------------+
    | .. image:: /images/icons/exportSkin.png       | Launches the Export Skin Weights tool.                           |
    +-----------------------------------------------+------------------------------------------------------------------+
    | .. image:: /images/icons/smartCopy.png        | Smart Copy Skin Weights function.                                |
    +-----------------------------------------------+------------------------------------------------------------------+
    | .. image:: /images/icons/moveInfs.png         | Launches the Move Influences tool.                               |
    +-----------------------------------------------+------------------------------------------------------------------+
    | .. image:: /images/icons/fixWeights.png       | Fix Skin Weights function.                                       |
    +-----------------------------------------------+------------------------------------------------------------------+
    | .. image:: /images/icons/hammer.png           | Maya's Hammer Skin Weights function.                             |
    +-----------------------------------------------+------------------------------------------------------------------+
    | .. image:: /images/icons/wizard.png           | Launches the Weight Wizard tool (finalize setup wizard)          |
    +-----------------------------------------------+------------------------------------------------------------------+
    | .. image:: /images/icons/bindTool.png         | Launches only the Bind Skin portion of the Weight Wizard tool.   |
    +-----------------------------------------------+------------------------------------------------------------------+
    | .. image:: /images/icons/rename.png           | Launches the Override Joint Names tool, for renaming joints.     |
    +-----------------------------------------------+------------------------------------------------------------------+

Paint Skin Weights Mode
-----------------------

With a mesh selected, click on the Paint Skin Weight mode button to enter the paint skin weights tool. You will see what
is essentially a re-skinned version of Maya's paint skin weights tool. The main difference is the influence list.

The influence list is broken into two sections: modules and bones within selected modules. This allows you to filter
the list of bones you see to reduce clutter.

.. figure:: /images/influence_list.gif
    :width: 489px
    :height: 329px

    By selecting different modules in the left list, I can filter what bones I see in the right list.

There are also search bars at the tops of each list for narrowing down things even more. The search bar above the module
list supports multiple search terms, separated by a comma:

.. image:: /images/influence_list_search.gif

To exit paint weights mode, switch to a different tool, like the move, rotate, or select tool.


Add or Remove Influences Tool
-----------------------------

With a mesh selected, you can use this tool to, well, add or remove influences.

.. figure:: /images/add_remove_influences.gif
    :width: 300
    :height: 480

    In this example, I remove a bunch of finger bones from the selected mesh, then add the root influence to the
    skinCluster.

As you can see in the interface, there are also options for removing unused influences and pruning weights.


Import Skin Weights Tool
------------------------


Export Skin Weights Tool
------------------------

Smart Copy Weights
------------------

Move Influences Tool
--------------------

Fix Weights
-----------

Weight Wizard
-------------

Bind Skin Tool
--------------

Override Joint Names Tool
-------------------------

