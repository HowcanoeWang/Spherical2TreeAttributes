import os
import pandas as pd
from plant_fraction_hemi import PF

import sys
sys.path.insert(0, '..')
import config

g = os.walk(r'Conversed_57.5/')

# plant fraction, leaf fraction, stem Fraction sky fraction
pai_data = pd.DataFrame(columns=['File_name', 'PlantFrac', 'LeafFrac', 'StemFrac', 'SkyFrac'])

'''
write_dir = f'./Classified_57.5_ver.{config.hsv_version}/'
if not os.path.exists(write_dir):
    os.mkdir(write_dir)
'''


for path, dir_list, file_list in g:
    for file_name in file_list:
        if file_name[-4:] == '.JPG':

            img_path = os.path.join(path, file_name)
            img = PF(img_path, config.hsv_threshold)

            result_list = [file_name,
                           img.pf_value('plant', 57.5),
                           img.pf_value('leaf', 57.5),
                           img.pf_value('stem', 57.5),
                           img.pf_value('sky', 57.5)]
            
            #img.write_result(write_dir + file_name)
            
            #result_list.append()

            pai_data.loc[len(pai_data)] = result_list

            print(str(result_list))
            
    
pai_data.to_csv(f'pf57.5_3classes_fisheye_ver.{config.hsv_version}.csv', index=False)