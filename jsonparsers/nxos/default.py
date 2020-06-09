'''

Default JSON parser - Get all leaf keys recursively and build a list array with them

'''

# Global variables used to store results of the recursive functions
leaf_keys = []
table = []

def parse(json_data):
    def get_leaf_keys(json_data):
        '''
        Recursively walk into nested dictionnaries to grab the leaf keys
        '''
        global leaf_keys

        for k, v in json_data.items():
            if isinstance(v, dict):
                get_leaf_keys(v)
            else:
                if not k in leaf_keys:
                    leaf_keys.append(k)

    def make_table(json_data, leaf_keys):
        '''
        Recursively walk into nested dictionnaries to build a table based on a list of keys
        '''
        global table

        for _, v in json_data.items():
            if isinstance(v, dict):
                make_table(v, leaf_keys)
            else:
                t = []
                for key in leaf_keys:
                    t.append(json_data.get(key, "N/A"))
                table.append(t)
                break   # Needed to exit the loop after appending the row, else it will be run len(dict.items) times
                # The break statement may be problematic with some data structures - to be investigated and improved !!!
    
    global table
    global leaf_keys

    get_leaf_keys(json_data)
    header = [key.upper() for key in leaf_keys]
    make_table(json_data, leaf_keys)
    table = [header] + table

    return table