import numpy as np
import pickle


class Batch:
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

        self.set_N_band_waves()

        self.create_batch_file()

    def create_batch_file(self, path="/Users/braulier/Documents/HE60/run/batch"):
        self.batch_file = open(path + '/' + self.batch_name, "w+")

    def set_title(self, title):
        self.run_title = title

    def set_rootname(self, rootname):
        self.rootname = rootname

    def set_N_band_waves(self, N_band=15):
        self.Nwave = N_band

    def set_record1(self):
        self.meta['record1']['sOutDir'] = '/Users/braulier/Documents/HE60/output'
        self.meta['record1']['Parmin'] = 400                            # lowest wavelength included in PAR calculations
        self.meta['record1']['Parmax'] = 700                            # highest wavelength included in PAR calculations
        self.meta['record1']['PhiChl'] = 0.02                           # chlorophyll fluorescence efficiency
        self.meta['record1']['Raman0'] = 488                            # Raman reference wavelength
        self.meta['record1']['RamanXS'] = 0.00026                       # Raman scattering coefficient at the reference wavelength
        self.meta['record1']['iDynz'] = 1                               # inelastic sources are present and an infinitely-deep bottom is selected
        self.meta['record1']['RamanExp'] = 5.5                          # wavelength dependence of the Raman scattering coefficient
                                                                        # see HydroLight Technical Note 10

    def prep_record1(self):
        self.record1_str = '{sOutDir}, {Parmin}, {Parmax}, {PhiChl}, {Raman0}, {RamanXS}, {iDynz}, {RamanExp}'.format(**self.meta['record1'])

    def set_record2(self):
        self.meta['record2']['ititle'] = self.run_title

    def prep_record2(self):
        self.record2_str = '{ititle}'.format(**self.meta['record2'])

    def set_record3(self):
        self.meta['record3']['rootname'] = self.rootname

    def prep_record3(self):
        self.record3_str = '{rootname}'.format(**self.meta['record3'])

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

    def prep_record4(self):
        self.record4_str = '{iOptPrnt}, {iOptDigital}, {iOptExcelS}, {iOptExcelM}, {iOptRad}\n' \
                           '{iIOPmodel}, {iSkyRadmodel}, {iSkyIrradmodel}, {iIOPTS}, {iChl}, {iCDOM}'.format(**self.meta['record4'])

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
        self.meta['record5']['null_water_file'] = 'TODO_NULL_WATER'      # TODO: add null water properties
        self.meta['record5']['user_absorption_file'] = 'TODO_ABS_FILE'   # TODO: add null water properties
        # record 5e: Specific scattering parameters
        self.meta['record5']['5e_line1'] = '0, -999, -999, -999, -999, -999'   # Pure water
        self.meta['record5']['5e_line2'] = '-666, -999, -999, -999, -999, -999'   # Measured IOP line
        # record 5f: Specific scattering data file names
        self.meta['record5']['5f_line1'] = 'dummybstar.txt'              # Dummy
        self.meta['record5']['5f_line2'] = 'dummybstar.txt'              # Dummy
        # record 5g: type of concentrations and phase functions
        self.meta['record5']['5g_line1'] = '0,0,550,0.01,0'              # Dummy values phase functions
        self.meta['record5']['5g_line2'] = '0,0,550,0.01,0'              # Dummy values phase functions
        # record 5h
        self.meta['record5']['5h_line1'] = 'dpf_pure_H2O.txt'               # TODO NULL
        self.meta['record5']['5h_line2'] = 'dpf_Petzold_avg_particle.txt'   # TODO

    def prep_record5(self):
        self.record5_str = '{ncomp}, {nconc}\n{compconc}\n{5c_line1}\n{5c_line2}\n{null_water_file}\n' \
                           '{user_absorption_file}\n{5e_line1}\n{5e_line2}\n{5f_line1}\n{5f_line2}\n' \
                           '{5g_line1}\n{5g_line2}\n{5h_line1}\n{5h_line2}'.format(**self.meta['record5'])

    def set_record6(self):
        self.meta['record6']['Nwave'] = self.Nwave
        inc = (self.meta['record1']['Parmax'] - self.meta['record1']['Parmin'])/ self.Nwave
        print(inc)
        self.meta['record6']['bands'] = np.arange(self.meta['record1']['Parmin'], self.meta['record1']['Parmax'], self.Nwave)

    def prep_record6(self):
        self.meta['record6']['bands_str'] = ','.join([str(i) for i in self.meta['record6']['bands']])
        self.record6_str = '{Nwave}\n{bands_str}'.format(**self.meta['record6'])





if __name__ == '__main__':
    print('\n')
    test_1 = Batch(batch_name='test')
    test_1.set_record1()
    test_1.set_record4()
    test_1.prep_record4()
    print(test_1.record4_str)

    test_1.set_record5()
    test_1.prep_record5()
    print(test_1.record5_str)
    test_1.set_record6()
    test_1.prep_record6()
    print(test_1.record6_str)