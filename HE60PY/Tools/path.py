import os
import pathlib


class Path:
    def __init__(self):
        self.filepath = f"{pathlib.Path.home()}/Documents/HE60_PY/HE60PY/Tools/path_to_HE60.txt"
        self.to_HE60 = self.load_path()
        self.to_usr = pathlib.Path.home()

    def load_path(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as file:
                return file.readline()
        else:
            return self.create_prompt_for_path()

    def create_prompt_for_path(self):
        path_to_HE60 = input("No path to HE60 was found\nPlease enter the path to HE60.app: ")
        while self.verify_path(path_to_HE60) is False:
                path_to_HE60 = input("\nThis path is invalid\nPlease enter the path to HE60.app: ")
        with open(self.filepath, 'w+') as file:
            file.write(path_to_HE60)
        return path_to_HE60

    def verify_path(self, path):
        file = "/Contents/source_code/common_data_modules/mod_DimensDefaults.f95"
        return os.path.exists(path+file)

if __name__ == '__main__':
    path = Path()