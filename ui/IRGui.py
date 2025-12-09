import sys
import numpy as np
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QApplication
from ui.IRGuiUI import Ui_IrDialog
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure


class IRWindow(QDialog):
    def __init__(self, ccdata, parent=None):
        super().__init__(parent)

        self.ui = Ui_IrDialog()
        self.ui.setupUi(self)

        self.ccdata = ccdata

        self.figure = Figure(figsize=(10, 4))
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot(111)

        layout = self.ui.widget.layout()
        if layout is None:
            layout = QVBoxLayout(self.ui.widget)
            self.ui.widget.setLayout(layout)

        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        # Dibujar espectro inicial
        self.plot_spectrum()

        # Conectar slider a actualización del espectro
        self.ui.gaussslider.valueChanged.connect(self.update_gaussian_width)

    def compute_spectrum(self, sigma):
        freqs = np.array(self.ccdata.vibfreqs)
        ints = np.array(self.ccdata.vibirs)

        wavelength = np.linspace(4000, 0, 8000)
        absorbance = np.zeros_like(wavelength)

        for f, I in zip(freqs, ints):
            absorbance += I * np.exp(-0.5 * ((wavelength - f) / sigma) ** 2)

        # Normalización
        absorbance /= absorbance.max()

        transmittance = 1.0 - absorbance
        return wavelength, transmittance

    def style_axes(self):
        """Aplica formato estándar al gráfico IR."""
        self.ax.set_xlim(4000, 400)
        self.ax.set_ylim(-0.2, 1.01)
        self.ax.set_xlabel("Wavenumber (cm$^{-1}$)")
        self.ax.set_ylabel("Intensity")
        # Ticks mayores cada 200
        major_ticks = np.arange(400, 4001, 200)
        self.ax.set_xticks(major_ticks)

        # Ticks menores cada 100 (sin etiquetas)
        minor_ticks = np.arange(400, 4001, 100)
        self.ax.set_xticks(minor_ticks, minor=True)

        # Ocultar números de ticks menores
        self.ax.tick_params(axis='x', which='minor', labelbottom=False)

        # Estética opcional: hacer ticks más visibles
        self.ax.tick_params(axis='x', which='major', length=7, width=1)
        self.ax.tick_params(axis='x', which='minor', length=4, width=0.8)

        # Grid suave (si lo deseas)
        self.ax.grid(True, linestyle="--", alpha=0.3)

    def plot_spectrum(self):
        sigma = self.ui.gaussslider.value()
        x, y = self.compute_spectrum(sigma)

        self.ax.clear()
        self.ax.plot(x, y, color='black', linewidth=1.2)
        self.style_axes()
        self.figure.tight_layout()
        self.canvas.draw()

    def update_gaussian_width(self, value):
        self.ui.widthlabel.setText(str(value))
        x, y = self.compute_spectrum(value)

        self.ax.clear()
        self.ax.plot(x, y, color='black', linewidth=1.2)
        self.style_axes()
        self.figure.tight_layout()
        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    x = np.linspace(4000, 400, 1000)
    y = np.exp(-((x - 1700)**2)/(2*25**2))

    window = IRWindow((x, y))
    window.show()

    sys.exit(app.exec())
