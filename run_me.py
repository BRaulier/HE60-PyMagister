from HE60PY.ac9simulation import AC9Simulation
from HE60PY.seaicesimulation import SeaIceSimulation
from HE60PY.dataparser import DataParser
from HE60PY.dataviewer import DataViewer

if __name__ == "__main__":
    path_to_user_files = r'/Users/braulier/Documents/HE60/run'
    #
    # mobley_sim = AC9Simulation(path=path_to_user_files, run_title='test', root_name='Mobley_1998_example', mode='sea_ice')
    # mobley_sim.build_and_run_mobley_1998_example()
    # mobley_results = DataFinder(mobley_sim.hermes)
    # results = mobley_results.get_Eudos_lambda()
    # results.to_csv('TEMPORARY_example_results.txt')

    simple_example_SeaIce =SeaIceSimulation(mode='HE60DORT', run_title='test', root_name='simple_built_example')
    simple_example_SeaIce.set_z_grid(z_max=2.0)
    simple_example_SeaIce.add_layer(z1=0.0, z2=0.10, abs=0.5, scat=100, dpf='dpf_OTHG_0_98.txt')
    simple_example_SeaIce.add_layer(z1=0.10, z2=0.5, abs=0.5, scat=100, dpf='dpf_OTHG_0_98.txt')
    simple_example_SeaIce.add_layer(z1=0.5, z2=2.01, abs=0.4, scat=200, dpf='dpf_OTHG_0_98.txt')
    simple_example_SeaIce.run_simulation(printoutput=True)

    new_mode = SeaIceSimulation(run_title='test', root_name='test', mode='HE60DORT', windspd=0.0)
    new_mode.set_z_grid(z_max=3.00, wavelength_list=[484, 544, 602])
    new_mode.add_layer(z1=0.0, z2=0.20, abs={'484': 0.0430, '544': 0.0683, '602': 0.12}, scat=.0,
                       dpf='dpf_OTHG_0_98.txt')  # 2277 # bb arg is not relevent since we use a discretized phase function in a file indepêdnant of depth (g=0.98)
    new_mode.add_layer(z1=0.20, z2=0.80, abs={'484': 0.0430, '544': 0.0683, '602': 0.12}, scat=.0,
                       dpf='dpf_OTHG_0_98.txt')  # 303
    new_mode.add_layer(z1=0.80, z2=2.00, abs={'484': 0.0430, '544': 0.0683, '602': 0.12}, scat=.0,
                       dpf='dpf_OTHG_0_98.txt')  # 79
    new_mode.add_layer(z1=2.0, z2=3.01, abs={'484': 1.36e-2, '544': 5.11e-2, '602': 2.224e-1}, scat=0.0,
                       dpf='dpf_OTHG_0_98.txt')
    new_mode.run_simulation(printoutput=True)
    new_mode.parse_results()
    test_draw = DataViewer(root_name='test')
    test_draw.draw_Eudos_profiles()
    test_draw.draw_zenith_radiance_maps()
    plt.show()
    test_draw.draw_zenith_radiance_profiles(requested_depths=[-1.0, 0., 0.05, 0.10, 0.15, .20, .40])
    plt.show()

    # for station_file_name in station_file_names:
    #     for input_file in input_files:
    #         lisa_sim = AC9Simulation(path=path_to_user_files,
    #                                  mode='Lisa',
    #                                  root_name='RG100od_C10',
    #                                  run_title='Chl a profiles based on real data: b - baseline, 10 - 10% to 100 - 100% ',
    #                                  station_filename='RG100od',
    #                                  ac9_filename='aActot_homChl10.txt',
    #                                  chlaz_filename='Chlaz_homChl10.txt')
    #         lisa_sim.run_simulation(printoutput=True)
