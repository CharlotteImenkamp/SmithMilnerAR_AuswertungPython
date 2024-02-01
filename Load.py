import json
from deep_translator import GoogleTranslator, MyMemoryTranslator


# load data
def load_positions(path_end: str, path_start: str, label: str):
    endpos = []
    names = []
    startpos = []
    data = []

    # end positions
    o = open(path_end)
    data = json.load(o)
    tmp = data["entries"][0]["GameObjects"]
    o.close()

    # sort alphabetically according to 'Objectname'
    tmp = sorted(tmp, key= lambda x:x['Objectname']) 
    
    offset = data['entries'][0]['PositionOffset']

    counter = 0
    for p in tmp:
        # save x and y positions and add offset 
        x = p['GlobalPosition']['x'] + offset['x']
        y = p['GlobalPosition']['z'] + offset['z']
        endpos.append(([x, y]))

        # translate and save objectnames
        if label == 'english':
            names.append(GoogleTranslator(source = 'german', target = 'english').translate(p['Objectname']).lower())
        elif label == 'german':
            names.append(p['Objectname'].upper())
        elif label == 'numbers':
            # print(f"{GoogleTranslator(source = 'german', target = 'english').translate(p['Objectname']).lower()} ({counter}), ")
            names.append(counter)
            counter = counter + 1 
        else :
            raise Exception(f"Wrong label input. Valid input is 'english', 'german' or 'number' not {label}") 

    # start positions
    o = open(path_start)
    data = json.load(o)
    tmp = data["entries"][0]["GameObjects"]
    o.close()

    # sort alphabetically according to 'Objectname'
    tmp = sorted(tmp, key= lambda x:x['Objectname']) 

    for p in tmp:
        x = p['GlobalPosition']['x'] + data['entries'][0]['PositionOffset']['x']
        y = p['GlobalPosition']['z'] + data['entries'][0]['PositionOffset']['z']
        startpos.append(([x, y]))

    startpos = startpos
    endpos = endpos

    return startpos, endpos, names


