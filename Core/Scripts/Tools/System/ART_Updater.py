"""
This module contains the class that holds the core functionality for updating the tools.
"""

import maya.cmds as cmds
import os
import Utilities.utils
import urllib2
import zipfile
import shutil
import stat
from ThirdParty.Qt import QtCore


# noinspection SpellCheckingInspection
class ART_Updater(object):
    """
    Class used for checking for updates on the github repository as well as downloading those updates and making
    back-ups of current versions.

    Usage:

        .. code-block:: python

                        import Tools.System.ART_Updater as updater
                        updater_inst = updater.ART_Updater()
                        updater_inst.update_tools()

    """

    def __init__(self, gui_instance=None):

        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.tools_path = settings.value("toolsPath")
        self.gui_instance = gui_instance
        self.path = None
        self.read_only_files = []

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def check_for_updates(self):
        """
        Checks to see if updates are available by comparing the local version to the latest available version.
        """

        local_version = self.find_latest_local_version()
        latest_version = self.find_latest_available_version()

        if latest_version[0] > local_version:
            self._show_info(["Updates available!"], (79, 180, 250))
            self._show_info(["Current version: " + str(local_version)], (79, 180, 250))
            self._show_info(["Available version: " + str(latest_version)], (79, 180, 250))
            self.update_tools()

        else:
            self._show_info(["You are up-to-date!"], (0, 183, 52))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def find_latest_local_version(self):
        """
        Finds the local version of the tools installed.

        :return: Returns the version number of the tools currently installed.
        """

        path = os.path.join(self.tools_path, "Documentation\\build\\_versions")
        local_versions = os.listdir(path)

        versions = []
        for version in local_versions:
            version_info = version.partition("version_")[2].partition(".html")[0]
            version_num = version_info.replace("_", ".")
            versions.append(version_num)
        return max(versions)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def find_latest_available_version(self):
        """
        Finds the latest available version of the tools off of github.

        :return:  Returns the version number of the latest available version.
        """

        url = "https://github.com/epicernst/Animation-and-Rigging-Toolkit-v2/tree/master"
        url += "/ARTv2/Documentation/build/_versions"

        request = urllib2.Request(url)
        try:
            result = urllib2.urlopen(request)
            page_content = result.read()
            versions = {}

            for line in page_content.splitlines(True):
                if line.find("title=\"version_") != -1:
                    version_string = line.partition("title=\"version_")[2].partition(".html")[0]
                    version = version_string.replace("_", ".")
                    versions[version] = version_string
            latest_version = max(versions)
            return [latest_version, versions.get(latest_version)]
        except urllib2.HTTPError as e:
            cmds.warning(str(e))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def check_for_issues(self):
        """
        Checks the local installation for read-only files. If it finds any, it will not attempt to auto-update, but
        instead create an update directory that contains the new version of the tools.

        :return: Returns a bool for whether there were issues or not.
        """

        directories = self.get_overwrite_directories()
        base_tools_dir = os.path.dirname(self.tools_path)
        for directory in directories:
            full_path = os.path.normpath(os.path.join(base_tools_dir, directory))
            self._find_read_only_files(full_path)

        if len(self.read_only_files) > 0:
            self._show_info(["The following files were marked as read-only and could not be updated:"],
                            (202, 5, 5))

            for f in self.read_only_files:
                self._show_info(["    " + str(f)], (203, 196, 136))

            return True

        return False

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def update_self(self):
        """
        Updates this module (ART_Updater). Currently, this is called from the GUI. Once the module is up-to-date,
        it gets reloaded and then continues to update the rest of the tools.

        This class does not call on this method. However, if you wanted to, you could call on it via command line, and
        manually refresh the module before continuing.
        """

        issues_present = self.check_for_issues()
        if issues_present:
            return
        if self.path is None:
            self.path = self.download_zip()

        zip_archive = os.path.join(self.path, "master.zip")
        with zipfile.ZipFile(zip_archive) as zip_file:
            for name in zip_file.namelist():
                if name.find("ART_Updater.py") != -1:
                    local_extracted_path = Utilities.utils.returnFriendlyPath(os.path.join(self.path, name))
                    file_path = local_extracted_path.rpartition("ARTv2")[2]

                    destination = Utilities.utils.returnFriendlyPath(self.tools_path) + file_path
                    self._show_info(["attempting to update " + destination + ".."], (79, 180, 250))
                    if os.path.exists(destination):
                        self._find_read_only_files(os.path.dirname(destination))

                        if destination not in self.read_only_files:
                            shutil.copy(local_extracted_path, destination)
                            self._show_info(["        updated " + destination + "!\n\n"], (0, 183, 52))
                        else:
                            self._show_info(["        Could not update " + destination + "!\n\n"], (202, 5, 5))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def download_zip(self):
        """
        Downloads the archive from github of the latest tools. Extracts the archive to the user's home directory.

        :return: Returns a string of the directory where the zip file (downloaded from github) is located.
        """

        request = urllib2.Request("https://github.com/epicernst/Animation-and-Rigging-Toolkit-v2/archive/master.zip")
        result = urllib2.urlopen(request)
        zip_content = result.read()

        filename = os.path.basename("https://github.com/epicernst/Test/blob/master/master.zip")
        path = os.environ["home"]
        file_path = os.path.join(path, filename)

        with open(file_path, 'w') as f:
            f.write(zip_content)

        master_dir = os.path.dirname(file_path)
        maya_tools_zip = master_dir

        with zipfile.ZipFile(file_path, 'r') as zfile:
            for name in zfile.namelist():
                if name.find(".zip") != -1:
                    maya_tools_zip = os.path.join(maya_tools_zip, name)
            zfile.extractall(master_dir)

        self.path = master_dir
        return master_dir

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _find_read_only_files(self, full_path):

        contents = os.listdir(full_path)
        for each in contents:
            if os.path.isfile(os.path.join(full_path, each)):
                fileAttr = os.access(os.path.join(full_path, each), os.W_OK)
                if fileAttr is not False:
                    os.chmod(os.path.join(full_path, each), stat.S_IWRITE)
                else:
                    self.read_only_files.append(Utilities.utils.returnFriendlyPath(os.path.join(full_path, each)))
            if os.path.isdir(os.path.join(full_path, each)):
                self._find_read_only_files(os.path.join(full_path, each))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def update_tools(self):
        """
        The core function for updating the tools. Calls on many methods throughout that back up the existing
        installation, and copy the updated files over the installed location.

        .. seealso:: :meth:`ART_Updater.ART_Updater._create_backup`
        .. seealso:: :meth:`ART_Updater.ART_Updater._overwrite_tools`
        .. seealso:: :meth:`ART_Updater.ART_Updater.clean_up`
        """

        full_copy = False

        issues_present = self.check_for_issues()
        if issues_present:
            full_copy = True

        if self.path is None:
            self._show_info(["Downloading update...\n\n"], (249, 168, 12))
            self.download_zip()

        self._show_info(["Unpacking update...\n\n"], (249, 168, 12))

        base_tools_dir = os.path.dirname(self.tools_path)
        zip_archive = os.path.join(self.path, "master.zip")

        with zipfile.ZipFile(zip_archive) as zf:
            remove_dirs = self.get_overwrite_directories()
            for directory in remove_dirs:
                full_path = os.path.normpath(os.path.join(base_tools_dir, directory))
                self._find_read_only_files(full_path)
                if issues_present is False:
                    full_copy = self._create_backup(full_path)

                if full_copy is False:
                    full_copy = self._overwrite_tools(full_path, directory, zf)

            if full_copy:
                self._auto_update_failed(zf)
            else:
                self._show_info(["\n\nUpdate Operation Completed!", "You must restart Maya to have updates applied."],
                                (48, 255, 0))
        self.clean_up()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def get_overwrite_directories(self):
        """
        Returns the core directories that get updated. Scripts, Icons, joint movers, plug-ins, and documentation.

        :return: Returns a list of relative directory paths.
        """

        return ["ARTv2/Core/Scripts/", "ARTv2/Core/Icons/", "ARTv2/Core/JointMover/", "ARTv2/plug-ins/",
                "ARTv2/Documentation/"]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def clean_up(self):
        """
        Deletes the downloaded zip archive and associated temp files.
        """

        try:
            if os.path.exists(os.path.join(self.path, "Animation-and-Rigging-Toolkit-v2-master")):
                shutil.rmtree(os.path.join(self.path, "Animation-and-Rigging-Toolkit-v2-master"))
            if os.path.exists(os.path.join(self.path, "master.zip")):
                os.remove(os.path.join(self.path, "master.zip"))
        except Exception, e:
            self._show_info(["Unable to clean up temporary files..", str(e)], (249, 168, 12))

        for i in range(10):
            self._increment_progress()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _auto_update_failed(self, zip_file):

        self._show_info(["Could not apply updates automatically."], (249, 168, 12))

        # extract all to an Update folder
        version = self.find_latest_available_version()[0]
        updateDir = os.path.join(self.tools_path, "Update_" + str(version))
        if not os.path.exists(updateDir):
            os.makedirs(updateDir)

        self._show_info(["Extracting updated files to:\n    " + str(updateDir)], (79, 180, 250))
        try:
            zip_file.extractall(updateDir)
        except Exception, e:
            self._show_info(["Operation Failed", str(e)], (249, 168, 12))

        # report on operation
        text = "Update Extracted. Since the automatic operation failed, you will need to manually integrate" \
               " and apply the updates."
        self._show_info([text], (249, 168, 12))

        for i in range(10):
            self._increment_progress()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _create_backup(self, full_path):

        whole_copy = False
        self._show_info(["\n########################################################\n"], (200, 200, 200))
        self._show_info(["Creating Backup of current version.. " + str(full_path)], (79, 180, 250))

        version_number = self.find_latest_local_version()
        backup_dir = os.path.join(os.path.dirname(self.tools_path), "Backups")
        backup_dir = os.path.normpath(os.path.join(backup_dir, str(version_number)))
        backup_dir = Utilities.utils.returnFriendlyPath(backup_dir)
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        full_path = Utilities.utils.returnFriendlyPath(full_path)

        try:
            shutil.move(full_path, backup_dir)
            self._show_info(["    Backups created in " + str(backup_dir)], (0, 183, 52))
        except Exception, e:
            self._show_info([str(e)], (249, 168, 12))
            self._show_info(["Backup not created."], (249, 168, 12))
            whole_copy = True

        return whole_copy

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _overwrite_tools(self, full_path, directory, zip_file):

        full_copy = False
        for name in zip_file.namelist():
            if name.find(directory) != -1:
                local_extracted_path = os.path.join(self.path, name)

                partial_path = local_extracted_path.partition(directory)[2]
                destination_path = Utilities.utils.returnFriendlyPath(os.path.join(full_path, partial_path))
                if not os.path.exists(destination_path):
                    try:
                        shutil.move(local_extracted_path, full_path)

                    except Exception, e:
                        self._show_info([str(e)], (249, 168, 12))
                        full_copy = True

        self._show_info(["\nExtracted updated files to " + str(full_path) + "!"], (0, 183, 52))
        self._increment_progress()
        return full_copy

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _show_info(self, text_array, color):

        if self.gui_instance is not None:
            self.gui_instance.show_info(text_array, color)
        else:
            for each in text_array:
                print each

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _increment_progress(self):
        if self.gui_instance is not None:
            value = self.gui_instance.progress_bar.value()
            self.gui_instance.progress_bar.setValue(value + 1)
