import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Line3DCollection

class ThreeDGraph:
    def __init__(self, ax):
        self.ax = ax
        self.ax.set_xlabel('Distance')
        self.ax.set_ylabel('Lateral Deviation')
        self.ax.set_zlabel('Height')
        self.ax.set_xlim(-1000, 1000)
        self.ax.set_ylim(-500, 500)
        self.ax.set_zlim(0, 1000)
        self.ax.plot([-1000, 1000], [0, 0], [0, 0], color='black')
        self.ax.plot([0, 0], [-1000, 1000], [0, 0], color='black')
        self.ax.plot([0, 0], [0, 0], [0, 1000], color='black')

    def plot_3d_line(self, init, end, line_color):
        xs = [init[0], end[0]]
        ys = [init[1], end[1]]
        zs = [init[2], end[2]]
        self.ax.plot(xs, ys, zs, color=line_color)

    def draw_3d_circle(self, x, rradius):
        theta = np.linspace(0, 2 * np.pi, 100)
        xc = x + rradius * np.cos(theta)  # X-coordinate is x+radius*cos(theta)
        yc = rradius * np.sin(theta)  # Y-coordinate is y+radius*sin(theta)
        zc = np.zeros_like(xc)  # Z-coordinate is always zero in 2D
        points = np.array([xc, yc, zc]).T.reshape(-1, 1, 3)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        lc = Line3DCollection(segments, colors='r', linewidths=1)
        self.ax.add_collection(lc)

    def draw_angle_labels(self, end_angle):
        angle_label_x = 500 * np.cos(end_angle)
        angle_label_y = 500 * np.sin(end_angle)
        self.ax.text(angle_label_x, angle_label_y, 0, f"{np.degrees(end_angle):.1f}°", fontsize=10, color="blue")