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
    def __init__(self, jo, jc, l1, l2, l3):
        self.theta = 45
        self.jo = jo
        self.ja = Joint(None, None)
        self.jc = jc
        self.jb = Joint(None, None)
        self.l0 = Link(jo, jc).length
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3

    def validate(self):

        if (self.l3 + self.l2) <= (self.l1 + self.l0) or (self.l3 + self.l2) <= (self.l0 - self.l1):
            print("Incompatible link lengths.")
            print("\tl0", self.l0)
            print("\tl1", self.l1)
            print("\tl2", self.l2)
            print("\tl3", self.l3)
            return False
        return True

    def length_errors(self):
        link0 = Link(self.jo, self.jc)
        link1 = Link(self.jo, self.ja)
        link2 = Link(self.ja, self.jb)
        link3 = Link(self.jb, self.jc)

        d0 = round((link0.length - self.l0) / self.l0, 3)
        d1 = round((link1.length - self.l1) / self.l1, 3)
        d2 = round((link2.length - self.l2) / self.l2, 3)
        d3 = round((link3.length - self.l3) / self.l3, 3)

        print(d0, d1, d2, d3)


    def calculate_positions(self, theta2):

        if not self.validate():
            return
        
        ### Accounting for tilt
        alpha = np.arctan((self.jc.y - self.jo.y) / (self.jc.x - self.jo.x))

        # theta2 = theta2 + alpha

        if theta2 > np.pi * 2:
            theta2 = theta2 - np.pi * 2
        # Calculating intermediate angles using law of cosines
        # Derivation of angles:
        # https://www.youtube.com/watch?v=4O-XPJ7flLU

        a_c = np.sqrt(self.l0 ** 2 + self.l1 ** 2 - 2 * self.l0 * self.l1 * np.cos(theta2))
        beta = np.arccos((self.l0 ** 2 + a_c ** 2 - self.l1 ** 2) / (2 * self.l0 * a_c))
        psi = np.arccos((self.l2 ** 2 + a_c ** 2 - self.l3 ** 2) / (2 * self.l2 * a_c))
        lmda = np.arccos((self.l3 ** 2 + a_c ** 2 - self.l2 ** 2) / (2 * self.l3 * a_c))

        # Calculating main angles

        theta3 = psi - beta
        theta4 = np.pi - lmda - beta

        if theta2 > np.pi:
            theta3 = psi + beta
            theta4 = np.pi - lmda + beta

        # Joints
        self.ja.x = self.jo.x + self.l1 * np.cos(theta2 + alpha)
        self.ja.y = self.jo.y + self.l1 * np.sin(theta2 + alpha)

        self.jb.x = self.jc.x + self.l3 * np.cos(theta4 + alpha)
        self.jb.y = self.jc.y + self.l3 * np.sin(theta4 + alpha)

        self.length_errors()

        return self.jo, self.ja, self.jc, self.jb

    def plot(self, theta, **kwargs):

        self.calculate_positions(theta)

        co1 = plt.Circle((self.jo.x, self.jo.y), self.l1,
                        color='r', fill=False, linewidth=1, linestyle="dashed")
        cc1 = plt.Circle((self.jc.x, self.jc.y), self.l3,
                              color='r', fill=False, linewidth=1, linestyle="dashed")
             
        plt.figure(figsize=(8, 8))
        ax = plt.axes(xlim=(-8, 12), ylim=(-8, 12))

        ax.add_patch(co1)
        ax.add_patch(cc1)
        x = [self.jo.x, self.ja.x, self.jb.x, self.jc.x, self.jo.x]
        y = [self.jo.y, self.ja.y, self.jb.y, self.jc.y, self.jo.y]
        plt.plot(x, y, linewidth=2)
        plt.scatter(x,y)

        if kwargs.get("save"):
            plt.savefig("fourbar.jpg", dpi=300)
        if kwargs.get("show"):
            plt.show()

    def animate(self):

        co1 = plt.Circle((self.jo.x, self.jo.y), self.l1,
                              color='r', fill=False, linewidth=1, linestyle="dashed")
        cc1 = plt.Circle((self.jc.x, self.jc.y), self.l3,
                              color='r', fill=False, linewidth=1, linestyle="dashed")

        fig = plt.figure(figsize=(8, 8))
        ax = plt.axes(xlim=(-8, 12), ylim=(-8, 12))

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

        if not self.validate():
            return
        
        interval = 10
        anim = FuncAnimation(fig, animate, init_func=init,
                             frames=frames, interval=interval, blit=True)

        plt.show()


if __name__ == "__main__":

    _l0 = 7
    l_1 = 3
    l_2 = 7.5
    l_3 = 4.5
    ### Fixed joints
    jo = Joint(-1,-1)
    jc = Joint(_l0, 0)

    fourbar = Linkage(jo, jc, l_1, l_2, l_3)

    # fourbar.animate()
    fourbar.plot(.1, save=True)
 