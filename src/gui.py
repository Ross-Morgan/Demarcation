import sys

from PyQt5 import QtWidgets

import demarcation


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = demarcation.gui.EditorAppWindow()
    window.showMaximized()

    app.exec()


if __name__ == "__main__":
    main()
