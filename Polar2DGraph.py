import numpy as np
import matplotlib.pyplot as plt

class Polar2DGraph:
    def __init__(self, ax):
        self.ax = ax
        self.ax.set_theta_zero_location("N")
        self.ax.set_ylim(0, 100)
        self.course_line = None

    def draw_2d_polar_point(self, polar_coords):
        radius, angle = polar_coords
        self.ax.scatter(angle, radius, marker='o')
        plt.draw()

    def draw_2d_course_line(self, course):
        max_radius = max(self.ax.get_ylim())
        end_angle = course
        end_radius = max_radius
        course_line, = self.ax.plot([0, end_angle], [0, end_radius], 'r--')
        self.ax.text(end_angle, end_radius, 'Курс', fontsize=10, color='red')
        plt.draw()
        return course_line  # Return the course line object