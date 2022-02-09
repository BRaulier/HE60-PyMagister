import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


class DataFinder:
    def __init__(self, batch_name):
        self.data = None
        self.batch_name = batch_name

        self.broad_band_Kdz_df = None
        self.transmittance = None

    def hercule_poirot(self, xl_path, sheet):
        """
        Famous Agatha Christie's detective, always there
        when you need to find where you have put that
        sneaky data point.
        :return:
        """
        df = pd.read_excel(xl_path, sheet, header=3)
        return df

    def get_broadband_Kdz(self):
        path = '/Users/braulier/Documents/HE60/output/HydroLight/excel/M' + self.batch_name + '.xlsx'
        self.broad_band_Kdz_df = self.hercule_poirot(xl_path=path, sheet='KPAR')

    def get_broadband_transmittance(self):
        if self.broad_band_Kdz_df is None:
            self.get_broadband_Kdz()
        depths = np.array(self.broad_band_Kdz_df['depth'])
        Kdz = np.array(self.broad_band_Kdz_df['K_d (broadband)'])
        depths[1:] -= depths[:-1].copy()
        self.transmittance = np.cumprod(np.exp(-depths*Kdz))
        self.broad_band_Kdz_df['Transmittance'] = self.transmittance


if __name__ == "__main__":
    ssl_list = np.linspace(0.01, 0.20, 20)
    fig, axes = plt.subplots(1, 2)
    for ssl_thickness in ssl_list:
        ssl_thickness = round(ssl_thickness, 2)
        example = DataFinder(batch_name='BL_ssl_{}'.format(str(ssl_thickness).replace('.', '_')))
        example.get_broadband_transmittance()
        kd_df = example.broad_band_Kdz_df
        axes[0].plot(kd_df['depth'], kd_df['K_d (broadband)'])
        axes[1].scatter([ssl_thickness], [example.transmittance])
    axes[1].set_ylabel('Transmittance')
    axes[1].set_xlabel('SSL thickness    [m]')
    axes[1].set_xlim([0, 0.25])
    axes[0].set_xlim([0, 1.25])
    axes[0].gca().invert_yaxis()
    plt.show()

