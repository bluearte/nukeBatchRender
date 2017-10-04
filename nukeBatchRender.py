from PySide.QtCore import *
from PySide.QtGui import *
import time
import sys
import os


class RenderThread(QThread):
    def __init__(self, location, selected):
        super(RenderThread, self).__init__()
        self.location = location
        self.selected = selected

    def run(self):
        for each in self.selected:
            try:
                each.setForeground(Qt.green)
                fullpath = os.path.join(self.location, each.text())
                os.system("C:\\PrivateFolder\\_launcher\\Nuke10.0v1_backgroundRender.bat {}".format(fullpath))
                each.setForeground(Qt.gray)
            except:
                each.setForeground(Qt.red)


class Nuke(QWidget):
    def __init__(self):
        super(Nuke, self).__init__()
        self.setWindowTitle("Nuke Render Manager")
        self.setupUI()

    def setupUI(self):
        self.comboBox = QComboBox()
        comboBoxItems = self.getEpisode()
        self.comboBox.addItems(comboBoxItems)
        self.listWidget = QListWidget()
        listWidgetItems = self.getNukescripts()
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.btn2 = QPushButton()
        self.btn2.setText("Render Selected")

        self.vLayout = QVBoxLayout()
        self.vLayout.addWidget(self.comboBox)
        self.vLayout.addWidget(self.listWidget)
        self.vLayout.addWidget(self.btn2)

        self.setLayout(self.vLayout)

        self.comboBox.currentIndexChanged.connect(self.getNukescripts)
        self.btn2.clicked.connect(self.renderSelected)

    def getNukescripts(self):
        location = "C:\\PrivateFolder\\_projects\\nuke\\" + self.comboBox.currentText()
        listFile = []
        for eachFile in os.listdir(location):
            if os.path.isfile(os.path.join(location, eachFile)):
                if not eachFile.endswith(".nk~"):
                    listFile.append(eachFile)
        try:
            self.listWidget.clear()
        except Exception as e:
            print(e)
        finally:
            self.listWidget.addItems(listFile)

    def getEpisode(self):
        location = "C:\\PrivateFolder\\_projects\\nuke\\"
        listDir = []
        for eachDir in os.listdir(location):
            if os.path.isdir(os.path.join(location, eachDir)):
                listDir.append(eachDir)
        return listDir

    def markSelected(self):
        for each in self.listWidget.selectedItems():
            each.setForeground(Qt.blue)

    def renderSelected(self):
        self.markSelected()
        location = "C:\\PrivateFolder\\_projects\\nuke\\" + self.comboBox.currentText()
        self.renderThread = RenderThread(location, self.listWidget.selectedItems())
        self.renderThread.start()


def main():
    app = QApplication(sys.argv)
    nuke = Nuke()
    nuke.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
