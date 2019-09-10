import numpy as np
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
        self.img = np.asarray(img)
        
        self.threshold = threshold
        self.img_data = rgb2hsv(self.img)

        #self.binary = self._in_range(threshold['min'], threshold['max'])
        #self.overlay, self.pai = self.count_pai(self.binary)
        self.kind = self._classify()
        self.kind_ref = {'plant': self.kind != 2,
                        'stem': self.kind == 0,
                        'leaf': self.kind == 1,
                        'sky': self.kind == 2}


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
        
    def _classify(self):
        threshold = self.threshold
        self.sky_mask = self._in_range(threshold['sky']['min'], threshold['sky']['max'])
        self.leaf_mask = self._in_range(threshold['leaf']['min'], threshold['leaf']['max'])

        kind = np.zeros(self.img_data.shape[0:2], dtype=int)
        # stem = 0, leaf = 1, sky = 2
        kind[self.leaf_mask] = 1
        kind[self.sky_mask] = 2

        return kind
        
    @staticmethod
    def createCircularMask(h, w, center=None, radius=None):
        if center is None: # use the middle of the image
            center = [int(w/2), int(h/2)]
        if radius is None: # use the smallest distance between the center and image walls
            radius = min(center[0], center[1], w-center[0], h-center[1])

        Y, X = np.ogrid[:h, :w]
        dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

        mask = dist_from_center <= radius
        return mask

    '''
    def count_pai(self, binary_img):
        h, w = binary_img.shape
        r = w / 2
        mask = self.createCircularMask(h, w)
        overlay = binary_img * mask

        u_img, counts_img = np.unique(overlay, return_counts=True)
        u_mask, counts_mask = np.unique(mask, return_counts=True)

        sky_percent = counts_img[1] / counts_mask[1]
        pai = 1-sky_percent
        return overlay, pai
    
    def write_result(self, result_dir, mode='binary'):
        h, w, d = self.img.shape

        rua = np.zeros((h, w, 3))
        if mode=='colored'
            rua[:, :, 0] = self.img[:,:,0] * abs(self.overlay - 1)
            rua[:, :, 1] = self.img[:,:,1] * abs(self.overlay - 1)
            rua[:, :, 2] = self.img[:,:,2] * abs(self.overlay - 1)
            # merge img|classified
            img_comb = Image.fromarray( np.hstack((self.img, rua)).astype('uint8'))
            img_comb.save(result_dir)
        else:
            for i in range(0,3):
                rua[:,:,i] = self.binary * 255
            rua.save(result_dir)
    '''
    def pf_value(self, kind='plant', zenith_angle=57.5):
        h, w = self.kind.shape
        r = w / 2
        mask = self.createCircularMask(h, w)
        
        binary_img = self.kind_ref[kind]
        overlay = binary_img * mask

        u_img, counts_img = np.unique(overlay, return_counts=True)
        u_mask, counts_mask = np.unique(mask, return_counts=True)

        percent = counts_img[1] / counts_mask[1]

        return percent
        



