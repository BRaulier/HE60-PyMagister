import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
import matplotlib
import pickle

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

    def run_figure_routine(self, save_binaries, save_png):
        fig1 = self.draw_Eudos_profiles()
        fig2 = self.draw_IOP_profiles()
        fig3 = self.draw_zenith_radiance_maps()
        if save_binaries:
            pickle.dump(fig1, open(f'{self.wd}/eudos_profiles.fig.pickle', 'wb'))
            pickle.dump(fig2, open(f'{self.wd}/iop_profiles.fig.pickle', 'wb'))
            pickle.dump(fig3, open(f'{self.wd}/zenith_maps.fig.pickle', 'wb'))
        if save_png:
            fig1.savefig(f'{self.wd}/eudos_profiles.png', dpi=600)
            fig2.savefig(f'{self.wd}/iop_profiles.png', dpi=600)
            fig3.savefig(f'{self.wd}/zenith_maps.png', dpi=600)

    def draw_Eudos_profiles(self, depth_interval=None, desired_wavelengths=None, subplots=True):
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
            self.draw_Eudos_IOP_profile('Ed', wavelength, ax[i], ci=0, li=ls[i])
            self.draw_Eudos_IOP_profile('Eu', wavelength, ax[i], ci=1, li=ls[i])
            self.draw_Eudos_IOP_profile('Eo', wavelength, ax[i], ci=2, li=ls[i])
            self.include_extended_legend('Eudos', wavelength, ax[i])
            self.format_profile_plot(ax[i], depth_interval)
        fig.tight_layout()
        return fig

    def draw_IOP_profiles(self, depth_interval=None, desired_wavelengths=None):
        if desired_wavelengths is None:
            desired_wavelengths = self.run_bands
        # if no list of desired wavelengths is given, assume all are to be plotted
        self.load_Eudos_IOP_df()
        fig, ax = plt.subplots(1, 3, figsize=(12, 12))
        to_be_plotted = ['a', 'b', 'bb']
        for i, condition in enumerate(to_be_plotted):
            for j, wavelength in enumerate(desired_wavelengths):
                title = f'{condition}'
                self.draw_Eudos_IOP_profile(condition, wavelength, ax[i], ci=j, li=0)
                self.format_profile_plot(ax[i], depth_interval, title)
        fig.tight_layout()
        return fig

    def draw_zenith_radiance_maps(self, depth_interval=None, desired_wavelengths=None):
        if desired_wavelengths is None:
            desired_wavelengths = self.run_bands
        # if no list of desired wavelengths is given, assume all are to be plotted
        self.load_zenith_radiance()
        fig, ax = plt.subplots(1, len(desired_wavelengths), figsize=(9, 16))
        for i, wavelength in enumerate(desired_wavelengths):
            cm = self.draw_zenith_radiance_map(wavelength, ax[i], depth_interval)
        self.format_zenith_radiance_maps(fig, ax, cm)
        return fig
            
    def draw_zenith_radiance_map(self, wavelength, ax, depth_interval):
        # top_idx, bottom_idx = 
        to_be_reshaped = self.zenith_radiance[self.zenith_radiance[:, 2] == wavelength, :]
        total_radiance_image = to_be_reshaped[:, 3].reshape(len(self.depths)+1, 20)
        total_radiance_image[1:, :] = total_radiance_image[1:, :]
        cm = ax.imshow(total_radiance_image, aspect='auto', extent=[0, 180, 3.00, -0.01],
                  norm=matplotlib.colors.LogNorm(vmin=total_radiance_image.min(), vmax=total_radiance_image.max()),
                  cmap='gist_ncar')
        return cm

    def draw_Eudos_IOP_profile(self, cond, wavelength, ax, ci, li, ):
        if cond[0] == 'E':
            label = f'{cond[0]}$_{cond[1]}$'
        else:
            label = f'{wavelength:.1f}'
        y_to_plot = self.Eudos_IOPs_df['depths']
        x_to_plot = self.Eudos_IOPs_df[f'{cond}_{wavelength}']
        ax.plot(x_to_plot, y_to_plot, color=self.colors[ci],
                 linestyle=self.linestyles[li], label=label)

    def include_extended_legend(self, figtype, wavelength, ax):
        if figtype == 'Eudos':
            surf_Ed = self.Eudos_IOPs_df[f'Ed_{wavelength}'][0]  # In air
            surf_Eu = self.Eudos_IOPs_df[f'Eu_{wavelength}'][0]  # In air
            ice_bot_Ed = self.Eudos_IOPs_df[f'Ed_{wavelength}'][202]
            R = surf_Eu/surf_Ed # Surf Reflectance
            T = ice_bot_Ed/surf_Ed
            extd_label = f'$\\lambda$={wavelength:.0f}nm\nT={T:.2E}\nR={R:.2E}'
            ax.plot([], [], color="white", label=extd_label)
            
    def load_Eudos_IOP_df(self):
        if self.Eudos_IOPs_df is None:  # Only loads the df if doesn't already exists
            self.Eudos_IOPs_df = pd.read_csv(f'{self.wd}/eudos_iops.csv')
        else:
            pass

    def load_zenith_radiance(self):
        if self.zenith_radiance is None:
            self.zenith_radiance = np.loadtxt(f'{self.wd}/zenith_profiles.txt')

    def format_zenith_radiance_maps(self, fig, ax, cm):
        fig.subplots_adjust(right=0.8)
        cbar = fig.colorbar(cm, cax=fig.add_axes([0.85, 0.15, 0.05, 0.7]))
        cbar.ax.set_ylabel('L [W $\cdot$ m$^2$ $\cdot$ sr$^{-1}$ $\cdot$ mm$^{-1}$]', rotation=270, labelpad=25)
        fig.supylabel('Depth [m]')
        fig.supxlabel('Zenith angle [$^\circ$]')
        

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

