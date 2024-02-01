import numpy as np
import matplotlib.pyplot as plt

from AbsoluteError import AbsoluteError
from RelativeError import RelativeError
from Times import Times
from Rotations import Rotations
from HeadDirection import HeadDirection
from ObjectMovement import ObjectMovement
import Load
from Testbatterie import Testbatterie

if __name__ == '__main__':

    # ----------------------------------------------------------
    # EDIT FOR NEW DATASET
    allIDs = range(1, 41)
    # ----------------------------------------------------------

    # Add file paths
    pathEndPos = []
    pathStartPos = []
    path_moving = []
    path_obj = []
    userID = []

    # make sure all user ids are covered
    for i in allIDs:
        pathStartPos.append(f"Data/User{i}/StartLocationPrices{i}.json")
        pathEndPos.append(f"Data/User{i}/EndObjectLocations{i}.json")
        path_obj.append(f"Data/User{i}/StartObjectLocations{i}.json")
        path_moving.append(f"Data/User{i}/MovingObjectLocations{i}.json")
        userID.append(i)

    # Calculate
    startPos = []
    endPos = []
    startRot = []
    endRot = []
    relativeError = RelativeError()
    absoluteError = AbsoluteError()
    times = Times()
    rotationen = Rotations()
    headDirection = HeadDirection("Locations")
    objectMovement = ObjectMovement()

    calNeuroData = False
    showPlot = True
    calRotations = False
    calTimes = False
    calRelError = False
    calAbsError = True
    plotObjectMovement = False
    plotHeadDirection = False
    labelInput = 'numbers' # 'english', 'german', 'numbers'
    plotLegend = False

    userRange = [1, 20, 34] # range(0, len(pathStartPos)):

    for i in userRange:
        print(f"\n**** User{userID[i]}")

        startPos, endPos, names = Load.load_positions(pathEndPos[i], pathStartPos[i], labelInput)

        if calAbsError:
            absoluteError.plot_pos(startPos, endPos, names, userID[i], plotLegend)
            #absoluteError.plot_dist(startPos, endPos, names, userID[i]) 
            #absoluteError.write_excel_file()
            # absoluteError.plot_dist(startPos, endPos, names, userID[i])

        if calRelError:
            relativeError.plot_vro(startPos, endPos, userID[i], names)
            # relativeError.plot_del(startPos, endPos, names, userID[i])
            # relativeError.calculate_quadrants(np.array(startPos), np.array(endPos))

        if calRotations:
            rotationen.add_user(pathEndPos[i], pathStartPos[i], userID[i])

        if plotObjectMovement and userID[i] != 4:
            times.get_delta_time(path_moving[i])
            objectMovement.add_user(pathStartPos[i], pathEndPos[i], path_moving[i], userID[i])

        if plotHeadDirection and userID[i] != 29:
            headDirection.add_user("HeadData", "StartObjectLocations", "EndObjectLocations", userID[i])

    if calRelError: 
        relativeError.save()
    if calTimes: 
        times.save()
    if calRotations:
        rotationen.save(names)
    if calNeuroData: 
        neuroData = Testbatterie(False, False, False, False, False, False, False)
    if showPlot: 
        plt.show()
