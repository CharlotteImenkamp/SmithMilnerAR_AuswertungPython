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

    # for i in range(0, len(pathStartPos)):
        # print(f"\n**** User{userID[i]}")

        # startPos, endPos, names = Load.load_positions(pathEndPos[i], pathStartPos[i])

        # absoluteError.plot_pos(startPos, endPos, names, userID[i])
        # absoluteError.plot_dist(startPos, endPos, names, userID[i])

        # relativeError.plot_vro(startPos, endPos, userID[i], names)
        # relativeError.plot_del(startPos, endPos, names, userID[i])
        # relativeError.calculate_quadrants(np.array(startPos), np.array(endPos))

        # rotationen.add_user(pathEndPos[i], pathStartPos[i], userID[i])

        #if userID[i] is not 4:
            #times.get_delta_time(path_moving[i])
            #objectMovement.add_user(pathStartPos[i], pathEndPos[i], path_moving[i], userID[i])

        # if userID[i] is not 29:
            # headDirection.add_user("HeadData", "StartObjectLocations", "EndObjectLocations", userID[i])

    # relativeError.save()
    # times.save()
    # rotationen.save(names)
    neuroData = Testbatterie(False, False, False, False, False, False, True)
    plt.show()
