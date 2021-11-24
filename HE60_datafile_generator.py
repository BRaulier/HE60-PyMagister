import numpy as np


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


class Simulation:
    def __init__(self):
        #simbuild = EnvironmentBuilder()
        self.wavelengths = None
        self.n_wavelengths = None
        self.z_max = None
        self.delta_z = None
        self.z_grid = None
        self.z_ac_grid = None
        self.z_bb_grid = None

    def run_mobley_1998_example(self):
        """
        Four-layer model of sea ice, from Mobley et al. 1998 : MODELING LIGHT PROPAGATION IN SEA ICE
        """
        self.add_layer(z1=0.0, z2=0.1, abs=0.4, scat=250, bb=0.0109)
        self.add_layer(z1=0.1, z2=1.61, abs=0.4, scat=200, bb=0.0042)
        self.add_layer(z1=1.61, z2=1.74, abs=1.28, scat=200, bb=0.0042)
        self.add_layer(z1=1.74, z2=self.z_max+1, abs=0.5, scat=0.1, bb=0.005)

    def add_layer(self, z1, z2, abs, scat, bb):
        c = abs + scat
        self.z_ac_grid[(self.z_ac_grid[:, 0] >= z1) & (self.z_ac_grid[:, 0] < z2), 1: self.n_wavelengths] = abs
        self.z_ac_grid[(self.z_ac_grid[:, 0] >= z1) & (self.z_ac_grid[:, 0] < z2), self.n_wavelengths::] = c
        self.z_bb_grid[(self.z_bb_grid[:, 0] >= z1) & (self.z_bb_grid[:, 0] < z2), 1::] = bb

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



class EnvironmentBuilder:
    def __init__(self, sim_clss, path='ressources/'):
        self.path = path
        self.sim_clss = sim_clss

    def create_backscattering_file(self):
        header = "\\begin_header\n" \
                 "Backscattering file used to find a corresponding Fournier-Forand phase \n" \
                 "function. As described in https://www.oceanopticsbook.info/view/scattering/the-fournier-forand-phase-function\n" \
                 "Column headers (depth in m and bb in 1/m):\n" \
                 "depth {} ".format('\tbb'.join([str(int(i)) for i in self.sim_clss.wavelengths])) + "\n" \
                 "The first data record gives the number of wavelengths and the wavelengths.\n" \
                 "\\end_header\n"
        first_line = "{}\t{}\n".format(int(self.sim_clss.n_wavelengths), '\t'.join([str(i) for i in self.sim_clss.wavelengths]))
        footer = "\\end_data"
        with open('ressources/backscattering_file.txt', 'w') as file:
            file.write(header)
            file.write(first_line)
            np.savetxt(file, self.sim_clss.z_bb_grid, fmt='%1.2e', delimiter='\t')
            file.write(footer)

    def create_ac9_file(self):
        header = "\\begin_header\n" \
                 "Backscattering file used to find a corresponding Fournier-Forand phase \n" \
                 "function. As described in https://www.oceanopticsbook.info/view/scattering/the-fournier-forand-phase-function\n" \
                 "Column headers (depth in m; and and c in 1/m): \n" \
                 "depth {} {} ".format('a\t'.join([str(int(i)) for i in self.sim_clss.wavelengths]),
                                       '\tc'.join([str(int(i)) for i in self.sim_clss.wavelengths])) + "\n" \
                 "The first data record gives the number of wavelengths and the wavelengths.\n" \
                 "\\end_header\n"
        first_line = "{}\t{}\n".format(int(self.sim_clss.n_wavelengths), '\t'.join([str(i) for i in self.sim_clss.wavelengths]))
        footer = "\\end_data"
        with open('ressources/ac9_file.txt', 'w') as file:
            file.write(header)
            file.write(first_line)
            np.savetxt(file, self.sim_clss.z_ac_grid, fmt='%1.2e', delimiter='\t')
            file.write(footer)

if __name__ == "__main__":
    test_1 = Simulation()
    test_1.set_wavelengths(wvelgths=[412.0, 440.0, 488.0, 510.0, 532.0, 555.0, 650.0, 676.0, 715.0])
    test_1.set_z_grid(z_max=2.0)
    test_1.run_mobley_1998_example()
    test_build = EnvironmentBuilder(sim_clss=test_1)
    test_build.create_backscattering_file()
    test_build.create_ac9_file()


