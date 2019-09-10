import os
import time
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
from scipy import interpolate
from skimage import filters
from skimage.morphology import disk, binary_dilation
import multiprocessing

import scipy.interpolate as spint
import scipy.spatial.qhull as qhull
import itertools

# =================  Three main functions ================
def pano2fisheye(pil_img, model='equal_width', inter_method='linear', log='off', multi='off'):
    if log == 'on':
        print('|- Start conversing...')
    img_df, shape = img2dataframe(pil_img)
    if log == 'on':
        print('|-  Image DataFrame initialized')
    img_conv, fisheye_shape = coordinate_converse(img_df, shape, model=model)
    if log == 'on':
        print('|-  New pixel positions calculated')
    img_cali = unique_points(img_conv)
    if log == 'on':
        print('|-  Duplicated pixels removed')
    if log == 'on':
        print('|-  Start fixing holes')
    red, green, blue = interpolate_img(img_cali, fisheye_shape, method=inter_method, multi=multi, log=log)
    fisheye_img = merge_layers(red, green, blue)
    if log == 'on':
        print('|-  Image combined')
    return fisheye_img


def fisheye_correction(img, center_radius, model='equidistant', vision_angle=50, inter_method='linear',  multi='off', log='off'):
    x, y, r = center_radius
    if log == 'on':
        print('- Start conversing...')
    img_df, shape = img2dataframe(img, center_radius)
    if log == 'on':
        print('|-  Image DataFrame initialized')
    img_df = calculate_radius_calibrated(img_df, r, model=model)
    if log == 'on':
        print('|-  New radius calculated')
    img_df, r_new = zenith_filter(img_df, r, vision_angle)
    if log == 'on':
        print('|-  Vision angle filtered')
    img_df = calculate_new_xy(img_df, r, r_new)
    if log == 'on':
        print('|-  New pixel positions calculated')
    df_cali = unique_points(img_df)
    if log == 'on':
        print('|-  Duplicated pixels removed')
        print('|-  Start fixing holes')
    length = int(np.ceil(r_new * 2))
    red, green, blue = interpolate_img(df_cali, (length, length), method=inter_method, multi=multi)
    corrected_img = merge_layers(red, green, blue)
    if log == 'on':
        print('|-  Image combined')
    return corrected_img


def pano2fisheye_correction(pil_img, trans_model='equal_width', cali_model='equisolid', vision_angle=50,
                            inter_method='linear', multi='off', log='off'):
    if log == 'on':
        print('- Start conversing...')
    img_df, shape = img2dataframe(pil_img)
    del pil_img
    if log == 'on':
        print('|-  Image DataFrame initialized')
    img_conv, fisheye_shape = coordinate_converse(img_df, shape, model=trans_model)
    if log == 'on':
        print('|-  New pixel positions calculated')
    img_cali = unique_points(img_conv)
    if log == 'on':
        print('|-  Duplicated pixels removed')
    del img_conv

    r = int(fisheye_shape[0] / 2)

    img_df = calculate_radius_calibrated(img_cali, r, model=cali_model)
    del img_cali
    
    if log == 'on':
        print('|-  New radius calculated')
    img_df, r_new = zenith_filter(img_df, r, vision_angle)
    if log == 'on':
        print('|-  Vision angle filtered')
    img_df = calculate_new_xy(img_df, r, r_new)
    if log == 'on':
        print('|-  New pixel positions calculated')
    df_cali = unique_points(img_df)

    if log == 'on':
        print('|-  Start fixing holes')
    length = int(np.ceil(r_new * 2))
    red, green, blue = interpolate_img(df_cali, (length, length), method=inter_method, multi=multi)
    del df_cali
    
    fisheye_cali_img = merge_layers(red, green, blue)
    if log == 'on':
        print('|-  Image combined')

    return fisheye_cali_img


# =============== The modules that used for previews three main functions ======================
def img2dataframe(img, center_radius=None):
    '''
    if img is a fisheye image, (x, y, r) is required to crop fisheye edge.
    '''
    if type(center_radius) == tuple and len(center_radius) == 3:
        # fisheye image
        x, y, radius = center_radius
        img_crop = img.crop((x - radius - 1, y - radius - 1, x + radius - 1, y + radius - 1))

        mask = Image.new('RGBA', (2 * radius, 2 * radius))
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 2 * radius, 2 * radius), fill='blue', outline='blue')
        # overlay mask on image
        img_out = Image.new('RGBA', (2 * radius, 2 * radius))
        img_out.paste(img_crop, (0, 0), mask)
    else:
        # panorama image need crop half
        width, height = img.size
        img_out = img.crop((0, 0, width, int(height / 2)))

    '''PIL.img.size = (w, h)'''
    w, h = img_out.size
    np_img = np.asarray(img_out)
    '''
    numpy.ndarray:
     ┌─→ y
     │  np.asarray(img).shape = (h, w, d)
    x↓
    '''
    x_grid, y_grid = np.mgrid[0:h, 0:w]
    red = np_img[:, :, 0]
    green = np_img[:, :, 1]
    blue = np_img[:, :, 2]
    if np_img.shape[2] == 4:
        alpha = np.asarray(img_out)[:, :, 3]
        img_df = pd.DataFrame({'x': x_grid.flatten(), 'y': y_grid.flatten(),
                               'red': red.flatten(), 'green': green.flatten(), 'blue': blue.flatten(),
                               'alpha': alpha.flatten()},
                              columns=['x', 'y', 'red', 'green', 'blue', 'alpha'])
        # remove alpha layer
        img_df = img_df.loc[img_df['alpha'] == 255]
        img_df = img_df.drop(['alpha'], axis=1)
    else:
        img_df = pd.DataFrame({'x': x_grid.flatten(), 'y': y_grid.flatten(),
                               'red': red.flatten(), 'green': green.flatten(), 'blue': blue.flatten()},
                              columns=['x', 'y', 'red', 'green', 'blue'])
    np_shape = (h, w)
    return img_df, np_shape


def unique_points(img_df):
    '''
    remove duplicate points which overlay one the same pixel
    x: conversed x (float)
    y: conversed y (float)
    shape: (height, width)

    return x, y , v_new
    '''
    x_int = img_df['x_cali'].astype(int)
    y_int = img_df['y_cali'].astype(int)
    df_cali = pd.DataFrame(
        {'x': x_int, 'y': y_int, 'red': img_df['red'], 'green': img_df['green'], 'blue': img_df['blue']})
    df_cali = df_cali.groupby(['x', 'y'], as_index=False).mean()

    return df_cali


def interpolate_img(img_df, shape, method='none', log='off', multi='off'):
    '''
    shape: (height, width)

    method: using griddata.linear to interpolate, this is very slow and time consuming
    return 2D.ndarray of that layer
    '''
    xi, yi = np.mgrid[0:shape[0], 0:shape[1]]
    if method == 'none':
        red = np.zeros(shape)
        green = np.zeros(shape)
        blue = np.zeros(shape)

        red[img_df['x'], img_df['y']] = img_df['red']
        green[img_df['x'], img_df['y']] = img_df['green']
        blue[img_df['x'], img_df['y']] = img_df['blue']
        if log == 'on': print('| |- no interpolate method applied')

        return red, green, blue

    if method == 'linear':

        if multi == 'on':
            key_words = ['red', 'green', 'blue']
            multiprocessing.freeze_support()
            pool = multiprocessing.Pool(processes=3)
            pool_list = {}
            for channel in key_words:
                pool_list[channel] = pool.apply_async(interpolate.griddata,
                                                      args=((img_df['x'], img_df['y']), img_df[channel], (xi, yi)))

            result_list = {key:value.get() for key, value in pool_list.items()}

            pool.close()
            pool.join()
            return result_list['red'], result_list['green'], result_list['blue']
        else:
            mask_hole = np.zeros(shape)
            mask_hole[img_df['x'], img_df['y']] = 1
            mask_circ = createCircularMask(*shape)
            mask = (mask_hole==0) * mask_circ
            if log == 'on': print('| |- mask generated')
            
            red = np.zeros(shape).astype(np.uint16)
            green = np.zeros(shape).astype(np.uint16)
            blue = np.zeros(shape).astype(np.uint16)

            red[img_df['x'], img_df['y']] = img_df['red']
            green[img_df['x'], img_df['y']] = img_df['green']
            blue[img_df['x'], img_df['y']] = img_df['blue']
            
            red_filter = filters.rank.mean(red, disk(1),mask=mask_hole==1)
            green_filter = filters.rank.mean(green, disk(1),mask=mask_hole==1)
            blue_filter = filters.rank.mean(blue, disk(1),mask=mask_hole==1)
            if log == 'on': print('| |- filter generated')
            
            #mask_deli = binary_dilation(mask)
            
            red[mask] = red_filter[mask]
            green[mask] = green_filter[mask]
            blue[mask] = blue_filter[mask]
            '''
            t = time.time()
            red = interpolate.griddata((img_df['x'], img_df['y']), img_df['red'], (xi, yi))
            if log == 'on':
                print(f'| |- [red] channel finished, {time.time() - t}s spend')
            tr = time.time()
            green = interpolate.griddata((img_df['x'], img_df['y']), img_df['green'], (xi, yi))
            if log == 'on':
                print(f'| |- [green] channel finished, {time.time() - t}s spend')
            tr = time.time()
            blue = interpolate.griddata((img_df['x'], img_df['y']), img_df['blue'], (xi, yi))
            if log == 'on':
                print(f'| |- [blue] channel finished, {time.time() - t}s spend')
            '''
            return red, green, blue


def merge_layers(r, g, b):
    img = np.zeros((r.shape[0], r.shape[1], 3))
    img[:, :, 0] = r
    img[:, :, 1] = g
    img[:, :, 2] = b
    img[np.isnan(img)] = 0
    img = img.astype('uint8')
    pil_img = Image.fromarray(img)

    return pil_img


def coordinate_converse(img_df, panorama_size, model='equal_width'):
    '''
    panorama size = (h, w)
        h: panorama image height
        w: panorama image width
    model
    'equal_width': assume height of one pixel in panorama = the distance to circle center in fisheye
    'projection': assume height of panorama = height of hemisphere of fisheye ghostball,
                  which the radius of ghostball (r), height of pixel in panorama (h),
                  distance to circle center of fisheye for that pixel(d) satisfy:
                  r^2 = h^2 + d^2
    '''
    h, w = panorama_size
    r = h
    fisheye_size = (2 * r, 2 * r)
    theta = (img_df['y'] + 0.5) / w * 360  # +0.5 is to mark pixel center
    sin_theta = np.sin(np.deg2rad(theta))
    cos_theta = np.cos(np.deg2rad(theta))
    if model == 'equal_width':
        img_df['x_cali'] = r + sin_theta * img_df['x']
        img_df['y_cali'] = r + cos_theta * img_df['x']
    if model == 'projection':
        d = np.sqrt(abs(2 * (img_df['x'] + 0.5) * r - (img_df['x'] + 0.5) ** 2))
        img_df['x_cali'] = r + sin_theta * d
        img_df['y_cali'] = r + cos_theta * d

    return img_df, fisheye_size


def calculate_radius_calibrated(img_df, img_radius, model='equidistant', log='off'):
    '''
    img_radius: half of fisheye width or height
    models:
        'equidistant'
        'equidolid'
        'orthographic'
        'stereographic'
    '''
    if model == 'equidistant':
        f = img_radius * 2 / np.pi  # the radius of fake sphere
        d = np.sqrt((img_df['x'] - img_radius) ** 2 + (img_df['y'] - img_radius) ** 2)
        img_df['r_cali'] = f * np.tan(d / f)
    elif model == 'equisolid':
        f = img_radius / np.sqrt(2)
        d = np.sqrt((img_df['x'] - img_radius) ** 2 + (img_df['y'] - img_radius) ** 2)
        img_df['r_cali'] = f * np.tan(2 * np.arcsin(d / (2 * f)))
    elif model == 'orthographic':
        f = img_radius
        d = np.sqrt((img_df['x'] - img_radius) ** 2 + (img_df['y'] - img_radius) ** 2)
        img_df['r_cali'] = d / np.sqrt(1 + (d / f) ** 2)
    elif model == 'stereographic':
        f = img_radius / 2
        d = np.sqrt((img_df['x'] - img_radius) ** 2 + (img_df['y'] - img_radius) ** 2)
        img_df['r_cali'] = f * np.tan(2 * np.arctan(d / (2 * f)))
    else:
        d = np.sqrt((img_df['x'] - img_radius) ** 2 + (img_df['y'] - img_radius) ** 2)
        if log == 'on': print('no input [' + model + '] model, please choose another one!')
        img_df['r_cali'] = d

    return img_df


def zenith_filter(img_df, img_radius, filter_degree=50):
    f = img_radius * 2 / np.pi
    if filter_degree <= 70:
        threshold = f * np.tan(np.deg2rad(filter_degree))
        img_df = img_df.loc[np.abs(img_df['r_cali']) <= threshold]

        return img_df, threshold
    else:
        return img_df, False


def calculate_new_xy(img_df, img_radius, cali_radius):
    rad_theta = np.arctan2((img_df['x'] - img_radius), (img_df['y'] - img_radius))
    rad_theta += (img_df['x'] <= img_radius) * 2 * np.pi
    img_df = img_df.assign(x_cali=cali_radius + np.sin(rad_theta) * img_df['r_cali'])
    img_df = img_df.assign(y_cali=cali_radius + np.cos(rad_theta) * img_df['r_cali'])

    return img_df
    
    
def createCircularMask(h, w, center=None, radius=None):
    if center is None: # use the middle of the image
        center = [int(w/2), int(h/2)]
    if radius is None: # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w-center[0], h-center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask = dist_from_center <= radius
    return mask
