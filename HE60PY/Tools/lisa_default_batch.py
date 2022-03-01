from batchmaker import BatchMaker


class LisaDefaultBatch(BatchMaker):
    def __init__(self):

    def set_record1(self):
        self.meta['record1']['sOutDir'] = '"/Users/lisamatthes/Documents/HE60/output"'
        self.meta['record1']['Parmin'] = 400  # lowest wavelength included in PAR calculations
        self.meta['record1']['Parmax'] = 700  # highest wavelength included in PAR calculations
        self.meta['record1']['PhiChl'] = 0.02  # chlorophyll fluorescence efficiency
        self.meta['record1']['Raman0'] = 488  # Raman reference wavelength
        self.meta['record1']['RamanXS'] = 0.00026  # Raman scattering coefficient at the reference wavelength
        self.meta['record1']['iDyna'] = 1  # inelastic sources are present and an infinitely-deep bottom is selected
        self.meta['record1']['RamanExp'] = 5.3  # wavelength dependence of the Raman scattering coefficient
        # see HydroLight Technical Note 10

    def set_record2(self):
        self.meta['record2']['ititle'] = self.run_title + '\n'

    def set_record3(self):
        self.meta['record3']['rootname'] = self.rootname

    def set_record4(self):
        # Record 4a
        self.meta['record4']['iOptPrnt'] = 0  # -1: minimal output, 0: standard, 1: extensive
        self.meta['record4']['iOptDigital'] = 0  # Generation of Droot.txt file, 0 or 1
        self.meta['record4']['iOptExcelS'] = 2  # Generation of Excel single-wavelength output Sroot.txt (0 or 2)
        self.meta['record4']['iOptExcelM'] = 1  # Generation of Excel multi-wavelength output Mroot.txt (0 or 1)
        self.meta['record4']['iOptRad'] = 0  # Generation of the full radiance printout Lroot.txt (0 or 1)
        # Record 4b
        self.meta['record4']['iIOPmodel'] = 3  # User data IOP model
        self.meta['record4']['iSkyRadmodel'] = 1  # Harrison and Coombes 1998 semi-empirical model
        self.meta['record4']['iSkyIrradmodel'] = 1  # Calls RADTRANX to obtain direct and direct irradiances
        self.meta['record4']['iIOPTS'] = 4  # For pure water IOP's independent of temperature and salinity
        self.meta['record4']['iChl'] = 0
        self.meta['record4']['iCDOM'] = 1

    def set_record5(self):
        # record 5a: number of components
        self.meta['record5']['ncomp'] = 2  # Number of components
        self.meta['record5']['nconc'] = 4  # Number of concentrations
        # record 5b: component concentrations
        self.meta['record5']['compconc'] = '0, 0, 0, 0'  # Component concentrations
        # record 5c: Specific absorption parameters
        self.meta['record5']['5c_line1'] = '0, 0, 440, 1, 0.014'  # Pure water line
        self.meta['record5']['5c_line2'] = '2, -666, 440, 1, 0.014'  # Measured IOP line
        # record 5d: Specific absorption data file names
        self.meta['record5']['abs_files'] = '../data/H2OabsorpTS.txt\n' \
                                            '../data/defaults/astarpchl.txt\n' \
                                            'astarDummy.txt\n' \
                                            '/Users/lisamatthes/Documents/HE60/data/examples/astarchl.txt'# Water properties
        # record 5e: Specific scattering parameters
        self.meta['record5']['5e_line1'] = '0, -999, -999, -999, -999, -999'  # Pure water
        self.meta['record5']['5e_line2'] = '-666, -999, -999, -999, -999, -999'  # Measured IOP line
        # record 5f: Specific scattering data file names
        self.meta['record5']['5f_line1'] = 'dummybstar.txt'  # Dummy
        self.meta['record5']['5f_line2'] = 'dummybstar.txt'  # Dummy
        # record 5g: type of concentrations and phase functions
        self.meta['record5']['5g_line1'] = '0,0,550,0.01,0'  # Dummy values phase functions
        self.meta['record5']['5g_line2'] = '2,0,550,0.01,0'  # Dummy values phase functions
        # record 5h: discretized phase functions file names
        self.meta['record5']['5h_line1'] = 'dpf_pure_H2O.txt'  # TODO NULL
        self.meta['record5']['5h_line2'] = 'user_defined/backscattering_file.txt'  # TODO

    def set_record6(self):
        self.meta['record6']['Nwave'] = self.Nwave - 1
        self.meta['record6']['bands'] = np.linspace(self.meta['record1']['Parmin'], self.meta['record1']['Parmax'],
                                                    self.Nwave)
        self.meta['record6']['bands_str'] = ','.join([str(int(i)) for i in self.meta['record6']['bands']])

    def set_record7(self):
        self.meta['record7']['ibiolum'] = 0  # 0: no bioluminescence present
        self.meta['record7']['ichlfl'] = 0  # 0: no chlorophyll fluorescence present
        self.meta['record7']['icdomfl'] = 0  # 0: no CDOM fluorescence present
        self.meta['record7']['iraman'] = 0  # 0: no Raman scattering present
        self.meta['record7']['icompchl'] = 0  # index for the chlorophyll fluorescence component

    def set_record8(self):
        # record 8a
        self.meta['record8'][
            'iflagsky'] = 2  # 1: idealized sky, 2 (3): semi analytic, zenith angle or (time and location)
        self.meta['record8']['suntheta'] = 45.0  # solar zenith angle (degrees)
        self.meta['record8']['sunphi'] = 0.0  # solar azimuthal angle in degrees relative to the wind direction.
        self.meta['record8'][
            'nsky'] = 3  # sunphi = 0.0 is downwind and sunphi = 90.0 places the Sun at a right angle to the wind.
        self.meta['record8']['cloud'] = 0.5  # 0.0: clear sky, 1.0:solid overcast
        # record 8b     # CORRESPONDING TO THE CHOICE OF IFLAGSKY (2), must be changed if you use other sky model ( 1 or 3)
        self.meta['record8']['fjday'] = 180.0  # Julian day (for earth-sun distance)
        self.meta['record8']['rlat'] = 76.0  # latitude (degrees)
        self.meta['record8']['rlon'] = -83.0  # longitude (degrees)
        self.meta['record8'][
            'pres'] = 29.92  # sea level pressure (inches Hg) Value from https://www.britannica.com/science/atmospheric-pressure
        self.meta['record8']['am'] = 1.0  # marine aerosol type (1: marine, 10: continental) see Gathman, 1983
        self.meta['record8']['rh'] = 75  # relative humidity (percents), educated guess
        self.meta['record8'][
            'wv'] = 0.05  # precipitable content: the amount of moisture there is above a fixed point, see https://earth.nullschool.net
        self.meta['record8'][
            'vi'] = 15  # average horizontal visibility (km) https://essd.copernicus.org/articles/12/805/2020/
        self.meta['record8']['wsm'] = 6.0  # average wind speed (m/s) https://essd.copernicus.org/articles/12/805/2020/
        self.meta['record8']['ro3'] = 300  # ozone (Dobson units) https://ozonewatch.gsfc.nasa.gov/NH.html

    def set_record9(self):
        self.meta['record9'][
            'windspd'] = 15.0  # Wind speed (m/s), value from Mobley et al. Modeling Light Propagation in Sea Ice
        self.meta['record9'][
            'refr'] = 1.355  # Refraction index: Maykut & Light, Refractive-index measurements in freezing sea-ice and sodium chloride brines
        self.meta['record9']['temp'] = -1.8  # water temperature
        self.meta['record9']['salinty'] = 35.0  # salinity (PSU)
        self.meta['record9']['iSurfaceModelFlag'] = 3  # azimuthally averaged Cox-Munk surfaces

    def set_record10(self):
        self.meta['record10'][
            'ibotm'] = 0  # 0: infinitely deep column, 1: opaque Lambertian reflect=rflbot, 2: opaque Lambertiant, reflectance auto
        self.meta['record10']['rflbot'] = 0.2  # Bottom reflectance, only used when ibotm=1

    def set_record11(self):
        self.meta['record11']['iop'] = 0  # Flag, 0, (1): indicating geometrical (optical) depths
        self.meta['record11']['nznom'] = 100  # number of depths
        self.meta['record11']['zetanom'] = np.array(list(np.linspace(0, 0.97, 98, dtype=np.float16)) + [1.90, 2.00])

    def set_record12(self):
        self.meta['record12']['PureWaterDataFile'] = self.meta['record5']['null_water_file']
        self.meta['record12']['nac9Files'] = 1  # Number of ac9 files to read
        self.meta['record12']['ac9DataFile'] = self.ac9_path
        self.meta['record12']['Ac9FilteredDataFile'] = 'dummyFilteredAc9.txt'
        self.meta['record12']['HydroScatDataFile'] = self.bb_path  # TODO:  backscattering data
        self.meta['record12']['ChlzDataFile'] = 'dummyCHLdata.txt'  # Standard-format chlorophyll profile
        self.meta['record12'][
            'CDOMDataFile'] = 'dummyCDOMdata.txt'  # file containing values of CDOM absorption at a given reference wavelength
        self.meta['record12'][
            'RbottomFile'] = 'dummyR.bot'  # file containing values of CDOM absorption at a given reference wavelength
        self.meta['record12'][
            'TxtDataFile(i)'] = 'dummyComp.txt\ndummyComp.txt'  # Concentration profile data files for component i
        self.meta['record12'][
            'IrradDataFile'] = 'dummyIrrad.txt'  # Standard-format data file containing sea-surface total Ed (if not using RADTRAN-X model)
        self.meta['record12'][
            'S0biolumFile'] = 'dummyBiolum.txt'  # file containing bioluminescentsource strength (in W m-3 nm)
        self.meta['record12'][
            'LskyDataFile'] = 'dummyLsky.txt'  # file containing sky radiance data to be used instead of the RADTRAN-X and Harrison and Coombes sky models
