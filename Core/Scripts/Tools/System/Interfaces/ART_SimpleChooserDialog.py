import Utilities.interfaceUtils as interfaceUtils
from ThirdParty.Qt import QtWidgets


class SimpleChooser(interfaceUtils.baseDialog):
    """
    Create a simple dialog that displays a message and has a comboBox populated with the passed in choices.
    Lastly, a push button will set the instance of the class's result attribute to the choice.
    """
    def __init__(self, title, message, choices, parent=None):
        """

        :param str title: Window title
        :param str message: message for the QLabel to display.
        :param choices: a list of choices to populate the QComboBox with.
        :param parent: The parent widget of this dialog.

        :type choices: string array
        :type parent: QWidget
        """

        super(SimpleChooser, self).__init__(200, 150, 200, 150, parent)

        self.result = None
        self._build_interface(title, message, choices)

    def _build_interface(self, title, message, choices):

        self.setWindowTitle(title)

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        label = QtWidgets.QLabel(message)
        label.setWordWrap(True)
        layout.addWidget(label)

        self.combo_box = QtWidgets.QComboBox()
        layout.addWidget(self.combo_box)

        for choice in choices:
            self.combo_box.addItem(choice)

        button = QtWidgets.QPushButton("Okay")
        button.setObjectName("settings")
        button.setMinimumHeight(30)
        layout.addWidget(button)
        button.clicked.connect(self._set_choice)

        self.exec_()

    def _set_choice(self):
        self.result = self.combo_box.currentText()
        self.accept()
