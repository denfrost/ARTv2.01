#################
Deformation Phase
#################

    :Date: |today|
    :Author: **Jeremy Ernst**

.. attention:: This phase builds the deformation skeleton based on your module placement and is the time for you to get
                your initial smooth bind on your meshes.

When all of your modules are added and placed, you can proceed to the deformation phase by clicking on Finalize
Setup at the bottom of the Rig Creator interface.

Clicking on Finalize Setup will take you through a series of steps.


Skin Proxy Geometry
-------------------

The first thing it will ask is if you want the proxy geometry skinned. If you're using the proxy geometry to prototype
your character, and do not have a final mesh yet, you'll probably want to hit "Yes". If you already have a model you
plan on skinning, you could hit "No".

.. image:: /images/weightWizard.png

Skinning the proxy geometry is an automated process.


Add Custom Meshes
-----------------

If the tool finds that no meshes aside from the proxy geometry exists, it may ask you if you wanted to add those meshes
at this time (by bringing up an import dialog). This prompt was added to past confusion on when/how to add your own
meshes for skinning.

.. image:: /images/add_meshes.png

Import Weights
--------------

If the tool finds weight files that match the object names, you may see a prompt for importing those weights.

.. image:: /images/import_found_weights.png

This is incredibly useful when you want to go back to the previous phase and edit joint positions, add modules, or
change module settings after already skinning your asset. When you go forward again to finalize the the setup, you can
reimport all of your skinning.

Bind Skin
---------

If the tool finds custom meshes that either had no weight files, or importing them was skipped, you will be
asked if you would like to skin this custom geometry. If you choose Yes, you will be presented with a simple tool for
quickly getting skinClusters on your meshes.

.. image:: /images/add_skinning.png

.. note:: This process is no different than going to the Skin > Bind Skin > Smooth Bind menu in Maya.

.. figure:: /images/smooth_bind_tool.gif
    :width: 940px
    :height: 433px

    Adding a skinCluster to the belt geometry, using the selected joints in the list.

Deformation Toolkit
-------------------

Check out the :doc:`Deformation Toolkit <../deformationToolkit>` page to get in-depth documentation on each tool
included in that interface during this phase.