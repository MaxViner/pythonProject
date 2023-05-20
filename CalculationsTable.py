
import math
import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QHBoxLayout, QLabel, QLineEdit, QTextEdit,
                             QTableWidgetItem, QHeaderView, QTableWidget)


class CalculationsTable(QWidget):
    def __init__(self, coords, std_devs, mean_coords, params=None):
        super().__init__()

        self.width = 1200
        self.height = 600
        self.mean_coords = mean_coords
        self.coords = coords
        self.std_devs = std_devs
        print(std_devs)
        self.params = params or {"distance": 0, "dive_angle": 0, "init_z": 0}

        self.setWindowTitle('Расчеты')
        self.setGeometry(0, 0, self.width * 0.6, self.height * 0.6)

        calculations_layout = QVBoxLayout()
        self.setLayout(calculations_layout)

        # Создаем и инициализируем атрибут self.calculations_table перед вызовом метода populate_table()
        self.calculations_table = QTableWidget()
        self.calculations_table.setRowCount(len(self.coords))
        self.calculations_table.setColumnCount(12)

        headers = [
            'условия пуска: ',
            "пересчет углов",
            "координаты точки падения",
            'Х_карт= Х * sin(угол_пик)',
            'Xt= (1000 * X / distance)',
            'Yt= (1000 * Y / distance)',
            'X_mean', 'Y_mean', 'Z_mean',  # Добавляем средние значения в заголовки таблицы
            'X_std', 'Y_std', 'Z_std',
        ]
        self.calculations_table.setHorizontalHeaderLabels(headers)

        # Increase header height and row height to fit 4 lines of text
        self.calculations_table.horizontalHeader().setFixedHeight(100)
        self.calculations_table.verticalHeader().setDefaultSectionSize(100)

        # Вызываем populate_table() после создания и инициализации self.calculations_table
        self.populate_table(self.params["distance"], math.radians(self.params["dive_angle"]), self.params["init_z"])

        self.calculations_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        calculations_layout.addWidget(self.calculations_table)

    def update_table(self, coords, std_devs, mean_coords, params):
        self.update_data(coords, std_devs, mean_coords, params)
        self.calculations_table.setRowCount(0)
        self.populate_table()

    def update_data(self, coords, std_devs, mean_coords, params):
        self.coords = coords
        self.std_devs = std_devs
        print(std_devs)
        self.mean_coords = mean_coords
        self.params = params
        self.populate_table()

    def populate_table(self, distance=None, dive_angle=None, init_z=None, course=None, angle=None, radius=None):
        # If arguments are not provided, use values from self.params
        distance = distance or self.params["distance"]
        dive_angle = dive_angle or math.radians(self.params["dive_angle"])
        init_z = init_z or self.params["init_z"]

        mean_label = QTableWidgetItem("Mean:")
        x_mean, y_mean, z_mean = self.mean_coords  # Извлекаем средние значения координат

        # If course is not provided, use the value from self.params or None
        course = course or self.params.get("course", None)
        angle = angle or self.params.get("angle", None)
        radius = radius or self.params.get("radius", None)

        # Clear existing data
        self.calculations_table.setRowCount(0)
        # Add mean values to the table
        mean_label = QTableWidgetItem("Mean:")

        for i, (end, color) in enumerate(self.coords):
            end_x, end_y, end_z = end
            x_std, y_std, z_std = self.std_devs
            params_item = QTableWidgetItem(
                f"дальность: {distance}\nугол пик (deg): {180 / math.pi * (dive_angle)}\nвысота пука: {init_z}"
                f"\nкурс-{course} \n"
                f"угол места цели- {angle}\n"
                f"радиус-{radius}"
            )

            radians_angles = QTableWidgetItem(
                f"курс-{math.radians(course) if course is not None else 'None'}\n"
                f"угол места цели-{math.radians(angle) if angle is not None else 'None'}\n"
                f"пик-{dive_angle}"
            )
            end_points = QTableWidgetItem(
                f"Х-{end_x})\n"
                f"Z-{end_z}"
            )
            image_x = (end_x - distance) * math.sin(dive_angle)
            xt = 1000 * image_x / distance
            yt = 1000 * end_y / distance

            self.calculations_table.insertRow(i)
            self.calculations_table.setItem(i, 0, params_item)
            self.calculations_table.setItem(i, 1, radians_angles)
            self.calculations_table.setItem(i, 2, end_points)
            self.calculations_table.setItem(i, 3, QTableWidgetItem(str(image_x)))
            self.calculations_table.setItem(i, 4, QTableWidgetItem(str(xt)))
            self.calculations_table.setItem(i, 5, QTableWidgetItem(str(yt)))
            self.calculations_table.setItem(i, 6,
                                            QTableWidgetItem(str(x_mean)))  # Добавляем средние координаты X в таблицу
            self.calculations_table.setItem(i, 7,
                                            QTableWidgetItem(str(y_mean)))  # Добавляем средние координаты Y в таблицу
            self.calculations_table.setItem(i, 8, QTableWidgetItem(str(z_mean)))
            self.calculations_table.setItem(i, 9, QTableWidgetItem(str(x_std)))
            self.calculations_table.setItem(i, 10, QTableWidgetItem(str(y_std)))
            self.calculations_table.setItem(i, 11, QTableWidgetItem(str(z_std)))