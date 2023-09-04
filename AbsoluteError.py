import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


class AbsoluteError:
    def __init__(self):
        self.data = []
        self.dist_data = pd.DataFrame()

    def write_excel_file(self):
        if len(self.data) is not 0:
            self.__write_excel_mean_std_min_max(self.data)
        if len(self.dist_data) is not 0:
            self.dist_data.insert(0, 'Names', self.names)
            self.dist_data.to_excel("Results/Auswertung_AR_Distanzen.xlsx")
        if len(self.del_data) is not 0:
            self.__excel.write_excel_neighbors(self.del_data)

    # calculate and plot absolute distances, mean, std ...
    def plot_dist(self, pos_start, pos_end, names, id):
        dist = self.__calculate_error_distances(pos_start, pos_end)
        mean = np.mean(dist)
        # print(f"\nPunkte: {dist} \n")
        print(f"M: {mean}\tSD: {np.std(dist)}\tMax.: {np.max(dist)} \tMin: {np.min(dist)}")

        # plot figure
        fig = plt.figure()
        ax = plt.subplot(111)
        plt.title(f" User {id}: Absolute Distanzen")
        plt.xticks(list(range(0, 16)), names, rotation='vertical')
        plt.ylabel("Distanzen in Unity Einheiten")
        plt.xlabel("Objekte")

        plt.plot(list(range(0, 16)), dist, '+b', label="Absoluter Fehler")
        plt.plot((0, 15), (mean, mean), '--k', label="Mittlerer absoluter Fehler")

        # shrink axis
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + 0.3 * box.height, box.width, box.height * 0.7])
        plt.legend()

        # save
        plt.savefig(f"Results/Images/User{id}_Distanz")

        d = [mean, np.std(dist), np.min(dist), np.max(dist)]
        self.data.append(d)
        self.dist_data[f'User {id}'] = self.__make_position_df(self, pos_start, pos_end)

    # plot positions of objects at start and end
    def plot_pos(self, pos_start, pos_end, names, id):
        pos = plt.figure()
        ax = plt.subplot(111)

        # draw error distances
        for i in range(0, 16):
            if i == 0:
                plt.plot((pos_start[i][0], pos_end[i][0]), (pos_start[i][1], pos_end[i][1]), '--b', label='error')
            else:
                plt.plot((pos_start[i][0], pos_end[i][0]), (pos_start[i][1], pos_end[i][1]), '--b')
            plt.text(pos_start[i][0], pos_start[i][1] + 0.01, names[i],
                     fontsize='x-small',
                     backgroundcolor=(1, 1, 1, 0.5))
        # draw points
        plt.plot(np.asarray(pos_start[:])[:, 0], np.asarray(pos_start[:])[:, 1], 'ob', label='start position')
        plt.plot(np.asarray(pos_end[:])[:, 0], np.asarray(pos_end[:])[:, 1], 'or', label='end position')

        # shrink axis
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 1.0, box.height * 1.0])

        # legend and label
        plt.legend(loc = 'lower right') #bbox_to_anchor= (1, 0))# (1.04, 1))
        plt.ylabel("y-coordinate")
        plt.xlabel("x-coordinate")
        plt.title(f" User {id}: positions")

        # save
        plt.savefig(f"Results/Images/User{id}_Positionen")

    @staticmethod
    def __make_position_df(self, pos_start, pos_end):
        dist = np.zeros(16)
        for i in range(0, 16):
            dist[i] = np.sqrt(np.sum(np.square(np.asarray(pos_start)[i] - np.asarray(pos_end)[i])))
        return dist

    # calculate error distances
    def __calculate_error_distances(self, pos_start, pos_end):
        dist = np.zeros(16)
        for i in range(0, 16):
            dist[i] = np.sqrt(np.sum(np.square(np.asarray(pos_start)[i] - np.asarray(pos_end)[i])))
        return dist

    def __write_excel_mean_std_min_max(self, data):
        col = []
        for d in range(0, len(data)):
            col.append(str(d))
        df = pd.DataFrame(data, columns=['Mittelwert', 'Standardabweichung', 'Min', 'Max'])
        df.to_excel("Auswertung_AR_absolut.xlsx")

    def __write_excel_neighbors(self, data):
        col = []
        for d in range(0, len(data)):
            col.append(str(d))
        df = pd.DataFrame(data, columns=['Prozent'])
        df.to_excel("Auswertung_AR_relativ.xlsx")


