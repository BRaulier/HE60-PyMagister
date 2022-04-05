# Olympus is where gods are created
import os
import pickle

class Hermes:
    # Hermes is used everywhere to be an almighty information transmitter. It can be modified by any scripts
    # thanks to Marc-André Vigneault!
    def __init__(self, root_name=None, run_title=None, mode=None,  kwargs=None, rebirth_path=None):
        if rebirth_path:
            self.rebirth(path=rebirth_path)
        else:
            self.dict = {}
            self.birth(root_name, run_title, mode, kwargs)

    def birth(self, root_name, run_title, mode, kwargs):
        self.dict['root_name'] = root_name
        self.dict['run_title'] = run_title
        self.dict['mode'] = mode
        self.dict.update(kwargs)

    def rebirth(self, path):
        ThisNeedToExist(path)
        with open(path, 'rb') as handle:
            self.dict = pickle.load(handle)

    def save_dict(self, path):
        with open(path, 'wb') as handle:
            pickle.dump(self.dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


class InvalidFile(Exception):
    def __init__(self, filename, ):
        self.filename = filename
        self.message = 'This user provided file does not exist: ' + self.filename
        super().__init__(self.message)


class InvalidMode(Exception):
    def __init__(self, mode,):
        self.mode = mode
        self.message = 'This mode is invalid: ' + self.mode 
        super().__init__(self.message)


# class Pistis:
    # Pistis is the greek god of good faith, trust and reliability
    # As Ronald Reagan, using a Soviet proverb that Lenin oftenly used
    # Trust, but verify!                        Doveryai, no proveryai!


def CreateIfDoesntExist(path):
    if not DoesThisExist(path):
        os.makedirs(path)
    return path


def ThisNeedToExist(path):
    if not DoesThisExist(path):
        raise InvalidFile(path)


def DoesThisExist(path):
    return os.path.exists(path)


        





