import pandas as pd
from .Tools import olympus
from .Tools.builderdata import BuilderData


class DataViewer(BuilderData):
    def __init__(self, hermes=None, root_name=None):
        super(BuilderData, self).__init__(hermes, root_name)
        olympus.ThisNeedToExist(self.wd)
        
    def load_Eudos_profiles(self):
        if not self.Ed:
            self.load_Eudos_IOP_df()
        else:
            pass
        
    def load_IOP_profiles(self):
        if not self.a:
            self.load_Eudos_IOP_df()
        else:
            pass
    
    def load_zenith_radiance(self):
            
    def draw_Eudos_profiles(self, desired_wavelenghts=None):
        
    def load_Eudos_IOP_df(self):
        # Only loads the df if doesn't already exists
        if not self.Eudos_IOPs_df:
            self.Eudos_IOPs_df = pd.read_csv(f'{self.wd}/eudos_iops.csv')
        else:
            pass
    
    