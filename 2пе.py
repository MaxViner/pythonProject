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

        # Создаем layout и добавляем в него графики и журнал координат
        layout = QVBoxLayout()
        self.setLayout(layout)

        coord_input_layout = QHBoxLayout()
        layout.addLayout(coord_input_layout)

        coord_input_layout.addWidget(QLabel('Start (x, y, z):'))
        self.start_x_input = QLineEdit()
        coord_input_layout.addWidget(self.start_x_input)
        self.start_y_input = QLineEdit()
        coord_input_layout.addWidget(self.start_y_input)
        self.start_z_input = QLineEdit()
        coord_input_layout.addWidget(self.start_z_input)

        coord_input_layout.addWidget(QLabel('End (x, y, z):'))
        self.end_x_input = QLineEdit()
        coord_input_layout.addWidget(self.end_x_input)
        self.end_y_input = QLineEdit()
        coord_input_layout.addWidget(self.end_y_input)
        self.end_z_input = QLineEdit()
        coord_input_layout.addWidget(self.end_z_input)

        add_line_button = QPushButton('Add Line')
        add_line_button.clicked.connect(self.add_line)
        coord_input_layout.addWidget(add_line_button)

        self.fig_3d = plt.figure()
        self.ax = self.fig_3d.add_subplot(121, projection='3d')  # Изменили на 121, чтобы разместить графики рядом

        # Настройки 3D графика
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_zlim(-10, 10)

        layout.addWidget(self.fig_3d.canvas)

        self.ax_2d = self.fig_3d.add_subplot(122)
        self.ax_2d.set_xlabel('X')
        self.ax_2d.set_ylabel('Z')
        self.ax_2d.set_xlim(-10, 10)
        self.ax_2d.set_ylim(-10, 10)

        layout.addWidget(self.fig_3d.canvas)

        # Добавляем журнал координат в layout
        layout.addWidget(self.coords_log)

        layout.addWidget(self.fig_3d.canvas)

        # Создаем окно для вывода среднеквадратического отклонения
        self.std_dev_label = QLabel('СКО: x={:.2f}, y={:.2f}, z={:.2f}'.format(*self.std_devs))
        layout.addWidget(self.std_dev_label)

        layout.addWidget(self.coords_log)
        self.show()
        self.show()

    def add_line(self):
        start = (float(self.start_x_input.text()), float(self.start_y_input.text()), float(self.start_z_input.text()))
        end = (float(self.end_x_input.text()), float(self.end_y_input.text()), float(self.end_z_input.text()))

        line_color = (random.random(), random.random(), random.random())  # Генерация случайного цвета
        self.coords.append((start, end, line_color))

        # Рисуем линии 3D и 2D координат
        self.plot_3d_line(start, end, line_color)
        self.draw_2d_line(end, len(self.coords), line_color)

        # Добавляем координаты в лог
        log_entry = "Линия {0}: {1} -> {2}\n".format(len(self.coords), start, end)
        self.coords_log.append(log_entry)
        # Рассчитываем среднеквадратическое отклонение по каждой координате
        self.update_std_devs(end)

        # Обновляем значение среднеквадратического отклонения в окне
        self.std_dev_label.setText('STD: x={:.2f}, y={:.2f}, z={:.2f}'.format(*self.std_devs))

    def update_std_devs(self, new_coords):
        # Получаем массив координат конечных точек
        coords_array = np.array([end for start, end, color in self.coords])

        # Добавляем новые координаты
        coords_array = np.vstack((coords_array, new_coords))

        # Вычисляем среднеквадратическое отклонение по каждой координате
        self.std_devs = np.std(coords_array, axis=0)

    def plot_3d_line(self, start, end, line_color):
        xs = [start[0], end[0]]
        ys = [start[1], end[1]]
        zs = [start[2], end[2]]
        self.ax.plot(xs, ys, zs, color=line_color)

        self.fig_3d.canvas.draw()

    def draw_2d_line(self, end, index, line_color):
        xs = end[0]
        zs = end[2]
        self.ax_2d.scatter(xs, zs, color=line_color, marker='o')  # Рисуем точку на 2D-графике

        self.fig_3d.canvas.draw()  # Обновляем графики


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())