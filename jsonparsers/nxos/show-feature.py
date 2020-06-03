'''

JSON parser for "show feature set" (NXOS)

'''

def parse(json_data):
    header = ["FEATURE", "STATE"]
    table = []
    t = []
    table.append(header)
    for feature, subtree in json_data["feature"].items():
        t.append(feature)
        for index, value in subtree["instance"].items():   # This is only to get past the index number object
            t.append(value["state"])
        table.append(t)
        t = []
    return table