import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
import os
import warnings

from .Tools import header_library
from .Tools import olympus
from .Tools.builderdata import DataBuilder


class DataParser(DataBuilder):
    def __init__(self, hermes=None, root_name=None):
        super().__init__(hermes, root_name)
        olympus.CreateIfDoesntExist(self.wd)

        self.xlpath = f'{self.usr_path}/Documents/HE60/output/HydroLight/excel/M{self.root_name}.xlsx'
        self.lrootpath = f'{self.usr_path}/Documents/HE60/output/HydroLight/digital/L{self.root_name}.txt'
        
        self.zenith_radiance = np.zeros(((len(list(self.depths))+1) * len(list(self.run_bands)) * 19, 7))

    def hercule_poirot(self, sheet):
        """
        Famous Agatha Christie's detective, always there
        when you need to find where you have put that
        sneaky data point.
        :return:
        """
        with warnings.catch_warnings(record=True):  # To avoid annoying and useless openpyxl UserWarning 
            warnings.simplefilter("always")
            df = pd.read_excel(self.xlpath, sheet, header=3, engine="openpyxl")
        return df

    def run_data_parsing(self, delete_HE_outputs=True):
        self.compute_Eudos_and_IOPs()
        self.compute_zenith_radiance()
        if delete_HE_outputs:
            # Useful to avoid filling the computer's memory
            olympus.DeleteFile(self.xlpath)
            olympus.DeleteFile(self.lrootpath)
        
    def compute_Eudos_and_IOPs(self):
        self.Eu = self.get_Eu(integrate=False)
        self.Ed = self.get_Ed(integrate=False)
        self.Eo = self.get_Eo(integrate=False)
        self.Eod = self.get_Eod(integrate=False)
        self.Eou = self.get_Eou(integrate=False)
        self.a = self.get_a()
        self.b = self.get_b()
        self.bb = self.get_bb()
        self.kd = self.get_kd()
        self.g = self.get_g()

        result_array = np.zeros((self.n_depths+1, len(self.run_bands)*9+2))
        columns_labels = ['depths']
        result_array[1:, 0], result_array[0, 0] = np.around(self.hermes.get['zetanom'],4), 0.0

        params_to_save = [self.Eu, self.Ed, self.Eo, self.Eod, self.Eou, self.a, self.b, self.bb, self.kd]
        params_tags = ['Eu', 'Ed', 'Eo', 'Eod', 'Eou', 'a', 'b', 'bb', 'Kd']

        for i, wavelength in enumerate(self.run_bands):
            for j, param in enumerate(params_to_save):
                if params_tags[j][0] == 'E':
                    k = 1
                else:
                    k = 0
                result_array[:, len(params_to_save) * i + j + 1] = param[k:, i]
                columns_labels.append(params_tags[j]+f'_{wavelength}')

        result_array[1:, len(self.run_bands)*len(params_to_save)+1] = self.g
        columns_labels.append('g')
        self.Eudos_IOPs_df = pd.DataFrame(data=result_array, columns=columns_labels)
        self.Eudos_IOPs_df.to_csv(f'{self.wd}/eudos_iops.csv')
        return self.Eudos_IOPs_df

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

    def get_Eod(self, integrate=False):
        self.Eod = self.hercule_poirot(sheet='Eod').T.to_numpy()
        if integrate:
            self.Eod = np.sum(Eo_lambda.to_numpy()[1:, ], axis=1) * self.wavelength_binwidth
        return self.Eod

    def get_Eou(self, integrate=False):
        self.Eou = self.hercule_poirot(sheet='Eou').T.to_numpy()
        if integrate:
            self.Eou = np.sum(Eo_lambda.to_numpy()[1:, ], axis=1) * self.wavelength_binwidth
        return self.Eou
    
    def get_a(self, integrate=False):
        self.a = self.hercule_poirot(sheet='a').T.to_numpy()
        if integrate:
            self.a = np.sum(Eu_lambda.to_numpy()[1:, ], axis=1)*self.wavelength_binwidth
        return self.a

    def get_b(self, integrate=False):
        self.b = self.hercule_poirot(sheet='b').T.to_numpy()
        if integrate:
            self.b = np.sum(Ed_lambda.to_numpy()[1:, ], axis=1)*self.wavelength_binwidth
        return self.b

    def get_bb(self, integrate=False):
        self.bb = self.hercule_poirot(sheet='bb').T.to_numpy()
        if integrate:
            self.bb = np.sum(Eo_lambda.to_numpy()[1:, ], axis=1) * self.wavelength_binwidth
        return self.bb

    def get_kd(self):
        self.kd = self.hercule_poirot(sheet='Kd').T.to_numpy()
        return self.kd

    def get_g(self):
        self.g = np.zeros(self.hermes.get['zetanom'].shape)
        boundaries, assym_g_list = self.hermes.get['dpf_boundaries_table']
        for i, g in enumerate(assym_g_list):
            top_boundary, bot_boundary = boundaries[2*i], boundaries[2*i+1]
            mask = (self.hermes.get['zetanom'] < bot_boundary) * (self.hermes.get['zetanom'] >= round(top_boundary,2))
            self.g[mask] = round(g, 3)
        return self.g


    def compute_zenith_radiance(self):
        full_lroot = np.loadtxt(self.lrootpath, skiprows=16, usecols=[0, 1, 2, 3, 4, 5, 6])
        depths = [-1.00] + list(self.depths)
        phi_angles = [0., 10., 20., 30., 40, 50., 60., 70., 80., 90., 100., 110., 120., 130., 140., 150., 160., 170., 180.]
        i = 0
        for band in self.run_bands:
            for depth in depths:
                depth, band = round(depth, 2), round(band, 2)  # Rounding to avoid numerical errors messing comparison
                _full_radiance = full_lroot[(full_lroot[:, 0] == depth) & (full_lroot[:, 3] == band), :]
                for phi in phi_angles:
                    if phi == 90.:
                        _875 = _full_radiance[_full_radiance[:, 1] == 87.5, :].mean(axis=0)
                        _925 = _full_radiance[_full_radiance[:, 1] == 92.5, :].mean(axis=0)
                        self.zenith_radiance[i, :] = np.mean((_875, _925), axis=0)
                    else:
                        self.zenith_radiance[i, :] = _full_radiance[_full_radiance[:, 1] == phi, :].mean(axis=0)
                    i += 1
        del full_lroot  # Deallocate full_lroot memory
        self.zenith_radiance = self.zenith_radiance[:, (0, 1, 3, 4, 5, 6)]
        header, data_fmt = header_library.zenith_file()
        np.savetxt(f'{self.wd}/zenith_profiles.txt', self.zenith_radiance, fmt=data_fmt, header=header)
        

if __name__ == "__main__":
    print('\n')
    path_to_Lroot = '/Users/braulier/Documents/HE60/output/HydroLight/digital/LTest_John.txt'
    bands = [550]
    # full_lroot = np.loadtxt(path_to_Lroot, skiprows=16, usecols=[0,1,2,3,4,5,6])
    depths = [-1.00] + list(np.linspace(0.0, 3.0, 301))
    # result_zenith_profiles = np.zeros((len(depths)*len(bands)*20, 7))
    phi_angles = [0., 10., 20., 30., 40, 50., 60., 70., 80., 90., 100., 110., 120., 130., 140., 150., 160., 170., 180.]



    result_zenith_profile = np.loadtxt('DUMMY_RESULT.txt')
    fig, ax = plt.subplots(1,3)
    to_be_reshaped = result_zenith_profile[result_zenith_profile[:, 2] == 480.0, :]
    max = to_be_reshaped[:, 3].reshape(302, 19).max()
    print(max)
    for i, band in enumerate(bands):
        to_be_reshaped = result_zenith_profile[result_zenith_profile[:, 2] == band, :]
        total_radiance_image = to_be_reshaped[:, 3].reshape(302, 20)
        total_radiance_image[1:, :] = total_radiance_image[1:, :]/1.355**2
        ax[i].imshow(total_radiance_image[:10,:]/max, aspect='auto', norm=matplotlib.colors.LogNorm(), cmap='hot')
        # ax[i].set_xticks()
        # ax[i].set_xticklabels(phi_angles)
    plt.show()


    

