from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyshorteners
import sys
import os
import pyperclip

try:
    from PyQt5.QtWinExtras import QtWin
    myappid = 'shorten.url.python.program'
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)    
except ImportError:
    pass

def resource_path(relative_path):
    """used by pyinstaller to see the relative path"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)

urlGui = resource_path("./gui/main.ui")
urlLogo = resource_path("./gui/logo.png")
appbg = resource_path("./gui/bg.png")

class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        UIFile = QFile(urlGui)
        UIFile.open(QFile.ReadOnly)
        uic.loadUi(UIFile, self)
        UIFile.close()

        self.URL = pyshorteners.Shortener()
        bgapp = QPixmap(appbg)
        self.bg.setPixmap(bgapp)
        self.providedUrl.setStatusTip("Insert URL that you want to shorten!")
        self.createUrl.clicked.connect(self.cmdCreateShortUrl)
        self.createUrl.setStatusTip("Shorten the url with tinyurl!")
        self.urlOutput.setStatusTip("The shortened url!")
        self.copyLink.setStatusTip("Copy the link to the clipboard!")
        self.copyLink.clicked.connect(self.cmdCopyLink)

    def cmdCreateShortUrl(self):
        shorten = self.providedUrl.text()
        try:
            result = self.URL.tinyurl.short(shorten)
            self.urlOutput.setText(result)
        except Exception:
            pass

    def cmdCopyLink(self):
        pyperclip.copy(self.urlOutput.text())
        self.msgbox("Link copied to clipboard!")
    
    def msgbox(self, message):
        QMessageBox.information(self, "Information!", message)

style = '''
QMenuBar,
QPushButton,
QComboBox,
QLineEdit,
QMessageBox QPushButton {
    background-color: #eeeeee;
    border: 3px;
    border-color: #000000;
}

QMessageBox {
    color: #000000;
    background-color: #FFFFFF;
}
QMessageBox QLabel {
    color: #222831;
}
QPushButton:focus,
QLineEdit:focus,
QComboBox:focus {
    color: #000000;
    selection-background-color: #222831;
    background-color: #FFFFFF;
    border: none;
}  

QLabel {
    color: #eeeeee;
}

QComboBox QAbstractItemView {
    selection-color: #FED369;
    selection-background-color: #222831;
    background-color: #eeeeee;
}

QPushButton:hover,
QLineEdit:hover,
QComboBox:hover,
QMessageBox QPushButton {
    color: #000000;
    selection-background-color: #222831;
    background-color: #FFFFFF;
}  
QPushButton:pressed {
    color: #000000;
    background-color: #FFFFFF;
}  
'''


app = QApplication(sys.argv)
app.setWindowIcon(QIcon(urlLogo))
app.setStyleSheet(style) 
window = GUI()
window.show()
app.exec_()