from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class Extended3DGraph(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = '3D Plot with Extra Features'
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 600
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlabel('Distance')
        self.ax.set_ylabel('Lateral Deviation')
        self.ax.set_zlabel('Height')
        self.ax.set_xlim(-1000, 1000)
        self.ax.set_ylim(-500, 500)
        self.ax.set_zlim(0, 1000)
        self.ax.plot([-1000, 1000], [0, 0], [0, 0], color='black')
        self.ax.plot([0, 0], [-1000, 1000], [0, 0], color='black')
        self.ax.plot([0, 0], [0, 0], [0, 1000], color='black')

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        # Add extra features here

        self.show()

    def plot_3d_line(self, init, end, line_color):
        xs = [init[0], end[0]]
        ys = [init[1], end[1]]
        zs = [init[2], end[2]]
        self.ax.plot(xs, ys, zs, color=line_color)
        self.canvas.draw()