import json
import numpy as np
import matplotlib.pyplot as plt


class HandMovement:
    def __init__(self, type):
        self.type = type

    def add_user(self, path, path_start, path_end, path_corner, id):

        pos_start = self.__load_objects(f"Data/User{id}/{path_start}{id}.json")
        pos_end = self.__load_objects(f"Data/User{id}/{path_end}{id}.json")
        pos_corner = self.__load_corners(f"{path_corner}")
        pos_l_wrist, pos_r_wrist, pos_l_palm, pos_l_tips, pos_l_dist, pos_l_mid, pos_l_meta, pos_r_palm, pos_r_tips, \
        pos_r_dist, pos_r_mid, pos_r_meta = self.__load_hand_pos(f"{path}")

        # points = self.__intersection_point(plane_normal, plane_point1, origin, direction)
        self.__plot_heatmap(pos_l_wrist, pos_r_wrist, pos_l_tips, pos_r_tips, pos_l_dist, pos_r_dist,
                       pos_l_mid, pos_r_mid, pos_l_meta, pos_r_meta, pos_start, pos_end, pos_corner, id)

    def __load_hand_pos(self, datapath):
        l_wrist = []
        r_wrist = []
        l_palm = []
        r_palm = []

        l_tips = []
        r_tips = []
        l_distal = []
        r_distal = []
        l_metaca = []
        r_metaca = []
        l_middle = []
        r_middle = []

        o = open(datapath)
        data = json.load(o)
        tmp = data["entries"]
        o.close()

        for p in tmp:
            l_wrist.append(np.asarray([float(p['LeftWrist']['x']), float(p['LeftWrist']['y']),
                                       float(p['LeftWrist']['z'])]))
            r_wrist.append(np.asarray([float(p['RightWrist']['x']), float(p['RightWrist']['y']),
                                       float(p['RightWrist']['z'])]))
            l_palm.append(np.asarray([float(p['LeftPalm']['x']), float(p['LeftPalm']['y']), float(p['LeftPalm']['z'])]))
            r_palm.append(np.asarray([float(p['RightPalm']['x']), float(p['RightPalm']['y']),
                                      float(p['RightPalm']['z'])]))

            # 0-> thumb, 1-> index finger, 2-> middle finger, 3-> ring finger, 4-> pinky
            l_tips.append(np.asarray([[p['LeftTips'][0]['x'], p['LeftTips'][0]['y'], p['LeftTips'][0]['z']],
                                     [p['LeftTips'][1]['x'], p['LeftTips'][1]['y'], p['LeftTips'][1]['z']],
                                     [p['LeftTips'][2]['x'], p['LeftTips'][2]['y'], p['LeftTips'][2]['z']],
                                     [p['LeftTips'][3]['x'], p['LeftTips'][3]['y'], p['LeftTips'][3]['z']],
                                     [p['LeftTips'][4]['x'], p['LeftTips'][4]['y'], p['LeftTips'][4]['z']]]))
            r_tips.append(np.asarray([[p['RightTips'][0]['x'], p['RightTips'][0]['y'], p['RightTips'][0]['z']],
                                     [p['RightTips'][1]['x'], p['RightTips'][1]['y'], p['RightTips'][1]['z']],
                                     [p['RightTips'][2]['x'], p['RightTips'][2]['y'], p['RightTips'][2]['z']],
                                     [p['RightTips'][3]['x'], p['RightTips'][3]['y'], p['RightTips'][3]['z']],
                                     [p['RightTips'][4]['x'], p['RightTips'][4]['y'], p['RightTips'][4]['z']]]))
            l_distal.append(np.asarray([[p['LeftDistal'][0]['x'], p['LeftDistal'][0]['y'], p['LeftDistal'][0]['z']],
                                       [p['LeftDistal'][1]['x'], p['LeftDistal'][1]['y'], p['LeftDistal'][1]['z']],
                                       [p['LeftDistal'][2]['x'], p['LeftDistal'][2]['y'], p['LeftDistal'][2]['z']],
                                       [p['LeftDistal'][3]['x'], p['LeftDistal'][3]['y'], p['LeftDistal'][3]['z']],
                                       [p['LeftDistal'][4]['x'], p['LeftDistal'][4]['y'], p['LeftDistal'][4]['z']]]))
            r_distal.append(np.asarray([[p['RightDistal'][0]['x'], p['RightDistal'][0]['y'], p['RightDistal'][0]['z']],
                                       [p['RightDistal'][1]['x'], p['RightDistal'][1]['y'], p['RightDistal'][1]['z']],
                                       [p['RightDistal'][2]['x'], p['RightDistal'][2]['y'], p['RightDistal'][2]['z']],
                                       [p['RightDistal'][3]['x'], p['RightDistal'][3]['y'], p['RightDistal'][3]['z']],
                                       [p['RightDistal'][4]['x'], p['RightDistal'][4]['y'], p['RightDistal'][4]['z']]]))
            l_middle.append(np.asarray([[p['LeftMiddle'][0]['x'], p['LeftMiddle'][0]['y'], p['LeftMiddle'][0]['z']],
                                       [p['LeftMiddle'][1]['x'], p['LeftMiddle'][1]['y'], p['LeftMiddle'][1]['z']],
                                       [p['LeftMiddle'][2]['x'], p['LeftMiddle'][2]['y'], p['LeftMiddle'][2]['z']],
                                       [p['LeftMiddle'][3]['x'], p['LeftMiddle'][3]['y'], p['LeftMiddle'][3]['z']],
                                       [p['LeftMiddle'][4]['x'], p['LeftMiddle'][4]['y'], p['LeftMiddle'][4]['z']]]))
            r_middle.append(np.asarray([[p['RightMiddle'][0]['x'], p['RightMiddle'][0]['y'], p['RightMiddle'][0]['z']],
                                       [p['RightMiddle'][1]['x'], p['RightMiddle'][1]['y'], p['RightMiddle'][1]['z']],
                                       [p['RightMiddle'][2]['x'], p['RightMiddle'][2]['y'], p['RightMiddle'][2]['z']],
                                       [p['RightMiddle'][3]['x'], p['RightMiddle'][3]['y'], p['RightMiddle'][3]['z']],
                                       [p['RightMiddle'][4]['x'], p['RightMiddle'][4]['y'], p['RightMiddle'][4]['z']]]))
            l_metaca.append(np.asarray([[p['LeftMetacarpal'][0]['x'], p['LeftMetacarpal'][0]['y'], p['LeftMetacarpal']
                                       [0]['z']], [p['LeftMetacarpal'][1]['x'], p['LeftMetacarpal'][1]['y'],
                                       p['LeftMetacarpal'][1]['z']], [p['LeftMetacarpal'][2]['x'], p['LeftMetacarpal']
                                       [2]['y'], p['LeftMetacarpal'][2]['z']], [p['LeftMetacarpal'][3]['x'],
                                       p['LeftMetacarpal'][3]['y'], p['LeftMetacarpal'][3]['z']], [p['LeftMetacarpal']
                                       [4]['x'], p['LeftMetacarpal'][4]['y'], p['LeftMetacarpal'][4]['z']]]))
            r_metaca.append(np.asarray([[p['RightMetacarpal'][0]['x'], p['RightMetacarpal'][0]['y'],
                                       p['RightMetacarpal'][0]['z']], [p['RightMetacarpal'][1]['x'],
                                       p['RightMetacarpal'][1]['y'], p['RightMetacarpal'][1]['z']],
                                       [p['RightMetacarpal'][2]['x'], p['RightMetacarpal'][2]['y'], p['RightMetacarpal']
                                       [2]['z']], [p['RightMetacarpal'][3]['x'], p['RightMetacarpal'][3]['y'],
                                       p['RightMetacarpal'][3]['z']], [p['RightMetacarpal'][4]['x'],
                                       p['RightMetacarpal'][4]['y'], p['RightMetacarpal'][4]['z']]]))

        return (np.asarray(l_wrist), np.asarray(r_wrist),
                np.asarray(l_palm), np.asarray(l_tips), np.asarray(l_distal), np.asarray(l_middle),
                np.asarray(l_metaca), np.asarray(r_palm), np.asarray(r_tips), np.asarray(r_distal), np.asarray(r_middle),
                np.asarray(r_metaca))

    def __load_objects(self, datapath):
        positions = []
        o = open(datapath)
        data = json.load(o)
        tmp = data["entries"][0]["GameObjects"]
        offset = data["entries"][0]["PositionOffset"]
        o.close()

        for p in tmp:
            positions.append(([p['GlobalPosition']['x'], # + offset['x'],
                               p['GlobalPosition']['y'], # + offset['y'],
                               p['GlobalPosition']['z']])) # + offset['z']]))
        return np.asarray(positions)

    def __load_corners(self, datapath):
        positions = []
        o = open(datapath)
        data = json.load(o)
        tmp = data["entries"]
        o.close()

        for p in tmp:
            positions.append(np.asarray([p['TopLeft']['x'], p['TopLeft']['y'], p['TopLeft']['z']]))
            positions.append(np.asarray([p['TopRight']['x'], p['TopRight']['y'], p['TopRight']['z']]))
            positions.append(np.asarray([p['BotLeft']['x'], p['BotLeft']['y'], p['BotLeft']['z']]))
            positions.append(np.asarray([p['BotRight']['x'], p['BotRight']['y'], p['BotRight']['z']]))
        return np.asarray(positions)

    def __plot_heatmap(self, l_wrist_points, r_wrist_points, l_tips_points, r_tips_points, l_dist_points, r_dist_points,
                       l_mid_points, r_mid_points, l_meta_points, r_meta_points, obj_start, obj_end, tbl_corner, id):
        # right side azur, left side purple
        fig = plt.figure()
        plt.plot(l_wrist_points[:, 0], l_wrist_points[:, 2], 'o', markersize=5, color=(0.6, 0.0, 0.8, 0.1),
                 label="linkes Handgelenk")
        plt.plot(r_wrist_points[:, 0], r_wrist_points[:, 2], 'o', markersize=5, color=(0.0, 0.8, 0.8, 0.1),
                 label="rechtes Handgelenk")

        plt.plot(l_tips_points[0, 0], l_tips_points[0, 2], 'o', markersize=5, color=(0.75, 0.3, 0.9, 0.1),
                 label="linke Daumenspitzen")
        plt.plot(l_tips_points[1, 0], l_tips_points[1, 2], 'o', markersize=5, color=(0.75, 0.3, 0.9, 0.1),
                 label="linke Zeigefingerspitzen")
        plt.plot(r_tips_points[0, 0], r_tips_points[0, 2], 'o', markersize=5, color=(0.7, 0.9, 0.9, 0.1),
                 label="rechte Daumenspitzen")
        plt.plot(r_tips_points[1, 0], r_tips_points[1, 2], 'o', markersize=5, color=(0.7, 0.9, 0.9, 0.1),
                 label="rechte Zeigefingerspitzen")
        # plt.plot(l_tips_points[:, 0], l_tips_points[:, 2], 'o', markersize=5, color=(1.0, 0.5, 0.5, 0.1),
        #         label="Position linke Fingerspitzen")
        # plt.plot(r_tips_points[:, 0], r_tips_points[:, 2], 'o', markersize=5, color=(0.5, 1.0, 0.5, 0.1),
        #         label="Position rechte Fingerspitzen")

        # plt.plot(l_dist_points[:, 0], l_dist_points[:, 2], 'o', markersize=5, color=(0.9, 0.3, 0.3, 0.1),
        #         label="Position linkes Distalgelenk")
        # plt.plot(r_dist_points[:, 0], r_dist_points[:, 2], 'o', markersize=5, color=(0.3, 0.9, 0.3, 0.1),
        #         label="Position rechtes Distalgelenk")

        # plt.plot(l_mid_points[:, 0], l_mid_points[:, 2], 'o', markersize=5, color=(0.8, 0.2, 0.2, 0.1),
        #         label="Position linkes Mittelgelenk")
        # plt.plot(r_mid_points[:, 0], r_mid_points[:, 2], 'o', markersize=5, color=(0.2, 0.8, 0.2, 0.1),
        #         label="Position rechtes Mittelgelenk")

        # plt.plot(l_meta_points[:, 0], l_meta_points[:, 2], 'o', markersize=5, color=(0.7, 0.1, 0.1, 0.1),
        #         label="Position linkes Metacarpalgelenk")
        # plt.plot(r_meta_points[:, 0], r_meta_points[:, 2], 'o', markersize=5, color=(0.1, 0.7, 0.1, 0.1),
        #         label="Position rechtes Metacarpalgelenk")

        plt.plot(obj_start[:, 0], obj_start[:, 2], 'og', markersize=4, label="Startposition")
        plt.plot(obj_end[:, 0], obj_end[:, 2], 'or', markersize=4, label="Endposition")
        plt.plot(tbl_corner[:, 0], tbl_corner[:, 2], 'ob', markersize=4, label="Tischecken")
        plt.ylabel("Y-Koordinate")
        plt.xlabel("X-Koordinate")
        plt.ylim(((tbl_corner[2, 2]-0.1), (tbl_corner[0, 2]+0.1)))
        plt.xlim((tbl_corner[0, 0]-0.1, tbl_corner[1, 0]+0.5))
        plt.legend()
        plt.title(f" User {id}: Handbewegungen Ortsabfrage")

        # save
        plt.savefig(f"Results/Heatmap/User{id}_Handmap_{self.type}_variante")

    def __plot_3D(self, lWrist, rWrist, objects, id):
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        for i in range(len(lWrist)):
            ax.plot3D((lWrist[i, 0], lWrist[i, 0]),  # + [i, 0]),
                      (lWrist[i, 1], lWrist[i, 1]),  # + direc[i, 1]),
                      (lWrist[i, 2], lWrist[i, 2]))  # + direc[i, 2]))
            ax.plot3D((rWrist[i, 0], rWrist[i, 0]),  # + [i, 0]),
                      (rWrist[i, 1], rWrist[i, 1]),  # + direc[i, 1]),
                      (rWrist[i, 2], rWrist[i, 2]))  # + direc[i, 2]))

            ax.plot3D(objects[:, 0], objects[:, 1], objects[:, 2], marker='*')
            ax.plot3D(lWrist[:, 0], lWrist[:, 1], lWrist[:, 2], marker='+')
            ax.plot3D(rWrist[:, 0], rWrist[:, 1], rWrist[:, 2], marker='-')
            plt.title(f" User {id}: 3D Plot")
            plt.savefig(f"Images/User{id}_3DPlot_{self.type}")
