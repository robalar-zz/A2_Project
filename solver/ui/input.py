# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'input.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_input_window(object):
    def setupUi(self, input_window):
        input_window.setObjectName(_fromUtf8("input_window"))
        input_window.resize(738, 274)
        self.centralwidget = QtGui.QWidget(input_window)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setMinimumSize(QtCore.QSize(720, 215))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.inp_webview = QtWebKit.QWebView(self.groupBox)
        self.inp_webview.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.inp_webview.setObjectName(_fromUtf8("inp_webview"))
        self.horizontalLayout.addWidget(self.inp_webview)
        self.verticalLayout.addWidget(self.groupBox)
        input_window.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(input_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 738, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        input_window.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(input_window)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        input_window.setStatusBar(self.statusbar)

        self.retranslateUi(input_window)
        QtCore.QMetaObject.connectSlotsByName(input_window)

    def retranslateUi(self, input_window):
        input_window.setWindowTitle(_translate("input_window", "MainWindow", None))
        self.groupBox.setTitle(_translate("input_window", "Input", None))

from PyQt4 import QtWebKit

class input_window(QtGui.QMainWindow, Ui_input_window):
    def __init__(self, parent=None, f=QtCore.Qt.WindowFlags()):
        QtGui.QMainWindow.__init__(self, parent, f)

        self.setupUi(self)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    input_window = QtGui.QMainWindow()
    ui = Ui_input_window()
    ui.setupUi(input_window)
    input_window.show()
    sys.exit(app.exec_())

