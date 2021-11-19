import numpy as np
import pickle


class Batch:
    def __init__(self, batch_name):
        self.meta = {'record1': {}, 'record2' : {}, 'record3': {}, 'record4': {}, 'record5': {}, 'record6': {},
                     'record7': {}, 'record8': {}, 'record9': {}, 'record10': {}, 'record11': {}, 'record12': {}, 'record13': {}}
        self.record1_str, self.record2_str, self.record3_str, self.record4_str = None, None, None, None
        self.record5_str, self.record6_str, self.record7_str, self.record8_str = None, None, None, None
        self.record9_str, self.record10_str, self.record11_str, self.record12_str, self.record13_str = None, None, None, None, None


        self.batch_file = None
        self.run_title = None
        self.batch_name = batch_name

        self.create_batch_file()

    def create_batch_file(self, path="/Users/braulier/Documents/HE60/run/batch"):
        self.batch_file = open(path + '/' + self.batch_name, "w+")

    def set_title(self, title):
        self.run_title = title

    def set_record1(self):
        self.meta['record1']['sOutDir'] = '/Users/braulier/Documents/HE60/output'
        self.meta['record1']['Parmin'] = 400                            # lowest wavelength included in PAR calculations
        self.meta['record1']['Parmax'] = 700                            # highest wavelength included in PAR calculations
        self.meta['record1']['PhiChl'] = 0.02                           # chlorophyll fluorescence efficiency
        self.meta['record1']['Raman0'] = 488                            # Raman reference wavelength
        self.meta['record1']['RamanXS'] = 0.00026                       # Raman scattering coefficient at the reference wavelength
        self.meta['record1']['iDynz'] = 1                               # inelastic sources are present and an infintely-deep bottom is selected
        self.meta['record1']['RamanExp'] = 5.5                          # wavelength dependence of the Raman scattering coefficient
                                                                        # see HydroLight Technical Note 10

    def prep_record1(self):
        self.record1_str = '{sOutDir}, {Parmin}, {Parmax}, {PhiChl}, {Raman0}, {RamanXS}, {iDynz}, {RamanExp}'.format(**self.meta['record1'])

    def set_record2(self):
        self.meta['record2']['ititle'] = self.run_title

    def prep_record2(self):
        self.record2_str = '{ititle}'.format(**self.meta['record2'])

    def set_record3(self):
        self.meta['']






if __name__ == '__main__':
    print('\n')
