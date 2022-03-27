# standard imports
import os
from stat import S_IWUSR, S_IREAD
import tempfile
import traceback

import maya.cmds as cmds

from functools import partial
import utils
from ThirdParty.Qt import QtGui, QtCore, QtWidgets

# maya 2016< maya2017> compatability
try:
    import shiboken as shiboken
except:
    import shiboken2 as shiboken


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def getMainWindow():
    import maya.OpenMayaUI as mui
    pointer = mui.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(pointer), QtWidgets.QWidget)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def getMayaName(widget):
    import maya.OpenMayaUI as mui
    pointer = mui.MQtUtil.findControl(widget)
    return shiboken.wrapInstance(long(pointer), QtWidgets.QWidget)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def get_style_sheet(filePath):
    settings = QtCore.QSettings("Epic Games", "ARTv2")
    toolsPath = settings.value("toolsPath")

    styleSheetFile = utils.returnNicePath(toolsPath, "Core/Scripts/Tools/_StyleSheets/" + filePath + ".qss")
    f = open(styleSheetFile, "r")
    data = f.readlines()
    style = create_style_sheet(data)
    f.close()
    return style


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def create_style_sheet(data):
    settings = QtCore.QSettings("Epic Games", "ARTv2")
    iconPath = settings.value("iconPath")
    toolsPath = settings.value("toolsPath")

    newLines = []
    style = ""

    for line in data:
        if line.find("url(") != -1:
            if line.find("System/backgrounds") != -1:
                oldPath = line.partition("(")[2].rpartition("/")[0]
                replacePath = utils.returnNicePath(iconPath, "System/backgrounds")
                newLine = line.replace(oldPath, replacePath)
                newLines.append(newLine)
            if line.find("System/backgrounds") == -1:
                oldPath = line.partition("(")[2].rpartition("/")[0]
                replacePath = utils.returnNicePath(iconPath, "System")
                newLine = line.replace(oldPath, replacePath)
                newLines.append(newLine)
        else:
            newLines.append(line)

    user_dir = utils.returnFriendlyPath(os.path.join(toolsPath, "User"))
    if not os.path.exists(user_dir):
        try:
            os.makedirs(user_dir)
        except Exception, e:
            cmds.warning(str(e))

    full_path = (utils.returnFriendlyPath(os.path.join(user_dir, "style.qss")))
    f = open(full_path, 'w')
    f.writelines(newLines)
    f.close()

    f = open(full_path, 'r')
    style = f.read()
    f.close()

    os.remove(full_path)
    return style


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def addTextToButton(text, parent, centered=True, top=False, bottom=False, right=False, left=False, customColor=None):
    text = QtWidgets.QGraphicsSimpleTextItem(text, parent)
    text.setPen(QtGui.QPen(QtCore.Qt.transparent))

    if customColor is None:
        text.setBrush(QtGui.QBrush(QtCore.Qt.white))
    else:
        text.setBrush(QtGui.QBrush(customColor))
    font = QtGui.QFont()
    font.setPointSize(12)

    text.setFont(font)
    textPos = parent.boundingRect().center()
    textRect = text.boundingRect()
    parentRect = parent.boundingRect()

    if centered:
        text.setPos(textPos.x() - textRect.width() / 2, textPos.y() - textRect.height() / 2)

    if top:
        text.setPos(textPos.x() - textRect.width() / 2, textPos.y() - (parentRect.height() / 2 + textRect.height()))

    if bottom:
        text.setPos(textPos.x() - textRect.width() / 2, textPos.y() + (parentRect.height() / 2))

    if right:
        text.setPos((textPos.x() * 2) + 2, textPos.y() - (parentRect.height() / 2))

    if left:
        text.setPos((textRect.width() + 2) * -1, textPos.y() - (parentRect.height() / 2))

    return text


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def setCustomToolTip(name, widget):

    # get settings to get icon path
    settings = QtCore.QSettings("Epic Games", "ARTv2")
    iconPath = settings.value("iconPath")

    # build the image path
    image = utils.returnNicePath(iconPath, "Help/tooltips/" + name + ".png")

    tooltip = "<img src = \"" + image + "\">"
    widget.setToolTip(tooltip)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def generateToolTipImage(text, width, height, widget, size):

    # get settings to get icon path
    settings = QtCore.QSettings("Epic Games", "ARTv2")
    iconPath = settings.value("iconPath")

    # create font
    font = QtGui.QFont()
    font.setPointSize(10)

    # create a rect based on passed in args and create a color
    rect = QtCore.QRect(0, 0, width, height)
    text_rect = QtCore.QRect(5, 5, width - 10, height - 10)
    color = QtGui.QColor(155, 118, 67)

    # define the background image depending on height
    if size == "small":
        image = QtGui.QImage(utils.returnNicePath(iconPath, "System/backgrounds/tooltip_background_small.png"))
    else:
        image = QtGui.QImage(utils.returnNicePath(iconPath, "System/backgrounds/tooltip_background.png"))

    # create a pen and set the color
    pen = QtGui.QPen()
    pen.setColor(color)

    # create a pixmap to paint our image and text on
    pixmap = QtGui.QPixmap(width, height)

    # create the painter, set the pen, the font, and then draw the image first, then the text on top
    painter = QtGui.QPainter()
    painter.begin(pixmap)
    painter.setPen(pen)
    painter.setFont(font)
    painter.drawImage(rect, image)
    painter.drawText(text_rect, QtCore.Qt.TextWordWrap, text)
    painter.end()

    # write the tooltip to file
    dir_name = tempfile.gettempdir()
    file_name = QtCore.QFile(os.path.join(dir_name, "tooltip.png"))
    file_name.open(QtCore.QIODevice.WriteOnly)
    pixmap.save(file_name, "png")

    # return the file
    tooltip = "<img src = \"" + os.path.join(dir_name, "tooltip.png") + "\">"
    widget.setToolTip(tooltip)
    return tooltip


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
def display_error(error, error_tb):

    msg_box = QtWidgets.QMessageBox()
    msg_box.setIcon(QtWidgets.QMessageBox.Critical)
    msg_box.setInformativeText("______________________________________________________________________________")
    msg_box.setText("Error: {0}".format(error.strerror))
    full_traceback = utils.get_traceback(error_tb)
    msg_box.setDetailedText(full_traceback)
    msg_box.exec_()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class HotkeyLineEdit(QtWidgets.QLineEdit):

    def __init__(self):
        super(HotkeyLineEdit, self).__init__()

        self.keyPressed = QtCore.Signal()

    def keyPressEvent(self, event):

        key = event.key()
        modifiers = int(event.modifiers())

        keyname = QtGui.QKeySequence(modifiers + key).toString()
        self.setText(keyname)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class progressDialog(object):
    '''
    range is a tuple (min,max)
    example:
        myBar = progressDialog((0,100000), label="Exporting weights")
        for i in range(0,100000):
            myBar.setValue(i)
    '''

    def __init__(self, range, label='Doin Stuff..', freq=10):
        self.rangeMin, self.rangeMax, self.freq = range[0], range[1], freq
        self.bar = QtWidgets.QProgressDialog(label, None, self.rangeMin, self.rangeMax)
        self.bar.setWindowModality(QtCore.Qt.WindowModal)
        self.bar.autoClose()

    def setValue(self, val):
        self.bar.show()
        QtWidgets.QApplication.processEvents()
        if val % self.freq == 0 or (val + 1) == self.rangeMax:
            self.bar.setValue(val + 1)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class PickerList(QtWidgets.QListWidget):

    def __init__(self, menu, border, parent=None):
        QtWidgets.QListWidget.__init__(self, parent)
        self.menu = menu
        self.border = border

        # get the directory path of the tools
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def contextMenuEvent(self, event):

        import Tools.Animation.ART_SpaceSwitcher as SpaceSwitcher
        ART_Space = SpaceSwitcher.ART_SpaceSwitcherUI()

        # space icon
        spaceIcon = QtGui.QIcon((utils.returnFriendlyPath(os.path.join(self.iconsPath, "System/animSpace.png"))))

        # get existing menu QActions
        actionObjects = self.menu.children()
        actions = []

        for obj in actionObjects:
            actions.append([obj.text(), obj])

        for action in actions:
            if action[0].find("Switch to space:") != -1:
                self.menu.removeAction(action[1])

        # if the control has a space, add spaces to self.menu
        try:
            # get item at point
            item = self.itemAt(event.pos())
            itemData = item.data(QtCore.Qt.UserRole)

            # check to see if control (data) has space switching
            if cmds.objExists(itemData + ".space"):

                # get control spaces
                enumVal = cmds.addAttr(itemData + ".space", q=True, en=True)
                splitString = enumVal.split(":")

                for space in splitString:
                    self.menu.addAction(spaceIcon, "Switch to space: " + space, partial(ART_Space.switchSpace, itemData,
                                                                                        space))

        except AttributeError:
            pass

        point = QtWidgets.QCursor.pos()
        self.menu.exec_(point)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class ProgressBar(QtWidgets.QMainWindow):
    def __init__(self, title, parent=None):
        super(ProgressBar, self).__init__()

        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")

        # load stylesheet
        self.style = get_style_sheet("artv2_style")
        self.setStyleSheet(self.style)
        self.setWindowTitle(title)

        self.setMinimumSize(QtCore.QSize(400, 40))
        self.setMaximumSize(QtCore.QSize(400, 40))

        widget = QtWidgets.QWidget()
        self.setCentralWidget(widget)
        layout = QtWidgets.QVBoxLayout(widget)

        self.progress_bar = QtWidgets.QProgressBar()
        layout.addWidget(self.progress_bar)

    def setRange(self, min, max):

        self.progress_bar.setRange(min, max)

    def getValue(self):
        return self.progress_bar.value()

    def setValue(self, value):
        self.progress_bar.setValue(value)
        QtWidgets.QApplication.processEvents()

    def setFormat(self, string):
        self.progress_bar.setFormat(string)

    def setTextVisible(self, visibile):
        self.progress_bar.setTextVisible(visibile)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class commentBoxItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, x, y, w, h, scene, view, animUI):

        super(commentBoxItem, self).__init__(x, y, w, h)

        self.brush = QtGui.QBrush(QtGui.QColor(60, 60, 60, 125))
        self.brushColor = self.brush.color()
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        self.scale = 1
        self.menu = QtWidgets.QMenu()
        self.scene = scene
        self.view = view
        self.animUI = animUI

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)

        # add items to context menu
        self.menu.addAction("Change Color", self.changeBoxColor)
        self.menu.addAction("Rename", self.changeLabelText)
        self.menu.addAction("Remove Comment Box", self.deleteCommentBox)

        # add text
        self.textLabel = QtWidgets.QGraphicsTextItem("Comment Box", self)
        self.textLabel.setPos(x, y - 20)
        self.textLabel.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        # self.textLabel.setTextInteractionFlags(QtCore.Qt.TextEditable)

        self.classType = "comment"

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def boundingRect(self):
        rect = QtCore.QRectF(self.x, self.y, self.width, self.height)
        return rect

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def paint(self, painter, option, widget):
        rec = self.boundingRect()

        self.blackPen = QtGui.QPen(QtCore.Qt.black)
        self.blackPen.setWidth(0)
        painter.setPen(self.blackPen)
        painter.fillRect(rec, self.brush)
        painter.drawRect(rec)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def contextMenuEvent(self, event):
        self.menu.exec_(event.screenPos())

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def changeBoxColor(self):

        # launch a color dialog to  get a new color
        newColor = QtWidgets.QColorDialog.getColor()
        newColor.setAlpha(100)
        self.brush.setColor(newColor)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def changeLabelText(self):

        text = QtWidgets.QInputDialog.getText(self.scene.parent(), "Comment Box", "Enter Label Text:")
        if text:
            self.textLabel.setPlainText(text[0])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def deleteCommentBox(self):

        self.scene.removeItem(self)
        self.animUI.rubberband.hide()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def wheelEvent(self, event):

        # only if the focusable flag is set to true, do we continue
        flags = self.flags()
        if flags & QtWidgets.QGraphicsItem.ItemIsFocusable:

            self.scale = self.data(1)
            if self.scale is None:
                self.scale = 1
            scale = float(event.delta() / 8.0)
            self.scale = float((scale / 15.0) / 10) + self.scale
            self.setData(1, self.scale)

            self.setTransformOriginPoint(self.boundingRect().center())
            self.setScale(self.scale)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class pickerBorderItem(QtWidgets.QGraphicsRectItem):
    def __init__(self, x, y, w, h, brush, moduleName, niceName=None, menu=None):

        super(pickerBorderItem, self).__init__(x, y, w, h)

        self.brush = brush
        self.brushColor = brush.color()
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        self.scale = 1
        self.menu = menu

        self.mouseDown = False

        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges)

        self.setData(QtCore.Qt.UserRole, moduleName)
        self.setData(2, niceName)
        self.classType = "border"

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def boundingRect(self):
        rect = QtCore.QRectF(self.x, self.y, self.width, self.height)
        return rect

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def paint(self, painter, option, widget):
        rec = self.boundingRect()

        blackPen = QtGui.QPen(QtCore.Qt.transparent)
        blackPen.setWidth(0)
        blackPen.setStyle(QtCore.Qt.DotLine)
        painter.setPen(blackPen)

        flags = self.flags()
        if flags & QtWidgets.QGraphicsItem.ItemIsMovable:
            blackPen = QtGui.QPen(QtCore.Qt.black)
            blackPen.setWidth(0)
            blackPen.setStyle(QtCore.Qt.DotLine)
            painter.setPen(blackPen)

        if self.isSelected():
            blackPen = QtGui.QPen(QtCore.Qt.white)
            blackPen.setWidth(0)
            blackPen.setStyle(QtCore.Qt.DotLine)
            painter.setPen(blackPen)

        painter.fillRect(rec, self.brush)
        painter.drawRect(rec)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def wheelEvent(self, event):

        # only if the focusable flag is set to true, do we continue
        flags = self.flags()
        if flags & QtWidgets.QGraphicsItem.ItemIsFocusable:

            self.scale = self.data(1)
            if self.scale is None:
                self.scale = 1
            scale = float(event.delta() / 8.0)
            self.scale = float((scale / 15.0) / 10) + self.scale
            self.setData(1, self.scale)

            self.setTransformOriginPoint(self.boundingRect().center())
            self.setScale(self.scale)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def keyPressEvent(self, event):

        self.setTransformOriginPoint(self.boundingRect().center())

        if event.key() == QtCore.Qt.Key_Left:
            self.setRotation(self.rotation() - 10)

        if event.key() == QtCore.Qt.Key_Right:
            self.setRotation(self.rotation() + 10)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def contextMenuEvent(self, event):
        if self.menu is None:
            event.ignore()
        else:
            self.menu.exec_(event.screenPos())

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def mouseReleaseEvent(self, event):

        QtWidgets.QGraphicsItem.mouseReleaseEvent(self, event)
        pos = self.pos()

        x = self.roundPos(pos.x())
        y = self.roundPos(pos.y())

        self.setPos(x, y)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def roundPos(self, num, base=5):
        return int(base * round(float(num) / base))


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class customBorderItem(pickerBorderItem):
    def __init__(self, x, y, w, h, brush, moduleName, niceName=None, menu=None):
        super(customBorderItem, self).__init__(x, y, w, h, brush, moduleName)
        self.setData(99, "custom")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class pickerButton(QtWidgets.QGraphicsItem):
    def __init__(self, width, height, relativePos, controlObj, brush, parent=None):

        super(pickerButton, self).__init__(parent)

        self.parentItem().setZValue(1)
        self.setZValue(2)

        self.brush = QtGui.QBrush(brush)
        self.brushColor = brush

        self.width = width
        self.height = height
        self.relativePos = relativePos
        self.object = controlObj

        self.setPos(self.parentItem().boundingRect().topLeft())
        self.setPos(self.pos().x() + self.relativePos[0], self.pos().y() + self.relativePos[1])
        self.menu = QtWidgets.QMenu()

        self.classType = "pickerButton"

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def boundingRect(self):
        rect = QtCore.QRectF(0, 0, self.width, self.height)
        return rect

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def paint(self, painter, option, widget):
        rec = self.boundingRect()

        blackPen = QtGui.QPen(QtCore.Qt.black)
        blackPen.setWidth(1)
        painter.setPen(blackPen)

        painter.fillRect(rec, self.brush)
        painter.drawRect(rec)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def mousePressEvent(self, event):

        mods = cmds.getModifiers()
        if (mods & 1) > 0:
            cmds.select(self.object, tgl=True)
        if (mods & 1) == 0:
            cmds.select(self.object)

        if self.object in cmds.ls(sl=True):

            self.brush.setColor(QtCore.Qt.white)

        else:
            self.brush.setColor(self.brushColor)

        self.update()
        QtWidgets.QGraphicsItem.mousePressEvent(self, event)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def mousePressEventCustom(self, event):

        cmds.select(self.object, tgl=True)
        self.brush.setColor(self.brushColor)
        self.update()
        QtWidgets.QGraphicsItem.mousePressEvent(self, event)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def mouseMoveEvent(self, event):
        print "mouse move event"

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def dragMoveEvent(self, event):
        print "drag move event"

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def hoverMoveEvent(self, event):
        print "hover move event"

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def contextMenuEvent(self, event):
        self.addSpaces()
        self.menu.exec_(event.screenPos())

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addSpaces(self):
        pass

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class pickerButtonCustom(QtWidgets.QGraphicsPolygonItem):
    def __init__(self, width, height, pointArray, relativePos, controlObj, brush, parent=None):

        super(pickerButtonCustom, self).__init__(parent)

        self.parentItem().setZValue(1)
        self.setZValue(2)

        self.brush = QtGui.QBrush(brush)
        self.brushColor = brush
        self.pointArray = pointArray
        self.poly = self.createPolygon()
        self.setPolygon(self.poly)

        # position item
        self.relativePos = relativePos
        self.object = controlObj
        self.setPos(self.parentItem().boundingRect().topLeft())
        self.setPos(self.pos().x() + self.relativePos[0], self.pos().y() + self.relativePos[1])

        # create menu
        self.menu = QtWidgets.QMenu()
        self.classType = "pickerButton"

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def createPolygon(self):
        polygon = QtGui.QPolygonF()
        for each in self.pointArray:
            polygon.append(QtCore.QPointF(each[0], each[1]))
        return polygon

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def paint(self, painter, option, widget):

        blackPen = QtGui.QPen(QtCore.Qt.black)
        blackPen.setWidth(1)
        painter.setPen(blackPen)

        painter.setBrush(self.brush)
        painter.drawPolygon(self.polygon())

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def mousePressEvent(self, event):

        mods = cmds.getModifiers()
        if (mods & 1) > 0:
            cmds.select(self.object, tgl=True)
        if (mods & 1) == 0:
            cmds.select(self.object)

        if self.object in cmds.ls(sl=True):

            self.brush.setColor(QtCore.Qt.white)

        else:
            self.brush.setColor(self.brushColor)

        self.update()
        QtWidgets.QGraphicsPolygonItem.mousePressEvent(self, event)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def mousePressEventCustom(self, event):

        cmds.select(self.object, tgl=True)
        self.brush.setColor(self.brushColor)
        self.update()
        QtWidgets.QGraphicsItem.mousePressEvent(self, event)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def contextMenuEvent(self, event):
        self.addSpaces()
        self.menu.exec_(event.screenPos())

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def addSpaces(self):
        pass


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class pickerButtonAll(QtWidgets.QGraphicsItem):
    def __init__(self, width, height, relativePos, controlObjects, brush, parent=None):

        super(pickerButtonAll, self).__init__(parent)

        if parent is not None:
            self.parentItem().setZValue(1)
        self.setZValue(2)

        self.brush = QtGui.QBrush(brush)
        self.brushColor = brush

        self.width = width
        self.height = height
        self.relativePos = relativePos
        self.objects = controlObjects

        self.setData(5, self.objects)

        if parent is not None:
            self.setPos(self.parentItem().boundingRect().topLeft())
        self.setPos(self.pos().x() + self.relativePos[0], self.pos().y() + self.relativePos[1])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def boundingRect(self):
        rect = QtCore.QRectF(0, 0, self.width, self.height)
        return rect

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def paint(self, painter, option, widget):
        rec = self.boundingRect()

        blackPen = QtGui.QPen(QtCore.Qt.black)
        blackPen.setWidth(1)
        painter.setPen(blackPen)

        painter.fillRect(rec, self.brush)
        painter.drawRect(rec)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def mousePressEvent(self, event):

        mods = cmds.getModifiers()
        if (mods & 1) > 0:
            for obj in self.objects:
                cmds.select(obj, add=True)

        if (mods & 1) == 0:
            cmds.select(clear=True)
            for obj in self.objects:
                cmds.select(obj, tgl=True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def contextMenuEvent(self, event):
        self.menu.exec_(event.screenPos())

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class ScriptButton(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, width, height, relativePos, script, script_type, path, image=None, parent=None):

        super(ScriptButton, self).__init__(parent)

        if parent is not None:
            self.parentItem().setZValue(1)
        self.setZValue(5)

        self.setData(QtCore.Qt.UserRole, path)
        self.image = image
        self.width = width
        self.height = height
        self.relativePos = relativePos
        self.script = script
        self.script_type = script_type

        if self.image is not None:
            self.setPixmap(self.image.scaled(28, 28))

        if parent is not None:
            self.setPos(self.parentItem().boundingRect().topLeft())
        self.setPos(self.pos().x() + self.relativePos[0], self.pos().y() + self.relativePos[1])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def boundingRect(self):
        rect = QtCore.QRectF(0, 0, self.width, self.height)
        return rect

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def mousePressEvent(self, event):

        if self.script_type == "python":
            try:
                exec("" + self.script + "")
            except:
                pass

        if self.script_type == "mel":
            try:
                import maya.mel as mel
                mel.eval(self.script)
            except:
                pass


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class UserButton(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, width, height, relativePos, controlObjects, brush, path, image=None, parent=None):

        super(UserButton, self).__init__(parent)

        if parent is not None:
            self.parentItem().setZValue(1)
        self.setZValue(5)

        self.brush = QtGui.QBrush(brush)
        self.brushColor = brush

        self.setData(QtCore.Qt.UserRole, path)

        self.image = image
        self.width = width
        self.height = height
        self.relativePos = relativePos
        self.objects = controlObjects

        self.setData(5, self.objects)

        if self.image is not None:
            self.setPixmap(self.image.scaled(28, 28))

        if parent is not None:
            self.setPos(self.parentItem().boundingRect().topLeft())
        self.setPos(self.pos().x() + self.relativePos[0], self.pos().y() + self.relativePos[1])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def boundingRect(self):
        rect = QtCore.QRectF(0, 0, self.width, self.height)
        return rect

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def mousePressEvent(self, event):

        mods = cmds.getModifiers()
        if (mods & 1) > 0:
            for obj in self.objects:
                cmds.select(obj, add=True)

        if (mods & 1) == 0:
            cmds.select(clear=True)
            for obj in self.objects:
                cmds.select(obj, tgl=True)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class DialogMessage(QtWidgets.QMainWindow):
    def __init__(self, title, message, elementList, elementSize, parent=None):
        super(DialogMessage, self).__init__(parent)

        # get the directory path of the
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.toolsPath = settings.value("toolsPath")
        self.iconsPath = settings.value("iconPath")

        # load stylesheet
        style = get_style_sheet("artv2_style")
        self.setStyleSheet(style)

        # size policies
        mainSizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        # create the main widget
        self.mainWidget = QtWidgets.QWidget()
        self.setCentralWidget(self.mainWidget)

        # set qt object name
        self.setObjectName("pyART_customDialogMessageWin")
        self.setWindowTitle(title)

        # create the mainLayout for the rig creator UI
        self.mainLayout = QtWidgets.QVBoxLayout(self.mainWidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.resize(300, 200)
        self.setSizePolicy(mainSizePolicy)
        self.setMinimumSize(QtCore.QSize(300, 200))
        self.setMaximumSize(QtCore.QSize(300, 200))

        # create the background image
        self.frame = QtWidgets.QFrame()
        self.mainLayout.addWidget(self.frame)

        # create the layout for the widgets
        self.widgetLayout = QtWidgets.QVBoxLayout(self.frame)

        # add the message to the layout
        self.messageArea = QtWidgets.QTextEdit()
        self.messageArea.setReadOnly(True)
        self.widgetLayout.addWidget(self.messageArea)

        self.messageArea.setTextColor(QtGui.QColor(236, 217, 0))
        self.messageArea.append(message + "\n\n")

        string = ""
        for each in elementList:
            for i in range(elementSize):
                string += each[i] + " "

            self.messageArea.setTextColor(QtGui.QColor(255, 255, 255))
            self.messageArea.append(string)

        # add the OK button
        self.confirmButton = QtWidgets.QPushButton("OK")
        self.confirmButton.setObjectName("blueButton")
        self.widgetLayout.addWidget(self.confirmButton)
        self.confirmButton.clicked.connect(self.closeWindow)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    def closeWindow(self):

        cmds.deleteUI("pyART_customDialogMessageWin", wnd=True)


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class baseWindow(QtWidgets.QMainWindow):
    """
    Base ARTv2 window that loads the stylesheet, adds a window icon, and gets the settings of the directory paths.
    """

    def __init__(self, min_width, min_height, max_width, max_height, parent=None):

        super(baseWindow, self).__init__(parent)

        # Get the directory path values for the tools.
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.tools_path = settings.value("toolsPath")
        self.script_path = settings.value("scriptPath")
        self.icons_path = settings.value("iconPath")
        self.project_path = settings.value("projectPath")

        # Set the window icon.
        window_icon = QtGui.QIcon(os.path.join(self.icons_path, "System/logo.png"))
        self.setWindowIcon(window_icon)

        # Apply the style sheet.
        self.style_sheet = get_style_sheet("artv2_style")
        self.setStyleSheet(self.style_sheet)

        # set the window size
        self.setMinimumSize(QtCore.QSize(min_width, min_height))
        self.setMaximumSize(QtCore.QSize(max_width, max_height))


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class baseDialog(QtWidgets.QDialog):
    """
    Base ARTv2 window that loads the stylesheet, adds a window icon, and gets the settings of the directory paths.
    """

    def __init__(self, min_width, min_height, max_width, max_height, parent=None):

        super(baseDialog, self).__init__(parent)

        # Get the directory path values for the tools.
        settings = QtCore.QSettings("Epic Games", "ARTv2")
        self.tools_path = settings.value("toolsPath")
        self.script_path = settings.value("scriptPath")
        self.icons_path = settings.value("iconPath")
        self.project_path = settings.value("projectPath")

        # Set the window icon.
        window_icon = QtGui.QIcon(os.path.join(self.icons_path, "System/logo.png"))
        self.setWindowIcon(window_icon)

        # Apply the style sheet.
        self.style = get_style_sheet("artv2_style")
        self.setStyleSheet(self.style)

        # set the window size
        self.setMinimumSize(QtCore.QSize(min_width, min_height))
        self.setMaximumSize(QtCore.QSize(max_width, max_height))
