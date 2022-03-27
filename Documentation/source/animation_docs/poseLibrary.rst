############
Pose Library
############

    :Date: |today|
    :Author: **Jeremy Ernst**

*************
Loading Poses
*************

Interface Overview
------------------

.. image:: /images/pose_lib_overview.png

.. topic:: Parts of the UI

    1. The character in the scene to load poses onto.
    2. The default pose location for that character.
        .. note:: To set a default pose location for a character, go into the directory tree, and right click on a directory
                  to set that directory as the default pose location. Now, anytime you open the pose library with this
                  character, it will default to this location.

        .. image:: /images/pose_lib_default_location.png

    3. How to load the pose, whether it be by using control attribute values only (Local Space), or by
       calculating new values so that the pose loads exactly as it was originally posed, regardless of any
       active spaces controls may be in (World Space).
    4. Whether to load the pose on all of the controls, or only selected controls for the character.
    5. Launches interface for creating new poses. (See `Creating Poses`_ section)
    6. Search field for searching directories.
    7. Search field for searching poses.
    8. Directory tree containing all projects and their directories.
    9. Pose view. Any available poses in the selected directory will be shown here.
    10. A pose.
    11. Status bar. Contains information on poses and pose options.

Default Loading Behavior
------------------------

When you left click on a pose, it will load that pose on all controls it has data for. If you've set your Space or
Operate on: fields to something different than the default Local and All, it will load with those options instead.
If the pose only contains controls for fingers, for example, then left-clicking on that pose will only load the data
on those finger controls.

.. image:: /images/load_pose_default.gif

Loading on Selected
-------------------

If you've set the "Operate on:" field to "Selected Controls", clicking on a pose, regardless of how many controls have
data stored in that pose, will only load the pose on those controls.

.. image:: /images/load_pose_selected.gif

Choosing Local or World Space
-----------------------------

Loading a pose in local space will load the values for the attributes on each stored control. What this means, is that
if your control is in a different space, then the stored attribute values may be invalid for that control.

Loading a pose in world space will re-calculate all values so that the controls are in the same world space position
as they were when the pose was saved. This means your control could be in a different space from the pose, but would
still load correctly.

.. note:: Loading a pose in world space does take longer, as calculations have to be made for the new control values.

Loading a Mirrored Pose
-----------------------

To load a mirrored pose, right click on a pose to access some additional options.

.. image:: /images/pose_lib_mirror_pose.png

Here, you can use the mirrored options to load a mirrored pose in the set space, and operating on the controls set.
If your space is set to local, the pose will be mirrored across the character. If the space is set to world, the pose
will be mirrored across the world origin.

If you have it set to operate on all controls, the full pose will be mirrored. If you have it set to operate on selected
controls, the pose will be mirrored using the selection only.

.. image:: /images/load_pose_mirror.gif

Loading an Offset Pose
----------------------

Loading an offset pose will load the given pose at the location of the selected control. For example, we have a pose
that was saved at the world origin. Our character is now out away from the world origin, but we want to load the pose
at the character's current position. We could then select the body_anim control, or the root, and load pose from offset.

.. image:: /images/load_offset_pose.gif

.. note:: This function only works on all controls and is world space by default.

Editing a Pose
--------------

In the right-click menu of a pose, you will see options to update the thumbnail for the pose, rename the pose, and
delete the pose.

Hotkeys
-------

There are hotkeys for quickly switching the "space" setting and the "Operate on:" setting.

.. image:: /images/pose_lib_hotkeys.png

Operating on Current Pose
-------------------------

You can right click on the pose library icon in the animation interface to bring up some options for mirroring on the
pose currently on the character in the viewport.

.. image:: /images/pose_lib_current_pose.png

This saves time by not having to create a pose just to be able to mirror it.

.. image:: /images/load_pose_mirror_current.gif

**************
Creating Poses
**************

To create a pose, launch the pose library, and click on the "Add New Pose" button in the top right.

.. image:: /images/pose_lib_add_new_pose.png

This will launch a new interface, which is explained in the below image.

.. image:: /images/pose_lib_create_pose.png

Once you have the folder selected in the tree where you want the pose saved, and the pose has been given a name, you can
then choose to create a pose for all of the controls in the character, or create a pose for the selected controls,
which is referred to as a "partial pose". This would typically be things like hand and face poses.

.. note:: If you want to create a partial pose, check your selection to ensure it is correct, and then click on
          "Create Pose for Selected Controls".

.. note:: With regards to the viewport, it is simply a preview of the perspective viewport. Use the perspective
          viewport to manipulate the camera. See below.

          .. image:: /images/pose_lib_create_pose_camera.gif
