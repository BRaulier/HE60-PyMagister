import numpy as np
import os
import shutil


def create_null_pure_water():
    H2O_default_data = np.genfromtxt('ressources/H2OabsorpTS.txt', skip_header=16, skip_footer=1)
    H2O_NULL_WATER_PROP = np.array(H2O_default_data, dtype=np.float16)
    H2O_NULL_WATER_PROP[:, 1], H2O_NULL_WATER_PROP[:, 2], H2O_NULL_WATER_PROP[:, 3] = 0.0, 0.0, 0.0
    header = "\\begin_header \n" \
             "This null pure water data file is used when simulating a non immersed in water medium using the \n" \
             "measured IOP option. This way, Hydro Light will add null IOP's when addind the water contribution to\n " \
             "the scattering and absorption. See section 2.7 of HydroLight technical documentation.\n" \
             "wavelen[nm]  aref[1/m]  PsiT[(1/m)/deg C] PsiS[(1/m)/ppt] \n" \
             "\\end_header\n"
    footer = "\\end_data"
    with open('ressources/null_H2Oabsorps.txt', 'w') as file:
        file.write(header)
        np.savetxt(file, H2O_NULL_WATER_PROP, fmt='%1.2e', delimiter='\t')
        file.write(footer)


class EnvironmentBuilder:

    def create_simulation_environnement(self, path):
        self.create_backscattering_file(path)
        self.create_ac9_file(path)

    def create_backscattering_file(self, path):
        header = "\\begin_header\n" \
                 "Backscattering file used to find a corresponding Fournier-Forand phase \n" \
                 "function. As described in https://www.oceanopticsbook.info/view/scattering/the-fournier-forand-phase-function\n" \
                 "Column headers (depth in m and bb in 1/m):\n" \
                 "depth {} ".format('\tbb'.join([str(int(i)) for i in self.wavelengths])) + "\n" \
                 "The first data record gives the number of wavelengths and the wavelengths.\n" \
                 "\\end_header\n"
        first_line = "{}\t{}\n".format(int(self.n_wavelengths), '\t'.join([str(i) for i in self.wavelengths]))
        footer = "\\end_data"
        with open(path+'/backscattering_file.txt', 'w') as file:
            file.write(header)
            file.write(first_line)
            np.savetxt(file, self.z_bb_grid, fmt='%1.2e', delimiter='\t')
            file.write(footer)
        shutil.copy(src=path+'/backscattering_file.txt', dst=r'/Applications/HE60.app/Contents/data/phase_functions/HydroLight/user_defined/backscattering_file.txt')

    def create_ac9_file(self, path):
        header = "\\begin_header\n" \
                 "ac9 file used to describe the arbitrary chosen medium \n" \
                 "Column headers (depth in m; and and c in 1/m): \n" \
                 "depth {} {} ".format('a\t'.join([str(int(i)) for i in self.wavelengths]),
                                       '\tc'.join([str(int(i)) for i in self.wavelengths])) + "\n" \
                 "The first data record gives the number of wavelengths and the wavelengths.\n" \
                 "\\end_header\n"
        first_line = "{}\t{}\n".format(int(self.n_wavelengths), '\t'.join([str(i) for i in self.wavelengths]))
        footer = "\\end_data"
        with open(path+'/ac9_file.txt', 'w') as file:
            file.write(header)
            file.write(first_line)
            np.savetxt(file, self.z_ac_grid, fmt='%1.2e', delimiter='\t')
            file.write(footer)


class Simulation(EnvironmentBuilder):
    def __init__(self, path):
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

    def build_mobley_1998_example(self):
        """
        Four-layer model of sea ice, from Mobley et al. 1998 : MODELING LIGHT PROPAGATION IN SEA ICE
        """
        self.set_wavelengths(wvelgths=[412.0, 440.0, 488.0, 510.0, 532.0, 555.0, 650.0, 676.0, 715.0])
        self.set_z_grid(z_max=2.0)
        self.add_layer(z1=0.0, z2=0.1, abs=0.4, scat=250, bb=0.0109)
        self.add_layer(z1=0.1, z2=1.61, abs=0.4, scat=200, bb=0.0042)
        self.add_layer(z1=1.61, z2=1.74, abs=1.28, scat=200, bb=0.0042)
        self.add_layer(z1=1.74, z2=self.z_max+1, abs=0.5, scat=0.1, bb=0.005)
        self.create_simulation_environnement(path=self.path)

    def add_layer(self, z1, z2, abs, scat, bb):
        c = abs + scat
        self.z_ac_grid[(self.z_ac_grid[:, 0] >= z1) & (self.z_ac_grid[:, 0] < z2), 1: self.n_wavelengths] = abs
        self.z_ac_grid[(self.z_ac_grid[:, 0] >= z1) & (self.z_ac_grid[:, 0] < z2), self.n_wavelengths::] = c
        self.z_bb_grid[(self.z_bb_grid[:, 0] >= z1) & (self.z_bb_grid[:, 0] < z2), 1::] = bb * scat 

    def set_z_grid(self, z_max, delta_z=0.01):
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
    test_1 = Simulation(path='ressources/')
    test_1.set_wavelengths(wvelgths=[412.0, 440.0, 488.0, 510.0, 532.0, 555.0, 650.0, 676.0, 715.0])
    test_1.set_z_grid(z_max=2.0)
    test_1.build_mobley_1998_example()


