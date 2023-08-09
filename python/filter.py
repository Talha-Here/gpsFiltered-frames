# import numpy as np
# import matplotlib.pyplot as plt
# from scipy import interpolate
# from mpl_toolkits.mplot3d import Axes3D

import json
import numpy as np
from scipy import interpolate
import utm
import pandas as pd

from scipy.interpolate import make_interp_spline # Different interface to the same function
from scipy.interpolate import splprep, splev

# Read the JSON file

file_path = './gps/gps.json'
with open(file_path, 'r') as json_file:
    gps_data = json.load(json_file)
    # print(gps_data)



def filter_gps_data(gps_data, k=11, s=5):

    # if 'samples' not in gps_data or not isinstance(gps_data['samples'], list):
    #     raise ValueError("Invalid 'gps_data' format. 'samples' key not found or not a list.")

    # try:
    #     gpsS = np.array([sample['values'][:2] for sample in gps_data['samples']])
    #     altS = np.array([sample['values'][2] for sample in gps_data['samples']])
    # except KeyError as e:
    #     raise ValueError(f"Invalid 'gps_data' format. Key not found: {e}")
    #print(gps_data['GPS5']['samples'])

    gpsS = np.array([sample['values'][:2] for sample in gps_data['GPS5']['samples']])
    #gpsS = ([sample['values'][:2] for sample in gps_data['GPS5']['samples']])
    altS = np.array([sample['values'][2] for sample in gps_data['GPS5']['samples']])
    #print(gpsS)
    pts_x, pts_y, deg, zone = utm.from_latlon(gpsS[:, 0], gpsS[:, 1])

    i = np.arange(len(pts_x))

    interp_i = np.linspace(0, i.max(), 100 * i.max())
    print(interp_i)
    k=11;
    xi = make_interp_spline(i, pts_x, k=1, bc_type=None)(interp_i)
    yi = make_interp_spline(i, pts_y, k=1, bc_type=None)(interp_i)
    zi = make_interp_spline(i, altS, k=1, bc_type=None)(interp_i)
    # print("X VALUES:", xi)
    # print("\nravel() : ", xi.ravel())
    # print(len(xi))
    # print(type(xi))
    #print("Y VALUES:", yi)
    #print("Z VALUES:", zi)
    tck, u = splprep([xi, yi, zi], s=5)
    new_points = splev(u, tck)

    gps_filtered = {
        'samples': [
            {
                'values': [gpsS[i][0], gpsS[i][1], new_points[2][i]],
                'date': sample['date'],
                'millis': sample['millis'],
                'diff': sample['diff'],
                'speed_2d': sample['speed_2d'],
                'speed_3d': sample['speed_3d'],
                'pdop': sample['pdop']
            }
            for i, sample in enumerate(gps_data['samples'])
        ]
    }

    return gps_filtered


# Call the filtering function
filtered_gps_data = filter_gps_data(gps_data)

# Return the filtered GPS data 
print(filtered_gps_data)


output_file_path = './gps/filtered_gps_data.json'

# Write the filtered_gps_data to the JSON file
with open(output_file_path, 'w') as json_file:
    json.dump(filtered_gps_data, json_file)

print(f"Filtered GPS data has been saved to '{output_file_path}'.")

with open("filtered_gps_data.json", "r") as file:
    data = json.load(file)

df = pd.json_normalize(data)
df.to_csv("flattened_output.csv", index=False)


