import numpy as np
# from display import display
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Joint():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Link():
    def __init__(self, js, je, length):
        self.js = js
        self.je = je
        self.length = length

class Linkage():
    def __init__(self, jo, jc, l0, l1, l2, l3):
        self.jo = jo
        self.ja = Joint(None, None)
        self.jc = jc
        self.jb = Joint(None, None)
        self.l0 = l0
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3

    def calculate_positions(self, theta2):

        if theta2 > np.pi * 2:
            theta2 = theta2 - np.pi * 2
        ### Calculating intermediate angles using law of cosines
        # Derivation of angles:
        # https://www.youtube.com/watch?v=4O-XPJ7flLU

        a_c = np.sqrt(self.l0 ** 2 + self.l1 ** 2 - 2 * self.l0 * self.l1 * np.cos(theta2))
        beta = np.arccos((self.l0 ** 2 + a_c ** 2 - self.l1 ** 2) / (2 * self.l0 * a_c))
        psi = np.arccos((self.l2 ** 2 + a_c ** 2 - self.l3 ** 2) / (2 * self.l2 * a_c))
        lmda = np.arccos((self.l3 ** 2 + a_c ** 2 - self.l2 ** 2) / (2 * self.l3 * a_c))

        ### Calculating main angles

        theta3 = psi - beta
        # theta4 = np.pi - lmda - beta

        if theta2 > np.pi:
            theta3 = psi + beta
            theta4 = np.pi - lmda + beta

        ### Joints
        self.ja.x = self.l1 * np.cos(theta2)
        self.ja.y = self.l1 * np.sin(theta2)

        self.jb.x = self.jo.x + self.ja.x + self.l2 * np.cos(theta3)
        self.jb.y = self.jo.y + self.ja.y + self.l2 * np.sin(theta3)


def animate_linkage(linkage, interval):

    fig = plt.figure()
    ax = plt.axes(xlim=(-5, 10), ylim=(-5, 10))
    line, = ax.plot([], [], lw=3)

    frames = 360

    def init():
        line.set_data([], [])
        return line,
    def animate(i):
        theta = i * np.pi / 180
        linkage.calculate_positions(theta)
        x = [linkage.jo.x, linkage.ja.x, linkage.jb.x, linkage.jc.x, linkage.jo.x]
        y = [linkage.jo.y, linkage.ja.y, linkage.jb.y, linkage.jc.y, linkage.jo.y]
        line.set_data(x, y)
        return line,

    anim = FuncAnimation(fig, animate, init_func=init,
                                frames=frames, interval=interval, blit=True)

    plt.show()

if __name__ == "__main__":

    l0 = 7
    l1 = 3
    l2 = 7.5
    l3 = 4.5
    origin = Joint(1, 1)
    anchor = Joint(l0, 0)
    fourbar = Linkage(origin, anchor, l0, l1, l2, l3)

    animate_linkage(fourbar, 10)