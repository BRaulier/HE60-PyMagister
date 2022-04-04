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
    
    
    