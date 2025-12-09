from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication, QFileDialog
from ui.MainGuiui import Ui_analyzer
from ui.IRGui import IRWindow
from geometry.molviewer import MolecularViewer
from geometry.compchem import xyz_from_cclib
import sys


class MainWindow(QMainWindow, Ui_analyzer):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        layout =QVBoxLayout(self.molviewer)
        self.viewer = MolecularViewer(self.molviewer)
        layout.addWidget(self.viewer)

        # Computational
        self.calc_data = ''


        # Signals and slots
        self.actionOpen.triggered.connect(self.open)
        self.actionIR.triggered.connect(self.irspectrum)

    def open(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Select file', '', 'All files (*)')
        if filename:
            xyz, data = xyz_from_cclib(filename)
            self.calc_data = data
            self.viewer.load_xyz(xyz)

    def irspectrum(self):
        irspectrumwindow = IRWindow(self.calc_data, parent=self)
        irspectrumwindow.exec()



if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
