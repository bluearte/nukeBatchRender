from Qt import QtWidgets
from Qt import QtGui
from Qt import QtCore
import time
import sys
import os


class RenderThread(QtCore.QThread):
    def __init__(self, location, selected):
        super(RenderThread, self).__init__()
        self.location = location
        self.selected = selected

    def run(self):
        for each in self.selected:
            try:
                each.setForeground(QtCore.Qt.green)
                fullpath = os.path.join(self.location, each.text())
                os.system("C:\\PrivateFolder\\_launcher\\Nuke10.0v1_backgroundRender.bat {}".format(fullpath))
                each.setForeground(QtCore.Qt.gray)
            except Exception as e:
                print(e)
            else:
                each.setForeground(QtCore.Qt.red)
            finally:
                print("Done!!!")

class NukescriptListWidget(QtWidgets.QListWidget):
    def __init__(self, nukescripts=None, parent=None):
        super(NukescriptListWidget, self).__init__(parent)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

class NukeWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(NukeWidget, self).__init__(parent)
        epi_label = QtWidgets.QLabel()
        self._epi_combo = QtWidgets.QComboBox()
        self._epi_combo.addItems([])
        sequence_label = QtWidgets.QLabel()
        self._sequence_combo = QtWidgets.QComboBox()
        self._sequence_combo.addItems([])
        shot_label = QtWidgets.QLabel()
        self._shot_combo = QtWidgets.QComboBox()
        self._shot_combo.addItems([])

        epi_combo_layout = QtWidgets.QVBoxLayout()
        epi_combo_layout.addWidget(self.epi_label)
        epi_combo_layout.addWidget(self.epi_combo)

        seq_combo_layout = QtWidgets.QVBoxLayout()
        seq_combo_layout.addWidget(self.sequence_label)
        seq_combo_layout.addWidget(self.sequence_combo)

        shot_combo_layout = QtWidgets.QVBoxLayout()
        shot_combo_layout.addWidget(self.shot_label)
        shot_combo_layout.addWidget(self.shot_combo)

        combo_layout = QtWidgets.QHBoxLayout()
        combo_layout.addLayout(epi_combo_layout)
        combo_layout.addLayout(seq_combo_layout)
        combo_layout.addLayout(shot_combo_layout)

        self._nk_list = NukescriptListWidget()

        self._render_button = QtWidgets.QPushButton()
        self._render_button.setText("Render")
        self._render_button.setEnabled(False)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(combo_layout)
        main_layout.addWidget(self.nk_list)
        main_layout.addWidget(self.render_button)

        self._epi_combo.currentIndexChanged[str].connect(self._change_shot)
        self._sequence_combo.currentIndexChanged[str].connect(self._change_shot)
        self._shot_combo.currentIndexChanged[str].connect(self._change_shot)
        self._render_button.clicked.connect(self._render_selected)
    
    def _change_shot(self):
        pass

    def _render_selected(self):
        location = ""
        self.renderThread = RenderThread(location, self.nk_list.selectedItems())
        self.renderThread.start()


def main():
    app = QtWidgets.QApplication(sys.argv)
    nuke = NukeWidget()
    nuke.show()
    sys.exit(app.exec_())
