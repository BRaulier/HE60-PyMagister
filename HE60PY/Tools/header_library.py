def irrad():
    header = "\\begin_header\n" \
             "HydroLight standard format for total (Ed_total) Irradiance \n" \
             "Total irradiance includes sun + sky sea level irradiance\n" \
             "wavelength    Ed_total\n" \
             "(nm)    (W/m^2 nm)\n" \
             "\\end_header\n"
    footer = "\\end_data"
    return header, footer


def null_water():
    header = "\\begin_header \n" \
             "This null pure water data file is used when simulating a non immersed in water medium using the \n" \
             "measured IOP option. This way, Hydro Light will add null IOP's when addind the water contribution to\n " \
             "the scattering and absorption. See section 2.7 of HydroLight technical documentation.\n" \
             "wavelen[nm]  aref[1/m]  PsiT[(1/m)/deg C] PsiS[(1/m)/ppt] \n" \
             "\\end_header\n"
    footer = "\\end_data"
    return header, footer


def backscattering_file(wavelengths):
    n_wavelengths = len(list(wavelengths))
    header = "\\begin_header\n" \
             "Backscattering file used to find a corresponding Fournier-Forand phase \n" \
             "function. As described in https://www.oceanopticsbook.info/view/scattering/the-fournier-forand-phase-function\n" \
             "Column headers (depth in m and bb in 1/m):\n" \
             "depth {} ".format('\tbb'.join([str(int(i)) for i in wavelengths])) + "\n" \
             "The first data record gives the number of wavelengths and the wavelengths.\n" \
             "\\end_header\n" \
            "{}\t{}\n".format(int(n_wavelengths), '\t'.join([str(i) for i in wavelengths]))
    footer = "\\end_data"
    return header, footer


def ac9_file(wavelengths):
    n_wavelengths = len(list(wavelengths))
    header = "\\begin_header\n" \
             "ac9 file used to describe the arbitrary chosen medium \n" \
             "Column headers (depth in m; and and c in 1/m): \n" \
             "depth {} {} ".format('a\t'.join([str(int(i)) for i in wavelengths]),
                                   '\tc'.join([str(int(i)) for i in wavelengths])) + "\n" \
             "The first data record gives the number of wavelengths and the wavelengths.\n" \
             "\\end_header\n" \
             "{}\t{}\n".format(int(n_wavelengths), '\t'.join([str(i) for i in wavelengths]))
    footer = "\\end_data"
    return header, footer


def zenith_file():
    header = f'\\begin_header\n Zenith viewing profiles\n theta = 0 to 90 is downwelling; theta = 90 to 180 is' \
             f' upwelling;\n (theta = 180 is nadir-viewing; theta = 0 is zenith-viewing) \n' \
             f'depth = -1.0 labels values in air (just above the sea surface)\n' \
             f'L_sky is incident sky radiance; theta = 0 to 90 deg only; in air only\n' \
             f'L_w is water-leaving radiance; theta = 90 to 180 deg only; in air only\n' \
             f'L_sr is surface-reflected radiance; theta = 90 to 180 deg only; in air only\n' \
             f'L_dir is in-water direct radiance; theta = 0 to 90 deg only; in water only\n' \
             f'L_dif is in-water diffuse radiance; theta = 0 to 180 deg; in water only\n' \
             f'   depth   theta    lambda  total radiance L_sky or L_dir   L_w or L_dif\n' \
             f'[m]    [deg]   [deg]   [nm]   [W/(m^2 sr nm)]\n' \
             f'\end_header'
    data_fmt = '%1.2f    %2.1f    %3.2f    %1.7E    %1.7E    %1.7E'
    return header, data_fmt

def surface_file():
    header = '\\begin_header' \
             'HydroLight air-water surface file for U =  0.0 m/s and refr = 1.00 ' \
             'The surface model is Cox-Munk with azimuthally dependent slope statistics of Light and Water Eq. (4.32)' \
             'The data are the discretized spectral amplitudes of Light and Water Eqs (8.50) and (8.51) in the order' \
             'that1(a,w), that2(a,w), rhat1(w,a), rhat2(w,a), that1(w,a), that2(w,a), rhat1(a,w), rhat2(a,w)' \
             'This is the order expected by the HydroLight load_surface routine.' \
             '\end_header'
    footer = '\end_data'
    return header, footer
    
    
    