import json
import os

def correction():
    dir_list = os.listdir()
    result_list = []
    for file in dir_list:
        if file.startswith("Result"):
            result_list.append(file)
    
    with open(result_list[-1], "r+") as f:
        veri = json.load(f, object_hook=dict)
        with open("corrected-Result.json", "w+") as cf:
            for key in list(veri["conversion_rates"].keys()):
                veri["conversion_rates"][key] = 1 / float(veri["conversion_rates"][key])
            json.dump(veri, cf, indent=4)
            
if __name__ == "__main__":
    correction()