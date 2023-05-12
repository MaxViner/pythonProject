import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QScrollArea, QWidget


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
        # задаем размеры окна
        self.setGeometry(100, 100, 650, 500)

        # задаем заголовок окна
        self.setWindowTitle("Rocket Launcher")

        # добавляем поля ввода для параметров ракет
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

        # добавляем кнопку для запуска ракет
        self.launch_button = QPushButton("Launch Rockets", self)
        self.launch_button.setGeometry(200, 400, 150, 30)
        self.launch_button.clicked.connect(self.launch_rockets)

        # добавляем кнопку для расчета СКО
        self.sko_button = QPushButton("Рассчитать СКО", self)
        self.sko_button.setGeometry(400, 400, 150, 30)
        self.sko_button.clicked.connect(self.calculate_sko)

        # добавляем панель для отображения предыдущих вводов
        self.input_log = QVBoxLayout()
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setGeometry(400, 50, 200, 340)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_area_widget)
        self.scroll_area_widget

        # выводим окно на экран
        self.show()

    def launch_rockets(self):
        # получаем значения из полей ввода
        self.launch_counter += 1
        angle = float(self.angle_input.text())
        self.angles.append(angle)
        radius = float(self.radius_input.text())
        course = float(self.course_input.text())
        zet = float(self.zet_input.text())
        x = float(self.x_input.text())
        # здесь должен быть код для запуска ракет с указанными параметрами
        # пока что оставим его пустым

        # добавляем информацию о параметрах в панель для отображения предыдущих вводов
        input_info = QLabel(
            f"пуск {self.launch_counter} :\n Angle: {angle} \n, Radius: {radius} \n, Course: {course} \n, Zet: {zet} \n,"
            f" X: {x} \n, "
            # f"Dive Angle: {dive_angle} "
            f"\n, Range: {range}")
        self.input_log.addWidget(input_info)

        # сбрасываем значения в полях ввода
        self.angle_input.setText('')
        self.radius_input.setText('')
        self.course_input.setText('')
        self.zet_input.setText('')
        self.x_input.setText('')
        self.dive_angle_input.setText('')
        self.range_input.setText('')


if __name__ == "__main__":
    # создаем приложение и главное окно
    app = QApplication(sys.argv)
    main_window = MainWindow()

    # запускаем главный цикл приложения
    sys.exit(app.exec())