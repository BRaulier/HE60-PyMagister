

class DataViewer:
    def __init__(self, hermes=None, root_name=None):
        # This class is initialized either by passing hermes or root_name, in the latter it is used to initialize hermes
        if hermes:
            self.hermes = hermes
            self.root_name = self.hermes.get['root_name']
            self.hermes.save_dict(path=f'{os.getcwd()}/data/{self.root_name}/hermes.pickle')
        elif root_name:
            self.root_name = root_name
            self.hermes = olympus.Hermes(rebirth_path=f'{os.getcwd()}/data/{self.root_name}/hermes.pickle')
            
    def draw_Eudos_profiles(self, desired_wavelenghts):
        
    