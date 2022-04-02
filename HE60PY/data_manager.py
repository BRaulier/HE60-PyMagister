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
        
        self.bands = self.hermes['bands']
        self.n_depths, = self.hermes['zetanom'].shape
        self.Eu, self.Ed, self.Eo = None, None, None
        
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
        result_array[1:, 0], result_array[0, 0] = self.hermes['zetanom'], 0.0

        for i, wavelength in enumerate(analyzed_wavelengths):
            result_array[:, 3*i+1] = self.Eu[1:, i]
            columns_labels.append(f'Eu_{wavelength}')
            result_array[:, 3*i+2] = self.Ed[1:, i]
            columns_labels.append(f'Ed_{wavelength}')
            result_array[:, 3*i+3] = self.Eo[1:, i]
            columns_labels.append(f'Eo_{wavelength}')
        result_df = pd.DataFrame(data=result_array, columns=columns_labels)
        return result_df

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


if __name__ == "__main__":
    print('\n')

