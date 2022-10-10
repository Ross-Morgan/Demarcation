import os
import pathlib

from PyQt6 import QtCore, QtGui, QtWidgets

from . import highlighter
from .logger import AppLogger

logger = AppLogger("logger")


class EditorWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setStyleSheet("QWidget { font-size: 30px; }")

        self.font_size = 30

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

        self.setWindowIcon(QtGui.QIcon(os.path.normpath(f"{__file__}/../../../assets/demarcation-logo.png")))  # noqa

        self.editor = EditorWidget()

        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.GlobalColor.darkGray)

        self.setCentralWidget(self.editor)

        self.setup_menu()

    def setup_menu(self):
        menu_bar = QtWidgets.QMenuBar()

        open_action = QtGui.QAction("Open", self)
        open_action.setShortcut("ctrl+o")

        save_action = QtGui.QAction("Save", self)
        save_action.setShortcut("ctrl+s")

        save_as_action = QtGui.QAction("Save As", self)
        save_as_action.setShortcut("ctrl+shift+s")

        quit_action = QtGui.QAction("Quit", self)
        quit_action.setShortcut("ctrl+shift+q")

        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(quit_action)

        file_menu.triggered.connect(self.handle_file_event)

        self.setMenuBar(menu_bar)

    def handle_file_event(self, action: QtGui.QAction):
        match action.text().lower():
            case "quit":
                self.close()
            case "open":
                self.open_file()
            case "save":
                self.save_file()
            case _:
                logger.error(f"Unhandled file event: '{action.text()}'")

    def open_file(self):
        dialog = QtWidgets.QFileDialog.getOpenFileName(directory=os.path.normpath(f"{pathlib.Path.home()}/Documents/"))  # noqa

        open_path = dialog[0]

        with open(open_path, "r") as f:
            self.editor.text_box.setPlainText(f.read())

    def save_file(self):
        dialog = QtWidgets.QFileDialog.getSaveFileName(directory=os.path.normpath(f"{pathlib.Path.home()}/Documents/untitled.bml"))  # noqa

        save_path = dialog[0]

        with open(save_path, "w") as f:
            f.write(self.editor.text_box.toPlainText())
