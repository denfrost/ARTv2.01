##############
Space Switcher
##############

    :Date: |today|
    :Author: **Jeremy Ernst**

***************
Creating Spaces
***************

Creating a space must be done in the unreferenced rig file. View "Setting up Control Spaces" in the Rigging section of
the documentation.


****************
Switching Spaces
****************

To switch spaces, there are a few ways you can access space switching:

Through the UI
--------------
    To switch spaces through the UI, click on the Space Switcher icon in the animation tools interface:

        .. image:: /images/switch_space.gif



    Here is an in-depth look at each of the elements on the space switcher interface:

        .. figure:: /images/space_switcher_switch_ui.png
            :width: 458px
            :height: 251px

            The interface for switching spaces.

            +----------------+-----------------------------------------------------------------------------------------+
            | Field          | Description                                                                             |
            +================+=========================================================================================+
            | Operation      | Whether the function the interface performs will be to switch a space or bake a space.  |
            +----------------+-----------------------------------------------------------------------------------------+
            | Control        | This is the control that contains spaces. Start typing in this text field to            |
            |                | auto-populate suggestions.                                                              |
            +----------------+-----------------------------------------------------------------------------------------+
            | Space          | This is the list of spaces you can switch to.                                           |
            +----------------+-----------------------------------------------------------------------------------------+
            | Update         | This section gives functions for updating the matching on space switching if the motion |
            | Matching       | was updated after the space was switched.                                               |
            +----------------+-----------------------------------------------------------------------------------------+

            +-----------------------------------------------+--------------------------------------------------------+
            | Buttons                                       | Description                                            |
            +===============================================+========================================================+
            | .. image:: /images/icons/use_selection.png    | Adds the currently selected control to the "Control:"  |
            |                                               | text field.                                            |
            +-----------------------------------------------+--------------------------------------------------------+
            | .. image:: /images/icons/list.png             | Shows a new widget for seeing all valid controls that  |
            |                                               | have space-switching available. Select a control from  |
            |                                               | the list to populate the 'Control:' text field.        |
            +-----------------------------------------------+--------------------------------------------------------+
            | .. image:: /images/icons/prev.png             | Select a previously available space-switching key from |
            |                                               | the current frame.                                     |
            +-----------------------------------------------+--------------------------------------------------------+
            | .. image:: /images/icons/match_prev.png       | Matches the previous frame's space-switching pose.     |
            +-----------------------------------------------+--------------------------------------------------------+
            | .. image:: /images/icons/match_next.png       | Matches the next frame's space-switching pose.         |
            +-----------------------------------------------+--------------------------------------------------------+
            | .. image:: /images/icons/next.png             | Select the next available space-switching key from the |
            |                                               | current frame.                                         |
            +-----------------------------------------------+--------------------------------------------------------+

        To add a control, you have several options available to you. First, you can start typing in the name of a
        control and the UI will provide auto-complete suggestions:

        .. figure:: /images/space_switch_auto_complete.gif
            :width: 456px
            :height: 248px

            Auto-completion for typing in a control.

        You can also use the list picker button, to bring up a widget that shows all controls with space switching, and
        select from there.

        .. figure:: /images/space_switch_list.gif
            :width: 533px
            :height: 322px

            The control selection list for selecting controls with space-switching setup.

    Lastly, you can simply select the control in the viewport or using the control picker, and plug it in using the
    "use selection" button:

        .. figure:: /images/space_switch_use_selection.gif
            :width: 533px
            :height: 254px

            Use the "use selection" button to plug in your currently selected control into the UI.

    .. note::

        The space in the combo box will update to show the active space on the current frame when scrubbing the
        timeline.



Using Hotkeys
-------------
    In the ARTv2 Hotkey Editor, there is a hotkey available for toggling the space on a control. To set this up, open
    the hotkey editor, found under the ARTv2 menu:

        .. figure:: /images/hotkey_editor_menu.png
            :width: 260px
            :height: 340px

            Opens the ARTv2 Hotkey Editor.

    In the "Rig Manipulation" section, you will find an entry for "Toggle Spaces on Control":

        .. figure:: /images/toggle_spaces_on_control.png
            :width: 755px
            :height: 477px

            Setup the hotkey to toggle spaces on the selected control. Hitting the assigned hotkey will switch to the
            next available space.


Using the Animation Picker
--------------------------

    Lastly, if you right-click on a control in the animation picker, the available spaces for that control will appear
    at the bottom of the menu. Choose one to switch to that space!

        .. figure:: /images/space_switch_in_picker.gif
            :width: 426px
            :height: 535px

            Any control that has space switching setup will have their spaces available to switch to in the right-click
            context menu in the animation control picker.

*****************
Space Switch Keys
*****************

    All keyframes set for space switching are done on the control itself. When you switch a space, a "bookmark" key is
    set on the previous frame in order to ensure there are no pops when the space switches. You will see two keyframes
    side-by-side any time you switch spaces.

        .. figure:: /images/space_switch_keys3.png
            :width: 1349px
            :height: 487px

            Space switching is happening here on frames 1, 10, and 20, with a "bookmark" key being set on the previous
            key before each space switch (frames 0, 9, and 19).

    The matching is done by setting new values on the control translates and rotates, as you can see in the graph
    editor:

        .. figure:: /images/space_switch_keys2.png
            :width: 759px
            :height: 370px

            Each time the space is switched (frames 1, 10, and 20), you can see a jump in the control's translate and
            rotate values, which is done to ensure that no pops occur when the space is switched.

    Only visible in the graph editor, is the follow attribute (as seen in the first image), which is the actual space
    switch keyframes (whereas the translate and rotates are the matching keyframes).

    All keys are on the control so that re-timing your animation is simple! Just make sure to keep any side-by-side keys
    together (treat them as one pose) and your space switches won't get messed up.

***************
Update Matching
***************

    Sometimes, you may end up adjusting a pose after you've done your space switches. Because the control had keys set
    to ensure there were no pops when matching, those keys may now be invalid if the underlying pose has changed!

        .. figure:: /images/space_switch_update_matching1.gif
            :width: 560px
            :height: 626px

            In this example, the posing on the spine changed, and now our pistol pops when it switches spaces to the
            left hand. Notice in the Space Switcher UI how the space changes from holster to l hand? The pistol should
            not be moving there!

    To fix this, you can use the Update Matching tool found in the space switcher UI.

        .. figure:: /images/space_switcher_switch_ui.png
            :width: 458px
            :height: 251px

            The bottom section contains buttons for browsing to space switching keys and matching the previous or next
            frame's pose.

    Use the next and previous buttons to browse to the next or previously available space switch key set. Then use the
    match next or match previous buttons to choose which frame of the key set to update.

        .. figure:: /images/space_switch_update_matching2.gif
            :width: 560px
            :height: 626px

            In this example, the next frame's pose is matched to fix the pop introduced by changing the spine
            motion. Now the pistol smoothly transitions to the left hand space.

*************
Baking Spaces
*************

Baking spaces allows you to take a control with animation, and either bake all of the current space-switching down
into one space, or bake sections of the animation into different spaces.

Example:

    .. figure:: /images/bake_space.gif
        :width: 829px
        :height: 451px

        This will bake the gun space into the holster space during the entire animation.

To bake a space, open the space switcher interface, and change the operation to "Bake Space". Much of the UI remains
the same as the Switch Space operation, so if you need a refresher to what the different buttons do, take a look at
Switching Spaces Through the UI.

The new parts here are a frame range and a Bake button. Set the control whose space you want to bake, select the
space to bake, and enter the frame range that you want the control baked into the given space. In the below example,
the weapon_jnt_anim will be baked into the l hand space during frames 53-72. Assuming the control was only in default
space previously, this means that it will remain in default space, except during that frame range, in which case, it
will be in the left hand space.

    .. figure:: /images/space_switcher_bake_ui.png
        :width: 458px
        :height: 255px

        This will bake the weapon_jnt_anim control into the left hand space during frames 53-72.


