class RecordBuilder:
    def __init__(self):
        self.default = {'record1': {}, 'record2': {}, 'record3': {}, 'record4': {}, 'record5': {}, 'record6': {},
                        'record7': {}, 'record8': {}, 'record9': {}, 'record10': {}, 'record11': {}, 'record12': {},
                        'record13': {}}

    def build_records(self):
        self.set_all_default_records()
        updated_dict = self.update_parameters()
        return updated_dict

    def set_all_default_records(self):
        self.set_record1()
        self.set_record2()
        self.set_record3()
        self.set_record4()
        self.set_record5()
        self.set_record6()
        self.set_record7()
        self.set_record8()
        self.set_record9()
        self.set_record10()
        self.set_record11()
        self.set_record12()
        return self.default

    def update_parameters(self):
        updated_dict = self.default.copy()
        for param_to_update_key in self.hermes.get.keys():
            for record in self.default.keys():
                default_param_key_list = list(self.default[record].keys())
                if param_to_update_key in default_param_key_list:
                    updated_dict[record][param_to_update_key] = self.hermes.get[param_to_update_key]
        [self.hermes.get.update(updated_dict[record]) for record in self.default.keys()]
        self.update_bands()
        return updated_dict
    
    def update_bands(self):
        bands = self.hermes.get['bands']
        step = bands[1] - bands[0]
        run_bands = []
        for i in range(len(bands) - 1):
            run_bands.append(bands[i] + step / 2)
        self.hermes.get['run_bands'] = run_bands
