from PyQt6 import QtCore, QtGui, QtWidgets

from . import highlighter, icon
from .logger import AppLogger


logger = AppLogger("logger")


class EditorWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("QWidget { font-size: 30px; }")

        self.font_size = 30

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

        self.setMinimumSize(640, 480)

        p = QtGui.QPixmap()
        p.loadFromData(icon.icon_data)

        self.setWindowIcon(QtGui.QIcon(p))  # noqa

        e = EditorWidget()

        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.GlobalColor.darkGray)

        self.setCentralWidget(e)

        self.setup_menu()

    def setup_menu(self):
        grid = QtWidgets.QGridLayout()

        menu_bar = QtWidgets.QMenuBar()
        grid.addWidget(menu_bar, 0, 0)

        open_action = QtGui.QAction("Open")
        open_action.setShortcut("ctrl+o")

        save_action = QtGui.QAction("Save")
        save_action.setShortcut("ctrl+s")

        save_as_action = QtGui.QAction("Save As")
        save_as_action.setShortcut("ctrl+shift+s")

        quit_action = QtGui.QAction("Quit")
        quit_action.setShortcut("ctrl+shift+q")

        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(quit_action)

        file_menu.triggered.connect(self.handle_file_event)

        self.setLayout(grid)

    def handle_file_event(self, action: QtGui.QAction):
        match action.text().lower():
            case "open":
                self.open_file()
            case "save":
                self.save_file()
            case _:
                logger.error(f"Unhandled file event: '{action.text()}'")

    def open_file(self):
        print("Opening file...")

    def save_file(self):
        dialog = QtWidgets.QFileDialog.getOpenFileName(directory="~")

        print(dialog)
