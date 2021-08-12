import os
import configparser
import ast
from simulation import Simulation

#set seed for reproducibility
#np.random.seed(100)

class SimDirector():
    def __init__(self, scenario="default"):
        self.scenario = scenario

    def construct(self):    
        if self.scenario == "default":
            print("Building default scenario simulation")
            return SimBuilder()
        elif self.scenario == "custom":
            print("Building custom scenario simulation")
            return SimBuilder().build_custom()
        elif self.scenario == "lockdown":
            print("Building lockdown scenario simulation")
            return SimBuilder().build_lockdown()
        elif self.scenario == "reduced_interaction":
            print("Building reduced interaction scenario simulation")
            return SimBuilder().build_reduced_interaction()
        elif self.scenario == "self_isolation":
            print("Building self isolation scenario simulation")
            return SimBuilder().build_self_isolation()
        else:
            print("Invalid scenario!")



class SimBuilder(SimDirector):
    def __init__(self):
        self.sim = Simulation()
        self.sim.Config.simulation_steps = 20000

    def build_custom(self):
        '''reads config from filename'''
        path = os.path.dirname(os.path.realpath(__file__)) + '\custom_config.ini'
        config = configparser.ConfigParser()
        config.read(path)
        for section in config.sections():
            for key in config[section]:
                try:
                    # converts the string value into its corresponding data type
                    value = ast.literal_eval(config[section][key])
                except ValueError:
                    print("Invalid custom config value for: " + key)
                self.sim.Config.set(key, value)
        return self
        
    def build_lockdown(self):
        self.sim.Config.set_lockdown(lockdown_percentage = 0.1, lockdown_compliance = 0.95)
        return self

    def build_reduced_interaction(self):
        self.sim.Config.set_reduced_interaction()
        self.sim.population_init()
        return self

    def build_self_isolation(self):
        self.sim.Config.set_self_isolation(self_isolate_proportion = 0.9,
                                    isolation_bounds = [0.02, 0.02, 0.09, 0.98],
                                    traveling_infects=False)
        self.sim.population_init() #reinitialize population to enforce new roaming bounds
        return self
    
    def run(self):
        self.sim.run()


if __name__ == '__main__':
    # Possible scenarios: "default", "custom", "lockdown", "reduced_interaction", "self_isolation"
    sim = SimDirector(scenario="default").construct()
    sim.run()
