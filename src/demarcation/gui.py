from PyQt5 import QtCore, QtGui, QtWidgets

from . import highlighter, icon


class EditorWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("QWidget { font-size: 30px; }")

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.setup_ui()
        self.setup_editor()

    def setup_ui(self):
        self.text_box = QtWidgets.QPlainTextEdit(self)
        self.text_box.resize(self.size())
        self.text_box.setFont(QtGui.QFont("Consolas"))
        self.text_box.setStyleSheet("background-color: #232323; color: white;")  # noqa

    def setup_editor(self):
        self.highlighter = highlighter.new_highlighter()
        self.highlighter.setDocument(self.text_box.document())

    def resizeEvent(self, new: QtGui.QResizeEvent) -> None:
        self.text_box.resize(new.size())


class EditorAppWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__(parent=None)

        self.setWindowTitle("Demarcation")

        p = QtGui.QPixmap()
        p.loadFromData(icon.icon_data)

        self.setWindowIcon(QtGui.QIcon(p))  # noqa

        e = EditorWidget()

        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.GlobalColor.darkGray)

        self.setCentralWidget(e)

        self.setup_menu()

    def setup_menu(self):
        menu_bar = self.menuBar()

        file_menu = QtWidgets.QMenu("&File", self)
        edit_menu = menu_bar.addMenu("&Edit")          # noqa NOSONAR
        scts_menu = menu_bar.addMenu("&Shortcuts")     # noqa NOSONAR
        help_menu = menu_bar.addMenu("&Help")          # noqa NOSONAR

        open_action = QtWidgets.QAction("Open", self)
        save_action = QtWidgets.QAction("Save", self)

        open_action.triggered.connect(self.open_file)
        save_action.triggered.connect(self.save_file)

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)

    def open_file(self):
        print("Opening file...")

    def save_file(self):
        print("Saving file...")
