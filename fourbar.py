import numpy as np
# from display import display
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Joint():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Link():
    def __init__(self, js, je):
        self.js = js
        self.je = je
        self.length = self.calc_length()

    def calc_length(self):
        return np.sqrt((self.je.x-self.js.x) ** 2 + (self.je.y-self.js.y) ** 2)


class Linkage():
    def __init__(self, jo, jc, l0, l1, l2, l3):
        self.theta = 45
        self.jo = jo
        self.ja = Joint(None, None)
        self.jc = jc
        self.jb = Joint(None, None)
        self.l0 = l0
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3

    def validate_lengths(self):
        link0 = Link(self.jo, self.jc)
        link1 = Link(self.jo, self.ja)
        link2 = Link(self.ja, self.jb)
        link3 = Link(self.jb, self.jc)
        d0 = round((link0.length - self.l0) / self.l0, 3)
        d1 = round((link1.length - self.l1) / self.l1, 3)
        d2 = round((link2.length - self.l2) / self.l2, 3)
        d3 = round((link3.length - self.l3) / self.l3, 3)

        print(d0, d1, d2, d3)

        # if l3 + l2 > l1 + l0:
        #     print("INVALID")

    def calculate_positions(self, theta2):

        if theta2 > np.pi * 2:
            theta2 = theta2 - np.pi * 2
        # Calculating intermediate angles using law of cosines
        # Derivation of angles:
        # https://www.youtube.com/watch?v=4O-XPJ7flLU

        a_c = np.sqrt(self.l0 ** 2 + self.l1 ** 2 - 2 *
                      self.l0 * self.l1 * np.cos(theta2))
        beta = np.arccos((self.l0 ** 2 + a_c ** 2 -
                         self.l1 ** 2) / (2 * self.l0 * a_c))
        psi = np.arccos((self.l2 ** 2 + a_c ** 2 -
                        self.l3 ** 2) / (2 * self.l2 * a_c))
        lmda = np.arccos((self.l3 ** 2 + a_c ** 2 -
                         self.l2 ** 2) / (2 * self.l3 * a_c))

        # Calculating main angles

        theta3 = psi - beta
        # theta4 = np.pi - lmda - beta

        if theta2 > np.pi:
            theta3 = psi + beta
            theta4 = np.pi - lmda + beta

        # Joints
        self.ja.x = self.l1 * np.cos(theta2)
        self.ja.y = self.l1 * np.sin(theta2)

        self.jb.x = self.jo.x + self.ja.x + self.l2 * np.cos(theta3)
        self.jb.y = self.jo.y + self.ja.y + self.l2 * np.sin(theta3)

        self.validate_lengths()

        return self.jo, self.ja, self.jc, self.jb

    def animate(self):

        co1 = plt.Circle((self.jo.x, self.jo.y), self.l1,
                              color='r', fill=False, linewidth=1, linestyle="dashed")
        cc1 = plt.Circle((self.jc.x, self.jc.y), self.l3,
                              color='r', fill=False, linewidth=1, linestyle="dashed")

        fig = plt.figure(figsize=(5, 5))
        ax = plt.axes(xlim=(-5, 10), ylim=(-5, 10))

        ax.add_patch(co1)
        ax.add_patch(cc1)

        line, = ax.plot([], [], lw=3)

        frames = 360

        def init():
            line.set_data([], [])
            return line,

        def animate(i):
            theta = i * np.pi / 180
            self.calculate_positions(theta)
            x = [self.jo.x, self.ja.x, self.jb.x, self.jc.x, self.jo.x]
            y = [self.jo.y, self.ja.y, self.jb.y, self.jc.y, self.jo.y]
            line.set_data(x, y)
            return line,

        interval = 10
        anim = FuncAnimation(fig, animate, init_func=init,
                             frames=frames, interval=interval, blit=True)

        plt.show()


if __name__ == "__main__":

    l0 = 7
    l1 = 3
    l2 = 7.5
    l3 = 4.5
    jo = Joint(1, 1)
    jc = Joint(l0, 0)

    fourbar = Linkage(jo, jc, l0, l1, l2, l3)

    fourbar.animate()
