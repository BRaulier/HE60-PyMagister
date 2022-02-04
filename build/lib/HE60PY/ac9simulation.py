import numpy as np
import matplotlib.pyplot as plt
from HE60PY.Tools.batchmaker import BatchMaker
from HE60PY.Tools.environmentbuilder import EnvironmentBuilder


class AC9Simulation(BatchMaker, EnvironmentBuilder):  # Todo composition classes instead of inheritance
    def __init__(self, path, batch_name, non_default_dict=None):
        super().__init__(batch_name)
        self.wavelengths = None
        self.n_wavelengths = None
        self.z_max = None
        self.delta_z = None
        self.z_grid = None
        self.z_ac_grid = None
        self.z_bb_grid = None
        self.path = path

        self.ac9_path = self.path + '/ac9_file.txt'
        self.bb_path = '/Applications/HE60.app/Contents/data/phase_functions/HydroLight/user_defined/backscattering_file.txt'
        
        self.set_N_band_waves()
        self.set_title(self.batch_name)
        self.set_rootname(self.batch_name)
        self.set_all_records(non_default_dict=non_default_dict)
        self.set_wavelengths(wvelgths=self.meta['record6']['bands'])

    def build_and_run_mobley_1998_example(self):
        """
        Four-layer model of sea ice, from Mobley et al. 1998 : MODELING LIGHT PROPAGATION IN SEA ICE
        """
        self.set_z_grid(z_max=2.0)
        self.add_layer(z1=0.0, z2=0.1, abs=0.4, scat=250, bb=0.0109)
        self.add_layer(z1=0.1, z2=1.61, abs=0.4, scat=200, bb=0.0042)
        self.add_layer(z1=1.61, z2=1.74, abs=1.28, scat=200, bb=0.0042)
        self.add_layer(z1=1.74, z2=self.z_max+1, abs=0.5, scat=0.1, bb=0.005)
        self.run_built_model()

    def run_built_model(self, printoutput=False):
        print('Preparing files...')
        self.write_batch_file()
        print('Creating simulation environnement...')
        self.create_simulation_environnement()
        print('Running Hydro Light simulations...')
        self.create_run_delete_bash_file(print_output=printoutput)

    def add_layer(self, z1, z2, abs, scat, bb):
        c = abs + scat
        self.z_ac_grid[(self.z_ac_grid[:, 0] >= z1) & (self.z_ac_grid[:, 0] < z2), 1: self.n_wavelengths + 1] = abs
        self.z_ac_grid[(self.z_ac_grid[:, 0] >= z1) & (self.z_ac_grid[:, 0] < z2), self.n_wavelengths+1::] = c
        self.z_bb_grid[(self.z_bb_grid[:, 0] >= z1) & (self.z_bb_grid[:, 0] < z2), 1::] = bb * scat

    def set_z_grid(self, z_max, delta_z=0.001):
        self.z_max = z_max
        self.delta_z = delta_z
        nz = int(z_max/delta_z)+1
        z_mesh = np.linspace(0, z_max, nz)
        self.z_ac_grid, self.z_bb_grid = np.zeros((nz, self.n_wavelengths*2 + 1)), np.zeros((nz, self.n_wavelengths + 1))
        self.z_ac_grid[:, 0], self.z_bb_grid[:, 0] = z_mesh, z_mesh

    def set_wavelengths(self, wvelgths):
        self.n_wavelengths = len(wvelgths)
        self.wavelengths = np.array(wvelgths)


if __name__ == "__main__":
    print('\n')
    plt.scatter()


