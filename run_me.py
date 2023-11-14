import matplotlib.pyplot as plt
from HE60PY.ac9simulation import AC9Simulation
from HE60PY.seaicesimulation import SeaIceSimulation
from HE60PY.dataparser import DataParser
from HE60PY.dataviewer import DataViewer
from HE60PY.phasefunctions import *


if __name__ == "__main__":
    # path_to_user_files = r'/Users/braulier/self.hermes./HE60/run'
    # mobley_sim = AC9Simulation(path=path_to_user_files, run_title='test', root_name='Mobley_1998_example', mode='sea_ice')
    # mobley_sim.build_and_run_mobley_1998_example()
    # mobley_results = DataFinder(mobley_sim.hermes)
    # results = mobley_results.get_Eudos_lambda()
    # results.to_csv('TEMPORARY_example_results.txt')
    #
    simple_example_SeaIce = SeaIceSimulation(mode='bare_ice', run_title='test', root_name='simple_built_example', wavelength_list=[500], ice_thickness = 1.05-0.10, snow_thickness=0.10)
    simple_example_SeaIce.set_z_grid(z_max=2.0)
    simple_example_SeaIce.add_layer(z1=0.0, z2=0.10, abs="pure_sea_ice", scat=500, dpf='dpf_OTHG_0_90.txt')
    simple_example_SeaIce.add_layer(z1=0.10, z2=1.00, abs="pure_sea_ice", scat=50, dpf='dpf_OTHG_0_90.txt')
    simple_example_SeaIce.add_layer(z1=1.00, z2=1.05, abs="pure_sea_ice", scat=50, dpf='dpf_OTHG_0_90.txt')
    simple_example_SeaIce.add_layer(z1=1.05, z2=2.01, abs="pure_sea_ice", scat=0.1, dpf='dpf_OTHG_0_90.txt')
    simple_example_SeaIce.run_simulation(printoutput=True)
    simple_example_SeaIce.parse_results()
    simple_example_SeaIce.draw_figures()

    # open_water_example = AC9Simulation(run_title='test_open', root_name='test_open', mode='open_water')
    # open_water_example.set_z_grid(z_max=3.00)
    # open_water_example.add_layer(z1=0.0, z2=3.01, abs=0.1, scat=1, bb=0.50)
    # open_water_example.run_simulation(printoutput=True)
    # open_water_example.parse_results()
    #
    # new_mode_analyze = DataViewer(root_name='test_open')
    # fig, ax =  new_mode_analyze.draw_zenith_radiance_profiles(requested_depths=[2.00, 3.00], interpolate=False)
    # new_mode_analyze.draw_stepped_zenith_radiance_profiles(requested_depths=[ 2.00, 3.00], fig=fig, ax=ax)
    # plt.show()

    # new_mode = SeaIceSimulation(run_title='test', root_name='test', mode='Oden', wavelength_list=[480])
    # wv1, warren1 = new_mode.load_warren_pure_ice_absorption_look_up_table()
    # wv2, perovich1 = new_mode.load_perovich_ice_absorption_look_up_table()
    # plt.plot(wv1[90:], warren1[90:], label="warren")
    # plt.semilogy(wv2, perovich1, label="perovich")
    # plt.legend()
    # plt.show()
    # new_mode.set_z_grid(z_max=3.00)
    # new_mode.add_layer(z1=0.0, z2=0.20, abs={'540': 0.0683, '600': 0.01, '480': 0.01}, scat=100, dpf=OTHG(0.99))  # 2277 # bb arg is not relevent since we use a discretized phase function in a file indepêdnant of depth (g=0.98)
    # new_mode.add_layer(z1=0.20, z2=0.80, abs={'540': 0.0683, '480': 0.01,  '600': 0.12}, scat=100, dpf='dpf_OTHG_0_99.txt')  # 303
    # new_mode.add_layer(z1=0.80, z2=2.00, abs={'540': 0.0683, '480': 0.01,  '600': 0.12}, scat=100, dpf='dpf_OTHG_0_99.txt')  # 79
    # new_mode.add_layer(z1=2.0, z2=3.01, abs={'480': 0.01, '540': 500, '600': 2.224e-1}, scat=100, dpf='dpf_OTHG_0_99.txt')
    # new_mode.run_simulation(printoutput=True)
    # new_mode.parse_results()
    # # new_mode.draw_figures()
    # new_mode_analyze = DataViewer(root_name='test')
    # fig, ax = new_mode_analyze.draw_Eudos_profiles()
    # plt.show()
    # fi
    #
    # g, ax =  new_mode_analyze.draw_zenith_radiance_profiles(requested_depths=[0.20, 0.40, 0.60, 0.80, 1.00], interpolate=False)
    # new_mode_analyze.draw_stepped_zenith_radiance_profiles(requested_depths=[0.20, 0.40, 0.60, 0.80, 1.00], fig=fig, ax=ax)
    # plt.show()


    # for station_file_name in station_file_names:
    #     for input_file in input_files:
    lisa_sim = AC9Simulation(path=path_to_user_files,
                             mode='Lisa',
                             root_name='RG100od_C10',
                             run_title='Chl a profiles based on real data: b - baseline, 10 - 10% to 100 - 100% ',
                             station_filename='RG100od',
                             ac9_filename='aActot_homChl10.txt',
                             chlaz_filename='Chlaz_homChl10.txt')
    lisa_sim.run_simulation(printoutput=True)
    #         lisa_sim.run_simulation(printoutput=True)
