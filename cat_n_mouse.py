import numpy as np
import random
import math
import time
from colorama import Fore, Back, Style
import os
import platform


class Chase:
    """
    Takes the initial positions of the the cat and the mouse and computes
    the dynamic variables of the chase which are the angles between velocity vectors,
    distances between cat and mouse, and velocities of cat and mouse.

    cp: ndarray. A vector for the catss starting position in the chase space
    rp: ndarray. A vector for the mouse starting position in the chase space
    span: Int. A number representing the upper limits of each component of the chase space.

    **all arrays must be of the same length
    """
    def __init__(self, cp=None, rp=None, span=60):
        self.span = span
        self.cp = np.array(cp, dtype=float) #Starting chaser position
        self.rp = np.array(rp, dtype=float) #Starting runner position
        self.dim = len(cp)

    def get_rv(self):
        """
        Gives a random mouse velocity
        """
        components = [random.randint(-50, 50) for i in range(self.dim)]
        if np.linalg.norm(np.array(components)) != 0: #Check for zero vector to prevent zero division error
            self.rv = np.array(components) * (1/(np.linalg.norm(components))) #Normalize runner velocity
        else:
            self.rv = np.array(components)

    def get_d(self):
        """
        Calculate updated direction vector extending from cp to rp and its magnitude
        """
        self.d = np.array(self.rp - self.cp, dtype=float)
        self.d_mag = np.linalg.norm(self.d) #Magnitude of d

    def get_alpha(self):
        self.alpha = math.acos((self.d @ self.rv)/self.d_mag) #Angle between d and rv

    def get_cv1(self, init_d=None, rundown=False):
        """
        Update chaser velocity
        """
        perp_scalor = self.d @ self.rv #An important scalor value
        if rundown:
            self.cv = self.d * (1/self.d_mag)
        elif self.alpha <= (math.pi/2): #Runner moves with some component of velocity away from chaser
            self.cv = self.rv
        elif self.alpha == 0 or math.pi: #Runner moves directly away or toward chaser
            self.cv = self.d * (1/np.linalg.norm(self.d))
        elif self.rv == np.array([0, 0]): #Runner not moving
            self.cv = self.d * (1/self.d_mag)
        else:
            perp_scalor = math.acos(self.d @ self.rv) #An important scalor value
            tp = self.rp + (perp_scalor * self.rv)
            self.cv = (tp - self.cp) * (1/(np.linalg.norm(tp - self.cp))) #A normalized velocity vector that is perpendicular to rv

    def get_cv2(self):
        pass
        """
        A second chase method. This method functions the same as the first if the
        runner is moving away but put the chaser on a colision course with the runner
        if it is moving toward.
        """   #Alternitive cv algorithm

    def vis(self, a, b, span):
        print("\n\n\n\n\n\n\n\n\n\n\n\n", "              ",
        Back.BLUE + "     Chaser    ", Style.RESET_ALL, "   ",
        Back.GREEN + "     Runner    ", Style.RESET_ALL, "\n") #Header
        combo_list = []
        dim_lables = ["a", "a", "b", "b", "c", "c", "d", "d", "e"
        , "e", "f", "f", "g", "g", "h", "h", "i", "i", "j", "j", "k", "k", "l", "l", "m", "m", "n", "n", "o", "o", #This is a list of lables for the grah and it is not a good way of doing it
        "p", "p", "q", "q", "r", "r", "s", "s", "t", "t", "u", "u", "v", "v", "w", "w", "x", "x", "y", "y", "z", "z"]
        for i in range(len(a)):
            combo_list.append(a[i])
            combo_list.append(b[i])
        vis_list = [[" " for n in range(round(i) + span)]for i in combo_list]
        for i in range(len(vis_list)):
            if i % 2 != 0:
                print(Fore.GREEN, dim_lables[i], Back.GREEN, "".join(vis_list[i]), Style.RESET_ALL, "\n")
            else:
                print(Fore.BLUE, dim_lables[i], Back.BLUE, "".join(vis_list[i]) + " ", Style.RESET_ALL)

    def vis1(self, a, b, span):
        a_list = []
        b_list = []
        print("\n\n\n\n\n\n\n\n\n\n\n\n", "".join([" " for i in range(span - 16)]),
        Back.BLUE + Fore.WHITE + "     Cat    ", Style.RESET_ALL, "   ",
        Back.GREEN + "     Mouse    ", Style.RESET_ALL, "\n") #Header
        combo_list = []
        dim_lables = ["a", "a", "b", "b", "c", "c", "d", "d", "e"
            , "e", "f", "f", "g", "g", "h", "h", "i", "i", "j", "j", "k", "k", "l", "l", "m", "m", "n", "n", "o", "o",
            "p", "p", "q", "q", "r", "r", "s", "s", "t", "t", "u", "u", "v", "v", "w", "w", "x", "x", "y", "y", "z", "z"]
        for i in a:
            if i > 0:
                bar = [">" for n in range(round(i))]
                i = list([" " for n in range(span)])
                i.extend(bar)
                a_list.append(i)
            else:
                bar = ["<" for n in range(abs(round(i)))]
                i = [" " for n in range(span + round(i))]
                i.extend(bar)
                a_list.append(i)
        for i in b:
            if i > 0:
                bar = [">" for n in range(round(i))]
                i = [" " for n in range(span)]
                i.extend(bar)
                b_list.append(i)
            else:
                bar = ["<" for n in range(abs(round(i)))]
                i = [" " for n in range(span + round(i))]
                i.extend(bar)
                b_list.append(i)
        for i in range(len(a_list)):
            combo_list.append(a_list[i])
            combo_list.append(b_list[i])
        for i in range(len(combo_list)):
            if i % 2 != 0:
                print(Fore.GREEN, dim_lables[i], Fore.GREEN, "".join(combo_list[i]), Style.RESET_ALL, "\n --", "".join([" " for i in range(span - 2)]), "--")
            else:
                print(Fore.BLUE, dim_lables[i], Fore.BLUE, "".join(combo_list[i]) + " ", Style.RESET_ALL)

    def chase_results(self, first_distance, n):
        self.average_rate = first_distance/n
        print("Initial Distance =", first_distance)
        print("n =", n)
        print("dim =", self.dim)
        print("init_dist/n =", self.average_rate, "(Average rate of closure)") #average distance gained on the runner per step


    def clear(self):
        if platform.system() == "Windsow":
            os.system("cls")
        else:
            os.system("clear")


    def chase_loop(self, vis=False, rundown=False):
        n = 0
        self.get_d()
        first_distance = self.d_mag
        if not vis and not rundown: #The most common condition.
            while True:
                self.get_rv()
                self.get_d()
                self.get_alpha()
                self.get_cv1(rundown=rundown)
                self.cp += self.cv
                self.rp += self.rv
                n += 1
                if self.d_mag < 2:
                    break
            return first_distance / n #Returns the average rate of gain
        elif vis and rundown:
            # start = "start"
            self.vis1(self.cp, self.rp, self.span)
            start = input("Press ENTER to start.")
            while True:
                self.clear()
                self.rv = np.array([0 for i in range(len(self.rp))])
                self.get_d()
                self.get_alpha()
                self.get_cv1(rundown=rundown)
                self.vis1(self.cp, self.rp, self.span)
                time.sleep(0.04)
                self.cp += self.cv
                self.rp += self.rv
                n += 1
                if self.d_mag < 2:
                    break
            self.chase_results(first_distance, n)
        elif vis:
            # start = "start"
            self.vis1(self.cp, self.rp, self.span)
            start = input("Press ENTER to start. ")
            while True:
                self.clear()
                self.get_rv()
                self.get_d()
                self.get_alpha()
                self.get_cv1(rundown=rundown)
                self.vis1(self.cp, self.rp, self.span) #Testing vis funcs
                time.sleep(0.04)
                self.cp += self.cv
                self.rp += self.rv
                n += 1
                if self.d_mag < 2:
                    break
            self.chase_results(first_distance, n)
        else:
            while True:
                self.rv = np.array([0 for i in range(len(self.rp))])
                self.get_d()
                self.get_alpha()
                self.get_cv1(rundown=rundown)
                self.cp += self.cv
                self.rp += self.rv
                n += 1
                if self.d_mag < 2:
                    break
            self.chase_results(first_distance, n)


def main():
    # chase1 = Chase([50, -20], [-40, 40], span = 60)
    # chase1 = Chase([50, -20, 44, -30, 18, -44, 22, -21, 33], [-40, 40, -23, 27, -44, 8, -27, 27, -18], span = 60)
    # chase1.chase_loop(vis=True, rundown=True)

    aux_chase = Chase(cp=[0], rp=[0])
    rundown = {"y": True, "n": False}
    while True:
        aux_chase.clear()
        dimensionality = input("Enter the number of dimensions[1-6]: ")
        try:
            dimensionality = int(dimensionality)
            break
        except ValueError:
            continue
    while True:
        aux_chase.clear()
        rd = input("Straight line path?[y/n]: ")
        if rd in ["y", "n"]:
            aux_chase.clear()
            break
    cat_position = [random.randint(-60, 60) for i in range(dimensionality)]
    mouse_position = [random.randint(-60, 60) for i in range(dimensionality)]
    chase = Chase(cp=cat_position, rp=mouse_position, )
    chase.chase_loop(vis=True, rundown=rundown[rd])








if __name__ == "__main__":
    main()
