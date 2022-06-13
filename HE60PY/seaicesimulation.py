import numpy as np
import pathlib
import matplotlib.pyplot as plt

from HE60PY.Tools.batchmaker import BatchMaker
from HE60PY.Tools.environmentbuilder import EnvironmentBuilder
from HE60PY.Tools.olympus import Hermes
from .dataparser import DataParser
from .dataviewer import DataViewer


class SeaIceSimulation(EnvironmentBuilder):  # Todo composition classes instead of inheritance
    def __init__(self, root_name, run_title, mode='sea_ice', **kwargs):
        # General initialisation
        self.whoamI = 'SeaIceSimulation'
        
        self.usr_path = pathlib.Path.home()
        self.path = f'{self.usr_path}/Documents/HE60/run'
        self.kwargs = kwargs

        self.root_name = root_name
        self.run_title = run_title
        self.mode = mode

        # Wavelengths initialisation
        self.initialize_wavelengths()

        # Hermes's initialisation (used to pass information all over the module)
        self.hermes = Hermes(self.root_name, self.run_title, self.mode, self.kwargs)

        self.ac9_path = self.path + '/ac9_file.txt'
        self.bb_path = '/Applications/HE60.app/Contents/data/phase_functions/HydroLight/user_defined/backscattering_file.txt'
        self.hermes.get['ac9_path'], self.hermes.get['bb_path'] = self.ac9_path, self.bb_path

        # BatchMaker  initialisation
        self.batchmaker = BatchMaker(self.hermes)

        # EnvironmentBuilder needed parameters, only needed for sea_ice mode TODO: Remove this part and activate it only for the proper mode
        self.z_max = None
        self.delta_z = None
        self.z_grid = None
        self.z_ac_grid = None
        self.z_bb_grid = None

        self.z_boundaries_dddpf = []  # Boundaries for the Discretized Depth Dependant Phase Function
        self.dpf_objects = []
        self.dpf_filenames = []  # Filenames for the Discredized Depth Dependant Phase Function

    def build_and_run_mobley_1998_example(self):
        """
        Four-layer model of sea ice, from Mobley et al. 1998 : MODELING LIGHT PROPAGATION IN SEA ICE
        """
        self.set_z_grid(z_max=2.0)
        self.add_layer(z1=0.0, z2=0.1, abs=0.4, scat=250, bb=0.0109)
        self.add_layer(z1=0.1, z2=1.61, abs=0.4, scat=200, bb=0.0042)
        self.add_layer(z1=1.61, z2=1.74, abs=1.28, scat=200, bb=0.0042)
        self.add_layer(z1=1.74, z2=self.z_max+1, abs=0.5, scat=0.1, bb=0.005)
        self.run_simulation(True)

    def run_simulation(self, printoutput=False):
        print('Preparing files...')
        self.batchmaker.write_batch_file()
        print('Creating simulation environnement...')
        self.create_simulation_environnement()
        print('Running Hydro Light simulations...')
        self.create_run_delete_bash_file(print_output=printoutput)

    def parse_results(self):
        parser = DataParser(hermes=self.hermes)
        print('Parsing Hydro Light results...')
        parser.run_data_parsing(delete_HE_outputs=True)

    def draw_figures(self, save_binaries=False, save_png=True):
        viewer = DataViewer(hermes=self.hermes)
        print('Making figures...')
        viewer.run_figure_routine(save_binaries, save_png)

    def add_layer(self, z1, z2, abs, scat, bb=0, dpf=''):
        # If dpf is a string, suppose it gives the filename of the discretized phase function
        if type(dpf) is not str:
            # If it is not a string, suppose it is a class that has the attribute "discretize_if_needed"
            dpf.discretize_if_needed()
            dpf = dpf.dpf_name + '.txt'
            self.dpf_objects.append(dpf)
        # Boundaries for the depth dependant phase function
        self.z_boundaries_dddpf.extend([z1, z2])
        self.dpf_filenames.extend([dpf, dpf])
        # If the abs parameter is a float, absorption is assumed wavelength independent (rarely the case in reality)
        if isinstance(abs, float):
            c = abs + scat
            self.z_ac_grid[(self.z_ac_grid[:, 0] >= z1) & (self.z_ac_grid[:, 0] < z2), 1: self.n_wavelengths + 1] = abs
            self.z_ac_grid[(self.z_ac_grid[:, 0] >= z1) & (self.z_ac_grid[:, 0] < z2), self.n_wavelengths+1::] = c
            self.z_bb_grid[(self.z_bb_grid[:, 0] >= z1) & (self.z_bb_grid[:, 0] < z2), 1::] = bb * scat
        # If the abs parameter is a dict, suppose the keys are the wavelengths and the value is the abs coeff [m^-1]
        elif isinstance(abs, dict):
            for wavelength in sorted(self.wavelengths):
                wavelength_key = f"{wavelength:d}"
                abs_wv = abs[wavelength_key]
                c_wv = abs_wv + scat
                indexes, = np.where(self.wavelength_header == int(wavelength))
                self.z_ac_grid[(self.z_ac_grid[:, 0] >= z1) & (self.z_ac_grid[:, 0] < z2), indexes[0]] = abs_wv
                self.z_ac_grid[(self.z_ac_grid[:, 0] >= z1) & (self.z_ac_grid[:, 0] < z2), indexes[1]] = c_wv
                self.z_bb_grid[(self.z_bb_grid[:, 0] >= z1) & (self.z_bb_grid[:, 0] < z2), 1::] = bb * scat

    def set_z_grid(self, z_max, delta_z=0.001):
        if self.wavelengths is None: # If wavelengths aren't already initialized, do it with default parameters
            wavelength_list = self.batchmaker.meta['record6']['bands']
            self.initialize_wavelengths(mode='default', wvelgths=wavelength_list)
        self.z_max = z_max
        self.delta_z = delta_z
        nz = int(z_max/delta_z)+1
        z_mesh = np.linspace(0, z_max, nz)
        self.z_ac_grid, self.z_bb_grid = np.zeros((nz, self.n_wavelengths*2 + 1)), np.zeros((nz, self.n_wavelengths + 1))
        self.z_ac_grid[:, 0], self.z_bb_grid[:, 0] = z_mesh, z_mesh

    def initialize_wavelengths(self, mode='init', wvelgths=False):
        if mode == 'init':
            if 'wavelength_list' in self.kwargs:
                self.wavelengths = np.array(sorted(self.kwargs['wavelength_list']))
                self.n_wavelengths = len(self.wavelengths)
        else:
            self.wavelengths = wvelgths
            self.n_wavelengths = len(self.wavelengths)
        if self.n_wavelengths == 1:
            half_step = 10
            bands = np.array([self.wavelengths[0]-half_step, self.wavelengths[0]+half_step])
        else:
            half_step = np.ones(self.wavelengths.shape) * (self.wavelengths[1]-self.wavelengths[0])/2
            bands = np.hstack((np.array(self.wavelengths-half_step), np.array(self.wavelengths[-1]+half_step[0])))
        self.kwargs['bands'] = bands
        self.kwargs['Nwave'] = self.n_wavelengths
        self.kwargs['bands_str'] = ','.join([str(int(i)) for i in self.kwargs['bands']])
        self.wavelength_header = np.array(np.hstack((np.array([100000]), self.wavelengths, self.wavelengths)), dtype=np.int)


if __name__ == "__main__":
    print('\n')


