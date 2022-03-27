"""
This module contains the class for showing the interface to the user for updating the tools.
"""

from ThirdParty.Qt import QtGui, QtCore, QtWidgets
import maya.cmds as cmds
import urllib2
import Utilities.interfaceUtils as interfaceUtils
import Tools.System.ART_Updater as updater

# maya 2016< 2017> compatibility
try:
    import shiboken as shiboken
except ImportError:
    import shiboken2 as shiboken

windowTitle = "ARTv2: Check For Updates"
windowObject = "pyArtUpdaterWin"


class ART_UpdaterUI(interfaceUtils.baseWindow):
    """
    Class for displaying the graphical user interface that interacts with the ART_Updater class. This UI is used
    primarily for displaying useful information to the user, such as patch notes and logging information during the
    update process.

    .. image:: /images/updateUI.png
    """

    def __init__(self, parent=None):

        super(ART_UpdaterUI, self).__init__(600, 600, 600, 600, parent)

        self.updater_inst = updater.ART_Updater(self)
        self.path = None

        needs_update = self._check_for_update()

        if needs_update is None:
            self.close()
            self.deleteLater()
            return

        else:
            self._build_interface()
            self.show()
            QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
            QtWidgets.QApplication.processEvents()
            self._update_tools()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _build_interface(self):

        # create the main widget
        main_widget = QtWidgets.QFrame()
        self.setCentralWidget(main_widget)

        # set qt object name
        self.setObjectName(windowObject)
        self.setWindowTitle(windowTitle)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # create the mainLayout for the rig creator UI
        main_layout = QtWidgets.QVBoxLayout(main_widget)

        # create the QFrame
        self.frame = QtWidgets.QFrame()
        main_layout.addWidget(self.frame)
        widget_layout = QtWidgets.QVBoxLayout(self.frame)

        # detailed information
        self.info_text = QtWidgets.QTextEdit()
        self.info_text.setMinimumWidth(550)
        self.info_text.setMaximumWidth(550)
        self.info_text.acceptRichText()
        self.info_text.setReadOnly(True)
        self.info_text.setAutoFormatting(QtWidgets.QTextEdit.AutoBulletList)
        self.info_text.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
        widget_layout.addWidget(self.info_text)

        self.info_text.append("")

        # progress bar
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setMinimumSize(QtCore.QSize(550, 25))
        self.progress_bar.setMaximumSize(QtCore.QSize(550, 25))
        widget_layout.addWidget(self.progress_bar)

        # button bar
        button_layout = QtWidgets.QHBoxLayout()
        widget_layout.addLayout(button_layout)

        cancel_button = QtWidgets.QPushButton("Close")
        cancel_button.setMinimumHeight(30)
        button_layout.addWidget(cancel_button)
        cancel_button.setObjectName("settings")
        cancel_button.clicked.connect(self._cancel)

        QtWidgets.QApplication.processEvents()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _check_for_update(self):

        local_version = self.updater_inst.find_latest_local_version()
        latest_version = self.updater_inst.find_latest_available_version()
        page = self._fetch_notes(latest_version[0].replace(".", "_"))

        if latest_version[0] > local_version:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setTextFormat(QtCore.Qt.RichText)
            msg_box.setText("Updates Available! Would you like to install the updates?")
            msg_box.setInformativeText("<a href=\"" + page + "\" style=\"color:#FF0000\">View Patch Notes</a>")
            detailed_text = "Installing updates will create a backup of your currently installed version. If for any " \
                            "reason the updates cannot be applied automatically, the latest version will be extracted " \
                            "to a new folder."
            msg_box.setDetailedText(detailed_text)
            msg_box.addButton("Yes", QtWidgets.QMessageBox.YesRole)
            msg_box.addButton("No", QtWidgets.QMessageBox.NoRole)
            msg_box.setIcon(QtWidgets.QMessageBox.Information)
            ret = msg_box.exec_()

            if ret == 0:
                return True

            else:
                return None

        else:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setText("No Updates Available!")
            msg_box.setIcon(QtWidgets.QMessageBox.Information)
            msg_box.exec_()
            return None

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _update_tools(self):

        QtWidgets.QApplication.processEvents()
        remove_dirs = self.updater_inst.get_overwrite_directories()
        self.progress_bar.setMaximum(len(remove_dirs) + 1)
        self.progress_bar.setValue(0)

        self.updater_inst.update_self()

        reload(updater)
        self.updater_inst = updater.ART_Updater(self)
        self.updater_inst.update_tools()
        QtWidgets.QApplication.restoreOverrideCursor()
        QtWidgets.QApplication.processEvents()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def show_info(self, text_array, color):
        """
        Called on from ART_Updater, it adds the given text to the QTextEdit using the given color.

        :param str text_array: Text to add to the QTextEdit.
        :param color: RGB values for the color of the text.
        :type color: tuple of 3 integers, in a range of 0 - 255.
        """

        self.info_text.setTextColor(QtGui.QColor(color[0], color[1], color[2]))
        for each in text_array:
            self.info_text.append(each)
        self.info_text.moveCursor(QtGui.QTextCursor.End)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _cancel(self):

        self.updater_inst.clean_up()
        self.close()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def _fetch_notes(self, latest_version):

        web_link = "https://artv2.com/_versions/version_" + latest_version + ".html"
        code = urllib2.urlopen(web_link).code
        if code / 100 >= 4:
            web_link = "https://artv2.com/versions.html"

        return web_link


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def run():
    """
    Instantiates the user interface and show it to the user. If the user interface already existed, it will be deleted
    first.
    """

    if cmds.window("pyArtUpdaterWin", exists=True):
        cmds.deleteUI("pyArtUpdaterWin", wnd=True)

    gui = ART_UpdaterUI(interfaceUtils.getMainWindow())
    gui.show()
