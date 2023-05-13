import math
import sys
import random
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QLineEdit, QTextEdit
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


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

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        coord_input_layout = QHBoxLayout()
        layout.addLayout(coord_input_layout)

        self.angle_input = QLineEdit()
        coord_input_layout.addWidget(QLabel('Angle (degrees):'))
        coord_input_layout.addWidget(self.angle_input)

        self.radius_input = QLineEdit()
        coord_input_layout.addWidget(QLabel('Radius:'))
        coord_input_layout.addWidget(self.radius_input)

        self.distance_input = QLineEdit()
        coord_input_layout.addWidget(QLabel('Distance:'))
        coord_input_layout.addWidget(self.distance_input)

        self.course_input = QLineEdit()
        coord_input_layout.addWidget(QLabel('Course:'))
        coord_input_layout.addWidget(self.course_input)

        self.init_z_input = QLineEdit()
        coord_input_layout.addWidget(QLabel('Initial Z:'))
        coord_input_layout.addWidget(self.init_z_input)

        self.dive_angle_input = QLineEdit()
        coord_input_layout.addWidget(QLabel('Dive Angle (degrees):'))
        coord_input_layout.addWidget(self.dive_angle_input)

        self.target_radius_input = QLineEdit()
        coord_input_layout.addWidget(QLabel('Target Radius:'))
        coord_input_layout.addWidget(self.target_radius_input)

        add_line_button = QPushButton('Add Line')
        add_line_button.clicked.connect(self.add_line)
        coord_input_layout.addWidget(add_line_button)

        self.fig_3d = plt.figure()

        self.ax = self.fig_3d.add_subplot(121, projection='3d')

        self.ax.set_xlabel('Distance')
        self.ax.set_ylabel('Lateral Deviation')
        self.ax.set_zlabel('Height')
        self.ax.set_xlim(0, 1000)
        self.ax.set_ylim(-100, 100)
        self.ax.set_zlim(0, 1000)

        layout.addWidget(self.fig_3d.canvas)

        self.ax_2d = self.fig_3d.add_subplot(122)
        self.ax_2d.set_xlabel('Distance')
        self.ax_2d.set_ylabel('Lateral Deviation')
        self.ax_2d.set_xlim(0, 1000)
        self.ax_2d.set_ylim(-100, 100)

        layout.addWidget(self.fig_3d.canvas)

        layout.addWidget(self.coords_log)

        self.std_dev_label = QLabel('STD: x={:.2f}, y={:.2f}, z={:.2f}'.format(*self.std_devs))
        layout.addWidget(self.std_dev_label)

        self.show()
        self.show()

    def add_line(self):
        angle = math.radians(float(self.angle_input.text()))
        radius = float(self.radius_input.text())
        distance = float(self.distance_input.text())
        course = math.radians(float(self.course_input.text()))
        init_z = float(self.init_z_input.text())
        dive_angle = math.radians(float(self.dive_angle_input.text()))
        target_radius = float(self.target_radius_input.text())

        end_x = distance + radius * math.cos(angle - course)
        end_y = math.sin(angle - course) * radius
        end_z = 0

        end = (end_x, end_y, end_z)

        image_x = (end_x-distance) * math.sin(dive_angle)

        line_color = (random.random(), random.random(), random.random())

        self.coords.append((end, line_color))

        self.plot_3d_line(init_z, end, line_color)
        self.draw_2d_line(end, len(self.coords), line_color)
        self.draw_2d_circle(distance ,target_radius)

        log_entry = f"Line {len(self.coords)}: ({distance}, {init_z}, 0) -> {end}\n"
        self.coords_log.append(log_entry)

        self.coords_log.append(f" X: {end_x-distance:.2f}")
        self.coords_log.append(f" Y: {end_y:.2f}")
        self.coords_log.append(f" Image X: {image_x:.2f}")

        self.update_std_devs(end)

        self.std_dev_label.setText('STD: x={:.2f}, y={:.2f}, z={:.2f}'.format(*self.std_devs))

    def update_std_devs(self, new_coords):
        coords_array = np.array([end for end, color in self.coords])

        coords_array = np.vstack((coords_array, new_coords))

        self.std_devs = np.std(coords_array, axis=0)

    def plot_3d_line(self, initZ, end, line_color):
        xs = [0, end[0]]
        ys = [0, end[1]]
        zs = [initZ, end[2]]
        self.ax.plot(xs, ys, zs, color=line_color)

        self.fig_3d.canvas.draw()

    def draw_2d_line(self, end, index, line_color):
        xs = end[0]
        zs = end[1]
        self.ax_2d.scatter(xs, zs, color=line_color, marker='o')

        self.fig_3d.canvas.draw()

    def draw_2d_circle(self, distance, radius):
        circle = plt.Circle((distance, 0), radius, color='r', fill=False)
        self.ax_2d.add_artist(circle)
        self.fig_3d.canvas.draw()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())