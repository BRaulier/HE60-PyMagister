import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import os

from .Tools import header_library
from .Tools import olympus


class DataFinder:
    def __init__(self, hermes=None, root_name=None):
        # This class is initialized either by passing hermes or root_name, in the latter it is used to initialize hermes
        if hermes:
            self.hermes = hermes
            self.root_name = self.hermes.get['root_name']
            self.hermes.save_dict(path=f'{os.getcwd()}/data/{self.root_name}/hermes.pickle')
        elif root_name:
            self.root_name = root_name
            self.hermes = olympus.Hermes(rebirth_path=f'{os.getcwd()}/data/{self.root_name}/hermes.pickle')

        self.usr_path = os.path.expanduser('~')
        self.wd = f'{os.getcwd()}/data/{self.root_name}'
        olympus.CreateIfDoesntExist(self.wd)

        self.xlpath = f'{self.usr_path}/Documents/HE60/output/HydroLight/excel/M{self.root_name}.xlsx'
        self.lrootpath = f'{self.usr_path}/Documents/HE60/output/HydroLight/digital/L{self.root_name}.txt'
        
        self.bands = self.hermes.get['bands']
        self.depths = self.hermes.get['zetanom']
        self.n_depths, = self.depths.shape
        self.Eu, self.Ed, self.Eo = None, None, None
        self.results_df = None  # Pandas dataframe to store and save results
        self.zenith_radiance = np.zeros((len(list(self.depths)) * len(list(self.bands)) * 20, 7))

    def hercule_poirot(self, sheet):
        """
        Famous Agatha Christie's detective, always there
        when you need to find where you have put that
        sneaky data point.
        :return:
        """
        df = pd.read_excel(self.xlpath, sheet, header=3)
        return df

    def get_Eudos_lambda(self):
        self.Eu = self.get_Eu(integrate=False)
        self.Ed = self.get_Ed(integrate=False)
        self.Eo = self.get_Eo(integrate=False)
        
        step = self.bands[1] - self.bands[0]
        analyzed_wavelengths = []
        for i in range(len(self.bands)-1):
            analyzed_wavelengths.append(self.bands[i]+step/2)
        result_array = np.zeros((self.n_depths+1, len(analyzed_wavelengths)*3+1))
        columns_labels = ['depths']
        result_array[1:, 0], result_array[0, 0] = self.hermes.get['zetanom'], 0.0

        for i, wavelength in enumerate(analyzed_wavelengths):
            result_array[:, 3*i+1] = self.Eu[1:, i]
            columns_labels.append(f'Eu_{wavelength}')
            result_array[:, 3*i+2] = self.Ed[1:, i]
            columns_labels.append(f'Ed_{wavelength}')
            result_array[:, 3*i+3] = self.Eo[1:, i]
            columns_labels.append(f'Eo_{wavelength}')
        self.results_df = pd.DataFrame(data=result_array, columns=columns_labels)
        self.results_df.to_csv(f'{self.wd}/eudos.csv')
        return self.results_df

    def get_Eu(self, integrate=False):
        self.Eu = self.hercule_poirot(sheet='Eu').T.to_numpy()
        if integrate:
            self.Eu = np.sum(Eu_lambda.to_numpy()[1:, ], axis=1)*self.wavelength_binwidth
        return self.Eu

    def get_Ed(self, integrate=False):
        self.Ed = self.hercule_poirot(sheet='Ed').T.to_numpy()
        if integrate:
            self.Ed = np.sum(Ed_lambda.to_numpy()[1:, ], axis=1)*self.wavelength_binwidth
        return self.Ed

    def get_Eo(self, integrate=False):
        self.Eo = self.hercule_poirot(sheet='Eo').T.to_numpy()
        if integrate:
            self.Eo = np.sum(Eo_lambda.to_numpy()[1:, ], axis=1) * self.wavelength_binwidth
        return self.Eo

    def get_zenith_profiles(self):
        full_lroot = np.loadtxt(self.lrootpath, skiprows=16, usecols=[0, 1, 2, 3, 4, 5, 6])
        depths = [-1.00] + list(self.depths)
        phi_angles = [0., 10., 20., 30., 40, 50., 60., 70., 80., 87.5,
                      92.5, 100., 110., 120., 130., 140., 150., 160., 170., 180.]
        i = 0
        for i_band, band in enumerate(bands):
            for i_depth, depth in enumerate(depths):
                depth = round(depth, 2)
                _full_radiance = full_lroot[(full_lroot[:, 0] == depth) & (full_lroot[:, 3] == band), :]
                for phi in phi_angles:
                    self.zenith_radiance[i, :] = _full_radiance[_full_radiance[:, 1] == phi, :].mean(axis=0)
                    i += 1
        del full_lroot  # Deallocate full_lroot memory
        self.zenith_radiance = self.result_zenith_profiles[:, (0, 1, 3, 4, 5, 6)]
        header, data_fmt = header_library.zenith_file()
        np.savetxt('DUMMY_RESULT.txt', self.zenith_radiance, fmt=data_fmt, header=header)




if __name__ == "__main__":
    print('\n')
    # path_to_Lroot = '/Users/braulier/Documents/HE60/output/HydroLight/digital/Lhe60_comp_dort.txt'
    bands = [480.0, 540.0, 600.0]
    # full_lroot = np.loadtxt(path_to_Lroot, skiprows=16, usecols=[0,1,2,3,4,5,6])
    depths = [-1.00] + list(np.linspace(0.0, 3.0, 301))
    # result_zenith_profiles = np.zeros((len(depths)*len(bands)*20, 7))
    phi_angles = [0., 10., 20., 30., 40, 50., 60., 70., 80., 87.5, 92.5, 100., 110., 120., 130., 140., 150., 160., 170., 180.]



    result_zenith_profile = np.loadtxt('DUMMY_RESULT.txt')
    fig, ax = plt.subplots(1,3)
    to_be_reshaped = result_zenith_profile[result_zenith_profile[:, 2] == 480.0, :]
    max = to_be_reshaped[:, 3].reshape(302, 20).max()
    print(max)
    for i, band in enumerate(bands):
        to_be_reshaped = result_zenith_profile[result_zenith_profile[:, 2] == band, :]
        total_radiance_image = to_be_reshaped[:, 3].reshape(302, 20)
        total_radiance_image[1:, :] = total_radiance_image[1:, :]/1.355**2
        ax[i].imshow(total_radiance_image[:10,:]/max, aspect='auto', norm=matplotlib.colors.LogNorm(), cmap='hot')
        # ax[i].set_xticks()
        # ax[i].set_xticklabels(phi_angles)
    plt.show()


    

