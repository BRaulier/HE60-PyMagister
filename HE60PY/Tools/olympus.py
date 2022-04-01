# Olympus is where gods are created
import os

class Hermes:
    # Hermes is used everywhere to be an almighty information transmitter. It can be modified by any scripts
    # thanks to Marc-André Vigneault!
    def __init__(self, root_name, run_title, mode, kwargs):
        self.dict = {}
        self.birth(root_name, run_title, mode, kwargs)

    def birth(self, root_name, run_title, mode, kwargs):
        self.dict['root_name'] = root_name
        self.dict['run_title'] = run_title
        self.dict['mode'] = mode
        self.dict.update(kwargs)


class InvalidFile(Exception):
    def __init__(self, filename, ):
        self.filename = filename
        self.message = 'This file does not exists: ' + filename
        super().__init__(self.message)


# class Pistis:
    # Pistis is the greek god of good faith, trust and reliability
    # As Ronald Reagan, using a Soviet proverb that Lenin oftenly used
    # Trust, but verify!                        Doveryai, no proveryai!
def ThisNeedToExist(filepath):
    if not os.path.isfile(filepath):
        raise InvalidFile(filepath)

        





