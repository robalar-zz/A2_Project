from main import MainWindow
from input import input_window

from PyQt4 import QtGui, QtCore
import sys

from solver.core.parser import parse
from solver.formating.mathjax import ascii_math

class Window(MainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.compute_button.clicked.connect(self.parse)

        self.show()

    def parse(self):
        inp = str(self.input_line.text())
        parsed_inp_html = ascii_math(parse(inp))

        bin_dir = QtCore.QUrl('file:///A2_Project/bin/')

        try:
            self.inp_window.inp_webview.setHtml(parsed_inp_html, bin_dir)
        except AttributeError:
            self.inp_window = input_window(self)
            self.verticalLayout.addWidget(self.inp_window)
            self.inp_window.inp_webview.setHtml(parsed_inp_html, bin_dir)


app = QtGui.QApplication(sys.argv)
gui = Window()
sys.exit(app.exec_())