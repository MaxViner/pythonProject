import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QScrollArea, \
    QWidget, QSizePolicy


class SKOWindow(QWidget):
    def __init__(self, angles):
        super().__init__()
        self.setGeometry(800, 100, 400, 500)
        self.setWindowTitle("SKO")
        self.angle_labels = []
        self.angle_values = []
        for i, angle in enumerate(angles):
            label = QLabel(self)
            label.setGeometry(50, 50 + i * 30, 150, 30)
            label.setText(f"Угол {i + 1}:")
            value = QLabel(self)
            value.setGeometry(200, 50 + i * 30, 150, 30)
            value.setText(str(angle))
            self.angle_labels.append(label)
            self.angle_values.append(value)
        self.show()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.launch_counter = 0  # счетчик пусков ракет
        self.angles = []  # список углов для расчета СКО
        self.setGeometry(0, 0, 1280, 720)
        self.setWindowTitle("Rocket Launcher")

        self.angle_label = QLabel("Angle:", self)
        self.angle_label.setGeometry(50, 50, 150, 30)
        self.angle_input = QLineEdit(self)
        self.angle_input.setGeometry(200, 50, 150, 30)

        self.radius_label = QLabel("Radius:", self)
        self.radius_label.setGeometry(50, 100, 150, 30)
        self.radius_input = QLineEdit(self)
        self.radius_input.setGeometry(200, 100, 150, 30)

        self.course_label = QLabel("Course:", self)
        self.course_label.setGeometry(50, 150, 150, 30)
        self.course_input = QLineEdit(self)
        self.course_input.setGeometry(200, 150, 150, 30)

        self.zet_label = QLabel("Zet:", self)
        self.zet_label.setGeometry(50, 200, 150, 30)
        self.zet_input = QLineEdit(self)
        self.zet_input.setGeometry(200, 200, 150, 30)

        self.x_label = QLabel("X:", self)
        self.x_label.setGeometry(50, 250, 150, 30)
        self.x_input = QLineEdit(self)
        self.x_input.setGeometry(200, 250, 150, 30)

        self.dive_angle_label = QLabel("Dive Angle:", self)
        self.dive_angle_label.setGeometry(50, 300, 150, 30)
        self.dive_angle_input = QLineEdit(self)
        self.dive_angle_input.setGeometry(200, 300, 150, 30)

        self.range_label = QLabel("Range:", self)
        self.range_label.setGeometry(50, 350, 150, 30)
        self.range_input = QLineEdit(self)
        self.range_input.setGeometry(200, 350, 150, 30)

        self.launch_button = QPushButton("Launch Rockets", self)
        self.launch_button.setGeometry(200, 400, 150, 30)
        self.launch_button.clicked.connect(self.launch_rockets)

        # добавляем панель для отображения предыдущих вводов
        self.input_log = QVBoxLayout()
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(400, 50, 200, 340)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area_widget.setLayout(self.input_log)

        self.sko_button = QPushButton("Рассчитать СКО", self)
        self.sko_button.setGeometry(400, 400, 150, 30)
        self.sko_button.clicked.connect(self.calculate_sko)

        self.graph_widget = QWidget(self)
        self.graph_widget.setGeometry(600, 50, 600, 600)
        self.graph_layout = QVBoxLayout(self.graph_widget)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.graph_layout.addWidget(self.canvas)
        self.ax = None

        self.show()

    def launch_rockets(self):
        self.launch_counter += 1
        angle = float(self.angle_input.text())
        self.angles.append(angle)
        radius = float(self.radius_input.text())
        course = float(self.course_input.text())
        zet = float(self.zet_input.text())
        x = float(self.x_input.text())

        input_info = QLabel(
            f"пуск {self.launch_counter} :\n Angle: {angle} \n, Radius: {radius} \n, Course: {course} \n, Zet: {zet} \n,"
            f" X: {x} \n, ")
        self.input_log.addWidget(input_info)

        self.angle_input.setText('')
        self.radius_input.setText('')
        self.course_input.setText('')
        self.zet_input.setText('')
        self.x_input.setText('')
        self.dive

    def update_plot(self, x, zet, angle, radius):
        if self.ax is None:
            self.ax = self.figure.add_subplot(111, projection='3d')
        t = np.linspace(0, 1, num=100)
        z = zet + radius * np.cos(angle * np.pi / 180) * t
        y = radius * np.sin(angle * np.pi / 180) * t
        self.ax.plot(x * t, y, z)
        self.ax.set_xlabel("X-axis")
        self.ax.set_ylabel("Y-axis")
        self.ax.set_zlabel("Z-axis")
        self.canvas.draw()

    def calculate_sko(self):
        sko_window = SKOWindow(self.angles)


if __name__ == "__main__":
    # создаем приложение и главное окно
    app = QApplication(sys.argv)
    main_window = MainWindow()

    # запускаем главный цикл приложения
    sys.exit(app.exec())