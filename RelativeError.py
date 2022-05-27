from scipy.spatial import Voronoi, voronoi_plot_2d, Delaunay, delaunay_plot_2d, KDTree
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

SAVEPATH = "Results/Images"


class RelativeError:
    def __init__(self):
        self.del_data = []
        self.quadrants_total_error = []
        self.quadrants_error_perc = []

    def save(self):
        if len(self.quadrants_error_perc) is not 0:
            df = pd.DataFrame(self.quadrants_error_perc)
            df.to_excel("Results/Auswertung_Quadranten.xlsx")

    def plot_vro(self, pos_start, pos_end, id, names):
        """
        plot voronoi diagram
        :param pos_start:
        :param pos_end:
        :param id:
        :param names:
        """
        # neighbours
        var_end = KDTree(pos_end)
        var = KDTree(pos_start)
        n_start = np.zeros((len(pos_start), 3))
        n_end = np.zeros((len(pos_end), 3))
        neighbors_start = []
        neighbors_end = []

        for i in range(0, len(pos_start)):
            # find the three nearest neighbors of each point in start positions
            n = var.query(pos_start[i], 3)

            n_start[i] = n[1]
            if (n[1][0], n[1][1]) not in neighbors_start:
                if (n[1][1], n[1][0]) not in neighbors_start:
                    neighbors_start.append((n[1][0], n[1][1]))
            if (n[1][0], n[1][2]) not in neighbors_start:
                if (n[1][2], n[1][0]) not in neighbors_start:
                    neighbors_start.append((n[1][0], n[1][2]))

            # find the three nearest neighbors of each point in end positions
            n = var_end.query(pos_end[i], 3)
            if (n[1][0], n[1][1]) not in neighbors_end:
                if (n[1][1], n[1][0]) not in neighbors_end:
                    neighbors_end.append((n[1][0], n[1][1]))
            if (n[1][0], n[1][2]) not in neighbors_end:
                if (n[1][2], n[1][0]) not in neighbors_end:
                    neighbors_end.append((n[1][0], n[1][2]))
            n_end[i] = n[1]

        # figure
        pos = plt.figure()
        ax = plt.subplot(111)

        # draw neighbours
        n = 0
        for i in range(0, len(neighbors_end)):
            if (neighbors_end[i][0], neighbors_end[i][1]) in neighbors_start:
                c = '-b'
                n = n + 1
            elif (neighbors_end[i][1], neighbors_end[i][0]) in neighbors_start:
                c = '-b'
                n = n + 1
            else:
                c = '-r'
            plt.plot((pos_end[int(neighbors_end[i][0])][0], pos_end[int(neighbors_end[i][1])][0]),
                     (pos_end[int(neighbors_end[i][0])][1], pos_end[int(neighbors_end[i][1])][1]),
                     c)
        # plt.text(f"Score: {n}/{len(neighbors_start)}")
        plt.figtext(0.88, 0.5, f"Score: {round(n / len(neighbors_start), 2) * 100} %", horizontalalignment="right",
                    verticalalignment="top", fontsize=12, bbox={"facecolor": "white", "alpha": 0.5, "pad": 4})
        print(f"Vronoi 4 nearest neighbours: {round(n / len(neighbors_start), 2) * 100} %")

        # draw names
        for i in range(0, 16):
            plt.text(pos_end[i][0], pos_end[i][1] + 0.01, names[i],
                     fontsize='x-small',
                     backgroundcolor=(1, 1, 1, 0.5))

        # draw points
        plt.plot(np.asarray(pos_start[:])[:, 0], np.asarray(pos_start[:])[:, 1], 'xk', label='Anfangsposition',
                 markersize=5)
        plt.plot(np.asarray(pos_end[:])[:, 0], np.asarray(pos_end[:])[:, 1], 'or', label='Endposition')

        # shrink axis
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])

        # legend and label
        plt.legend(bbox_to_anchor=(1.04, 1))
        plt.ylabel("Y-Koordinate")
        plt.xlabel("X-Koordinate")
        plt.title(f" User {id}: Positionen")

        # save
        plt.savefig(f"{SAVEPATH}/User{id}_Neighbors")

    def plot_del(self, pos_start, pos_end, names, id):
        """
        plot delauny diagram
        :param pos_start:
        :param pos_end:
        :param names:
        :param id:
        """
        f, (ax1, ax2) = plt.subplots(1, 2)

        # first diagram
        tri1 = Delaunay(pos_start)
        fig1 = delaunay_plot_2d(tri1, ax1)
        for i in range(0, len(tri1.points)):
            ax1.text(tri1.points[i, 0], tri1.points[i, 1], names[i],
                     fontsize='x-small',
                     backgroundcolor=(1, 1, 1, 0.5), figure=fig1)
        neib1 = self.__delauny_neighbours(tri1)

        # second diagram
        tri2 = Delaunay(pos_end)
        fig2 = delaunay_plot_2d(tri2, ax2)
        for i in range(0, len(tri2.points)):
            ax2.text(tri2.points[i][0], tri2.points[i][1], names[i],
                     fontsize='x-small',
                     backgroundcolor=(1, 1, 1, 0.5), figure=fig2)
        neib2 = self.__delauny_neighbours(tri2)
        match = self.__delauny_coverage(neib1, neib2)

        print(f"Delauny nearest neighbours: {match} %")
        fig2.suptitle(f" User {id}: Delaunay")
        self.del_data.append(match)

    def calculate_quadrants(self, startPos, endPos):
        error = 0
        for i in range(len(startPos)):
            startQuad = self.__quadrants(startPos[i], startPos)
            endQuad = self.__quadrants(endPos[i], endPos)
            error = error + self.__compare_quadrants(startQuad, endQuad)

        self.quadrants_total_error.append(error)
        self.quadrants_error_perc.append((error / 240) * 100)

    def plot_example_quadrants(self, orig, pos):
        pos_trans = np.zeros((len(pos), 2))

        # koordinatentransformation
        pos_trans[:, 0] = pos[:, 0] - orig[0]
        pos_trans[:, 1] = pos[:, 1] - orig[1]

        ax = plt.subplot(111)

        for m in range(len(pos_trans)):
            if pos_trans[m, 1] == 0 and pos_trans[m, 0] == 0:
                c = 'om'
                legend = 'Zentrum'
            elif pos_trans[m, 1] < 0:
                if pos_trans[m, 0] < 0:
                    c = 'ob'
                    legend = 'Quadrant 1'
                else:
                    c = 'or'
                    legend = 'Quadrant 2'
            else:
                if pos_trans[m, 0] < 0:
                    c = 'og'
                    legend = 'Quadrant 3'
                else:
                    c = 'oy'
                    legend = 'Quadrant 4'
            plt.plot(pos_trans[m, 0], pos_trans[m, 1], c, label=legend)

        # sort  labels and handles by labels
        handles, labels = ax.get_legend_handles_labels()
        labels, handles = zip(*sorted(zip(labels, handles), key=lambda t: t[0]))

        # get unique labels
        unique = [(h, l) for n, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:n]]
        ax.legend(*zip(*unique), bbox_to_anchor=(1.04, 1))

        # move axis to center
        ax.spines[["left", "bottom"]].set_position(("data", 0))
        # Hide others.
        ax.spines[["top", "right"]].set_visible(False)

        # draw arrow
        ax.plot(1, 0, ">k", transform=ax.get_yaxis_transform(), clip_on=False)
        ax.plot(0, 1, "^k", transform=ax.get_xaxis_transform(), clip_on=False)

        # shrink axis
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])

        plt.title("Einteilung der Punktmenge nach Quadranten")

    def __delauny_neighbours(self, tri):
        """
        calculate delauny neighbors
        :param tri:
        :return:
        """
        l = tri.vertex_neighbor_vertices
        neib = []
        for i in range(len(l[0]) - 1):
            neib.append(list(l[1][l[0][i]:l[0][i + 1]]))
        return neib

    def __delauny_coverage(self, neib1, neib2):
        """
        compare equal delauny neighbours
        :param neib1:
        :param neib2:
        :return: percent value
        """
        perc_points = np.zeros(16)
        for i in range(0, len(neib1)):
            equal = 0
            for j in range(0, len(neib1[i])):
                if neib1[i][j] in neib2[i]:
                    equal = equal + 1
                perc_points[i] = equal / len(neib1[i])
        return np.mean(perc_points) * 100

    def __quadrants(self, orig, pos):
        pos_trans = np.zeros((len(pos), 2))
        quadrants = np.empty(len(pos), dtype=object)

        # koordinatentransformation
        pos_trans[:, 0] = pos[:, 0] - orig[0]
        pos_trans[:, 1] = pos[:, 1] - orig[1]

        for i in range(len(pos_trans)):
            if pos_trans[i, 1] == 0 and pos_trans[i, 0] == 0:
                c = 'center'
            elif pos_trans[i, 1] < 0:
                if pos_trans[i, 0] < 0:
                    c = 'lowerLeft'
                else:
                    c = 'lowerRight'
            else:
                if pos_trans[i, 0] < 0:
                    c = 'upperLeft'
                else:
                    c = 'upperRight'
            quadrants[i] = c

        return quadrants

    def __compare_quadrants(self, start, end):
        correct = 0
        false = 0

        for k in range(len(start)):
            if start[k] == end[k]:
                if start[k] != 'center':
                    correct = correct + 1
            else:
                false = false + 1
        if len(start) != 16:
            false = false + (16 - len(start))
        return false




