import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pathlib


class DataFinder:
    def __init__(self, hermes):
        self.usr_path = pathlib.Path.home()
        self.hermes = hermes
        self.root_name = self.hermes['root_name']
        self.xlpath = f'{self.usr_path}/Documents/HE60/output/HydroLight/excel/M{self.root_name}.xlsx'

        self.data = None
        self.broad_band_Kdz_df = None
        self.transmittance = None
        self.reflectance = None

    def hercule_poirot(self, sheet):
        """
        Famous Agatha Christie's detective, always there
        when you need to find where you have put that
        sneaky data point.
        :return:
        """
        df = pd.read_excel(self.xlpath, sheet, header=3)
        return df

    def get_broadband_Kdz(self):
        self.broad_band_Kdz_df = self.hercule_poirot(sheet='KPAR')

    def get_broadband_transmittance(self):
        if self.broad_band_Kdz_df is None:
            self.get_broadband_Kdz()
        depths = np.array(self.broad_band_Kdz_df['depth'])
        Kdz = np.array(self.broad_band_Kdz_df['K_d (broadband)'])
        depths[1:] -= depths[:-1].copy()
        self.transmittance = np.cumprod(np.exp(-depths*Kdz))
        self.broad_band_Kdz_df['Transmittance'] = self.transmittance

    def get_reflectance_and_transmittance(self):
        self.wavelength_binwidth = self.hermes['bands'][1] - self.hermes['bands'][0]
        self.Eu = self.get_Eu()
        self.Ed = self.get_Ed()
        self.Eo = self.get_Eo()
        self.transmittance = self.Ed[1:]/self.Ed[1]
        self.reflectance = self.Eu[1:]/self.Ed[1:]  # In the water
        self.albedo = self.Eu[0]/self.Ed[0]*np.ones(self.Eu[1:].shape)  # In the air

        result_array = np.zeros((100, 7))
        result_array[:,0], result_array[:,1] = self.hermes['zetanom'], self.albedo
        result_array[:,2], result_array[:,3] = self.transmittance, self.reflectance
        result_array[:, 4], result_array[:, 5], result_array[:, 6] = self.Ed[1:], self.Eu[1:], self.Eo[1:]
        result_df = pd.DataFrame(data=result_array, columns=['depths', 'albedo', 'transmittance', 'reflectance', 'Ed', 'Eu', 'Eo'])
        return result_df

    def get_Eu(self):
        Eu_lambda = self.hercule_poirot(sheet='Eu').T
        Eu = np.sum(Eu_lambda.to_numpy()[1:, ], axis=1)*self.wavelength_binwidth
        return Eu

    def get_Ed(self):
        Ed_lambda = self.hercule_poirot(sheet='Ed').T
        Ed = np.sum(Ed_lambda.to_numpy()[1:, ], axis=1)*self.wavelength_binwidth
        return Ed

    def get_Eo(self):
        Eo_lambda = self.hercule_poirot(sheet='Ed').T
        Eo = np.sum(Eo_lambda.to_numpy()[1:, ], axis=1) * self.wavelength_binwidth
        return Eo


if __name__ == "__main__":
    print('\n')

