import numpy as np
import os
import pandas as pd
from PIL import Image, ImageDraw
from skimage.color import rgb2hsv
from math import floor

import sys
sys.path.insert(0, '..')
import config


class PF:

    def __init__(self, img_path, threshold):
        img = Image.open(img_path)
        self.img_name = os.path.basename(img_path)

        w, h = img.size
        self.h_half = int(h / 2)
        
        self.threshold = threshold

        self.img = np.asarray(img.crop((0, 0, w, self.h_half)))
        self.img_data = rgb2hsv(self.img)
        self.height = self.radius = self.h_half
        self.width = w

        self.aw = self._angle_weight()
        self.kind = self._classify()
        self.row_percent = self._percent_each_row()
        self.ring_s = self._ring_area(calibration=True)

    def _classify(self):
        threshold = self.threshold
        self.sky_mask = self._in_range(threshold['sky']['min'], threshold['sky']['max'])
        self.leaf_mask = self._in_range(threshold['leaf']['min'], threshold['leaf']['max'])

        kind = np.zeros(self.img_data.shape[0:2], dtype=int)
        # Stem = 0, leaf = 1, sky = 2, plant =0 +1
        kind[self.leaf_mask] = 1
        kind[self.sky_mask] = 2

        return kind


    def _in_range(self, lower, upper):
        '''
        input a image and threshold, give a classified binary image (m*n booleans ndarray)
        Image out is binary w*h matrix, T is in threshold (sky), F is out of threshold (plant)
        '''
        img_data = self.img_data

        mask = np.zeros(img_data.shape[0:2], dtype=bool)

        for min, max in zip(lower, upper):
            mask_0 = (img_data[:, :, 0] >= min[0]) * (img_data[:, :, 0] <= max[0])
            mask_1 = (img_data[:, :, 1] >= min[1]) * (img_data[:, :, 1] <= max[1])
            mask_2 = (img_data[:, :, 2] >= min[2]) * (img_data[:, :, 2] <= max[2])

            mask_all = mask_0 * mask_1 * mask_2
            mask += mask_all

        return mask

    def _percent_each_row(self):
        stem_num = (self.kind == 0).sum(axis=1)
        leaf_num = (self.kind == 1).sum(axis=1)
        plant_num = stem_num + leaf_num
        sky_num = (self.kind == 2).sum(axis=1)

        stem_percent = stem_num / self.width
        leaf_percent = leaf_num / self.width
        plant_percent = plant_num / self.width
        sky_percent = sky_num / self.width

        return {'plant':plant_percent, 'leaf':leaf_percent, 'stem':stem_percent, 'sky':sky_percent}

    def _ring_area(self, calibration=False):
        r_range = np.arange(0, self.radius + 1)

        if calibration:
            f = self.radius / np.sqrt(2)
            r_new = f * np.tan(2 * np.arcsin(r_range / (2 * f)))
        else:
            r_new = r_range

        self.r_in = r_new[:-1]
        self.r_out = r_new[1:]

        s = np.pi * self.r_out ** 2 - np.pi * self.r_in ** 2

        return s
        
    def _angle_weight(self):
        line_id = np.arange(0, self.h_half, step=1)
        angle_weight = np.cos(line_id / self.h_half * np.pi / 2)
        
        return angle_weight
    
    # TODO
    def write_output(self, result_dir='outputs/', return_jpg=True, return_csv=False, merge=False):

        if return_jpg:
            rua = np.zeros((self.height, self.width, 3))

            #sky:   white R=255, G=255, B=255
            #plant: blue  R=0,   G=0,   B=255
            #leaf:  green R=0,   G=255, B=0

            # Red Channel
            rua[:, :, 0] = (self.kind == 2) * 255   # only sky = 255
            # Green Channel
            rua[:, :, 1] = ((self.kind == 1) | (self.kind == 2)) * 255  # sky & leaf = 255
            # Blue Channel
            rua[:, :, 2] = ((self.kind == 0) | (self.kind == 2)) * 255  # sky & plant = 255

            img_class = Image.fromarray((rua).astype('uint8'))
            
            d = ImageDraw.Draw(img_class)
            d.text((10,10), str(self.threshold), fill=(0,0,0))
            
            img_class.save(f'{result_dir}/class/{self.img_name}_class.jpg')
            if merge:
                # merge img|classified|leaf|plant|sky
                img_comb = Image.fromarray(np.vstack((np.asanyarray(self.img), rua)).astype('uint8'))
                d = ImageDraw.Draw(img_comb)
                d.text((10, 10), str(self.threshold), fill=(0,0,0))
                img_comb.save(f'{result_dir}/merge/{self.img_name}_merge.jpg')

        if return_csv:
            np.savetxt(f'{result_dir}/csv/{self.img_name}.csv', self.kind.astype(int), fmt='%i', delimiter=',')


    def pf_value(self, kind='plant', zenith_angle=57.5):
        # zenith_angle should < 80 to be more precious
        line_num = floor(self.height * zenith_angle / 90) - 1

        percent = self.row_percent[kind][:line_num]
        #aw = self.aw[:line_num]
        r_max = self.r_in[line_num]

        s_max = np.pi * r_max ** 2
        ring_s = self.ring_s[:line_num]
        weight = ring_s / s_max

        pf_row = percent * weight# * aw
        
        return pf_row.sum()
