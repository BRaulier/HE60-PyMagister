import numpy as np
import os
import shutil
import subprocess


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


class BatchMaker:
    def __init__(self, batch_name):
        self.meta = {'record1': {}, 'record2': {}, 'record3': {}, 'record4': {}, 'record5': {}, 'record6': {},
                     'record7': {}, 'record8': {}, 'record9': {}, 'record10': {}, 'record11': {}, 'record12': {}, 'record13': {}}
        self.record1_str, self.record2_str, self.record3_str, self.record4_str = None, None, None, None
        self.record5_str, self.record6_str, self.record7_str, self.record8_str = None, None, None, None
        self.record9_str, self.record10_str, self.record11_str, self.record12_str, self.record13_str = None, None, None, None, None

        self.batch_file = None
        self.run_title = None
        self.rootname = None
        self.Nwave = None
        self.batch_name = batch_name
        
    def set_title(self, title):
        self.run_title = title

    def set_rootname(self, rootname):
        self.rootname = rootname

    def set_N_band_waves(self, N_band=17):
        self.Nwave = N_band

    def set_all_records(self):
        self.set_record1()
        self.set_record2()
        self.set_record3()
        self.set_record4()
        self.set_record5()
        self.set_record6()
        self.set_record7()
        self.set_record8()
        self.set_record9()
        self.set_record10()
        self.set_record11()
        self.set_record12()

    def write_batch_file(self, path="/Users/braulier/Documents/HE60/run/batch/"):
        with open(path + self.batch_name+'.txt', "w+") as file:
            file.writelines([self.meta['record{}'.format(i)]['string'] for i in range(1, 13)])

    def set_record1(self):
        self.meta['record1']['sOutDir'] = '"/Users/braulier/Documents/HE60/output"'
        self.meta['record1']['Parmin'] = 300                            # lowest wavelength included in PAR calculations
        self.meta['record1']['Parmax'] = 700                            # highest wavelength included in PAR calculations
        self.meta['record1']['PhiChl'] = 0.02                           # chlorophyll fluorescence efficiency
        self.meta['record1']['Raman0'] = 488                            # Raman reference wavelength
        self.meta['record1']['RamanXS'] = 0.00026                       # Raman scattering coefficient at the reference wavelength
        self.meta['record1']['iDynz'] = 1                               # inelastic sources are present and an infinitely-deep bottom is selected
        self.meta['record1']['RamanExp'] = 5.5                          # wavelength dependence of the Raman scattering coefficient
                                                                        # see HydroLight Technical Note 10
        # String construction
        self.meta['record1']['string'] = '{sOutDir}, {Parmin}, {Parmax}, {PhiChl}, {Raman0}, {RamanXS}, {iDynz}, {RamanExp}\n'.format(**self.meta['record1'])

    def set_record2(self):
        self.meta['record2']['ititle'] = self.run_title + '\n'
        # String construction
        self.meta['record2']['string'] = '{ititle}'.format(**self.meta['record2'])

    def set_record3(self):
        self.meta['record3']['rootname'] = self.rootname
        # String construction
        self.meta['record3']['string'] = '{rootname}'.format(**self.meta['record3']) + '\n'

    def set_record4(self):
        # Record 4a
        self.meta['record4']['iOptPrnt'] = 0                        # -1: minimal output, 0: standard, 1: extensive
        self.meta['record4']['iOptDigital'] = 1                     # Generation of Droot.txt file, 0 or 1
        self.meta['record4']['iOptExcelS'] = 2                      # Generation of Excel single-wavelength output Sroot.txt (0 or 2)
        self.meta['record4']['iOptExcelM'] = 1                      # Generation of Excel multi-wavelength output Mroot.txt (0 or 1)
        self.meta['record4']['iOptRad'] = 1                         # Generation of the full radiance printout Lroot.txt (0 or 1)
        # Record 4b
        self.meta['record4']['iIOPmodel'] = 3                       # User data IOP model
        self.meta['record4']['iSkyRadmodel'] = 1                    # Harrison and Coombes 1998 semi-empirical model
        self.meta['record4']['iSkyIrradmodel'] = 0                  # Calls RADTRANX to obtain direct and direct irradiances
        self.meta['record4']['iIOPTS'] = 0                          # For pure water IOP's independent of temperature and salinity
        self.meta['record4']['iChl'] = 0
        self.meta['record4']['iCDOM'] = 0
        # String construction
        self.meta['record4']['string'] = '{iOptPrnt}, {iOptDigital}, {iOptExcelS}, {iOptExcelM}, {iOptRad}\n' \
                           '{iIOPmodel}, {iSkyRadmodel}, {iSkyIrradmodel}, {iIOPTS}, {iChl}, {iCDOM}\n'.format(**self.meta['record4'])

    def set_record5(self):
        # record 5a: number of components
        self.meta['record5']['ncomp'] = 2                           # Number of components
        self.meta['record5']['nconc'] = 2                           # Number of concentrations
        # record 5b: component concentrations
        self.meta['record5']['compconc'] = '0, 0'                        # Component concentrations
        # record 5c: Specific absorption parameters
        self.meta['record5']['5c_line1'] = '0, 0, 440, 1, 0.014'         # Pure water line
        self.meta['record5']['5c_line2'] = '2, -666, 440, 1, 0.014'      # Measured IOP line
        # record 5d: Specific absorption data file names
        self.meta['record5']['null_water_file'] = '../data/null_H2Oabsorps.txt'      # Null water properties
        self.meta['record5']['user_absorption_file'] = self.ac9_path  # TODO: add null water properties
        # record 5e: Specific scattering parameters
        self.meta['record5']['5e_line1'] = '0, -999, -999, -999, -999, -999'   # Pure water
        self.meta['record5']['5e_line2'] = '-666, -999, -999, -999, -999, -999'   # Measured IOP line
        # record 5f: Specific scattering data file names
        self.meta['record5']['5f_line1'] = 'dummybstar.txt'              # Dummy
        self.meta['record5']['5f_line2'] = 'dummybstar.txt'              # Dummy
        # record 5g: type of concentrations and phase functions
        self.meta['record5']['5g_line1'] = '0,0,550,0.01,0'              # Dummy values phase functions
        self.meta['record5']['5g_line2'] = '2,0,550,0.01,0'              # Dummy values phase functions
        # record 5h: discretized phase functions file names
        self.meta['record5']['5h_line1'] = 'dpf_pure_H2O.txt'               # TODO NULL
        self.meta['record5']['5h_line2'] = 'user_defined/backscattering_file.txt'   # TODO

        self.meta['record5']['string'] = '{ncomp}, {nconc}\n{compconc}\n{5c_line1}\n{5c_line2}\n{null_water_file}\n' \
                           '{user_absorption_file}\n{5e_line1}\n{5e_line2}\n{5f_line1}\n{5f_line2}\n' \
                           '{5g_line1}\n{5g_line2}\n{5h_line1}\n{5h_line2}\n'.format(**self.meta['record5'])

    def set_record6(self):
        self.meta['record6']['Nwave'] = self.Nwave - 1
        self.meta['record6']['bands'] = np.linspace(self.meta['record1']['Parmin'], self.meta['record1']['Parmax'], self.Nwave)
        self.meta['record6']['bands_str'] = ','.join([str(int(i)) for i in self.meta['record6']['bands']])
        self.meta['record6']['string'] = '{Nwave}\n{bands_str}\n'.format(**self.meta['record6'])

    def set_record7(self):
        self.meta['record7']['ibiolum'] = 0                         # 0: no bioluminescence present
        self.meta['record7']['ichlfl'] = 0                          # 0: no chlorophyll fluorescence present
        self.meta['record7']['icdomfl'] = 0                         # 0: no CDOM fluorescence present
        self.meta['record7']['iraman'] = 0                         # 0: no Raman scattering present
        self.meta['record7']['icompchl'] = 0                        # index for the chlorophyll fluorescence component
        self.meta['record7']['string'] = '{ibiolum}, {ichlfl}, {icdomfl}, {iraman}, {icompchl}\n'.format(**self.meta['record7'])

    def set_record8(self):
        # record 8a
        self.meta['record8']['iflagsky'] = 2                      # 1: idealized sky, 2 (3): semi analytic, zenith angle or (time and location)
        self.meta['record8']['suntheta'] = 45.0                   # solar zenith angle (degrees)
        self.meta['record8']['sunphi'] = 0.0                      # solar azimuthal angle in degrees relative to the wind direction.
        self.meta['record8']['nsky'] = 3                                                          # sunphi = 0.0 is downwind and sunphi = 90.0 places the Sun at a right angle to the wind.
        self.meta['record8']['cloud'] = 0.5                       # 0.0: clear sky, 1.0:solid overcast
        # record 8b     # CORRESPONDING TO THE CHOICE OF IFLAGSKY (2), must be changed if you use other sky model ( 1 or 3)
        self.meta['record8']['fjday'] = 180.0                     # Julian day (for earth-sun distance)
        self.meta['record8']['rlat'] = 76.0                       # latitude (degrees)
        self.meta['record8']['rlon'] = -83.0                     # longitude (degrees)
        self.meta['record8']['pres'] = 29.92                    # sea level pressure (inches Hg) Value from https://www.britannica.com/science/atmospheric-pressure
        self.meta['record8']['am'] = 1.0                         # marine aerosol type (1: marine, 10: continental) see Gathman, 1983
        self.meta['record8']['rh'] = 75                         # relative humidity (percents), educated guess
        self.meta['record8']['wv'] = 0.05                           # precipitable content: the amount of moisture there is above a fixed point, see https://earth.nullschool.net
        self.meta['record8']['vi'] = 15                             # average horizontal visibility (km) https://essd.copernicus.org/articles/12/805/2020/
        self.meta['record8']['wsm'] = 6.0                          # average wind speed (m/s) https://essd.copernicus.org/articles/12/805/2020/
        self.meta['record8']['ro3'] = 300                          # ozone (Dobson units) https://ozonewatch.gsfc.nasa.gov/NH.html
        self.meta['record8']['string'] = '{iflagsky}, {nsky}, {suntheta}, {sunphi}, {cloud}\n' \
                           '{fjday}, {rlat}, {rlon}, {pres}, {am}, {rh}, {wv}, {vi}, {wsm}, {ro3}\n'.format(**self.meta['record8'])

    def set_record9(self):
        self.meta['record9']['windspd'] = 15.0                      # Wind speed (m/s), value from Mobley et al. Modeling Light Propagation in Sea Ice
        self.meta['record9']['refr'] = 1.355                        # Refraction index: Maykut & Light, Refractive-index measurements in freezing sea-ice and sodium chloride brines
        self.meta['record9']['temp'] = -1.8                         # water temperature
        self.meta['record9']['salinty'] = 35.0                      # salinity (PSU)
        self.meta['record9']['iSurfaceModelFlag'] = 3               # azimuthally averaged Cox-Munk surfaces
        self.meta['record9']['string'] = '{windspd}, {refr}, {temp}, {salinty}, {iSurfaceModelFlag}\n'.format(**self.meta['record9'])

    def set_record10(self):
        self.meta['record10']['ibotm'] = 0                          # 0: infinitely deep column, 1: opaque Lambertian reflect=rflbot, 2: opaque Lambertiant, reflectance auto
        self.meta['record10']['rflbot'] = 0.2                       # Bottom reflectance, only used when ibotm=1
        self.meta['record10']['string'] = '{ibotm}, {rflbot}\n'.format(**self.meta['record10'])

    def set_record11(self):
        self.meta['record11']['iop'] = 0                        # Flag, 0, (1): indicating geometrical (optical) depths
        self.meta['record11']['nznom'] = 100                     # number of depths
        self.meta['record11']['zetanom'] = np.linspace(0, 2, self.meta['record11']['nznom']+1, dtype=np.float16)
        self.meta['record11']['zetanom_str'] = ','.join([str(i) for i in self.meta['record11']['zetanom']])
        self.meta['record11']['string'] = '{iop},{nznom},{zetanom_str}\n'.format(**self.meta['record11'])

    def set_record12(self):
        self.meta['record12']['PureWaterDataFile'] = self.meta['record5']['null_water_file']
        self.meta['record12']['nac9Files'] = 1                                       # Number of ac9 files to read
        self.meta['record12']['ac9DataFile'] = self.ac9_path
        self.meta['record12']['Ac9FilteredDataFile'] = 'dummyFilteredAc9.txt'
        self.meta['record12']['HydroScatDataFile'] = self.bb_path                       # TODO:  backscattering data
        self.meta['record12']['ChlzDataFile'] = 'dummyCHLdata.txt'                       # Standard-format chlorophyll profile
        self.meta['record12']['CDOMDataFile'] = 'dummyCDOMdata.txt'                       # file containing values of CDOM absorption at a given reference wavelength
        self.meta['record12']['RbottomFile'] = 'dummyR.bot'                       # file containing values of CDOM absorption at a given reference wavelength
        self.meta['record12']['TxtDataFile(i)'] = 'dummyComp.txt\ndummyComp.txt'  # Concentration profile data files for component i
        self.meta['record12']['IrradDataFile'] = 'dummyIrrad.txt'                       # Standard-format data file containing sea-surface total Ed (if not using RADTRAN-X model)
        self.meta['record12']['S0biolumFile'] = 'dummyBiolum.txt'                         # file containing bioluminescentsource strength (in W m-3 nm)
        self.meta['record12']['LskyDataFile'] = 'dummyLsky.txt' # file containing sky radiance data to be used instead of the RADTRAN-X and Harrison and Coombes sky models
        self.meta['record12']['string'] = '{PureWaterDataFile}\n{nac9Files}\n{ac9DataFile}\n{Ac9FilteredDataFile}' \
                        '\n{HydroScatDataFile}\n{ChlzDataFile}\n{CDOMDataFile}\n{RbottomFile}\n{TxtDataFile(i)}\n' \
                            '{IrradDataFile}\n{S0biolumFile}\n{LskyDataFile}'.format(**self.meta['record12'])


class EnvironmentBuilder:
    
    def create_simulation_environnement(self):
        self.create_backscattering_file(self.path)
        self.create_ac9_file(self.path)

    def create_run_delete_bash_file(self, print_output):
        bash_file_path = "/Applications/HE60.app/Contents/backend/run.sh"
        with open(bash_file_path, "w") as file:
            file.write("#!/bin/bash\n"
                       "./HydroLight6 < /Users/braulier/Documents/HE60/run/batch/"+self.batch_name+".txt")
        bash_command = './run.sh'
        path_to_he60 = '/Applications/HE60.app/Contents/backend'
        command_chmod = 'chmod u+x ' + bash_file_path
        chmod_process = subprocess.Popen(command_chmod.split(), stdout=subprocess.PIPE)
        chmod_process.communicate()
        HE60_process = subprocess.Popen(bash_command, stdout=subprocess.PIPE, cwd=path_to_he60, bufsize=1, universal_newlines=True)
        if print_output:
            with HE60_process as p:
                for line in p.stdout:
                    print(line, end='')
        else:
            HE60_process.communicate()
        os.remove(bash_file_path)

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


class Simulation(BatchMaker, EnvironmentBuilder):
    def __init__(self, path, batch_name):
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
        self.set_all_records()
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

    def run_built_model(self, printOutput = False):
        print('Preparing files...')
        self.write_batch_file()
        print('Creating simulation environnement...')
        self.create_simulation_environnement()
        print('Running Hydro Light simulations...')
        self.create_run_delete_bash_file(print_output=printOutput)

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
    print('\n')


