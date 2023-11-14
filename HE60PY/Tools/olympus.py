# Olympus is where gods are created
import os
import pickle
from .path import Path

class Hermes:
    # Hermes is used everywhere to be an almighty information transmitter. It can be modified by any scripts
    # thanks to Marc-André Vigneault!
    def __init__(self, root_name=None, run_title=None, mode=None,  kwargs=None, rebirth_path=None):
        if rebirth_path:
            self.rebirth(path=rebirth_path)
        else:
            self.get = {}
            self.birth(root_name, run_title, mode, kwargs)
        self.path = Path()
        self.root_to_HE60 = self.path.to_HE60
        self.usr_path = self.path.to_usr

    def birth(self, root_name, run_title, mode, kwargs):
        self.get['root_name'] = root_name
        self.get['run_title'] = run_title
        self.get['mode'] = mode
        self.get.update(kwargs)

    def rebirth(self, path):
        ThisNeedToExist(path)
        with open(path, 'rb') as handle:
            self.get = pickle.load(handle)

    # def update(self):

    def save_dict(self, path):
        with open(path, 'wb') as handle:
            pickle.dump(self.get, handle, protocol=pickle.HIGHEST_PROTOCOL)


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


class Invalid(Exception):
    def __init__(self, element,):
        self.message = f'This {element} is invalid.'
        super().__init__(self.message)

# class Pistis:
    # Pistis is the greek god of good faith, trust and reliability
    # As Ronald Reagan, using a Soviet proverb that Lenin oftenly used
    # Trust, but verify!                        Doveryai, no proveryai!

def DeleteFile(path):
    if DoesThisExist(path):
        os.remove(path)


def CreateIfDoesntExist(path):
    if not DoesThisExist(path):
        os.makedirs(path)
    return path


def ThisNeedToExist(path):
    if not DoesThisExist(path):
        raise InvalidFile(path)


def DoesThisExist(path):
    return os.path.exists(path)


        





