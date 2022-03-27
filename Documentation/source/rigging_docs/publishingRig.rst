##################
Publishing the Rig
##################

    :Date: |today|
    :Author: **Jeremy Ernst**

Once you have the deformations in a good enough place and are ready to actually build the rig, click on the "Build Rig"
button at the bottom of the deformation tools UI.

.. image:: /images/build_rig_button.png

This will launch a wizard that will take you through the publishing process. The first page just summarizes the steps
that the wizard will take you through.

.. figure:: /images/publish_rig_01.png
    :width: 605px
    :height: 433px

    The first page of the publish wizard just explains the steps the wizard will go through.


Asset Name and Location
-----------------------
Once you click continue, you will then need to give your asset a name and specify a location in the ARTv2 Projects
directory.

.. note:: The projects directory can be specified in the ARTv2 Settings.

          .. image:: /images/settings.png

Let's breakdown this page's elements:

.. figure:: /images/publish_rig_02.png
    :width: 605px
    :height: 433px

    On this page, you will give your asset a name and a location in the projects directory. You can also add a script
    to be run before the rig build (pre-script) and a script to be run after the rig build (post-script).

    +--------+------------------------------------------------------------------------------------------------+
    | Number |                                    Description                                                 |
    +========+================================================================================================+
    |   1    | Directory tree of the existing projects and their sub-folders in the ARTv2 projects directory. |
    +--------+------------------------------------------------------------------------------------------------+
    |   2    | Buttons to add a new project or new sub-folders to an existing project.                        |
    +--------+------------------------------------------------------------------------------------------------+
    |   3    | Preview of the relative path of the asset. In this example, the asset is being published to    |
    |        | the "Test" project.                                                                            |
    +--------+------------------------------------------------------------------------------------------------+
    |   4    | The name given to the asset. In this example, that will be "pirate".                           |
    +--------+------------------------------------------------------------------------------------------------+
    |   5    | If this asset is being re-published/re-built, you will see this section, which allows you to   |
    |        | add some information regarding the change. You will not see this if this is the first publish. |
    +--------+------------------------------------------------------------------------------------------------+
    |   6    | Add optional pre or post scripts to run either before or after the rig build. Can be mel or    |
    |        | python.                                                                                        |
    +--------+------------------------------------------------------------------------------------------------+
    |   7    | Continue to the next step of publishing the rig.                                               |
    +--------+------------------------------------------------------------------------------------------------+

Rig Pose
--------
The purpose of this next page is to be able to change the pose the rig is built in, if the pose the model is currently
in, is not the most ideal. For example, most models I work with tend to be in an "A" pose, but most of the animators
I work with prefer the rig, especially when IK controls are involved, to be in a "T" pose. This page allows you to
change the pose into a pose that is preferable for rigging.

.. image:: /images/publish_rig_03.png

.. note:: If you're re-publishing a rig, you may see the following dialog, which will restore your previous rig pose
          if you choose.

          .. image:: /images/restore_rig_pose.png

In most cases, you can just select the arms and legs in the left list, and slide the slider at the top to the T-Pose.

.. figure:: /images/rig_pose_01.gif
    :width: 1086px
    :height: 427px

    Using the global slider to set the rig pose of the left arm to a "T" pose.

What the sliders are doing is just zeroing out the rotations of each on the joints. If you want more control, you can
use the individual sliders, or, pose the joint mover manually, then select "Update Rig Pose".

.. figure:: /images/rig_pose_02.gif
    :width: 1086px
    :height: 427px

    Using individual sliders and manually adjusting the joint movers to create a new rig pose. Make sure to update the
    rig pose for those changes to take effect!

.. note:: At the top of each module's rig pose widget, under the global slider, is the Reset Rig Pose and Update Rig
          Pose buttons. The Reset Rig Pose sets the rig pose to be the default, which is all rotations zeroed out.
          Update Rig Pose takes manual adjustments or individual slider adjustments and sets those to be the new rig
          pose. As you can see in the above figure, once the rig pose has been updated, sliding the global slider
          between the model pose and rig pose goes between the original model pose and your new updated pose.

Mesh Slicer
-----------
The next page is optional. If you have a fairly heavy mesh, you may want to consider breaking it up into rigid pieces to
create a mesh that is good for viewport frame rate. This will make a copy of your mesh and cut it up into rigid pieces
based on the weighting information, giving the animators a choice to use the original mesh or the rigid mesh.

.. image:: /images/publish_rig_04.png


Asset Thumbnail
---------------
The next page is for creating a thumbnail of the asset or for loading your own thumbnail to use (200px x 200px).
When creating a thumbnail, it will use the perspective viewport as the camera. Just tumble around the perspective
viewport (rather than the tiny preview) to frame your shot:

.. figure:: /images/publish_rig_thumbnail.gif
    :width: 1086px
    :height: 427px

    Tumble around the perspective viewport to frame your shot for the thumbnail. You can also change the colors of the
    3 lights in the scene.

Summary
-------

.. image:: /images/publish_rig_05.png

The final page summarizes the options chosen before continuing to kick off the rig build. If everything looks good, hit
the "Build" button to start the rig build, which depending on the number of modules that make up the character, usually
takes about a minute.


Rig Build
---------

Once you click build, you will be presented with a progress window that will report progress, as well as any errors.
After that, your rig is ready!

.. image:: /images/rig_build.gif




