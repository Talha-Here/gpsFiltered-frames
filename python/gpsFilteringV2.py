import json
import utm
import math
from geopy import distance
from scipy.interpolate import make_interp_spline # Different interface to the same function
from scipy.interpolate import splprep, splev
import numpy as np
import pandas as pd
import csv


gpsPath = './gps/merged.json'
with open(gpsPath, 'r') as json_file:
    gps_data = json.load(json_file)
    # print(gps_data)

def filterGps(gpsPath):
    f = open(gpsPath)
    gpsData = json.load(f)
    gpsPts = []
    diff = []
    for i in range(len(gpsData['GPS5']['samples'])):
        gpsPts.append(gpsData['GPS5']['samples'][i]['values'][:2])
        diff.append(gpsData['GPS5']['samples'][i]['diff'])

    diff  = np.array(diff)

    allGps = [gpsPts[0]]
    allDiff = [diff[0]]
    startPoint = 0
    endPoint = 0
    while True:
        dist = 0
        while dist < 1:
            dist = distance.distance(gpsPts[startPoint],gpsPts[endPoint]).m
            if endPoint == len(gpsPts)-1:
                break
            endPoint = endPoint + 1
        allGps.append(gpsPts[endPoint])
        allDiff.append(diff[endPoint])
        if endPoint == len(gpsPts)-1:
            break
        startPoint = endPoint

    finalGps = clst_pt_spline(allGps)
    return np.array(finalGps).tolist(), np.array(allDiff).tolist()

def clst_pt_spline(gps_all):
    lat,long = np.array(gps_all).T
    pts_x,pts_y,deg,zone = utm.from_latlon(np.array(lat), np.array(long))
    i = np.arange(len(pts_x))
    interp_i = np.linspace(0, i.max(), 100 * i.max())
    k =11
    xi = make_interp_spline(i, pts_x,k=1, bc_type=None)(interp_i)
    yi = make_interp_spline(i, pts_y,k=1, bc_type=None)(interp_i)
    try:
        tck, u = splprep([xi, yi],s = 5)
        new_points = splev(u, tck)
        ### Uncomment Following if you want to visualize the spline
        # fig2 = plt.figure(2)
        # ax3d = fig2.add_subplot(111, projection='3d')
        # ax3d.plot(pts_x, pts_y,'ro')
        # ax3d.plot(new_points[0], new_points[1], 'b-')
        # fig2.show()
        # plt.show()
    except:
        print('Consecutive Numbers in xi & yi')
        res = []
        for idx in range(0, len(xi) - 1):
            if xi[idx] == xi[idx + 1]:
                res.append(idx)
        xi = np.delete(xi,res)
        yi = np.delete(yi,res)
        tck, u = splprep([xi, yi],s = 100)
        new_points = splev(u, tck)
        ### Uncomment Following if you want to visualize the spline
        # fig2 = plt.figure(2)
        # ax3d = fig2.add_subplot(111, projection='3d')
        # ax3d.plot(pts_x, pts_y,'ro')
        # ax3d.plot(new_points[0], new_points[1], 'b-')
        # fig2.show()
        # plt.show()
    distance = []
    for i in range(len(pts_x)):
        distance.append([])
        for j in range(len(new_points[0])):
            dist = abs(math.sqrt((pts_x[i]-new_points[0][j])**2 + (pts_y[i]-new_points[1][j] )**2 ))
            distance[-1].append(dist)

    closest_points_x = []
    closest_points_y = []
    for k in range(len(pts_x)):
        idx = np.argmin(distance[k])
        closest_points_x.append(new_points[0][idx])
        closest_points_y.append(new_points[1][idx])
    gps = []
    for i in range(len(closest_points_x)):
        gps.append(list(utm.to_latlon(closest_points_x[i],closest_points_y[i], deg, zone)))

    return gps

# for i in range(len(allGps)):
#     print()
#     print(allDiff[i])

filtered_gps_data, diff = filterGps('./gps/merged.json')

# print(filtered_gps_data);


# filtered_gps_data = filterGps(gpsPath)
# # filtered_gps_data = clst_pt_spline(gpsPath)

# # Call the filtering function
# # filtered_gps_data = filterGps(gps_data)

# # # Return the filtered GPS data 
# # print(filtered_gps_data)

# print(filtered_gps_data )

output_file_path = './output/V2_filtered_gps_data.json'

# # Write the filtered_gps_data to the JSON file
with open(output_file_path, 'w') as json_file:
     json.dump(filtered_gps_data, json_file)

print(f"Filtered GPS data has been saved to '{output_file_path}'.")

# with open("./gps/filtered_gps_data.json", "r") as file:
#     data = json.load(file)
#     for i in range(len(data)):
#         flattened_data = {i : data[i]}
#     #     flattened_data = data
#     #     print(f"FLATTENED DATA {flattened_data}")

# df = pd.json_normalize(flattened_data)
# df.to_csv("flattened_output.csv", index=False)

csv_file_path = './output/V2_gps_data.csv'

with open("./output/V2_filtered_gps_data.json", "r") as file:
    json_data = json.load(file)

df = pd.DataFrame(json_data, columns=['Latitude', 'Longitude'])

# Save the DataFrame as a CSV file
df.to_csv(csv_file_path, index=False, quoting=csv.QUOTE_NONNUMERIC)
print(f"Filtered GPS in CSV has been saved to '{csv_file_path}'.")
