# Olympus is where gods are created

# Hermes is used everywhere to be an almighty information transmitter. It can be modified by any scripts
# thanks to Marc-André Vigneault!
class Hermes:
    def __init__(self, root_name, run_title, mode):
        self.dict = {}
        self.birth(root_name, run_title, mode)

    def birth(self, root_name, run_title, mode, **kwargs):
        self.dict['root_name'] = root_name
        self.dict['run_title'] = run_title
        self.dict['mode'] = mode

        self.dict.update(kwargs)
        return self.dict
