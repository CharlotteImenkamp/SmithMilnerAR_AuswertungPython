import numpy as np
import pandas as pd
import math
import json


class Rotations:
    def __init__(self):
        self.error = pd.DataFrame()

    def save(self, names):
        self.error["Objekte"] = names
        self.error.to_excel("Results/Rotationen.xlsx")
        # print(self.error)

    def __abs_error_alt(self, start, end):
        diff = []
        for i in range(len(start)):
            s = self.__euler_y_from_quaternion(start[i])
            e = self.__euler_y_from_quaternion(end[i])
            diff.append(self.__difference(s, e))
        return np.asarray(diff)

    def __rad_to_degree(self, r):
        return r * (360 / (2 * math.pi)) + 180

    def __difference(self, a, b):
        return a - b if a > b else b - a

    def __euler_y_from_quaternion(self, quat):
        x = quat[0]
        y = quat[1]
        z = quat[2]
        w = quat[3]

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)

        return self.__rad_to_degree(pitch_y)  # in deg

    def __load_rotations(self, path_end, path_start):
        endrot = []
        names = []
        startrot = []

        # end positions
        o = open(path_end)
        data = json.load(o)
        tmp = data["entries"][0]["GameObjects"]
        o.close()

        for p in tmp:
            x = p['GlobalRotation']['x']
            y = p['GlobalRotation']['y']
            z = p['GlobalRotation']['z']
            w = p['GlobalRotation']['w']
            endrot.append([x, y, z, w])
            names.append(p['Objectname'])

        # start positions
        o = open(path_start)
        data = json.load(o)
        tmp = data["entries"][0]["GameObjects"]
        o.close()

        for p in tmp:
            x = p['GlobalRotation']['x']
            y = p['GlobalRotation']['y']
            z = p['GlobalRotation']['z']
            w = p['GlobalRotation']['w']
            startrot.append([x, y, z, w])

        return startrot, endrot, names

    def add_user(self, pathEnd, pathStart, id):
        startRot, endRot, names = self.__load_rotations(pathEnd, pathStart)
        abs_error = self.__abs_error_alt(startRot, endRot)
        self.error[f'User {id}'] = abs_error

