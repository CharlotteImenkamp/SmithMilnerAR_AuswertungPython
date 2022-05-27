import json
import numpy as np
import matplotlib.pyplot as plt


class ObjectMovement:

    def __load_moving_pos(self, path):
        positions = {}
        o = open(path)
        data = json.load(o)
        tmp = data["entries"]
        offset = data["entries"][0]["PositionOffset"]
        o.close()

        for p in tmp:
            p = p['GameObjects'][0]
            key = f"{p['Objectname']}"
            value = [p['GlobalPosition']['x'] + offset['x'],
                     p['GlobalPosition']['y'] + offset['y'],
                     p['GlobalPosition']['z'] + offset['z']]
            if key in positions:
                positions[key].append(value)
            else:
                positions[key] = [value]
        return positions

    def __plot(self, start, end, moving, id):
        line_color = (0.1, 0.2, 0.5, 0.5)
        line_size = 2
        line_style = 'dotted'
        pos = plt.figure()
        ax = plt.subplot(111)

        # convert dict values to array
        s = np.squeeze(np.array(list(start.values())))
        e = np.squeeze(np.array(list(end.values())))
        # s = np.squeeze(np.array(start))
        # e = np.squeeze(np.array(end))

        # draw points
        plt.plot(s[:, 0], s[:, 2], 'ob', label='Anfangsposition')
        plt.plot(e[:, 0], e[:, 2], 'or', label='Endposition')

        # draw movement
        for k in moving.keys():
            # first line
            plt.plot((start[k][0][0], moving[k][0][0]),
                     (start[k][0][2], moving[k][0][2]),
                     linestyle=line_style, color=line_color, linewidth=line_size)
            # movement lines
            for m in range(len(moving[k]) - 1):
                plt.plot((moving[k][m][0], moving[k][m + 1][0]),
                         (moving[k][m][2], moving[k][m + 1][2]),
                         linestyle=line_style, color=line_color, linewidth=line_size)
                # last line
                if m == len(moving[k]) - 2:
                    plt.plot((moving[k][m + 1][0], end[k][0][0]),
                             (moving[k][m + 1][2], end[k][0][2]),
                             linestyle=line_style, color=line_color, linewidth=line_size)

        # shrink axis
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])

        # legend and label
        plt.legend(bbox_to_anchor=(1.04, 1))
        plt.ylabel("Y-Koordinate")
        plt.xlabel("X-Koordinate")
        plt.ylim((0.8, 1.5))
        plt.title(f" Proband {id}: Objektbewegung")

        # save
        plt.savefig(f"Results/Movement/User{id}_Movement")

    def __load_positions(self, datapath):
        positions = {}
        o = open(datapath)
        data = json.load(o)
        tmp = data["entries"][0]["GameObjects"]
        offset = data["entries"][0]["PositionOffset"]
        o.close()
        for p in tmp:
            key = p["Objectname"]
            value = [p['GlobalPosition']['x'] + offset['x'],
                     p['GlobalPosition']['y'] + offset['y'],
                     p['GlobalPosition']['z'] + offset['z']]
            positions[key] = [value]
        return positions

    def add_user(self, path_start, path_end, path_moving, id):
        pos_start = self.__load_positions(path_start)
        pos_end = self.__load_positions(path_end)
        pos_moving = self.__load_moving_pos(path_moving)
        self.__plot(pos_start, pos_end, pos_moving, id)
