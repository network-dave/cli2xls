'''

JSON parser for "show feature set" (NXOS)

'''

def parse(json_data):
    '''
    Parse specific JSON data to a list array
    '''
    # Define headers for the columns here
    header = ["FEATURE", "STATE"]
    table = []
    t = []
    table.append(header)
    # Command specific parsing comes here
    for feature, subtree in json_data["feature"].items():
        t.append(feature)
        for index, value in subtree["instance"].items():   # This is only to get past the index number object
            t.append(value["state"])
        table.append(t)
        t = []
    return table