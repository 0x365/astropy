import os
import datetime

from skyfield.api import load, utc

from common import *

open_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(open_location):
    raise Exception("Data does not exist")
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(save_location):
    os.makedirs(save_location)

satellites = get_icsmd_satellites(open_location+"/active.tle", "icsmd_sats.txt")




ts = load.timescale()

start_date = datetime.datetime(2024,9,11, tzinfo=utc)
end_date = start_date + relativedelta(days=1)
time_range = date_range(start_date, end_date, 30, 'seconds')
time = ts.from_datetimes(time_range)

sat_pos = []
for sat in satellites:
    sat_pos.append(sat.at(time).position.km)

# (x.at(time) - y.at(time)).distance().km

sat_pos = np.array(sat_pos)
print(np.shape(sat_pos))