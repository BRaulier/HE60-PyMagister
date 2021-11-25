from batch_maker import BatchMaker
from HE60_datafile_generator import Simulation

if __name__ == "__main__":
    path_to_user_files = r'/Users/braulier/Documents/HE60/run/mobley'
    mobley_sim = Simulation(path=path_to_user_files)
    mobley_sim.build_mobley_1998_example()

    mobley_batch = BatchMaker('Mobley_1998_example')
    mobley_batch.set_title('Mobley 1998 example')
    mobley_batch.set_rootname('mobley_results')
    mobley_batch.create_batch_file()
    mobley_batch.set_all_records(ac9_file_path=mobley_sim.ac9_path, bb_file_path=mobley_sim.bb_path)
    mobley_batch.write_batch_file()

    bash_command = './HydroLight6 < /Users/braulier/Documents/HE60/run/batch/Mobley_1998_example.txt'
    path_to_he60 = '/Applications/HE60.app/Contents/backend/EcoLight6'






