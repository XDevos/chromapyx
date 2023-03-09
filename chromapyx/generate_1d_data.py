#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from skimage.registration import phase_cross_correlation
from scipy.ndimage import shift as scipy_shift


def compute_shift(reference_data, data_to_shift):
    shift,_,_ = phase_cross_correlation(reference_data, data_to_shift)
    return shift

def apply_shift(data, shift):
    shifted_data = scipy_shift(data, shift)
    return shifted_data

def register(data, data_fiducial, reference_fiducial):
    shift = compute_shift(reference_fiducial, data_fiducial)
    registered_data = apply_shift(data, shift)
    return registered_data

def segment_by_proxymity(mask):
    shadow = np.zeros_like(mask)
    shadow_number = 0
    shadow_id = 1
    for i in range(len(mask)):
        if mask[i] != 0:
            shadow[i] = shadow_id
            # indicate that we use this current shadow ID if it's the first time
            if shadow_number != shadow_id:
                shadow_number += 1
        else:
            # This means that we are outside any mask
            # Change shadow ID for the next mask if we just quit precedent mask
            if shadow_number == shadow_id:
                shadow_id += 1
    return shadow

def segment(mask):
    shadow = segment_by_proxymity(mask)
    return shadow

def localize_by_threshold(spots, threshold_value):
    positions = []
    for i in range(len(spots)):
        if spots[i] >= threshold_value:
            positions.append(i)
    return positions

def localize(spots):
    positions = localize_by_threshold(spots, 1)
    return positions

def assign(shadow, localizations):
    assigned_localizations = []
    pos_id = 0
    for spots_id in range(len(localizations)):
        for position in localizations[spots_id]:
            if shadow[position]:
                loc_dic = {}
                loc_dic["unique_id"] = pos_id
                loc_dic["mask_id"] = shadow[position]
                loc_dic["position"] = position
                assigned_localizations.append(loc_dic)
                pos_id += 1
    return assigned_localizations

# def format_data(data):
#     return formatted_data


mask = np.array([0,0,0,1,1,1,1,0,0,0,0,0,1,1,1,1,0,0,0,0])
mask_fiducial = np.array([0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0])

spot1 = np.array([0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0])
spot1_fiducial = np.array([0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0])

spot2 = np.array([0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0])
spot2_fiducial = np.array([0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0])

# print(mask)
# print(mask_fiducial)
# print(spot1)
# print(spot1_fiducial)
# print(spot2)
# print(spot2_fiducial)

# print(phase_cross_correlation(mask_fiducial, spot1_fiducial))
# print(phase_cross_correlation(mask_fiducial, spot2_fiducial))

# We admit that fiducial of mask is the reference for all fiducials
registered_mask = mask
registered_spot1 = register(spot1, spot1_fiducial, mask_fiducial)
registered_spot2 = register(spot2, spot2_fiducial, mask_fiducial)

# print(registered_mask)
# print(registered_spot1)
# print(registered_spot2)

segmented_mask = segment(registered_mask)
spot1_position = localize(registered_spot1)
spot2_position = localize(registered_spot2)

spots_positions = [spot1_position, spot2_position]

assigned_spots = assign(segmented_mask, spots_positions)

print(assigned_spots)

# formatted_assigned_spots = format_data(assigned_spots)


######################## LIST to CSV ########################
# import csv
  
  
# # field names 
# fields = ['Name', 'Branch', 'Year', 'CGPA'] 
    
# # data rows of csv file 
# rows = [ ['Nikhil', 'COE', '2', '9.0'], 
#          ['Sanchit', 'COE', '2', '9.1'], 
#          ['Aditya', 'IT', '2', '9.3'], 
#          ['Sagar', 'SE', '1', '9.5'], 
#          ['Prateek', 'MCE', '3', '7.8'], 
#          ['Sahil', 'EP', '2', '9.1']] 
  
# with open('GFG', 'w') as f:
      
#     # using csv.writer method from CSV package
#     write = csv.writer(f)
      
#     write.writerow(fields)
#     write.writerows(rows)
#############################################################

######################## DICT to CSV ########################
# import csv
# csv_columns = ['No','Name','Country']
# dict_data = [
# {'No': 1, 'Name': 'Alex', 'Country': 'India'},
# {'No': 2, 'Name': 'Ben', 'Country': 'USA'},
# {'No': 3, 'Name': 'Shri Ram', 'Country': 'India'},
# {'No': 4, 'Name': 'Smith', 'Country': 'USA'},
# {'No': 5, 'Name': 'Yuva Raj', 'Country': 'India'},
# ]
# csv_file = "Names.csv"
# try:
#     with open(csv_file, 'w') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
#         writer.writeheader()
#         writer.writerows(dict_data)
# except IOError:
#     print("I/O error")
#############################################################