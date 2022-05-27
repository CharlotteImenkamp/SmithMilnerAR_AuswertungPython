import json
import numpy as np
import pandas as pd


class Times:
    def __init__(self):
        self.movement_times = []

    def get_delta_time(self, datapath):
        times = []
        o = open(datapath)
        data = json.load(o)
        tmp = data["entries"]
        o.close()
        difference = tmp[-1]['Time'] - tmp[0]['Time']
        self.movement_times.append(difference)

    def save(self):
        if len(self.movement_times) is not 0:
            print(f" Mean Movement Time JG: {np.mean(self.movement_times[0:21])}")
            print(f" Mean Movement Time AG: {np.mean(self.movement_times[21:41])}")
            df = pd.DataFrame(self.movement_times)
            df.to_excel("Results/Auswertung_zeiten.xlsx")


