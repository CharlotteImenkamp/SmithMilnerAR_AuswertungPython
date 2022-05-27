import json


# load data
def load_positions(path_end, path_start):
    endpos = []
    names = []
    startpos = []
    data = []

    # end positions
    o = open(path_end)
    data = json.load(o)
    tmp = data["entries"][0]["GameObjects"]
    o.close()

    for p in tmp:
        x = p['GlobalPosition']['x']+data['entries'][0]['PositionOffset']['x']
        y = p['GlobalPosition']['z']+data['entries'][0]['PositionOffset']['z']
        endpos.append(([x, y]))
        names.append(p['Objectname'])

    # start positions
    o = open(path_start)
    data = json.load(o)
    tmp = data["entries"][0]["GameObjects"]
    o.close()

    for p in tmp:
        x = p['GlobalPosition']['x'] + data['entries'][0]['PositionOffset']['x']
        y = p['GlobalPosition']['z'] + data['entries'][0]['PositionOffset']['z']
        startpos.append(([x, y]))

    startpos = startpos
    endpos = endpos

    return startpos, endpos, names


