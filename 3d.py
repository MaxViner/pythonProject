import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtCore import Qt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 3D Plot'
        self.left = 10
        self.top = 10
        self.width = 800
        self.height = 600
        self.initUI()
        self.coords = []

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # Запрашиваем начальные координаты
        start_x_label = QLabel(self)
        start_x_label.setText("Начальная координата X: ")
        start_x_label.move(20, 20)
        self.start_x_input = QLineEdit(self)
        self.start_x_input.setValidator(QDoubleValidator())
        self.start_x_input.move(200, 20)

        start_y_label = QLabel(self)
        start_y_label.setText("Начальная координата Y: ")
        start_y_label.move(20, 50)
        self.start_y_input = QLineEdit(self)
        self.start_y_input.setValidator(QDoubleValidator())
        self.start_y_input.move(200, 50)

        start_z_label = QLabel(self)
        start_z_label.setText("Начальная координата Z: ")
        start_z_label.move(20, 80)
        self.start_z_input = QLineEdit(self)
        self.start_z_input.setValidator(QDoubleValidator())
        self.start_z_input.move(200, 80)

        # Запрашиваем конечные координаты
        end_x_label = QLabel(self)
        end_x_label.setText("Конечная координата X: ")
        end_x_label.move(20, 120)
        self.end_x_input = QLineEdit(self)
        self.end_x_input.setValidator(QDoubleValidator())
        self.end_x_input.move(200, 120)

        end_y_label = QLabel(self)
        end_y_label.setText("Конечная координата Y: ")
        end_y_label.move(20, 150)
        self.end_y_input = QLineEdit(self)
        self.end_y_input.setValidator(QDoubleValidator())
        self.end_y_input.move(200, 150)

        end_z_label = QLabel(self)
        end_z_label.setText("Конечная координата Z: ")
        end_z_label.move(20, 180)
        self.end_z_input = QLineEdit(self)
        self.end_z_input.setValidator(QDoubleValidator())
        self.end_z_input.move(200, 180)

        # Кнопка для рисования 3D линии
        draw_button = QPushButton('Нарисовать', self)
        draw_button.setToolTip("Нажмите кнопку, чтобы нарисовать 3D линию")
        draw_button.move(200, 220)
        draw_button.clicked.connect(self.on_draw_button_click)

        # Окно для отображения лога координат
        coords_log_label = QLabel(self)
        coords_log_label.setText("Лог координат: ")
        coords_log_label.move(450, 20)
        self.coords_log = QTextEdit(self)
        self.coords_log.setReadOnly(True)
        self.coords_log.setGeometry(450, 50, 300, 500)

        self.show()



    def on_draw_button_click(self):
        # Получаем начальные и конечные координаты из полей ввода
        start_x = float(self.start_x_input.text())
        start_y = float(self.start_y_input.text())
        start_z = float(self.start_z_input.text())
        end_x = float(self.end_x_input.text())
        end_y = float(self.end_y_input.text())
        end_z = float(self.end_z_input.text())

        # Добавляем координаты в список
        self.coords.append(((start_x, start_y, start_z), (end_x, end_y, end_z)))

        # Создаем 3D график
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Настройки 3D графика
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xlim3d(-10, 10)
        ax.set_ylim3d(-10, 10)
        ax.set_zlim3d(-10, 10)

        # Рисуем каждую линию из списка
        for i, (start, end) in enumerate(self.coords):
            plt.gca().set_prop_cycle(None)  # Смена цвета линии
            xs = [start[0], end[0]]
            ys = [start[1], end[1]]
            zs = [start[2], end[2]]
            ax.plot(xs, ys, zs)
            plt.show()

            # Отрисовываем отдельный 2D график
            self.draw_2d_graph()

        def draw_2d_graph(self):
            fig_2d = plt.figure()
            ax2 = fig_2d.add_subplot(111)

            # Настройки 2D графика
            ax2.set_xlabel('X')
            ax2.set_ylabel('Z')
            ax2.set_xlim(-10, 10)
            ax2.set_ylim(-10, 10)

            # Рисуем каждую конечную координату из списка на 2D графике
            for i, (_, end) in enumerate(self.coords):
                plt.gca().set_prop_cycle(None)  # Смена цвета точки
                xs = end[0]
                zs = end[2]
                ax2.scatter(xs, zs)

            plt.show()
            # Добавляем координаты в лог
            log_entry = "Линия {0}: ({1}, {2}, {3}) - ({4}, {5}, {6})\n".format(i + 1, start[0], start[1], start[2],
                                                                                end[0], end[1], end[2])
            if log_entry not in self.coords_log.toPlainText():
                self.coords_log.append(log_entry)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())