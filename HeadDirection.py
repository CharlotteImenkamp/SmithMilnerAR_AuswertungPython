import json
import numpy as np
import matplotlib.pyplot as plt


class HeadDirection:
    def __init__(self, type):
        self.type = type

    def add_user(self, path, path_obj, path_end, id):
        origin, direction = self.__load_gaze(f"Data/User{id}/{path}{self.type}{id}.json")
        pos = self.__load_objects(f"Data/User{id}/{path_obj}{id}.json")
        pos_end = self.__load_objects(f"Data/User{id}/{path_end}{id}.json")
        plane_point1 = np.array([pos[0, 0], pos[0, 1], pos[0, 2]])
        plane_point2 = np.array([pos[1, 0], pos[1, 1], pos[1, 2]])
        plane_point3 = np.array([pos[2, 0], pos[2, 1], pos[2, 2]])
        plane_normal = np.cross(plane_point3 - plane_point1, plane_point2 - plane_point1)
        points = self.__intersection_point(plane_normal, plane_point1, origin, direction)
        self.__plot_heatmap(np.asarray(points), pos, pos_end, id)
        # self.__plot_3D(origin, direction, pos, userID[i])

    def __load_gaze(self, datapath):
        orig = []
        dir = []

        o = open(datapath)
        data = json.load(o)
        tmp = data["entries"]
        o.close()

        for p in tmp:
            orig.append(np.asarray([p['GazeOrigin']['x'], p['GazeOrigin']['y'], p['GazeOrigin']['z']]))
            dir.append(np.asarray([p['GazeDirection']['x'], p['GazeDirection']['y'], p['GazeDirection']['z']]))

        return np.asarray(orig), np.asarray(dir)

    def __load_objects(self, datapath):
        positions = []
        o = open(datapath)
        data = json.load(o)
        tmp = data["entries"][0]["GameObjects"]
        offset = data["entries"][0]["PositionOffset"]
        o.close()

        for p in tmp:
            positions.append(([p['GlobalPosition']['x'] + offset['x'],
                               p['GlobalPosition']['y'] + offset['y'],
                               p['GlobalPosition']['z'] + offset['z']]))
        return np.asarray(positions)

    def __intersection_point(self, plane_n, plane_p, orig, direc):
        res = []
        for r in range(len(orig)):
            r3 = np.dot(direc[r], plane_n)
            if r3 == 0:
                print("FAILED")
            else:
                p3 = np.dot(orig[r] - plane_p, plane_n)
                a = -p3 / r3
                res.append(orig[r] + a * direc[r])
        return res

    def __plot_heatmap(self, intersection_points, obj_points, obj_end, id):
        fig = plt.figure()
        # plt.plot(intersection_points[:, 0], intersection_points[:, 2], 'o', markersize=6, color=(0.1, 0.2, 0.5, 0.05),
        # label="Blickpunkt")
        plt.plot(intersection_points[:, 0], intersection_points[:, 2], 'o', markersize=10, color=(0.1, 0.2, 0.5, 0.5),
                 label="Blickpunkt")
        plt.plot(obj_points[:, 0], obj_points[:, 2], 'og', markersize=4, label="Startposition")
        plt.plot(obj_end[:, 0], obj_end[:, 2], 'or', markersize=4, label="Endposition")
        plt.ylabel("Y-Koordinate")
        plt.xlabel("X-Koordinate")
        plt.ylim((0.9, 1.5))
        plt.xlim((-0.45, 0.65))
        plt.legend()
        plt.title(f" User {id}: Brillenausrichtung Ortsabfrage")

        # save
        plt.savefig(f"Results/Heatmap/User{id}_Heatmap_{self.type}_variante")

    def __plot_3D(self, orig, direc, objects, id):
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        for i in range(len(orig)):
            ax.plot3D((orig[i, 0], orig[i, 0] + direc[i, 0]),
                      (orig[i, 1], orig[i, 1] + direc[i, 1]),
                      (orig[i, 2], orig[i, 2] + direc[i, 2]))
        ax.plot3D(objects[:, 0], objects[:, 1], objects[:, 2], marker='*')
        ax.plot3D(orig[:, 0], orig[:, 1], orig[:, 2], marker='+')
        plt.title(f" User {id}: 3D Plot")
        plt.savefig(f"Images/User{id}_3DPlot_{self.type}")

