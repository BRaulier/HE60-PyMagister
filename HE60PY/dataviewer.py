import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
import matplotlib

from .Tools import olympus
from .Tools.builderdata import DataBuilder

plt.rcParams.update({'font.size': 14})


class DataViewer(DataBuilder):
    def __init__(self, hermes=None, root_name=None):
        super().__init__(hermes, root_name)
        olympus.ThisNeedToExist(self.wd)

        self.zenith_radiance = None
        self.linestyles = ['solid', 'dotted', 'dashed', 'dashdot']
        self.colors = ['#004599', '#0097b7', '#5ccc0c']

    def draw_Eudos_profiles(self, reduced=True, depth_interval=None, desired_wavelengths=None, subplots=True):
        if desired_wavelengths is None:
            desired_wavelengths = self.run_bands
        # if no list of desired wavelengths is given, assume all are needed
        self.load_Eudos_IOP_df()
        if subplots:
            fig, ax = plt.subplots(1, len(desired_wavelengths), figsize=(12, 12))
            ls = [0]*len(desired_wavelengths)
        else:
            fig, ax = plt.subplots(1, 1, figsize=(7, 10))
            ax = [ax]*len(desired_wavelengths)
            ls = np.arange(len(desired_wavelengths))
        for i, wavelength in enumerate(desired_wavelengths):
            self.draw_Eudos_IOP_profile('Ed', wavelength, reduced, ax[i], ci=0, li=ls[i])
            self.draw_Eudos_IOP_profile('Eu', wavelength, reduced, ax[i], ci=1, li=ls[i])
            self.draw_Eudos_IOP_profile('Eo', wavelength, reduced, ax[i], ci=2, li=ls[i])
            self.format_profile_plot(ax[i], depth_interval)
        fig.tight_layout()
        plt.show()
        
    def draw_IOP_profiles(self, reduced=False, depth_interval=None, desired_wavelengths=None):
        if desired_wavelengths is None:
            desired_wavelengths = self.run_bands
        # if no list of desired wavelengths is given, assume all are to be plotted
        self.load_Eudos_IOP_df()
        fig, ax = plt.subplots(1, 3, figsize=(12, 12))
        to_be_plotted = ['a', 'b', 'bb']
        for i, condition in enumerate(to_be_plotted):
            for j, wavelength in enumerate(desired_wavelengths):
                title = f'{condition}'
                self.draw_Eudos_IOP_profile(condition, wavelength, reduced, ax[i], ci=j, li=0)
                self.format_profile_plot(ax[i], depth_interval, title)
        fig.tight_layout()
        plt.show()

    def draw_zenith_radiance_maps(self, reduced=False, depth_interval=None, desired_wavelengths=None):
        if desired_wavelengths is None:
            desired_wavelengths = self.run_bands
        # if no list of desired wavelengths is given, assume all are to be plotted
        self.load_zenith_radiance()
        fig, ax = plt.subplots(1, len(desired_wavelengths), figsize=(12, 12))
        for i, wavelength in enumerate(desired_wavelengths):
            self.draw_zenith_radiance_map(wavelength, reduced, ax[i], depth_interval)
            
    def draw_zenith_radiance_map(self, wavelength, reduced, ax, depth_interval):
        if reduced:
            correction_factor = self.hermes.get['refr'] ** 2
        else:
            correction_factor = 1
        # top_idx, bottom_idx = 
        to_be_reshaped = self.zenith_radiance[self.zenith_radiance[:, 2] == wavelength, :]
        total_radiance_image = to_be_reshaped[:, 3].reshape(len(self.depths)+1, 20)
        total_radiance_image[1:, :] = total_radiance_image[1:, :] / correction_factor
        ax.imshow(total_radiance_image, aspect='auto', norm=matplotlib.colors.LogNorm(),
                     cmap='hot')

    def draw_Eudos_IOP_profile(self, cond, wavelength, reduced, ax, ci, li, ):
        if reduced:
            correction_factor = self.hermes.get['refr'] ** 2
        else:
            correction_factor = 1
        if cond[0] == 'E':
            label = f'{cond[0]}$_{cond[1]}$ $\lambda=$ {wavelength:.0f}'
        else:
            label = f'{wavelength:.1f}'
        y_to_plot = self.Eudos_IOPs_df['depths']
        x_to_plot = self.Eudos_IOPs_df[f'{cond}_{wavelength}'] / correction_factor
        ax.plot(x_to_plot, y_to_plot, color=self.colors[ci],
                 linestyle=self.linestyles[li], label=label)

    def load_Eudos_IOP_df(self):
        if self.Eudos_IOPs_df is None:  # Only loads the df if doesn't already exists
            self.Eudos_IOPs_df = pd.read_csv(f'{self.wd}/eudos_iops.csv')
        else:
            pass

    def load_zenith_radiance(self):
        if self.zenith_radiance is None:
            self.zenith_radiance = np.loadtxt(f'{self.wd}/zenith_profiles.txt')

    def format_profile_plot(self, ax, depth_interval, title=None, ylog=True):
        if depth_interval:
            ax.set_ylim(depth_interval[0], depth_interval[1])
        if title:
            ax.title.set_text(title)
        if ylog:
            ax.set_xscale("log")
        ax.invert_yaxis()
        ax.legend()
        ax.yaxis.set_major_locator(MultipleLocator(.50))
        ax.yaxis.set_minor_locator(MultipleLocator(.10))

