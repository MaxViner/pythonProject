from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

def create_layout(self):
    layout = QVBoxLayout()
    self.setLayout(layout)

    coord_input_layout = QHBoxLayout()
    layout.addLayout(coord_input_layout)

    self.distance_input = QLineEdit()
    coord_input_layout.addWidget(QLabel('Дистанция:'))
    coord_input_layout.addWidget(self.distance_input)
    self.distance_input.setStyleSheet("font-size: 20px")

    self.course_input = QLineEdit()
    coord_input_layout.addWidget(QLabel('Курс:'))
    coord_input_layout.addWidget(self.course_input)
    self.course_input.setStyleSheet("font-size: 20px")

    self.init_z_input = QLineEdit()
    coord_input_layout.addWidget(QLabel('Начальный Z:'))
    coord_input_layout.addWidget(self.init_z_input)
    self.init_z_input.setStyleSheet("font-size: 20px")

    coord_input_layout2 = QHBoxLayout()
    layout.addLayout(coord_input_layout2)

    self.angle_input = QLineEdit()
    coord_input_layout2.addWidget(QLabel('Угол (градусы):'))
    coord_input_layout2.addWidget(self.angle_input)
    self.angle_input.setStyleSheet("font-size: 20px")

    self.radius_input = QLineEdit()
    coord_input_layout2.addWidget(QLabel('Радиус:'))
    coord_input_layout2.addWidget(self.radius_input)
    self.radius_input.setStyleSheet("font-size: 20px")

    self.dive_angle_input = QLineEdit()
    coord_input_layout2.addWidget(QLabel('Угол погружения (градусы):'))
    coord_input_layout2.addWidget(self.dive_angle_input)
    self.dive_angle_input.setStyleSheet("font-size: 20px")