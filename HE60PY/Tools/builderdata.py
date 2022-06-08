import os
import numpy as np
from . import olympus


class DataBuilder:
    def __init__(self, hermes=None, root_name=None):
        """
        This class is used to build data classes
        
        This class is initialized either by passing hermes or root_name,
        in the latter it is used to initialize hermes
        """
        if hermes:
            self.hermes = hermes
            self.root_name = self.hermes.get['root_name']
            self.wd = f'{os.getcwd()}/data/{self.root_name}'
            olympus.CreateIfDoesntExist(self.wd)
            self.hermes.save_dict(path=f'{os.getcwd()}/data/{self.root_name}/hermes.pickle')
        elif root_name:
            self.root_name = root_name
            self.wd = f'{os.getcwd()}/data/{self.root_name}'
            olympus.CreateIfDoesntExist(self.wd)
            self.hermes = olympus.Hermes(rebirth_path=f'{os.getcwd()}/data/{self.root_name}/hermes.pickle')

        self.usr_path = os.path.expanduser('~')
        self.run_bands = self.hermes.get['run_bands']
        self.depths = np.array([round(depth,4) for depth in self.hermes.get['zetanom']])
        self.run_bands = self.hermes.get['run_bands']
        self.n_depths, = self.depths.shape

        self.Eudos_IOPs_df = None
        self.Ed, self.Eu, self.Eo = None, None, None
        self.a, self.b, self.bb = None, None, None