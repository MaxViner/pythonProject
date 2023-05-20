import math

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QHBoxLayout, QLabel, QLineEdit, QTextEdit,
                             QTableWidgetItem, QHeaderView, QTableWidget)


class CalculationsTable(QWidget):
    def __init__(self, coords, std_devs, params=None):
        super().__init__()

        self.width = 1200
        self.height = 600

        self.coords = coords
        self.std_devs = std_devs
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
            "пересчет углов"
            "координаты тоочки падения",
            'Х_карт= Х * sin(угол_пик)',
            'Xt= (1000 * X / distance)',
            'Yt= (1000 * Y / distance)',
            "Мат ожидание координат"
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

    def update_data(self, coords, std_devs, params):
        self.coords = coords
        self.std_devs = std_devs
        self.params = params
        self.populate_table()

    def update_table(self, coords, std_devs, params):
        self.update_data(coords, std_devs, params)
        self.calculations_table.setRowCount(0)
        self.populate_table()

    def populate_table(self, distance=None, dive_angle=None, init_z=None, course=None, angle=None):
        # If arguments are not provided, use values from self.params
        distance = distance or self.params["distance"]
        dive_angle = dive_angle or math.radians(self.params["dive_angle"])
        init_z = init_z or self.params["init_z"]

        # If course is not provided, use the value from self.params or None
        course = course or self.params.get("course", None)
        angle = angle or self.params.get("angle", None)
        radius= self.params.get("raius", None)
        # Clear existing data
        self.calculations_table.setRowCount(0)



        for i, (end, color) in enumerate(self.coords):
            end_x, end_y, end_z = end
            x_std, y_std, z_std = self.std_devs
            params_item = QTableWidgetItem(
                f"дальность: {distance}\nугол пик (deg): {180/math.pi*(dive_angle)}\nвысота пука: {init_z}"
                f"\nкурс-{course} \n"
                f"угол места цели- {angle}"
                f"радиус-{radius}"
            )
            raians_angles = QTableWidgetItem(
                f"курс-{math.radians(course)}\n"
                f"угол места целм-{math.radians(angle)}\n"
                f"пик-{dive_angle}"
            )
            endPoints = QTableWidgetItem(
                f"Х-{end_x})\n"
                f"Z-{end_y}"
            )
            Image_x = (end_x - distance) * math.sin(dive_angle)
            Xt = 1000 * Image_x / distance
            Yt = 1000 * end_y / distance

            # Average=QTableWidgetItem(
            #     f"Х-{Average_X})}\n"
            #     f"Z-{Average_Y}"
            # )

            self.calculations_table.insertRow(i)
            self.calculations_table.setItem(i, 0, params_item)
            self.calculations_table.setItem(i, 1, raians_angles)
            self.calculations_table.setItem(i, 2, endPoints)


            self.calculations_table.setItem(i, 3, QTableWidgetItem(str(Image_x)))
            self.calculations_table.setItem(i, 4, QTableWidgetItem(str(Xt)))
            self.calculations_table.setItem(i, 5, QTableWidgetItem(str(Yt)))

            self.calculations_table.setItem(i, 7, QTableWidgetItem(str(x_std)))
            self.calculations_table.setItem(i, 8, QTableWidgetItem(str(y_std)))
            self.calculations_table.setItem(i, 9, QTableWidgetItem(str(z_std)))

