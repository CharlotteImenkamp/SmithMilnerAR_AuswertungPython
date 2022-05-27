import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from NeuroData import NeuroData


class Testbatterie:
    def __init__(self, printExcel, vlmt, tmt, stroop, ar, figur, feedback):
        self.printExcel = printExcel
        self.vlmt = vlmt
        self.tmt = tmt
        self.stroop = stroop
        self.ar = ar
        self.figur = figur
        self.feedback = feedback

        jg = NeuroData('JG')
        ag = NeuroData('AG')

        if self.vlmt:
            xticks = []
            legend = ['JG', 'AG']

            d = {}
            d = {'Data': np.concatenate((jg.vlmt_diff, ag.vlmt_diff)),
                 'Type': np.repeat('Differenz DG5 -DG1', 40),
                 'Gruppe': np.concatenate((np.repeat('JG', 20), np.repeat('AG', 20)))}
            f = pd.DataFrame(data=d)

            e = {}
            e = {'Data': np.concatenate((jg.vlmt_sum, ag.vlmt_sum)),
                 'Type': np.repeat('Summe DG1 - DG5', 40),
                 'Gruppe': np.concatenate((np.repeat('JG', 20), np.repeat('AG', 20)))}
            f1 = pd.DataFrame(data=e)

            g = {}
            g = {'Data': np.concatenate((jg.vlmt_7, ag.vlmt_7)),
                 'Type': np.repeat('DG7', 40),
                 'Gruppe': np.concatenate((np.repeat('JG', 20), np.repeat('AG', 20)))}
            f2 = pd.DataFrame(data=g)
            cdf = pd.concat([f, f1, f2])

            self.__seaborn_boxplot(cdf, "VLMT", "Mittlere Punktzahl")

        if self.tmt:
            xticks = ['Zahlen', 'Buchstaben']
            legend = ['JG', 'AG']

            d = {}
            d = {'Data': np.concatenate((jg.tmt_zahl, jg.tmt_buchst, ag.tmt_zahl, ag.tmt_buchst)),
                 'Type': np.concatenate((np.repeat('Zahlen', 20), np.repeat('Buchstaben', 20),
                                         np.repeat('Zahlen', 20), np.repeat('Buchstaben', 20))),
                 'Gruppe': np.concatenate((np.repeat('JG', 40), np.repeat('AG', 40)))}

            f = pd.DataFrame(data=d)
            self.__seaborn_boxplot(f, "TMT", "Mittlere Zeit in s")

        if self.stroop:
            xticks = ['Wörter', 'Farben']
            legend = ['JG', 'AG']

            d = {}
            d = {'Data': np.concatenate((jg.stroop_wort, jg.stroop_farbe, ag.stroop_wort, ag.stroop_farbe)),
                 'Type': np.concatenate((np.repeat('Wort', 20), np.repeat('Farbe', 20),
                                         np.repeat('Wort', 20), np.repeat('Farbe', 20))),
                 'Gruppe': np.concatenate((np.repeat('JG', 40), np.repeat('AG', 40)))}
            f = pd.DataFrame(data=d)
            self.__seaborn_boxplot(f, "Stroop", "Mittlere Zeit in s")

        if self.ar:
            xticks = ['Abruf', 'Wiederkennung']
            legend = ['JG', 'AG']
            print(jg.ar_positions_rel)

            # papier
            # d = {}
            # d = {'Data': np.concatenate((jg.ar_abruf, jg.ar_recog, ag.ar_abruf, ag.ar_recog)),
              #   'Type': np.concatenate((np.repeat('Abruf', 20), np.repeat('Recognition', 20),
                #                         np.repeat('Abruf', len(ag.ar_abruf)), np.repeat('Recognition', len(ag.ar_recog)))),
                # 'Gruppe': np.concatenate((np.repeat('JG', 40), np.repeat('AG', 38)))}
            # f = pd.DataFrame(data=d)
            # self.__seaborn_boxplot(f, "AR Vortest", "Mittlere Anzahl richtiger Objekte")

            # AR ABSOLUT
            d = {}
            d = {'Data': np.concatenate((jg.ar_positions_abs, ag.ar_positions_abs)),
                 'Type': (np.repeat('Positions', 38)),
                 'Group': np.concatenate((np.repeat('YHA', 20), np.repeat('OHA', 18)))}
            f = pd.DataFrame(data=d)
            self.__seaborn_boxplot(f, "Absolute Error", "Absolute Error in m")

            # AR RELATIV
            d = {}
            d = {'Data': np.concatenate((jg.ar_positions_rel, ag.ar_positions_rel)),
                 'Type': (np.repeat('Positionen', 38)),
                 'Gruppe': np.concatenate((np.repeat('JG', 20), np.repeat('AG', 18)))}
            f = pd.DataFrame(data=d)
            # self.__seaborn_boxplot(f, "AR Positionen relativ", "Prozentzahl korrekter Nachbarn")

        if self.figur:
            xticks = ['Abmalen', 'Abruf']
            legend = ['JG', 'AG']

            d = {}
            d = {'Data': np.concatenate((jg.figur_abmalen, jg.figur_abruf, ag.figur_abmalen, ag.figur_abruf)),
                 'Type': np.concatenate((np.repeat('Copy', 20), np.repeat('Abruf', 20),
                                         np.repeat('Copy', 20), np.repeat('Abruf', 20))),
                 'Gruppe': np.concatenate((np.repeat('JG', 40), np.repeat('AG', 40)))}
            f = pd.DataFrame(data=d)
            self.__seaborn_boxplot(f, "Komplexe Figur", "Mittlere Bewertung")

        if self.feedback:
            feedback_fontsize_large = 'xx-large'
            feedback_fontsize_medium = 'medium'

            xticks = ['Instruktionen', 'Gefühl', 'Spaß', 'Aufmerksamkeit', 'Komplex',
                      'Real', 'Sichtbar', 'Bewegbar', 'Technik']
            legend = ['JG', 'AG']

            d = {}
            jg.feedback = jg.feedback.T
            jg.feedback.columns = ['Instructions', 'Gefühl', 'Fun', 'Aufmerksamkeit', 'Komplex',
                                   'Real', 'Sichtbar', 'Bewegbar', 'Technik']
            ag.feedback = ag.feedback.T
            ag.feedback.columns = ['Instructions', 'Gefühl', 'Fun', 'Aufmerksamkeit', 'Komplex',
                                   'Real', 'Sichtbar', 'Bewegbar', 'Technik']

            a = np.concatenate((jg.feedback['Instructions'], jg.feedback['Gefühl'], jg.feedback['Fun']))
            b = np.concatenate((a, jg.feedback['Aufmerksamkeit'], jg.feedback['Komplex']))
            c = np.concatenate((b, jg.feedback['Real'], jg.feedback['Sichtbar']))
            d = np.concatenate((c, jg.feedback['Bewegbar'], jg.feedback['Technik']))
            e = np.concatenate((d, ag.feedback['Instructions'], ag.feedback['Gefühl']))
            f = np.concatenate((e, ag.feedback['Fun'], ag.feedback['Aufmerksamkeit']))
            g = np.concatenate((f, ag.feedback['Komplex'], ag.feedback['Real']))
            h = np.concatenate((g, ag.feedback['Sichtbar'], ag.feedback['Bewegbar']))
            data = np.concatenate((h, ag.feedback['Technik']))

            i = np.concatenate((np.repeat('Instructions', 20), np.repeat('Gefühl', 20), np.repeat('Fun', 20)))
            j = np.concatenate((i, np.repeat('Aufmerksamkeit', 20), np.repeat('Komplex', 20)))
            k = np.concatenate((j, np.repeat('Real', 20), np.repeat('Sichtbar', 20)))
            l = np.concatenate((k, np.repeat('Bewegbar', 20), np.repeat('Technik', 20)))
            m = np.concatenate((l, np.repeat('Instructions', 18), np.repeat('Gefühl', 18)))
            n = np.concatenate((m, np.repeat('Fun', 18), np.repeat('Aufmerksamkeit', 18)))
            o = np.concatenate((n, np.repeat('Komplex', 18), np.repeat('Real', 18)))
            p = np.concatenate((o, np.repeat('Sichtbar', 18), np.repeat('Bewegbar', 18)))
            types = np.concatenate((p, np.repeat('Technik', 18)))

            d = {'Data': data,
                 'Type': types,
                 'Group': np.concatenate((np.repeat('YHA', 180), np.repeat('OHA', 162)))}

            # fig = plt.figure()
            df = pd.DataFrame({
                "not answered": [20-len(jg.feedback['Instructions']),
                                         20-len(ag.feedback['Instructions']),

                                         20-len(jg.feedback['Gefühl']),
                                         20-len(ag.feedback['Gefühl']),

                                         20-len(jg.feedback['Fun']),
                                         20-len(ag.feedback['Fun']),

                                         20-len(jg.feedback['Aufmerksamkeit']),
                                         20-len(ag.feedback['Aufmerksamkeit']),

                                         20-len(jg.feedback['Komplex'])+1,
                                         20-len(ag.feedback['Komplex'])+1,

                                         20-len(jg.feedback['Real']),
                                         20-len(ag.feedback['Real']),

                                                     20-len(jg.feedback['Sichtbar']),
                                         20-len(ag.feedback['Sichtbar']),

                                                     20-len(jg.feedback['Bewegbar']),
                                         20-len(ag.feedback['Bewegbar']),
                                                     20-len(jg.feedback['Technik']),
                                         20-len(ag.feedback['Technik'])],
                "strongly disagree": [list(jg.feedback['Instructions']).count(0),
                                         list(ag.feedback['Instructions']).count(0),

                                         list(jg.feedback['Gefühl']).count(0),
                                         list(ag.feedback['Gefühl']).count(0),

                                         list(jg.feedback['Fun']).count(0),
                                         list(ag.feedback['Fun']).count(0),

                                         list(jg.feedback['Aufmerksamkeit']).count(0),
                                         list(ag.feedback['Aufmerksamkeit']).count(0),

                                         list(jg.feedback['Komplex']).count(0),
                                         list(ag.feedback['Komplex']).count(0),

                                         list(jg.feedback['Real']).count(0),
                                         list(ag.feedback['Real']).count(0),

                                                     list(jg.feedback['Sichtbar']).count(0),
                                         list(ag.feedback['Sichtbar']).count(0),

                                                     list(jg.feedback['Bewegbar']).count(0),
                                         list(ag.feedback['Bewegbar']).count(0),

                                                     list(jg.feedback['Technik']).count(0),
                                         list(ag.feedback['Technik']).count(0)],

                               "disagree":[list(jg.feedback['Instructions']).count(1),
                                         list(ag.feedback['Instructions']).count(1),

                                         list(jg.feedback['Gefühl']).count(1),
                                         list(ag.feedback['Gefühl']).count(1),

                                         list(jg.feedback['Fun']).count(1),
                                         list(ag.feedback['Fun']).count(1),

                                         list(jg.feedback['Aufmerksamkeit']).count(1),
                                         list(ag.feedback['Aufmerksamkeit']).count(1),

                                         list(jg.feedback['Komplex']).count(1),
                                         list(ag.feedback['Komplex']).count(1),

                                         list(jg.feedback['Real']).count(1),
                                         list(ag.feedback['Real']).count(1),
                                                     list(jg.feedback['Sichtbar']).count(1),
                                         list(ag.feedback['Sichtbar']).count(1),

                                                     list(jg.feedback['Bewegbar']).count(1),
                                         list(ag.feedback['Bewegbar']).count(1),

                                                     list(jg.feedback['Technik']).count(1),
                                         list(ag.feedback['Technik']).count(1)],

                               "agree": [list(jg.feedback['Instructions']).count(2),
                                         list(ag.feedback['Instructions']).count(2),

                                         list(jg.feedback['Gefühl']).count(2),
                                         list(ag.feedback['Gefühl']).count(2),

                                         list(jg.feedback['Fun']).count(2),
                                         list(ag.feedback['Fun']).count(2),

                                         list(jg.feedback['Aufmerksamkeit']).count(2),
                                         list(ag.feedback['Aufmerksamkeit']).count(2),

                                         list(jg.feedback['Komplex']).count(2),
                                         list(ag.feedback['Komplex']).count(2),

                                         list(jg.feedback['Real']).count(2),
                                         list(ag.feedback['Real']).count(2),
                                                     list(jg.feedback['Sichtbar']).count(2),
                                         list(ag.feedback['Sichtbar']).count(2),
                                                     list(jg.feedback['Bewegbar']).count(2),
                                         list(ag.feedback['Bewegbar']).count(2),
                                                     list(jg.feedback['Technik']).count(2),
                                         list(ag.feedback['Technik']).count(2),

                                         ],

                               "strongly agree":[list(jg.feedback['Instructions']).count(3),
                                                 list(ag.feedback['Instructions']).count(3),
                                                     list(jg.feedback['Gefühl']).count(3),
                                                 list(ag.feedback['Gefühl']).count(3),
                                                     list(jg.feedback['Fun']).count(3),
                                                 list(ag.feedback['Fun']).count(3),
                                                     list(jg.feedback['Aufmerksamkeit']).count(3),
                                                 list(ag.feedback['Aufmerksamkeit']).count(3),

                                                 list(jg.feedback['Komplex']).count(3),
                                                 list(ag.feedback['Komplex']).count(3),

                                                 list(jg.feedback['Real']).count(3),
                                                 list(ag.feedback['Real']).count(3),

                                                 list(jg.feedback['Sichtbar']).count(3),
                                                 list(ag.feedback['Sichtbar']).count(3),

                                                 list(jg.feedback['Bewegbar']).count(3),
                                                 list(ag.feedback['Bewegbar']).count(3),
                                                     list(jg.feedback['Technik']).count(3),
                                                 list(ag.feedback['Technik']).count(3)

                                                    ],
                               "Group" : ['YHA', 'OHA', 'YHA', 'OHA','YHA', 'OHA','YHA', 'OHA','YHA', 'OHA','YHA', 'OHA','YHA', 'OHA','YHA', 'OHA','YHA', 'OHA' ],
                               "Type": ['Instructions', 'Instructions','Feeling', 'Feeling','Fun',  'Fun',
                                        'Attention', 'Attention',
                                        'Complexity', 'Complexity', 'Realism', 'Realism','Visibility', 'Visibility',
                                        'Movement',  'Movement','Technology','Technology'
                                        ]},
                                index =
                                ['Instructions YHA', '', 'Feeling YHA','',  'Fun YHA','',
                                 'Attention YHA','',
                                 'Complexity YHA', '','Realism YHA','', 'Visibility YHA','',
                                 'Movement YHA', '','Technology YHA',''
                                 ]
                                 # ['Instructions YHA', 'Instructions OHA','Feeling YHA', 'Feeling  OHA','Fun YHA',  'Fun OHA',
                                 #                         'Attention YHA', 'Attention OHA',
                                 #                         'Complexity YHA', 'Complexity OHA', 'Realism YHA', 'Realism OHA','Visibility YHA', 'Visibility OHA',
                                 #                         'Movement YHA',  'Movement OHA','Technology YHA','Technology OHA'
                                  #                      ]
                                    )

            # ax = df.plot.bar(x = x, stacked=True, width = 0.5,
            #                                    color=['grey', 'red', 'orange', 'lightgreen', 'darkgreen']
            #                                      )
            # ------------------------------------------------------------------------------------------------
            # create fake dataframes
            dfjg = np.array([[20-len(jg.feedback['Instructions']), list(jg.feedback['Instructions']).count(0), list(jg.feedback['Instructions']).count(1), list(jg.feedback['Instructions']).count(2), list(jg.feedback['Instructions']).count(3)],
                             [20-len(jg.feedback['Gefühl']), list(jg.feedback['Gefühl']).count(0), list(jg.feedback['Gefühl']).count(1), list(jg.feedback['Gefühl']).count(2), list(jg.feedback['Gefühl']).count(3)],
                             [20-len(jg.feedback['Fun']), list(jg.feedback['Fun']).count(0), list(jg.feedback['Fun']).count(1), list(jg.feedback['Fun']).count(2), list(jg.feedback['Fun']).count(3)],
                             [20-len(jg.feedback['Aufmerksamkeit']), list(jg.feedback['Aufmerksamkeit']).count(0), list(jg.feedback['Aufmerksamkeit']).count(1), list(jg.feedback['Aufmerksamkeit']).count(2), list(jg.feedback['Aufmerksamkeit']).count(3)],
                             [20-len(jg.feedback['Komplex'])+1, list(jg.feedback['Komplex']).count(0), list(jg.feedback['Komplex']).count(1), list(jg.feedback['Komplex']).count(2), list(jg.feedback['Komplex']).count(3)],
                             [20-len(jg.feedback['Real']), list(jg.feedback['Real']).count(0), list(jg.feedback['Real']).count(1), list(jg.feedback['Real']).count(2), list(jg.feedback['Real']).count(3)],
                             [20-len(jg.feedback['Sichtbar']), list(jg.feedback['Sichtbar']).count(0), list(jg.feedback['Sichtbar']).count(1), list(jg.feedback['Sichtbar']).count(2), list(jg.feedback['Sichtbar']).count(3)],
                             [20-len(jg.feedback['Bewegbar']), list(jg.feedback['Bewegbar']).count(0), list(jg.feedback['Bewegbar']).count(1), list(jg.feedback['Bewegbar']).count(2), list(jg.feedback['Bewegbar']).count(3)],
                             [20-len(jg.feedback['Technik']), list(jg.feedback['Technik']).count(0), list(jg.feedback['Technik']).count(1), list(jg.feedback['Technik']).count(2), list(jg.feedback['Technik']).count(3)]
            ])
            dfag = np.array([[20-len(ag.feedback['Instructions']), list(ag.feedback['Instructions']).count(0), list(ag.feedback['Instructions']).count(1), list(ag.feedback['Instructions']).count(2), list(ag.feedback['Instructions']).count(3)],
                             [20-len(ag.feedback['Gefühl']), list(ag.feedback['Gefühl']).count(0), list(ag.feedback['Gefühl']).count(1), list(ag.feedback['Gefühl']).count(2), list(ag.feedback['Gefühl']).count(3)],
                             [20-len(ag.feedback['Fun']), list(ag.feedback['Fun']).count(0), list(ag.feedback['Fun']).count(1), list(ag.feedback['Fun']).count(2), list(ag.feedback['Fun']).count(3)],
                             [20-len(ag.feedback['Aufmerksamkeit']), list(ag.feedback['Aufmerksamkeit']).count(0), list(ag.feedback['Aufmerksamkeit']).count(1), list(ag.feedback['Aufmerksamkeit']).count(2), list(ag.feedback['Aufmerksamkeit']).count(3)],
                             [20-len(ag.feedback['Komplex'])+1, list(ag.feedback['Komplex']).count(0), list(ag.feedback['Komplex']).count(1), list(ag.feedback['Komplex']).count(2), list(ag.feedback['Komplex']).count(3)],
                             [20-len(ag.feedback['Real']), list(ag.feedback['Real']).count(0), list(ag.feedback['Real']).count(1), list(ag.feedback['Real']).count(2), list(ag.feedback['Real']).count(3)],
                             [20-len(ag.feedback['Sichtbar']), list(ag.feedback['Sichtbar']).count(0), list(ag.feedback['Sichtbar']).count(1), list(ag.feedback['Sichtbar']).count(2), list(ag.feedback['Sichtbar']).count(3)],
                             [20-len(ag.feedback['Bewegbar']), list(ag.feedback['Bewegbar']).count(0), list(ag.feedback['Bewegbar']).count(1), list(ag.feedback['Bewegbar']).count(2), list(ag.feedback['Bewegbar']).count(3)],
                             [20-len(ag.feedback['Technik']), list(ag.feedback['Technik']).count(0), list(ag.feedback['Technik']).count(1), list(ag.feedback['Technik']).count(2), list(ag.feedback['Technik']).count(3)]])
            columns = ["not answered", "strongly disagree", "disagree", "agree", "strongly agree"]
            index = ['1 Instructions', '2 Feeling', '3 Fun','4 Attention',
                                 '5 Complexity','6 Realism', '7 Visibility',
                                 '8 Movement', '9 Technology']

            jg = pd.DataFrame(dfjg,
                               index=index,
                               columns=columns)
            ag = pd.DataFrame(dfag,
                               index=index,
                               columns=columns)

            # Then, just call :
            self.plot_clustered_stacked([jg, ag], ["YHA N = 20", "OHA N = 20"], "Feedback")

            # -------------------------------------------------------------------------------------------------

            # ax.yaxis.grid()
            # ax.set_axisbelow(True)
            # xlabels = ['Instructions YHA', 'Instructions OHA','Feeling YHA', 'Feeling  OHA','Fun YHA',  'Fun OHA',
            #                             'Attention YHA', 'Attention OHA',
            #                             'Complexity YHA', 'Complexity OHA', 'Realism YHA', 'Realism OHA','Visibility YHA', 'Visibility OHA',
            #                             'Movement YHA',  'Movement OHA','Technology YHA','Technology OHA'
            #
            #                             ]
            #
            # # ax.set_xticklabels(xlabels, rotation=35, horizontalalignment='right', fontsize=feedback_fontsize_medium)
            #
            # ax.set_yticks([0, 5, 10, 15, 20])
            # plt.subplots_adjust(bottom=0.2, left=0.2)
            # ax.set_ylabel("Ratings", fontsize=feedback_fontsize_large)
            # ax.set_xlabel("")
            # # plt.legend(fontsize=feedback_fontsize_medium)
            # plt.title("Feedback", fontsize=feedback_fontsize_large)
            # plt.savefig(f"Results/Neuroimages/Feedback_Boxplot.pdf")

        if self.printExcel:
            d = {'Typ': [], 'Gruppe': [], 'Mittelwert': [], 'Std': []}
            d = self.__add_line(d, 'VLMT Summe', ag.vlmt_sum, jg.vlmt_sum)
            d = self.__add_line(d, 'VLMT Differenz', ag.vlmt_diff, jg.vlmt_diff)
            d = self.__add_line(d, 'Figur_Copy', ag.figur_abmalen, jg.figur_abmalen)
            d = self.__add_line(d, 'Figur_Delay', ag.figur_abruf, jg.figur_abruf)
            d = self.__add_line(d, 'Stroop_Woerter', ag.stroop_wort, jg.stroop_wort)
            d = self.__add_line(d, 'Stoop_Farben', ag.stroop_farbe, jg.stroop_farbe)
            d = self.__add_line(d, 'TMT_Zahlen', ag.tmt_zahl, jg.tmt_zahl)
            d = self.__add_line(d, 'TMT_Buchstaben', ag.tmt_buchst, jg.tmt_buchst)
            d = self.__add_line(d, 'AR_Delay', ag.ar_abruf, jg.ar_abruf)
            d = self.__add_line(d, 'AR_Recognition', ag.ar_recog, jg.ar_recog)
            d = self.__add_line(d, 'AR_Positionen_rel', ag.ar_positions_rel, jg.ar_positions_rel)
            d = self.__add_line(d, 'AR_Positionen_abs', ag.ar_positions_abs, jg.ar_positions_abs)

            df = pd.DataFrame(data=d)
            df.to_excel("Results/Ergebnisse_Testbatterie.xlsx")
            print(df)

    def plot_clustered_stacked(self, dfall, labels=None, title="multiple stacked bar plot", H="/", **kwargs):
        """Given a list of dataframes, with identical columns and index, create a clustered stacked bar plot.
    labels is a list of the names of the dataframe, used for the legend
    title is a string for the title of the plot
    H is the hatch used for identification of the different dataframe"""
        feedback_fontsize_large = 'xx-large'
        feedback_fontsize_medium = 'x-large'

        n_df = len(dfall)
        n_col = len(dfall[0].columns)
        n_ind = len(dfall[0].index)
        axe = plt.subplot(111)

        for df in dfall:  # for each data frame
            axe = df.plot(kind="bar",
                          linewidth=0,
                          stacked=True,
                          ax=axe,
                          legend=False,
                          edgecolor='lightgray',
                          grid=False,
                          color=['grey', 'red', 'orange', 'lightgreen', 'green'],
                          **kwargs)  # make bar plots

        h, l = axe.get_legend_handles_labels()  # get the handles we want to modify
        for i in range(0, n_df * n_col, n_col):  # len(h) = n_col * n_df
            for j, pa in enumerate(h[i:i + n_col]):
                for rect in pa.patches:  # for each index
                    rect.set_x(rect.get_x() + 1 / float(n_df + 1) * i / float(n_col))
                    if i == 0:
                        rect.set_hatch(H * int(i / n_col))  # edited part
                    else:
                        rect.set_hatch(H * int((i+1) / n_col))  # edited part
                    rect.set_width(0.8 / float(n_df + 1))

        axe.set_xticks((np.arange(0, 2 * n_ind, 2) + 1 / float(n_df + 1)) / 2.)
        axe.set_xticklabels(df.index, rotation=25, horizontalalignment='right',fontsize=feedback_fontsize_medium)
        axe.set_yticks([0, 5, 10, 15, 20])
        axe.set_ylabel("Subjects", fontsize=feedback_fontsize_medium)
        axe.set_title(title, fontsize=feedback_fontsize_large)

        # Add invisible data to add another legend
        n = []
        for i in range(n_df):
            if i==0:
                n.append(axe.bar(0, 0, color="gray",edgecolor= 'lightgray', hatch=H * i))
            else:
                n.append(axe.bar(0, 0, color="gray",edgecolor= 'lightgray', hatch=H * (i+1)))

        l1 = axe.legend(h[:n_col], l[:n_col], loc=[1.01, 0.5])
        if labels is not None:
            l2 = plt.legend(n, labels, loc=[1.01, 0.1])
        axe.add_artist(l1)

        plt.subplots_adjust(bottom=0.2, top=0.9, left=0.2, right=0.7)
        plt.savefig(f"Results/Neuroimages/Feedback.pdf")

        return axe

    def __box_diagram(self, title, data, yerr, xticks, ylabel, legend, rotation):
        x = np.arange(len(data[0]))
        fig = plt.figure()
        ax = plt.subplot(111)
        plt.title(title)
        handles = []
        for i in range(0, len(data[:, 0])):
            a = ax.bar(x + 0.4 * i - 0.2, data[i], width=0.3,
                       yerr=yerr[i], error_kw={'ecolor': '0.2', 'capsize': 6},
                       alpha=0.7)
            handles.append(a)

        ax.set_ylabel(ylabel)
        ax.legend(handles, legend)
        ax.set_xticks(x)
        ax.set_xticklabels(xticks, rotation=rotation, horizontalalignment='right')
        if rotation != 0:
            plt.subplots_adjust(bottom=0.2)
        plt.savefig(f"Images/{title}_BarPlot")

    def __seaborn_boxplot(self, d, title, ylabel):
        boxplot_font_large = 'xx-large'
        boxplot_font_medium = 'x-large'

        fig = plt.figure()
        ax = plt.subplot(111)
        ax = sns.boxplot(x='Type', y='Data', data=d, hue='Group', width=0.6)
        ax.yaxis.grid()
        ax.set_xticklabels(['Positions'], fontsize=boxplot_font_large )
        ax.set_axisbelow(True)
        ax.set_ylabel(ylabel, fontsize=boxplot_font_large)
        # ax.set_yticklabels(fontsize = boxplot_font_medium)
        plt.yticks(fontsize=boxplot_font_medium)
        ax.set_xlabel("")
        plt.subplots_adjust(left=0.14)
        plt.legend(fontsize=boxplot_font_medium)
        plt.title(title, fontsize=boxplot_font_large )
        plt.savefig(f"Results/Neuroimages/{title}_Boxplot.pdf")

    def __add_line(self, edata, typ, alt, jung):
        edata['Typ'].append(typ)
        edata['Gruppe'].append('AG')
        edata['Mittelwert'].append(np.mean(alt))
        edata['Std'].append(np.std(alt))

        edata['Typ'].append(typ)
        edata['Gruppe'].append('JG')
        edata['Mittelwert'].append(np.mean(jung))
        edata['Std'].append(np.std(jung))

        return edata

