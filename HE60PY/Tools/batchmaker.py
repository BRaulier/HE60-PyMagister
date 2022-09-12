import numpy as np
import pathlib
from .default_batch_sea_ice import SeaIceDefaultBatch
from .default_batch_lisa import LisaDefaultBatch
from .default_batch_baie_des_chaleurs import BaieDesChaleursDefaultBatch
from .default_batch_oden import OdenDefaultBatch
from .default_batch_open_water import OpenWaterDefaultBatch
from .default_batch_bicolor_ice import BicolorIceDefaultBatch
from .olympus import InvalidMode


class BatchMaker:
    def __init__(self, hermes):
        # General initialisation
        self.usr_path = pathlib.Path.home()
        self.hermes = hermes
        self.mode = hermes.get['mode']
        self.root_name = hermes.get['root_name']
        self.run_title = hermes.get['run_title']

        # Record initialisation
        self.record1_str, self.record2_str, self.record3_str, self.record4_str = None, None, None, None
        self.record5_str, self.record6_str, self.record7_str, self.record8_str = None, None, None, None
        self.record9_str, self.record10_str, self.record11_str, self.record12_str, self.record13_str = None, None, None, None, None

        self.Nwave = None
        self.meta = None

        self.set_N_band_waves()
        self.set_all_records()

    def set_N_band_waves(self, N_band=17):
        self.Nwave = N_band

    def set_all_records(self):
        if self.mode == 'sea_ice':
            default_batch = SeaIceDefaultBatch(self.hermes)
        elif self.mode == 'Oden':
            default_batch = OdenDefaultBatch(self.hermes)
        elif self.mode == 'BaieDesChaleurs':
            default_batch = BaieDesChaleursDefaultBatch(self.hermes)
        elif self.mode == 'Lisa':
            default_batch = LisaDefaultBatch(self.hermes)
        elif self.mode == 'open_water':
            default_batch = OpenWaterDefaultBatch(self.hermes)
        elif self.mode == 'bicolor_ice':
            default_batch = BicolorIceDefaultBatch(self.hermes)
        else:
            raise InvalidMode(self.mode)
        self.meta = default_batch.build_records()
        self.prepare_record_strings()

    def prepare_record_strings(self):
        self.meta['record1']['string'] = '{sOutDir}, {Parmin}, {Parmax}, {PhiChl}, {Raman0}, {RamanXS}, {iDynz}, {RamanExp}\n'.format(**self.meta['record1'])
        self.meta['record2']['string'] = '{ititle}'.format(**self.meta['record2'])
        self.meta['record3']['string'] = '{rootname}'.format(**self.meta['record3']) + '\n'
        self.meta['record4']['string'] = '{iOptPrnt}, {iOptDigital}, {iOptExcelS}, {iOptExcelM}, {iOptRad}\n' \
                                         '{iIOPmodel}, {iSkyRadmodel}, {iSkyIrradmodel}, {iIOPTS}, {iChl}, {iCDOM}\n'.format(**self.meta['record4'])
        self.meta['record5']['string'] = '{ncomp}, {nconc}\n{compconc}\n{_5c_lines}\n{abs_files}\n' \
                                         '{_5e_line1}\n{_5e_line2}\n{_5f_line1}\n{_5f_line2}\n' \
                                         '{_5g_line1}\n{_5g_line2}\n{_5h_line1}\n{_5h_line2}\n'.format(**self.meta['record5'])
        self.meta['record6']['string'] = '{Nwave}\n{bands_str}\n'.format(**self.meta['record6'])
        self.meta['record7']['string'] = '{ibiolum},{ichlfl},{icdomfl},{iraman},{icompchl}\n'.format(**self.meta['record7'])
        if self.meta['record8']['iflagsky'] == 2:
            self.meta['record8']['string'] = '{iflagsky}, {nsky}, {suntheta}, {sunphi}, {cloud}\n' \
                                             '{fjday}, {rlat}, {rlon}, {pres}, {am}, {rh}, {wv}, {vi}, {wsm}, {ro3}\n'.format(**self.meta['record8'])
        if self.meta['record8']['iflagsky'] == 1.0:
            self.meta['record8']['string'] = '{iflagsky}, {nsky}, {suntheta}, {sunphi}, {C}, {rsky}, {Edtotal}\n' \
                                             '{fjday}, {rlat}, {rlon}, {pres}, {am}, {rh}, {wv}, {vi}, {wsm}, {ro3}\n'.format(**self.meta['record8'])
        self.meta['record9']['string'] = '{windspd}, {refr}, {temp}, {salinty}, {iSurfaceModelFlag}\n'.format(**self.meta['record9'])
        self.meta['record10']['string'] = '{ibotm}, {rflbot}\n'.format(**self.meta['record10'])
        self.meta['record11']['zetanom_str'] = ','.join([str(i) for i in self.meta['record11']['zetanom']])
        self.meta['record11']['string'] = '{iop},{nznom},{zetanom_str}\n'.format(**self.meta['record11'])
        self.meta['record12']['string'] = '{PureWaterDataFile}\n{nac9Files}\n{ac9DataFile}\n{Ac9FilteredDataFile}' \
                                          '\n{HydroScatDataFile}\n{ChlzDataFile}\n{CDOMDataFile}\n{RbottomFile}\n{TxtDataFile(i)}\n' \
                                          '{IrradDataFile}\n{S0biolumFile}\n{LskyDataFile}\n'.format(**self.meta['record12'])

        self.hermes.get['bands'] = self.meta['record6']['bands']
        self.hermes.get['Nwave'] = self.meta['record6']['Nwave']
        self.hermes.get['Parmin'] = self.meta['record1']['Parmin']
        self.hermes.get['Parmax'] = self.meta['record1']['Parmax']  # TODO Hermes could save all the data from the meta
        self.hermes.get['zetanom'] = self.meta['record11']['zetanom'] # (once updated) dictionnary, would be usefull for data_managing afterwarDs

    def write_batch_file(self):
        path = f"{self.usr_path}/Documents/HE60/run/batch/"
        with open(path + self.root_name + '.txt', "w+") as file:
            file.writelines([self.meta['record{}'.format(i)]['string'] for i in range(1, 13)])

