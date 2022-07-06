import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
from scipy.interpolate import interp1d
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
        self.linestyles = ['solid', 'dotted', 'dashed', 'dashdot', 'solid', 'dotted', 'dashed', 'dashdot', 'solid', 'dotted', 'dashed', 'dashdot']
        self.colors = ['#004599', '#0097b7', '#5ccc0c', '#004599', '#0097b7', '#5ccc0c', '#004599', '#0097b7', '#5ccc0c']

        self.color_maps = ['Reds', 'Greens', 'Blues', 'Reds', 'Greens', 'Blues', 'Reds', 'Greens', 'Blues', 'Reds', 'Greens', 'Blues']
        self.load_Eudos_IOP_df()

    # ========================= #
    # Available figure routines #
    # ========================= #

    def run_figure_routine(self, save_binaries=False, save_png=True, close=True):
        fig1, ax1 = self.draw_Eudos_profiles()
        fig2, ax2 = self.draw_IOP_profiles()
        try:
            fig3, ax3 = self.draw_zenith_radiance_maps()
            fig3.savefig(f'{self.wd}/zenith_maps.png', dpi=600)
            pickle.dump(fig3, open(f'{self.wd}/zenith_maps.fig.pickle', 'wb'))
        except:
            fig3, ax = plt.subplots()
            pass
        fig4, ax4 = self.draw_zenith_radiance_profiles([0., 0.20, 0.40, 0.60, 0.80, 1.00, 1.20, 1.41, 1.60, 1.80, 2.00])
        
        if save_binaries:
            pickle.dump(fig1, open(f'{self.wd}/eudos_profiles.fig.pickle', 'wb'))
            pickle.dump(fig2, open(f'{self.wd}/iop_profiles.fig.pickle', 'wb'))
            pickle.dump(fig4, open(f'{self.wd}/zenith_profiles.fig.pickle', 'wb'))
        if save_png:
            fig1.savefig(f'{self.wd}/eudos_profiles.png', dpi=600)
            fig2.savefig(f'{self.wd}/iop_profiles.png', dpi=600)
            fig4.savefig(f'{self.wd}/zenith_profiles.png', dpi=600)
        [plt.close(fig) for fig in [fig1, fig2, fig3, fig4]]

    # ================================== #
    # Complete figures drawing functions #
    # ================================== #

    def draw_Eudos_profiles(self, depth_interval=None, desired_wavelengths=None, subplots=True):
        if desired_wavelengths is None:
            desired_wavelengths = self.run_bands
        # if no list of desired wavelengths is given, assume all are needed
        self.load_Eudos_IOP_df()
        if subplots:
            fig, ax = plt.subplots(1, len(desired_wavelengths), figsize=(12, 12))
            ls = [0]*len(desired_wavelengths)
            if len(desired_wavelengths) == 1: ax = [ax] # So the loop below can run for 1 wavelength
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
        return fig, ax

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
        return fig, ax

    def draw_zenith_radiance_maps(self, depth_interval=None, desired_wavelengths=None):
        if desired_wavelengths is None:
            desired_wavelengths = self.run_bands
        # if no list of desired wavelengths is given, assume all are to be plotted
        self.load_zenith_radiance()
        fig, ax = plt.subplots(1, len(desired_wavelengths), figsize=(16, 9))
        for i, wavelength in enumerate(desired_wavelengths):
            cm = self.draw_zenith_radiance_map(wavelength, ax[i], depth_interval)
        self.format_zenith_radiance_maps(fig, ax, cm)
        return fig, ax

    def draw_zenith_radiance_profiles(self, requested_depths, desired_wavelengths=None, interpolate=True):
        if desired_wavelengths is None:
            desired_wavelengths = self.run_bands
        self.load_zenith_radiance()
        fig, ax = plt.subplots(1, len(desired_wavelengths), figsize=(12, 6))
        if len(desired_wavelengths) == 1: ax=[ax]
        for i, wavelength in enumerate(desired_wavelengths):
            self.draw_zenith_radiance_at_depths(requested_depths, wavelength, ax[i], interpolate)
        self.format_zenith_radiance_profiles(ax)
        return fig, ax

    def draw_stepped_zenith_radiance_profiles(self, requested_depths, desired_wavelengths=None, fig=None, ax=None):
        if desired_wavelengths is None:
            desired_wavelengths = self.run_bands
        self.load_zenith_radiance()
        if fig is None:
            fig, ax = plt.subplots(1, len(desired_wavelengths), figsize=(12, 6))
        if len(desired_wavelengths) == 1: ax=[ax]
        for i, wavelength in enumerate(desired_wavelengths):
            self.draw_stepped_zenith_radiance_at_depths(requested_depths, wavelength, ax[i])
        self.format_zenith_radiance_profiles(ax)
        return fig, ax

    # ================================================= #
    # Auxiliary functions used to draw complete figures #
    # ================================================= #

    def draw_zenith_radiance_map(self, wavelength, ax, depth_interval):
        i_wavelength = list(self.run_bands).index(wavelength)
        to_plot_image = self.zenith_radiance[:,:,i_wavelength]
        cm = ax.imshow(to_plot_image, aspect='auto', extent=[0, 180, 3.00, -0.01],
                  norm=matplotlib.colors.LogNorm(vmin=to_plot_image.min(), vmax=to_plot_image.max()),
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

    def draw_zenith_radiance_at_depths(self, depths, wavelength, ax, interpolate):
        i_wavelength = list(self.run_bands).index(wavelength)
        cm = self.color_maps[i_wavelength]
        cmap = matplotlib.cm.get_cmap(cm)
        intensities = np.linspace(0.40, 1.00, len(depths))
        for i, depth in enumerate(depths):
            x_angle, y_radiance = self.get_zenith_radiance_profile_at_depth(depth, wavelength, interpolate=interpolate)
            ax.plot(x_angle, y_radiance, color=cmap(intensities[i]), label=f'{depth} m')

    def draw_stepped_zenith_radiance_at_depths(self, depths, wavelength, ax):
        i_wavelength = list(self.run_bands).index(wavelength)
        cm = self.color_maps[i_wavelength]
        cmap = matplotlib.cm.get_cmap(cm)
        intensities = np.linspace(0.40, 1.00, len(depths))
        step_borders = [0, 5, 15, 25, 35, 45, 55, 65, 75, 85, 95, 105, 115, 125, 135, 145, 155, 165, 175, 180]
        for i, depth in enumerate(depths):
            x_angle, y_radiance = self.get_zenith_radiance_profile_at_depth(depth, wavelength, interpolate=False)
            for j, y_value  in enumerate(y_radiance):
                ax.plot((step_borders[j], step_borders[j+1]), (y_value, y_value), color=cmap(intensities[i]))
                if step_borders[j+1] < 180:
                    ax.plot((step_borders[j+1], step_borders[j+1]), (y_radiance[j], y_radiance[j+1]), color=cmap(intensities[i]))
            ax.plot([],[], color=cmap(intensities[i]), label=f'{depth} m')

    # ============ #
    # Data loaders #
    # ============ #

    def load_Eudos_IOP_df(self):
        if self.Eudos_IOPs_df is None:  # Only loads the df if doesn't already exists
            self.Eudos_IOPs_df = pd.read_csv(f'{self.wd}/eudos_iops.csv')
        else:
            pass

    def load_zenith_radiance(self):
        if self.zenith_radiance is None:
            self.zenith_radiance = np.zeros((len(self.depths) + 1, 19, len(self.run_bands))) # 3D array to store [depth, zenith angle, wvlgth]
            raw_zenith_radiance = np.loadtxt(f'{self.wd}/zenith_profiles.txt')
            for i, wavelength in enumerate(self.run_bands):
                to_be_reshaped = raw_zenith_radiance[raw_zenith_radiance[:, 2] == wavelength, :]
                total_radiance_image = to_be_reshaped[:, 3].reshape(len(self.depths) + 1, 19)
                self.zenith_radiance[:, :, i] = total_radiance_image

    def get_Eudos_at_depths(self, depths, wavelength):
        self.load_Eudos_IOP_df()
        Eu_list, Ed_list, Eo_list = [], [], []
        for depth in depths:
            Eu_i, Ed_i, Eo_i = self.get_Eudos_at_depth(depth, wavelength)
            Eu_list.append(Eu_i)
            Ed_list.append(Ed_i)
            Eo_list.append(Eo_i)
        return Eu_list, Ed_list, Eo_list

    def get_Eudos_at_depth(self, depth, wavelength):
        self.load_Eudos_IOP_df()
        i_depth = list(self.depths).index(round(depth,2)) + 1 # 0 is above the interface,
        Eu = self.Eudos_IOPs_df[f'Eu_{wavelength:.1f}'][i_depth]
        Ed = self.Eudos_IOPs_df[f'Ed_{wavelength:.1f}'][i_depth]
        Eo = self.Eudos_IOPs_df[f'Eo_{wavelength:.1f}'][i_depth]
        return Eu, Ed, Eo

    def get_abg_at_depths(self, depths, wavelength):
        self.load_Eudos_IOP_df()
        a_list, b_list, g_list = [], [], []
        for depth in depths:
            a, b, g = self.get_abg_at_depth(depth, wavelength)
            a_list.append(a)
            b_list.append(b)
            g_list.append(g)
        return np.array(a_list), np.array(b_list), np.array(g_list)

    def get_abg_at_depth(self, depth, wavelength):
        self.load_Eudos_IOP_df()
        i_depth = list(self.depths).index(round(depth,2)) + 1 # 0 is above the interface,
        a = self.Eudos_IOPs_df[f'a_{wavelength:.1f}'][i_depth]
        b = self.Eudos_IOPs_df[f'b_{wavelength:.1f}'][i_depth]
        g = self.Eudos_IOPs_df[f'g'][i_depth]
        return a, b, g

    def get_scalar_Eudos_at_depth(self, depth, wavelength):
        self.load_Eudos_IOP_df()
        i_depth = list(self.depths).index(depth) + 1 # 0 is above the interface,
        Eou = self.Eudos_IOPs_df[f'Eou_{wavelength:.1f}'][i_depth]
        Eod = self.Eudos_IOPs_df[f'Eod_{wavelength:.1f}'][i_depth]
        Eo = self.Eudos_IOPs_df[f'Eo_{wavelength:.1f}'][i_depth]
        return Eou, Eod, Eo

    def get_zenith_radiance_profile_at_depth(self, depth, wavelength, interpolate=True):
        self.load_zenith_radiance()
        i_wavelength = list(self.run_bands).index(wavelength)
        try:
            i_depth = list(self.depths).index(round(depth, 3))
        except:
            if depth == -1.:  # Depth -1 is the incoming radiation, just above the interface
                i_depth = -1
            else:
                print(f"Warning: Could not find resquested depth ({depth}) in: get_zenith_radiance_profile_at_depth")
        phi_angles = [0., 10., 20., 30., 40, 50., 60., 70., 80., 90.,
                      100., 110., 120., 130., 140., 150., 160., 170., 180.]  # Angles for which radiance is known

        zenith_radiance = self.zenith_radiance[i_depth+1, :, i_wavelength]
        if interpolate:
            f = interp1d(phi_angles, zenith_radiance, kind='cubic')
            x_new_angles = np.arange(181)
            y_new_radiance = f(x_new_angles)
            return x_new_angles, y_new_radiance
        else:
            return phi_angles, zenith_radiance

    def get_RT_at_wavelength(self, wavelength):
        self.load_Eudos_IOP_df()
        try:
            ice_bottom_index = list(self.depths).index(round(self.hermes.get['ice_thickness'],2)) + 1
        except:
            ice_bottom_index = 202
        surf_Ed = self.Eudos_IOPs_df[f'Ed_{wavelength:.1f}'][0]  # In air
        surf_Eu = self.Eudos_IOPs_df[f'Eu_{wavelength:.1f}'][0]  # In air
        ice_bot_Ed = self.Eudos_IOPs_df[f'Ed_{wavelength:.1f}'][ice_bottom_index]
        R = surf_Eu / surf_Ed  # Surf Reflectance
        T = ice_bot_Ed / surf_Ed
        return R, T

    def get_ext_coeff(self, wavelength):
        R, T = self.get_RT_at_wavelength(wavelength)
        thickness = self.hermes.get['ice_thickness']
        ext_coeff = -np.log(T)/thickness
        return ext_coeff

    # ========================================== #
    # Auxiliary functions used to format figures #
    # ========================================== #

    def include_extended_legend(self, figtype, wavelength, ax):
        if figtype == 'Eudos':
            R, T = self.get_RT(wavelength)
            extd_label = f'$\\lambda$={wavelength:.0f}nm\nT={T:.2E}\nR={R:.2E}'
            ax.plot([], [], color="white", label=extd_label)
            
    def format_zenith_radiance_profiles(self, axes):
        for ax in axes:
            ax.legend(prop={'size': 6})
            ax.set_xlabel("Zenith angles [$^\circ$]")
            ax.set_yscale("log")
            ax.xaxis.set_major_locator(MultipleLocator(45))
            ax.xaxis.set_minor_locator(MultipleLocator(15))
        axes[0].set_ylabel('L [W $\cdot$ m$^2$ $\cdot$ sr$^{-1}$ $\cdot$ mm$^{-1}$]')
        
    def format_zenith_radiance_maps(self, fig, ax, cm):
        fig.subplots_adjust(right=0.8)
        cbar = fig.colorbar(cm, cax=fig.add_axes([0.85, 0.15, 0.05, 0.7]))
        cbar.ax.set_ylabel('L [W $\cdot$ m$^2$ $\cdot$ sr$^{-1}$ $\cdot$ mm$^{-1}$]', rotation=270, labelpad=25)
        fig.supylabel('Depth [m]')
        fig.supxlabel('Zenith angle [$^\circ$]')
        
    def format_profile_plot(self, ax, depth_interval, title=None, xlog=True):
        if depth_interval:
            ax.set_ylim(depth_interval[0], depth_interval[1])
            interval = depth_interval[1] - depth_interval[0]
        if title:
            ax.title.set_text(title)
        if xlog:
            ax.set_xscale("log")
        ax.invert_yaxis()
        ax.legend()
        if depth_interval:
            ax.yaxis.set_major_locator(MultipleLocator(round(interval/10, 2)))
        else:
            ax.yaxis.set_major_locator(MultipleLocator(0.5))



if __name__ == "__main__":
    print('\n')

