import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QBasicTimer

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initWidget()

    def initWidget(self):
        #Button
        self.AButton = QPushButton('Import input Data')
        self.BButton = QPushButton('Model Learning')
        self.CButton = QPushButton('Produce TTS')

        #TODO: log 관련

        #TODO: button action AButton

        #TODO: button action BButton

        #TODO: button action CButton


        #button layout
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.AButton)
        hbox.addWidget(self.BButton)
        hbox.addWidget(self.CButton)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        self.setLayout(vbox)


        self.setWindowTitle('MPSinger_Widget')
        self.show()


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        wg = MyApp()
        self.setCentralWidget(wg)
        self.initUI()

    def initUI(self):
        #status Bar
        self.statusBar().showMessage('Main page')

        #Action defined
        exitAction = QAction(QIcon('exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        # menu Bar
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)
        #TODO: File Action
        filemenu = menubar.addMenu('&Edit')
        #TODO: Edit Action

        # Tool Bar
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

        #Window Attribute
        self.setWindowTitle('MPSinger')
        self.setGeometry(300, 300, 600, 600)
        self.show()







if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyMainWindow()
   sys.exit(app.exec_())