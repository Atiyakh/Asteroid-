from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
import sys

from codeblocks import CodeBlocks, ConnectorsLookup, GLOBAL_SCALE_VAR

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # main window
    main_window = QMainWindow()
    main = QWidget()
    main_layout = QHBoxLayout(main)
    main_window.setCentralWidget(main)
    # code blocks
    codeblocks = CodeBlocks()
    connectors_lookup = ConnectorsLookup()
    GLOBAL_SCALE_VAR['main-window'] = codeblocks
    GLOBAL_SCALE_VAR['connectors-lookup'] = connectors_lookup
    codeblocks.setMinimumSize(1000, 600)
    main_layout.addWidget(codeblocks)
    main_window.show()
    app.exec()
