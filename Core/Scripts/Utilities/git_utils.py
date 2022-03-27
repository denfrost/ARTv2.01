"""
Author: Jeremy Ernst

This module has utility functions for dealing with github interactions.
"""

from functools import partial

from ThirdParty.Qt import QtCore, QtWidgets


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def getGitCreds():
    """
    Get the github credentials stored in the QSettings

    :return: github username and password
    """

    settings = QtCore.QSettings("Epic Games", "ARTv2")

    user = settings.value("gitUser")
    password = settings.value("gitPass")

    if user is not None and password is not None:
        return [user, password]
    else:
        return None


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def gitWriteCreds(username, password, ui):
    """
    Set the QSettings values for the username and password with the supplied information.

    :param username: user-entered github username
    :param password: user-entered github password
    :param ui: instance of UI where use enters above information
    """

    settings = QtCore.QSettings("Epic Games", "ARTv2")
    settings.setValue("gitUser", username.text())
    settings.setValue("gitPass", password.text())
    ui.close()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def gitCredsUI(parent):
    """
    Create an interface that allows user to enter github username and password.

    :param parent: interface that this interface will be a child of.
    """

    credsDialog = QtWidgets.QDialog(parent)
    credsDialog.setWindowTitle("Github Credentials")
    credsDialog.setMinimumSize(QtCore.QSize(200, 120))
    credsDialog.setMaximumSize(QtCore.QSize(200, 120))

    layout = QtWidgets.QVBoxLayout(credsDialog)
    userName = QtWidgets.QLineEdit()
    userName.setPlaceholderText("Github User Name..")
    layout.addWidget(userName)

    password = QtWidgets.QLineEdit()
    password.setPlaceholderText("Github Password..")
    layout.addWidget(password)
    password.setEchoMode(QtWidgets.QLineEdit.Password)

    confirmButton = QtWidgets.QPushButton("Confirm")
    layout.addWidget(confirmButton)
    confirmButton.setObjectName("settings")
    confirmButton.setMinimumHeight(30)
    confirmButton.clicked.connect(partial(gitWriteCreds, userName, password, credsDialog))

    credsDialog.exec_()
