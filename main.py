import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QBasicTimer

import os
from os import path
import shutil

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class LogStringHandler(logging.Handler):
    def __init__(self, target_widget):
        super(LogStringHandler, self).__init__()
        self.target_widget = target_widget

    def emit(self, record):
        self.target_widget.append(record.asctime + ' -- ' + record.getMessage())

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initWidget()

    def initWidget(self):
        widgetGrid = QGridLayout()
        widgetGrid.addWidget(self.createInputDataImportGroup(), 0, 0)
        widgetGrid.addWidget(self.createModelLearningGroup(), 1, 0)
        widgetGrid.addWidget(self.createProduceTTSGroup(), 2, 0)

        loggroup = QGroupBox('Event Log')
        self.loggingtext = QTextBrowser()
        hbox = QHBoxLayout()
        hbox.addWidget(self.loggingtext)
        loggroup.setLayout(hbox)

        grid = QGridLayout()
        grid.addLayout(widgetGrid, 0, 0)
        grid.addWidget(loggroup, 0, 1)
        self.setLayout(grid)

        self.setWindowTitle('MPSinger_Widget')
        self.setGeometry(300, 300, 480, 320)
        self.show()

        logger = logging.getLogger()
        logger.addHandler(LogStringHandler(self.loggingtext))


    def createInputDataImportGroup(self):
        groupbox = QGroupBox('Import Input Data')

        self.smode = QRadioButton('By single file')
        self.dmode = QRadioButton('By directory')
        self.smode.setChecked(True)
        self.AButton = QPushButton('Select')
        self.AButton.clicked.connect(self.inputDataImport)

        hbox = QHBoxLayout()
        hbox.addWidget(self.smode)
        hbox.addStretch(1)
        hbox.addWidget(self.dmode)
        hbox.addStretch(3)

        grid = QGridLayout()
        grid.addLayout(hbox, 0, 0)
        grid.addWidget(self.AButton, 0, 1)
        groupbox.setLayout(grid)

        return groupbox

    def createModelLearningGroup(self):
        groupbox = QGroupBox('Model Learning')

        self.pbar = QProgressBar(self)
        self.BButton = QPushButton('Learn')
        # TODO: button action BButton

        hbox = QHBoxLayout()
        hbox.addWidget(self.pbar)

        grid = QGridLayout()
        grid.addLayout(hbox, 0, 0)
        grid.addWidget(self.BButton, 0, 1)
        groupbox.setLayout(grid)

        return groupbox

    def createProduceTTSGroup(self):
        groupbox = QGroupBox('Produce TTS')

        self.Dummybtn = QPushButton(' ')
        self.Dummybtn.setFlat(True)
        self.CButton = QPushButton('Produce')
        # TODO: button action CButton

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.Dummybtn)
        hbox.addStretch(3)

        grid = QGridLayout()
        grid.addLayout(hbox, 0, 0)
        grid.addWidget(self.CButton, 0, 1)
        groupbox.setLayout(grid)

        return groupbox

    def inputDataImport(self):
        reply = QMessageBox.question(self, 'Warning', 'This action will\nremove or overwrite files. continue?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if self.smode.isChecked():
                self.load_singleFile('mid')
                self.load_singleFile('txt')
                self.load_singleFile('wav')
            elif self.dmode.isChecked():
                self.load_directory('mid')
                self.load_directory('txt')
                self.load_directory('wav')

        else:
            print("data import rejected...")

    def load_singleFile(self, file_format):
        title = 'Open ' + file_format
        ffilter = file_format + ' File(*.' + file_format + ');; All File(*)'    #1-1. get source file path
        fname = QFileDialog.getOpenFileName(self, title, './', ffilter)

        if fname[0] != "":
            copy = r'..\mlp-singer\data\raw'            #1-2. get target file path
            copy = copy + '\\' + file_format
            existing_files = os.listdir(copy)           #2. remove existing files
            logging.info('removed files...')
            for file in existing_files:
                if path.exists(copy + '\\' + file):
                    os.unlink(copy + '\\' + file)
                    logging.info('\t' + file)

            shutil.copy(fname[0], copy)                 #3. load src to target
            logging.info('loaded files...')
            logging.info('\t' + os.path.basename(fname[0]))
        else:
            logging.info('skip loading ' + file_format + ' file')

    def load_directory(self, file_format):
        origin, ok = QInputDialog.getText(self, 'Input Path', file_format + " directory path:")   #1-1. get source directory path
        if ok:
            copy = r'..\mlp-singer\data\raw'            #1-2. get target directory path
            copy = copy + '\\' + file_format
            existing_files = os.listdir(copy)           #2. remove existing files
            logging.info('removed files...')
            for file in existing_files:
                if path.exists(copy + '\\' + file):
                    os.unlink(copy + '\\' + file)
                    logging.info('\t' + file)

            files = os.listdir(origin)                  #3. load src to target
            logging.info('loaded files...')
            for file in files:
                if not path.exists(copy + '\\' + file):
                    shutil.copy(origin + '\\' + file, copy + '\\' + file)
                    logging.info('\t' + file)
        else:
            logging.info('skip loading ' + file_format + ' directory')


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
        #self.setGeometry(300, 300, 600, 600)
        self.setGeometry(300, 300, 960, 540)    #compact version
        self.show()


if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyMainWindow()
   sys.exit(app.exec_())