##################
ARTv2 Installation
##################

    :Date: |today|
    :Author: **Jeremy Ernst**

*****************
Previous Versions
*****************

If you have had alpha or beta versions on ARTv2 installed previously, you will need to do some clean-up before
installing, as directory structures haved changed.

In Maya's script editor, open a Python tab. Run the following code:

.. code-block:: python

    from PySide2 import QtCore
    settings = QtCore.QSettings("Epic Games", "ARTv2")
    settings.clear()

.. note:: If you are running Maya 2016, using PySide instead of PySide2.

It may be a good idea to completely remove the old directory as well. You can copy and paste your ARTv2/Projects
folder into the new ARTv2 installation to keep any rigs you had made.

**************************
Easy Install (recommended)
**************************

To install ARTv2, browse to the ARTv2 folder and find the install.mel file. Open Maya, and drag the install.mel file
into the viewport. If everything was successful, Maya will then close.

Re-open Maya, and under Windows > Settings/Preferences > Plug-in Manager, load the ARTv2 plugin.

.. image:: /images/artv2_plugin.png

You will then be prompted to locate the ARTv2 directory on your drive. Once you have done that, you should now see a new
menu in Maya called A.R.T. 2.0, which completes installation.

.. note:: This has been thoroughly tested on a Windows OS. However, it is possible that on Mac or Linux, the install
          script may fail. If so, I will describe the manual steps below for getting the tools installed.

**************
Manual Install
**************

In the case the install.mel script fails for you, this section will walk you through what the install.mel script is
doing so that you can do the same steps manually to get the tools installed.

The first thing to do is to figure out where Maya is looking for modules. Usually, this is where the install script
fails, because the path it tries to construct is invalid. In Maya's script editor, in a Python tab, run the following
code:

.. code-block:: python

    import os
    paths = os.environ["MAYA_MODULE_PATH"]
    for path in paths:
        print path

This will give us a list of directories that Maya will be looking for .mod files in. Inside the ARTv2 folder, is an
ARTv2.mod file. Copy that file and paste it into one of the directories that was printed out above. If a modules
folder doesn't exist, create one, and then paste in the mod file.

Open the .mod file and edit it so that it points to the ARTv2 directory on your drive. You will notice a
"REPLACE_TO_YOUR_PATH" in there. Replace that with the path to the ARTv2 folder. For example:

.. code-block:: none

    + ARTv2 1.0 C:\Users\user_name\Documents\artv2\ARTv2

Now, if you restart Maya, and look in the Windows > Settings/Preferences > Plug-in Manager, ARTv2 should now show up.
Go ahead and load it, and then follow the prompt to browse to the ARTv2 folder. The tools should now be installed.


*******
Updates
*******

To check and acquire updates, use the "Check for Updates" menu item in the ARTv2 menu.