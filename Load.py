import json
from deep_translator import GoogleTranslator, MyMemoryTranslator


# load data
def load_positions(path_end: str, path_start: str, english: bool):
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
        if english:
            names.append(GoogleTranslator(source = 'german', target = 'english').translate(p['Objectname']).lower())
        else:
            names.append(p['Objectname'].upper())

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


