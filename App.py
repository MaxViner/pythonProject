import sys
import math
import random
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QLineEdit, QTextEdit, \
    QTableWidgetItem, QHeaderView, QTableWidget
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from CalculationsTable import CalculationsTable
from Extended3DGraph import Extended3DGraph
from Polar2DGraph import Polar2DGraph
from ThreeDGraph import ThreeDGraph

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = '2D and 3D Plots'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.coords_log = QTextEdit()
        self.coords = []
        self.std_devs = [0, 0, 0]
        self.init_ui()
        self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.mean_coords = [0, 0, 0]

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        layout = QVBoxLayout()
        self.setLayout(layout)

        coord_input_layout = QHBoxLayout()
        layout.addLayout(coord_input_layout)

        self.distance_input = QLineEdit()
        coord_input_layout.addWidget(QLabel('Distance:'))
        coord_input_layout.addWidget(self.distance_input)
        self.distance_input.setStyleSheet("font-size: 20px")

        self.course_input = QLineEdit()
        coord_input_layout.addWidget(QLabel('Course:'))
        coord_input_layout.addWidget(self.course_input)
        self.course_input.setStyleSheet("font-size: 20px")

        self.init_z_input = QLineEdit()
        coord_input_layout.addWidget(QLabel('Initial Z:'))
        coord_input_layout.addWidget(self.init_z_input)
        self.init_z_input.setStyleSheet("font-size: 20px")

        coord_input_layout2 = QHBoxLayout()
        layout.addLayout(coord_input_layout2)

        self.angle_input = QLineEdit()
        coord_input_layout2.addWidget(QLabel('Angle (degrees):'))
        coord_input_layout2.addWidget(self.angle_input)
        self.angle_input.setStyleSheet("font-size: 20px")

        self.radius_input = QLineEdit()
        coord_input_layout2.addWidget(QLabel('Radius:'))
        coord_input_layout2.addWidget(self.radius_input)
        self.radius_input.setStyleSheet("font-size: 20px")

        self.dive_angle_input = QLineEdit()
        coord_input_layout2.addWidget(QLabel('Dive Angle (degrees):'))
        coord_input_layout2.addWidget(self.dive_angle_input)
        self.dive_angle_input.setStyleSheet("font-size: 20px")
        self.target_radius_input = QLineEdit()
        coord_input_layout2.addWidget(QLabel('Target Radius:'))
        coord_input_layout2.addWidget(self.target_radius_input)
        self.target_radius_input.setStyleSheet("font-size: 20px")
        add_line_button = QPushButton('Add Line')
        add_line_button.clicked.connect(self.add_line)
        coord_input_layout2.addWidget(add_line_button)

        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.ax = self.fig.add_subplot(121, projection='3d')
        self.three_d_graph = ThreeDGraph(self.ax)

        self.ax_2d = self.fig.add_subplot(122, polar=True)
        self.polar_2d_graph = Polar2DGraph(self.ax_2d)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.coords_log)
        self.std_dev_label = QLabel('STD: x={:.2f}, y={:.2f}, z={:.2f}'.format(*self.std_devs))
        layout.addWidget(self.std_dev_label)
        self.std_dev_label.setStyleSheet("font-size: 20px")

        self.calculations_table = CalculationsTable(self.coords, self.std_devs, {
            "distance": 0,
            "dive_angle": 0,
            "init_z": 0,
        })

        # добавить кнопку "Открыть в отдельном окне"
        open_in_new_window_button = QPushButton('Открыть в отдельном окне')
        open_in_new_window_button.clicked.connect(self.open_in_new_window)
        layout.addWidget(open_in_new_window_button)

        # Add "Show Calculations" button
        self.show_calculations_button = QPushButton('Показать расчеты')
        self.show_calculations_button.clicked.connect(self.show_calculations)
        layout.addWidget(self.show_calculations_button)
        # Initialize calculations table instance
        self.calculations_table = CalculationsTable(self.coords, self.std_devs)

        self.show()

    def add_line(self):
        angle = math.radians(float(self.angle_input.text()))
        radius = float(self.radius_input.text())
        distance = float(self.distance_input.text())

        course = math.radians(float(self.course_input.text()))
        init_z = float(self.init_z_input.text())
        dive_angle = math.radians(float(self.dive_angle_input.text()))
        target_radius = float(self.target_radius_input.text())
        end_x = distance + radius * math.cos(angle-course)
        end_y = radius * math.sin(angle-course)
        end_z = 0
        init_x = 0
        init_y = 0
        init = (init_x, init_y, init_z)
        line_color = (random.random(), random.random(), random.random())
        end = (end_x, end_y, end_z)
        self.coords.append((end, line_color))
        self.three_d_graph.plot_3d_line(init, end, line_color)
        end_angle = angle - course
        print(end_angle)
        polar_coords = (radius, end_angle)

        self.polar_2d_graph.draw_2d_polar_point(polar_coords)
        self.polar_2d_graph.draw_2d_course_line(course)

        self.three_d_graph.draw_3d_circle(end_x, target_radius)

        Image_x=end_x*math.sin(dive_angle)
        Xt=Image_x*1000/distance
        Yt=end_y*1000/distance
        log_entry = f"Line {len(self.coords)}: Angle-{angle},\n" \
                    f"X={end_x-distance} Z={end_y} Хкарт={Image_x}\n Xт={Xt}  Zt={Yt}\n" \
                    f"Course- {course}, Dive Angle -{dive_angle} ({0}, 0, {init_z})) -> {end}\n"
        self.coords_log.append(log_entry)
        self.coords_log.append(f" X: {end_x:.2f}")
        self.coords_log.append(f" Y: {end_y:.2f}")
        print("Xt Yt")

        # Update calculations table
        self.update_std_devs(end)
        params = {
            "distance": float(self.distance_input.text()),
            "dive_angle": math.radians(float(self.dive_angle_input.text())),
            "init_z": float(self.init_z_input.text()),
            "course": math.radians(float(self.course_input.text())),
        }
        self.update_calculations_table(params)
        self.calculations_table.update_table(self.coords, self.std_devs, params)

        # Add angle labels on the 3D graph
        self.three_d_graph.draw_angle_labels(end_angle)

        std = self.get_std_devs()

        print(std)
    def on_scroll(self, event):
        ax = event.inaxes
        if ax is None:
            return

        scale = 1.2 if event.button == 'up' else 0.8
        ax.set_xlim(ax.get_xlim()[0] * scale, ax.get_xlim()[1] * scale)
        ax.set_ylim(ax.get_ylim()[0] * scale, ax.get_ylim()[1] * scale)
        ax.set_zlim(ax.get_zlim()[0] * scale, ax.get_zlim()[1] * scale)
        self.canvas.draw()

        # функция для открытия графика в отдельном окне с дополнительным функционалом

    def open_in_new_window(self):
        print("Открываем график в отдельном окне...")
        # Create a new instance of the Extended3DGraph class
        extended_graph = Extended3DGraph(self)

        # Copy the existing plot data to the new graph
        for end, line_color in self.coords:
            init = (0, 0, 0)
            extended_graph.plot_3d_line(init, end, line_color)

        # Add any additional features or data to the extended_graph as needed

        extended_graph.show()

    def update_std_devs(self, new_coords):
        coords_array = np.array([end for end, color in self.coords])
        coords_array = np.vstack((coords_array, new_coords))
        self.std_devs = np.std(coords_array, axis=0)
        self.mean_coords = np.mean(coords_array, axis=0)
        self.std_dev_label.setText('STD: x={:.2f}, y={:.2f}, z={:.2f}, Mean: x={:.2f}, y={:.2f}, z={:.2f}'.format(
            *self.std_devs, *self.mean_coords))

    def update_calculations_table(self, params):
        self.calculations_table.update_data(self.coords, self.std_devs, params)
    def get_std_devs(self):
        return self.std_devs


    def show_calculations(self):
        self.calculations_table.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())