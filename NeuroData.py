import pandas as pd


def load(self, start, end):
    file = pd.read_excel('Data/Auswertung_Copy.xlsx')
    self.vlmt_sum = file.iloc[15, start:end]
    self.vlmt_diff = file.iloc[16, start:end]
    self.vlmt_7 = file.iloc[13, start:end]
    self.figur_abmalen = file.iloc[17, start:end]
    self.figur_abruf = file.iloc[18, start:end]
    self.tmt_zahl = file.iloc[20, start:end]
    self.tmt_buchst = file.iloc[21, start:end]
    self.stroop_wort = file.iloc[23, start:end]
    self.stroop_farbe = file.iloc[24, start:end]
    self.ar_abruf = file.iloc[27, start:end]
    self.ar_recog = file.iloc[28, start:end]
    self.feedback = file.iloc[30:39, start:end]
    file2 = pd.read_excel('Data/Auswertung_AR_absolut_Copy.xlsx')
    self.ar_positions_abs = file2.iloc[2, start:end]
    file3 = pd.read_excel('Data/Auswertung_AR_relativ_Copy.xlsx')
    self.ar_positions_rel = file3.iloc[2, start:end]


class NeuroData:
    def __init__(self, type):
        self.vlmt_sum = []
        self.vlmt_diff = []
        self.vlmt_7 = []
        self.figur_abmalen = []
        self.figur_abruf = []
        self.tmt_zahl = []
        self.tmt_buchst = []
        self.stroop_wort = []
        self.stroop_farbe = []
        self.ar_abruf = []
        self.ar_recog = []
        self.ar_positions_rel = []
        self.ar_positions_abs = []
        self.feedback= []
        if type == 'JG':
            load(self, 2, 22)
        elif type == 'AG':
            load(self, 32, 52)

