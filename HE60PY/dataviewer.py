import pandas as pd
import matplotlib.pyplot as plt

from .Tools import olympus
from .Tools.builderdata import DataBuilder


class DataViewer(DataBuilder):
    def __init__(self, hermes=None, root_name=None):
        super().__init__(hermes, root_name)
        olympus.ThisNeedToExist(self.wd)

        self.linestyles = ['solid', 'dotted', 'dashed', 'dashdot']
        self.colors = ['#004599', '#0097b7', '#5ccc0c']

    # def load_Eudos_profiles(self):
    #     if not self.Ed:
    #         self.Ed, self.Eu, self.Eo = {}, {}, {}
    #         self.load_Eudos_IOP_df()
    #         for wavelength in self.run_bands:
    #             self.Ed[f'{wavelength}'] =
    #     else: pass
    #     
    def load_IOP_profiles(self):
        if not self.a:
            self.load_Eudos_IOP_df()
        else:
            pass

    # def load_zenith_radiance(self):

    def draw_Eudos_profiles(self, reduced=True, depth_interval=None, desired_wavelengths=None):
        if desired_wavelengths is None:
            desired_wavelengths = self.run_bands
        # if no list of desired wavelengths is given, assume all are needed
        self.load_Eudos_IOP_df()
        fig, ax = plt.subplots(1, len(desired_wavelengths))
        for i, wavelength in enumerate(desired_wavelengths):
            self.draw_Eudos_profile('Ed', wavelength, reduced, ax[i], ci=0, li=0)
            self.draw_Eudos_profile('Eu', wavelength, reduced, ax[i], ci=1, li=0)
            self.draw_Eudos_profile('Eo', wavelength, reduced, ax[i], ci=2, li=0)
            ax[i].set_xscale("log")
            ax[i].invert_yaxis()
            ax[i].legend()
        plt.show()

    def draw_Eudos_profile(self, cond, wavelength, reduced, axe, ci, li, ):
        if reduced:
            correction_factor = self.hermes.get['refr'] ** 2
        else:
            correction_factor = 1
        y_to_plot = self.Eudos_IOPs_df['depths']
        x_to_plot = self.Eudos_IOPs_df[f'{cond}_{wavelength}'] / correction_factor
        axe.plot(x_to_plot, y_to_plot, color=self.colors[ci],
                 linestyle=self.linestyles[li], label=f'{cond[0]}$_{cond[1]}$ $\lambda=$ {wavelength:.0f}')

    def load_Eudos_IOP_df(self):
        # Only loads the df if doesn't already exists
        if not self.Eudos_IOPs_df:
            self.Eudos_IOPs_df = pd.read_csv(f'{self.wd}/eudos_iops.csv')
        else:
            pass
