from scipy.interpolate import make_interp_spline # Different interface to the same function
from scipy.interpolate import splprep, splev

import json
import numpy as np
from scipy import interpolate
import utm


file_path = './gps/gps.json'
with open(file_path, 'r') as json_file:
    gps_data = json.load(json_file)

gpsS = ([sample['values'][:2] for sample in gps_data['GPS5']['samples']])
altS = np.array([sample['values'][2] for sample in gps_data['GPS5']['samples']])

pts_x ,pts_y,deg,zone = utm.from_latlon(np.array(gpsS).T[0], np.array(gpsS).T[1])	#Lat,Long to UTM
i = np.arange(len(pts_x))
interp_i = np.linspace(0, i.max(), 100 * i.max())
k =11
xi = make_interp_spline(i, pts_x,k=1, bc_type=None)(interp_i)
yi = make_interp_spline(i, pts_y,k=1, bc_type=None)(interp_i)
zi = make_interp_spline(i, altS,k=1, bc_type=None)(interp_i)
tck, u = splprep([xi, yi,zi],s=5)
new_points = splev(u, tck)
# fig2 = plt.figure(2)
# ax3d = fig2.add_subplot(111, projection='3d')
# ax3d.plot(pts_x, pts_y, altS ,'ro')
# ax3d.plot(new_points[0], new_points[1],new_points[2], 'b-')
#fig2.show()
#plt.show()		

splinePoints = np.array(new_points).T

# # Call the filtering function
# filtered_gps_data = filter_gps_data(gps_data)

# # Return the filtered GPS data 
# print(filtered_gps_data)


# output_file_path = './gps/filtered_gps_data.json'

