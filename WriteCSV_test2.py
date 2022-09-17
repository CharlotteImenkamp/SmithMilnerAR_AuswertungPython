import csv
import json
import numpy as np
import pandas as pd

id = 1
i = 0
index_err = 0
key_err = 0
count = 0
obj_count = 0
once = 0
string = ''
line_SLP = 0
line_SOL = 0
line_MOL = 0
line_EOL = 0
object_files = ['StartLocationPrices', 'StartObjectLocations', 'MovingObjectLocations', 'EndObjectLocations']
head_files = ['HeadDataPrices', 'HeadDataLocations']
hand_files =['HandDataPrices', 'HandDataLocations']
table_files = ['TableCornersPrices', 'TableCornersLocations']

table_rows = []
rows = []
objects_time = []
positions = {}
rotations = {}
objects = np.empty(16, dtype=object)

orig = []
dir = []
tim = []
tab = []


def myget(pr, t, o, x):
    try:
        var = pr.get(t).get(f'{objects[o]}')
        if var is None:
            return ''
        return var[0][x]
    except IndexError:
        global index_err
        index_err += 1
        return ''
    except KeyError:
        global key_err
        key_err += 1
        return ''


for fi in table_files:
    datapath = f"Data/User{id}/{fi}{id}.json"
    o = open(datapath)
    data = json.load(o)
    tmp = data["entries"]
    o.close()

    for p in tmp: # top left, top right, bot left, bot right
        tab.append((p['TopLeft']['x'], p['TopLeft']['y'], p['TopLeft']['z']))
        tab.append((p['TopRight']['x'], p['TopRight']['y'], p['TopRight']['z']))
        tab.append((p['BotLeft']['x'], p['BotLeft']['y'], p['BotLeft']['z']))
        tab.append((p['BotRight']['x'], p['BotRight']['y'], p['BotRight']['z']))

for he in head_files:
    datapath = f"Data/User{id}/{he}{id}.json"
    o = open(datapath)
    data = json.load(o)
    tmp = data["entries"]
    o.close()

    for p in tmp:
        orig.append(([p['GazeOrigin']['x'], p['GazeOrigin']['y'], p['GazeOrigin']['z']]))
        dir.append(([p['GazeDirection']['x'], p['GazeDirection']['y'], p['GazeDirection']['z']]))
        tim.append([p['TimeAfterStart']])

for ob in object_files:
    datapath = f"Data/User{id}/{ob}{id}.json"
    o = open(datapath)
    data = json.load(o)
    tmp = data["entries"][0]["GameObjects"]
    offset = data["entries"][0]["PositionOffset"]
    timestamp = data["entries"]

    o.close()

    if ob == "MovingObjectLocations":
        line_MOL = line_SOL # moving_object_locations begins after start_object_location
        # count = 0
        for p in timestamp:
            line_MOL = line_MOL+1
            times = f'{p["Time"]}'
            objects_time.append(times)
            # p = p['GameObjects'][0]
            key = f"{p['GameObjects'][0]['Objectname']}"
            value = [p['GameObjects'][0]['GlobalPosition']['x'] + offset['x'],
                     p['GameObjects'][0]['GlobalPosition']['y'] + offset['y'],
                     p['GameObjects'][0]['GlobalPosition']['z'] + offset['z']]
            if times in positions and key in positions[times]:
                positions[times][key].append(value)
            elif times in positions:
                positions[times][key] = [value]
            else:
                positions[times] = {}
                positions[times][key] = [value]

            value = [p['GameObjects'][0]['GlobalRotation']['x'],
                     p['GameObjects'][0]['GlobalRotation']['y'],
                     p['GameObjects'][0]['GlobalRotation']['z'],
                     p['GameObjects'][0]['GlobalRotation']['w']]
            if times in rotations and key in rotations[times]:
                rotations[times][key].append(value)
            elif times in rotations:
                rotations[times][key] = [value]
            else:
                rotations[times] = {}
                rotations[times][key] = [value]
            # count += 1

    else:
        if ob == 'StartObjectLocations':
            line_SOL = line_SLP # start_object_location begins after start_location_prices
        if ob == 'EndObjectLocations':
            line_EOL = line_MOL # end_object_location begins after moving_object_locations

        for pk in timestamp:
            times = f'{pk["Time"]}'
            for p in tmp:
                if ob == 'StartLocationPrices':
                    line_SLP = line_SLP+1
                if ob == 'StartObjectLocations':
                    line_SOL = line_SOL+1
                if ob == 'EndObjectLocations':
                    line_EOL = line_EOL+1

                key = p["Objectname"]
                value = [p['GlobalPosition']['x'] + offset['x'],
                         p['GlobalPosition']['y'] + offset['y'],
                         p['GlobalPosition']['z'] + offset['z']]
                if times in positions and key in positions[times]:
                    positions[times][key].append(value)
                elif times in positions:
                    positions[times][key] = [value]
                else:
                    positions[times] = {}
                    positions[times][key] = [value]
                    # positions.get(count[key], []) + [value]
                value = [p['GlobalRotation']['x'],
                         p['GlobalRotation']['y'],
                         p['GlobalRotation']['z'],
                         p['GlobalRotation']['w']]

                objects[i] = p["Objectname"]
                i += 1
                if times in rotations and key in rotations[times]:
                    rotations[times][key].append(value)
                elif times in rotations:
                    rotations[times][key] = [value]
                else:
                    rotations[times] = {}
                    rotations[times][key] = [value]
            # count += 1
            i = 0

fieldnames = ['Time', 'TableCorners_Price_x', 'TableCorners_Price_y', 'TableCorners_Price_z',
              'TableCorners_Location_x', 'TableCorners_Location_y', 'TableCorners_Location_z', 'ObjectFile',
              'ObjectTime',
              objects[0] + '_x', objects[0] + '_y', objects[0] + '_z', objects[0] + '_rot_x',
              objects[0] + '_rot_y', objects[0] + '_rot_z', objects[0] + '_rot_w',
              objects[1] + '_x', objects[1] + '_y', objects[1] + '_z', objects[1] + '_rot_x',
              objects[1] + '_rot_y', objects[1] + '_rot_z', objects[1] + '_rot_w', objects[2] + '_x',
              objects[2] + '_y', objects[2] + '_z',
              objects[2] + '_rot_x', objects[2] + '_rot_y', objects[2] + '_rot_z', objects[2] + '_rot_w',
              objects[3] + '_x', objects[3] + '_y',
              objects[3] + '_z', objects[3] + '_rot_x', objects[3] + '_rot_y', objects[3] + '_rot_z',
              objects[3] + '_rot_w', objects[4] + '_x',
              objects[4] + '_y', objects[4] + '_z', objects[4] + '_rot_x', objects[4] + '_rot_y',
              objects[4] + '_rot_z', objects[4] + '_rot_w',
              objects[5] + '_x', objects[5] + '_y', objects[5] + '_z', objects[5] + '_rot_x',
              objects[5] + '_rot_y', objects[5] + '_rot_z',
              objects[5] + '_rot_w', objects[6] + '_x', objects[6] + '_y', objects[6] + '_z',
              objects[6] + '_rot_x', objects[6] + '_rot_y',
              objects[6] + '_rot_z', objects[6] + '_rot_w', objects[7] + '_x', objects[7] + '_y',
              objects[7] + '_z', objects[7] + '_rot_x',
              objects[7] + '_rot_y', objects[7] + '_rot_z', objects[7] + '_rot_w', objects[8] + '_x',
              objects[8] + '_y', objects[8] + '_z',
              objects[8] + '_rot_x', objects[8] + '_rot_y', objects[8] + '_rot_z', objects[8] + '_rot_w',
              objects[9] + '_x',
              objects[9] + '_y', objects[9] + '_z', objects[9] + '_rot_x', objects[9] + '_rot_y',
              objects[9] + '_rot_z', objects[9] + '_rot_w',
              objects[10] + '_x', objects[10] + '_y', objects[10] + '_z', objects[10] + '_rot_x',
              objects[10] + '_rot_y', objects[10] + '_rot_z'
              , objects[10] + '_rot_w', objects[11] + '_x', objects[11] + '_y', objects[11] + '_z',
              objects[11] + '_rot_x', objects[11] +
              '_rot_y', objects[11] + '_rot_z', objects[11] + '_rot_w', objects[12] + '_x', objects[12] + '_y',
              objects[12] + '_z',
              objects[12] + '_rot_x', objects[12] + '_rot_y', objects[12] + '_rot_z', objects[12] + '_rot_w',
              objects[13] + '_x', objects[13] +
              '_y', objects[13] + '_z', objects[13] + '_rot_x', objects[13] + '_rot_y', objects[13] + '_rot_z',
              objects[13] + '_rot_w',
              objects[14] + '_x', objects[14] + '_y', objects[14] + '_z', objects[14] + '_rot_x',
              objects[14] + '_rot_y', objects[14] + '_rot_z'
              , objects[14] + '_rot_w', objects[15] + '_x', objects[15] + '_y', objects[15] + '_z',
              objects[15] + '_rot_x', objects[15] +
              '_rot_y', objects[15] + '_rot_z', objects[15] + '_rot_w',
              'Gaze_Origin_x', 'Gaze_Origin_y', 'Gaze_Origin_z', 'Gaze_Direction_x', 'Gaze_Direction_y',
              'Gaze_Direction_z',
              'LeftTips_Thumb_x', 'LeftTips_Thumb_y', 'LeftTips_Thumb_z', 'LeftTips_Index_x', 'LeftTips_Index_y'
              , 'LeftTips_Index_z', 'LeftTips_Middle_x', 'LeftTips_Middle_y', 'LeftTips_Middle_z',
              'LeftTips_Ring_x', 'LeftTips_Ring_y', 'LeftTips_Ring_z', 'LeftTips_Pinky_x', 'LeftTips_Pinky_y',
              'LeftTips_Pinky_z', 'RightTips_Thumb_x', 'RightTips_Thumb_y', 'RightTips_Thumb_z',
              'RightTips_Index_x', 'RightTips_Index_y', 'RightTips_Index_z', 'RightTips_Middle_x',
              'RightTips_Middle_y', 'RightTips_Middle_z', 'RightTips_Ring_x', 'RightTips_Ring_y',
              'RightTips_Ring_z', 'RightTips_Pinky_x', 'RightTips_Pinky_y', 'RightTips_Pinky_z',
              'LeftDistal_Thumb_x', 'LeftDistal_Thumb_y', 'LeftDistal_Thumb_z', 'LeftDistal_Index_x',
              'LeftDistal_Index_y', 'LeftDistal_Index_z', 'LeftDistal_Middle_x', 'LeftDistal_Middle_y',
              'LeftDistal_Middle_z', 'LeftDistal_Ring_x', 'LeftDistal_Ring_y', 'LeftDistal_Ring_z',
              'LeftDistal_Pinky_x', 'LeftDistal_Pinky_y', 'LeftDistal_Pinky_z', 'RightDistal_Thumb_x',
              'RightDistal_Thumb_y', 'RightDistal_Thumb_z', 'RightDistal_Index_x', 'RightDistal_Index_y',
              'RightDistal_Index_z', 'RightDistal_Middle_x', 'RightDistal_Middle_y', 'RightDistal_Middle_z',
              'RightDistal_Ring_x', 'RightDistal_Ring_y', 'RightDistal_Ring_z', 'RightDistal_Pinky_x',
              'RightDistal_Pinky_y', 'RightDistal_Pinky_z', 'LeftMetacarpal_Thumb_x', 'LeftMetacarpal_Thumb_y',
              'LeftMetacarpal_Thumb_z', 'LeftMetacarpal_Index_x', 'LeftMetacarpal_Index_y',
              'LeftMetacarpal_Index_z', 'LeftMetacarpal_Middle_x', 'LeftMetacarpal_Middle_y',
              'LeftMetacarpal_Middle_z', 'LeftMetacarpal_Ring_x', 'LeftMetacarpal_Ring_y',
              'LeftMetacarpal_Ring_z', 'LeftMetacarpal_Pinky_x', 'LeftMetacarpal_Pinky_y',
              'LeftMetacarpal_Pinky_z', 'RightMetacarpal_Thumb_x', 'RightMetacarpal_Thumb_y',
              'RightMetacarpal_Thumb_z', 'RightMetacarpal_Index_x', 'RightMetacarpal_Index_y',
              'RightMetacarpal_Index_z', 'RightMetacarpal_Middle_x', 'RightMetacarpal_Middle_y',
              'RightMetacarpal_Middle_z', 'RightMetacarpal_Ring_x', 'RightMetacarpal_Ring_y',
              'RightMetacarpal_Ring_z', 'RightMetacarpal_Pinky_x', 'RightMetacarpal_Pinky_y',
              'RightMetacarpal_Pinky_z', 'LeftMiddle_Thumb_x', 'LeftMiddle_Thumb_y', 'LeftMiddle_Thumb_z',
              'LeftMiddle_Index_x', 'LeftMiddle_Index_y', 'LeftMiddle_Index_z', 'LeftMiddle_Middle_x',
              'LeftMiddle_Middle_y', 'LeftMiddle_Middle_z', 'LeftMiddle_Ring_x', 'LeftMiddle_Ring_y',
              'LeftMiddle_Ring_z', 'LeftMiddle_Pinky_x', 'LeftMiddle_Pinky_y', 'LeftMiddle_Pinky_z',
              'RightMiddle_Thumb_x', 'RightMiddle_Thumb_y', 'RightMiddle_Thumb_z', 'RightMiddle_Index_x',
              'RightMiddle_Index_y', 'RightMiddle_Index_z', 'RightMiddle_Middle_x', 'RightMiddle_Middle_y',
              'RightMiddle_Middle_z', 'RightMiddle_Ring_x', 'RightMiddle_Ring_y', 'RightMiddle_Ring_z',
              'RightMiddle_Pinky_x', 'RightMiddle_Pinky_y', 'RightMiddle_Pinky_z', 'LeftWrist_x', 'LeftWrist_y',
              'LeftWrist_y', 'LeftWrist_z', 'RightWrist_x', 'RightWrist_y', 'RightWrist_z', 'LeftPalm_x',
              'LeftPalm_y', 'LeftPalm_z', 'RightPalm_x', 'RightPalm_y', 'RightPalm_z', 'TrackedHand']

for e in tim:
    i = 0
    for eo in positions:
        if obj_count <= line_SLP:
            string = object_files[0]
        elif line_SLP < obj_count <= line_SOL:
            string = object_files[1]
        elif line_SOL < obj_count <= line_MOL:
            string = object_files[2]
        elif line_MOL < obj_count <= line_EOL:
            string = object_files[3]
        else:
            string = 'no object file'

        f = eo.find('.') # cut to length with [:length]
        check = eo[:f+5]
        if int(check[-1]) >= 5: # round properly
            check = eo[:f+4].replace('.', ',')
            f = int(check[-1]) + 1
            check = check[:-1] + f'{f}'
        else:
            check = eo[:f+4].replace('.', ',')
        if int(check[-1]) == 0:
            check = check[:-1]
        # print(e[0], check)

        if e[0] == check:  # time of object positions gets shortened to gaze time
            rows.append({'Time': tim[count][0], 'Gaze_Origin_x': orig[count][0], 'Gaze_Origin_y': orig[count][1],
                         'Gaze_Origin_z': orig[count][2], 'Gaze_Direction_x': dir[count][0], 'Gaze_Direction_y':
                             dir[count][1], 'Gaze_Direction_z': dir[count][2], 'ObjectTime': eo,
                         'ObjectFile': string,
                         f'{objects[0]}_x': myget(positions, eo, obj_count, 0),
                         f'{objects[0]}_y': myget(positions, eo, obj_count, 1),
                         f'{objects[0]}_z': myget(positions, eo, obj_count, 2),
                         f'{objects[0]}_rot_x': myget(rotations, eo, obj_count, 0),
                         f'{objects[0]}_rot_y': myget(rotations, eo, obj_count, 1),
                         f'{objects[0]}_rot_z': myget(rotations, eo, obj_count, 2),
                         f'{objects[0]}_rot_w': myget(rotations, eo, obj_count, 3),

                         f'{objects[1]}_x': myget(positions, eo, obj_count, 0),
                         f'{objects[1]}_y': myget(positions, eo, obj_count, 1),
                         f'{objects[1]}_z': myget(positions, eo, obj_count, 2),
                         f'{objects[1]}_rot_x': myget(rotations, eo, obj_count, 0),
                         f'{objects[1]}_rot_y': myget(rotations, eo, obj_count, 1),
                         f'{objects[1]}_rot_z': myget(rotations, eo, obj_count, 2),
                         f'{objects[1]}_rot_w': myget(rotations, eo, obj_count, 3),

                         f'{objects[2]}_x': myget(positions, eo, obj_count, 0),
                         f'{objects[2]}_y': myget(positions, eo, obj_count, 1),
                         f'{objects[2]}_z': myget(positions, eo, obj_count, 2),
                         f'{objects[2]}_rot_x': myget(rotations, eo, obj_count, 0),
                         f'{objects[2]}_rot_y': myget(rotations, eo, obj_count, 1),
                         f'{objects[2]}_rot_z': myget(rotations, eo, obj_count, 2),
                         f'{objects[2]}_rot_w': myget(rotations, eo, obj_count, 3),

                         f'{objects[3]}_x': myget(positions, eo, obj_count, 0),
                         f'{objects[3]}_y': myget(positions, eo, obj_count, 1),
                         f'{objects[3]}_z': myget(positions, eo, obj_count, 2),
                         f'{objects[3]}_rot_x': myget(rotations, eo, obj_count, 0),
                         f'{objects[3]}_rot_y': myget(rotations, eo, obj_count, 1),
                         f'{objects[3]}_rot_z': myget(rotations, eo, obj_count, 2),
                         f'{objects[3]}_rot_w': myget(rotations, eo, obj_count, 3),

                         f'{objects[4]}_x': myget(positions, eo, obj_count, 0),
                         f'{objects[4]}_y': myget(positions, eo, obj_count, 1),
                         f'{objects[4]}_z': myget(positions, eo, obj_count, 2),
                         f'{objects[4]}_rot_x': myget(rotations, eo, obj_count, 0),
                         f'{objects[4]}_rot_y': myget(rotations, eo, obj_count, 1),
                         f'{objects[4]}_rot_z': myget(rotations, eo, obj_count, 2),
                         f'{objects[4]}_rot_w': myget(rotations, eo, obj_count, 3),

                         f'{objects[5]}_x': myget(positions, eo, obj_count, 0),
                         f'{objects[5]}_y': myget(positions, eo, obj_count, 1),
                         f'{objects[5]}_z': myget(positions, eo, obj_count, 2),
                         f'{objects[5]}_rot_x': myget(rotations, eo, obj_count, 0),
                         f'{objects[5]}_rot_y': myget(rotations, eo, obj_count, 1),
                         f'{objects[5]}_rot_z': myget(rotations, eo, obj_count, 2),
                         f'{objects[5]}_rot_w': myget(rotations, eo, obj_count, 3),

                         f'{objects[6]}_x': myget(positions, eo, obj_count, 0),
                         f'{objects[6]}_y': myget(positions, eo, obj_count, 1),
                         f'{objects[6]}_z': myget(positions, eo, obj_count, 2),
                         f'{objects[6]}_rot_x': myget(rotations, eo, obj_count, 0),
                         f'{objects[6]}_rot_y': myget(rotations, eo, obj_count, 1),
                         f'{objects[6]}_rot_z': myget(rotations, eo, obj_count, 2),
                         f'{objects[6]}_rot_w': myget(rotations, eo, obj_count, 3),

                         f'{objects[7]}_x': myget(positions, eo, obj_count, 0),
                         f'{objects[7]}_y': myget(positions, eo, obj_count, 1),
                         f'{objects[7]}_z': myget(positions, eo, obj_count, 2),
                         f'{objects[7]}_rot_x': myget(rotations,eo, obj_count, 0),
                         f'{objects[7]}_rot_y': myget(rotations, eo, obj_count, 1),
                         f'{objects[7]}_rot_z': myget(rotations, eo, obj_count, 2),
                         f'{objects[7]}_rot_w': myget(rotations, eo, obj_count, 3),

                         f'{objects[8]}_x': myget(positions, eo, obj_count, 0),
                         f'{objects[8]}_y': myget(positions, eo, obj_count, 1),
                         f'{objects[8]}_z': myget(positions, eo, obj_count, 2),
                         f'{objects[8]}_rot_x': myget(rotations, eo, obj_count, 0),
                         f'{objects[8]}_rot_y': myget(rotations, eo, obj_count, 1),
                         f'{objects[8]}_rot_z': myget(rotations, eo, obj_count, 2),
                         f'{objects[8]}_rot_w': myget(rotations, eo, obj_count, 3),

                         f'{objects[9]}_x': myget(positions, eo, obj_count, 0),
                         f'{objects[9]}_y': myget(positions, eo, obj_count, 1),
                         f'{objects[9]}_z': myget(positions, eo, obj_count, 2),
                         f'{objects[9]}_rot_x': myget(rotations, eo, obj_count, 0),
                         f'{objects[9]}_rot_y': myget(rotations, eo, obj_count, 1),
                         f'{objects[9]}_rot_z': myget(rotations, eo, obj_count, 2),
                         f'{objects[9]}_rot_w': myget(rotations, eo, obj_count, 3),

                         f'{objects[10]}_x': myget(positions, eo, obj_count, 0),
                         f'{objects[10]}_y': myget(positions, eo, obj_count, 1),
                         f'{objects[10]}_z': myget(positions, eo, obj_count, 2),
                         f'{objects[10]}_rot_x': myget(rotations, eo, obj_count, 0),
                         f'{objects[10]}_rot_y': myget(rotations, eo, obj_count, 1),
                         f'{objects[10]}_rot_z': myget(rotations, eo, obj_count, 2),
                         f'{objects[10]}_rot_w': myget(rotations, eo, obj_count, 3),

                         f'{objects[11]}_x': myget(positions, eo, obj_count, 0),
                         f'{objects[11]}_y': myget(positions, eo, obj_count, 1),
                         f'{objects[11]}_z': myget(positions, eo, obj_count, 2),
                         f'{objects[11]}_rot_x': myget(rotations, eo, obj_count, 0),
                         f'{objects[11]}_rot_y': myget(rotations, eo,obj_count, 1),
                         f'{objects[11]}_rot_z': myget(rotations, eo, obj_count, 2),
                         f'{objects[11]}_rot_w': myget(rotations, eo, obj_count, 3),

                         f'{objects[12]}_x': myget(positions, eo, obj_count, 0),
                         f'{objects[12]}_y': myget(positions, eo, obj_count, 1),
                         f'{objects[12]}_z': myget(positions, eo, obj_count, 2),
                         f'{objects[12]}_rot_x': myget(rotations, eo, obj_count, 0),
                         f'{objects[12]}_rot_y': myget(rotations, eo, obj_count, 1),
                         f'{objects[12]}_rot_z': myget(rotations, eo, obj_count, 2),
                         f'{objects[12]}_rot_w': myget(rotations, eo, obj_count, 3),

                         f'{objects[13]}_x': myget(positions, eo, obj_count, 0),
                         f'{objects[13]}_y': myget(positions, eo, obj_count, 1),
                         f'{objects[13]}_z': myget(positions, eo, obj_count, 2),
                         f'{objects[13]}_rot_x': myget(rotations, eo, obj_count, 0),
                         f'{objects[13]}_rot_y': myget(rotations, eo, obj_count, 1),
                         f'{objects[13]}_rot_z': myget(rotations, eo, obj_count, 2),
                         f'{objects[13]}_rot_w': myget(rotations, eo, obj_count, 3),

                         f'{objects[14]}_x': myget(positions, eo, obj_count, 0),
                         f'{objects[14]}_y': myget(positions, eo, obj_count, 1),
                         f'{objects[14]}_z': myget(positions, eo, obj_count, 2),
                         f'{objects[14]}_rot_x': myget(rotations, eo, obj_count, 0),
                         f'{objects[14]}_rot_y': myget(rotations, eo, obj_count, 1),
                         f'{objects[14]}_rot_z': myget(rotations, eo, obj_count, 2),
                         f'{objects[14]}_rot_w': myget(rotations, eo, obj_count, 3),

                         f'{objects[15]}_x': myget(positions, eo, obj_count, 0),
                         f'{objects[15]}_y': myget(positions, eo, obj_count, 1),
                         f'{objects[15]}_z': myget(positions, eo, obj_count, 2),
                         f'{objects[15]}_rot_x': myget(rotations, eo, obj_count, 0),
                         f'{objects[15]}_rot_y': myget(rotations, eo, obj_count, 1),
                         f'{objects[15]}_rot_z': myget(rotations, eo, obj_count, 2),
                         f'{objects[15]}_rot_w': myget(rotations, eo, obj_count, 3)})
            obj_count += 1
            count += 1
            i = 1
    if i == 0:
        rows.append({'Time': tim[count][0], 'Gaze_Origin_x': orig[count][0],
                     'Gaze_Origin_y': orig[count][1], 'Gaze_Origin_z': orig[count][2], 'Gaze_Direction_x':
                         dir[count][0], 'Gaze_Direction_y': dir[count][1], 'Gaze_Direction_z': dir[count][2]})
        count = count+1

table_rows = {'TableCorners_Price_x': f'topleft{tab[0][0]}', 'TableCorners_Price_y': f'{tab[0][1]}',
              'TableCorners_Price_z': f'{tab[0][2]}', 'TableCorners_Location_x': f'topleft{tab[4][0]}',
              'TableCorners_Location_y': f'{tab[4][1]}', 'TableCorners_Location_z': f'{tab[4][2]}'}, \
             {'TableCorners_Price_x': f'topright{tab[1][0]}', 'TableCorners_Price_y': f'{tab[1][1]}',
              'TableCorners_Price_z': f'{tab[1][2]}', 'TableCorners_Location_x': f'topright{tab[5][0]}',
              'TableCorners_Location_y': f'{tab[5][1]}', 'TableCorners_Location_z': f'{tab[5][2]}'}, \
             {'TableCorners_Price_x': f'botleft{tab[2][0]}', 'TableCorners_Price_y': f'{tab[2][1]}',
              'TableCorners_Price_z': f'{tab[2][2]}', 'TableCorners_Location_x': f'botleft{tab[6][0]}',
              'TableCorners_Location_y': f'{tab[6][1]}', 'TableCorners_Location_z': f'{tab[6][2]}'}, \
             {'TableCorners_Price_x': f'botright{tab[3][0]}', 'TableCorners_Price_y': f'{tab[3][1]}',
              'TableCorners_Price_z': f'{tab[3][2]}', 'TableCorners_Location_x': f'botright{tab[7][0]}',
              'TableCorners_Location_y': f'{tab[7][1]}', 'TableCorners_Location_z': f'{tab[7][2]}'}

once = 0
# open the file in the write mode
with open(f"Data/User{id}/User{id}_test2.csv", 'w', newline='') as f:
    # create the csv writer
    if once == 0:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        once = 1
    # write rows to the csv file
    writer.writerows(table_rows)
    writer.writerows(rows)
    f.close()

print(index_err, key_err)
    # rotations.clear()
    # positions.clear()
