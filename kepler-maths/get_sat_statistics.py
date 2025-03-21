import matplotlib.pyplot as plt
import numpy as np
import os
import csv
from commons import *
import ephem
from datetime import datetime

def get_sat_statistics(START_TIME):
    save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    if not os.path.exists(save_location):
        os.makedirs(save_location)

    try:
        sats = load_json(save_location+"/sorted_sats.json")
    except:
        f_all = open(save_location+"/../TLE.txt", "r")
        rep_all = f_all.read()
        # rep = rep.text.replace("\r", "")
        content = rep_all.split("\n")
        all_sats = []
        for i in range(0,len(content)-(len(content)%3),3):
            all_sats.append({
                "name": clean_file_name(content[i]),
                "line1": content[i+1],
                "line2": content[i+2]
            })
        try:
            f_chosen = open(save_location+"/../chosen_sats.txt", "r")
            rep_chosen = f_chosen.read()
            use_sats = []
            content = rep_chosen.split("\n")
            for i in range(len(content)):
                use_sats.append(clean_file_name(content[i]))
            sats = []
            for i in range(len(all_sats)):
                # print( all_sats[i]["name"] in use_sats)
                if all_sats[i]["name"] in use_sats:
                    sats.append(all_sats[i])
            save_json(save_location+"/sorted_sats.json", sats)
        except:
            save_json(save_location+"/sorted_sats.json", all_sats)

    all_sats = []
    for sat_data in sats:
        all_sats.append(ephem.readtle(sat_data["name"], sat_data["line1"], sat_data["line2"]))


    timestep = datetime.fromtimestamp(START_TIME)
    sat_data = []
    for sat in all_sats:
        sat.compute(timestep)
        sat_data.append([sat.inc, sat.raan, sat.e, sat.ap, sat.M, sat.n])
    sat_data = np.array(sat_data)
    return sat_data