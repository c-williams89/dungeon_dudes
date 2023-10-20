'''Limited Dictionary Class for Dungeon Dudes'''

class LimitedDict:
    '''Limited Dictionary with Predefined Allowed Keys'''

    def __init__(self, allowed_keys: [tuple, str], default_value : [str,int]= "EMPTY"):
        if isinstance(allowed_keys, str):
            self._allowed_keys = (allowed_keys)
            self.data = {allowed_keys: default_value}
        else:
            self._allowed_keys = allowed_keys
            self.data = {key: default_value for key in self._allowed_keys}

    def __getitem__(self, key):
        try:
            return self.data[key]
        except KeyError:
            pass

    def __contains__(self, key):
        '''Check if a key exists in the dictionary'''
        return key in self.data

    def __setitem__(self, key, value):
        if key not in self._allowed_keys:
            raise KeyError(f"{'Key '+key+' is not allowed.'}"
                            f"{'Allowed keys are: '+ ', '.join(self._allowed_keys)}")
        self.data[key] = value

    def __delitem__(self, key):
        self.data[key] = "EMPTY"

    def __repr__(self):
        return repr(self.data)

    def get(self, key, default=None):
        '''Get Function Set to Mimic Builtin Dictionary'''
        return self.data.get(key, default)

    def items(self):
        '''Items Function to Mimic Builtin Dictionary'''
        return self.data.items()
