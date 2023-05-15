import sys
import math
import random
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QLineEdit, QTextEdit
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.mplot3d.art3d import Line3DCollection


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

        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.ax = self.fig.add_subplot(121, projection='3d')
        self.ax.set_xlabel('Distance')
        self.ax.set_ylabel('Lateral Deviation')
        self.ax.set_zlabel('Height')
        self.ax.set_xlim(-1000, 1000)
        self.ax.set_ylim(-100, 100)
        self.ax.set_zlim(0, 1000)

        self.ax_2d = self.fig.add_subplot(122, polar=True)
        self.ax_2d.set_theta_zero_location("N")
        self.ax_2d.set_ylim(0, 100)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.coords_log)

        self.std_dev_label = QLabel('STD: x={:.2f}, y={:.2f}, z={:.2f}'.format(*self.std_devs))
        layout.addWidget(self.std_dev_label)

        self.show()

    def add_line(self):
        angle = math.radians(float(self.angle_input.text()))

        radius = float(self.radius_input.text())
        distance = float(self.distance_input.text())
        course = math.radians(float(self.course_input.text()))
        init_z = float(self.init_z_input.text())
        dive_angle = math.radians(float(self.dive_angle_input.text()))
        target_radius = float(self.target_radius_input.text())

        end_x = distance * math.cos(angle)
        end_y = distance * math.sin(angle)
        end_z = 0

        init_x = end_x - distance * math.cos(dive_angle)
        init_y = end_y - distance * math.sin(dive_angle)
        init_z = distance * math.sin(dive_angle)

        line_color = (random.random(), random.random(), random.random())
        end = (end_x, end_y, end_z)
        init = (init_x, init_y, init_z)
        print(radius)
        print(math.sin((angle-course)))
        print(end_x)
        print(end_y)

        print(distance)
        image_x = (end_x-distance) * math.sin(dive_angle)

        Xt=1000*image_x/distance
        print(Xt)
        Zt=1000*end_y/distance
        print(Zt)

        line_color = (random.random(), random.random(), random.random())
        end = (Xt, Zt, 0)
        points3d=(Xt+distance,Zt,0)

        self.coords.append((end, line_color))

        self.plot_3d_line(init, end, line_color)
        end_angle = angle - course
        polar_coords = (radius, end_angle)

        self.draw_2d_polar_point(polar_coords)

        self.draw_3d_circle(distance, target_radius)

        log_entry = f"Line {len(self.coords)}: угол-{angle}, курс- {course}, пикирование -{dive_angle} ({distance}, {init_z}, 0) -> {end}\n"
        self.coords_log.append(log_entry)

        self.coords_log.append(f" X: {end_x:.2f}")
        self.coords_log.append(f" Y: {end_y:.2f}")
        self.coords_log.append(f" Image X: {image_x:.2f}")

        self.update_std_devs(end)
        self.draw_2d_course_line(course)  # Add this line
        self.std_dev_label.setText('STD: x={:.2f}, y={:.2f}, z={:.2f}'.format(*self.std_devs))

        std = self.get_std_devs()

        print(std)

    def update_std_devs(self, new_coords):
        coords_array = np.array([end for end, color in self.coords])

        coords_array = np.vstack((coords_array, new_coords))

        self.std_devs = np.std(coords_array, axis=0)

    def get_std_devs(self):
        return self.std_devs

    def plot_3d_line(self, init, end, line_color):
        xs = [init[0], end[0]]
        ys = [init[1], end[1]]
        zs = [init[2], end[2]]
        self.ax.plot(xs, ys, zs, color=line_color)

        self.canvas.draw()

    def draw_2d_polar_point(self, polar_coords):
        radius, angle = polar_coords
        self.ax_2d.scatter(angle, radius, marker='o')

        self.canvas.draw()

    def draw_2d_circle(self, radius):
        circle = plt.Circle((0, 0), radius, color='r', fill=False)
        self.ax_2d.add_patch(circle)
        self.ax_2d.set_aspect('equal')
        self.fig.canvas.draw()

    def draw_2d_course_line(self, course):
        max_radius = max(self.ax_2d.get_ylim())
        end_angle = course
        end_radius = max_radius
        self.ax_2d.plot([0, end_angle], [0, end_radius], 'r--')
        self.ax_2d.text(end_angle, end_radius, 'Курс', fontsize=10, color='red')
        self.canvas.draw()

    def draw_3d_circle(self, distance, radius):
        theta = np.linspace(0, 2 * np.pi, 100)
        x = distance + radius * np.cos(theta)
        y = radius * np.sin(theta)
        z = np.zeros_like(x)

        points = np.array([x, y, z]).T.reshape(-1, 1, 3)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        lc = Line3DCollection(segments, colors='r', linewidths=1)
        self.ax.add_collection(lc)

        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())