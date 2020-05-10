import time
import numpy as np

from scipy import ndimage
from scipy.interpolate import interp1d
import imageio

from skimage.exposure import equalize_hist

def mecator_conversion(img_path, zenith=85, equalize=False, gcp=0):
    img = imageio.imread(img_path)
    h, w, d = img.shape
    #>>> (2688. 5736, 3)
    
    if equalize:
        img = equalize_hist(img)
    
    h_id = np.arange(h) 
    '>>> array([   0,    1,    2, ..., 2685, 2686, 2687], len=2688)'
    w_id = np.arange(w)  
    
    angle_id = h/2 - h_id - 0.5
    '>>> array([ 1343.5,  1342.5, ..., -1342.5, -1343.5], len=2688)'
    angle = angle_id / angle_id.max() * 90 # degree
    'array([ 90.,  89.933, ..., -89.933, -90.])'
    
    select = abs(angle) <= zenith
    select_angle = angle[select] 
    '>>> [ 84.97580945  84.90882025  ...  -84.90882025 -84.97580945], len=2538'
    
    select_img = img[select, :, :]
    select_h, _, _ = select_img.shape  # (2538, 5376, 3)
    
    mecator_coord = h / 2 * np.log(np.tan(np.deg2rad(45 + select_angle / 2)))
    '''
    >>> array([ 4201.97396912,  4184.14924484,  4166.55692064, ...,
               -4166.55692064, -4184.14924484, -4201.97396912], len=2583)'''
    
    mecator_coord_zero = mecator_coord.max() - mecator_coord
    '>>> array([   0.,   17.82472427,   35.41704847, ..., 8368.53088976, 8386.12321396, 8403.94793823])'
    
    f = interp1d(mecator_coord_zero, np.arange(select_h), fill_value="extrapolate")
    xnew = np.arange(0, np.ceil(mecator_coord.max())*2, 1)  
    '>>> array([0, 1, 2, ..., 8401, 8402, 8403])'
    mecator_id = f(xnew)  # related img_h id in raw image (85 degree selected)
    '''   
    >>> array([0.00000000e+00, 5.61018496e-02, 1.12203699e-01, ...,
               2.53683462e+03, 2.53689072e+03, 2.53694682e+03], len=8404)'''
    
    # table to refer mecator_id -> zenith angle
    f_angle = interp1d(mecator_coord_zero, select_angle, fill_value="extrapolate")
    mecator_angle = f_angle(xnew)
    
    ww, hh = np.meshgrid(w_id, mecator_id) # shape (8404, 5376)
    
    img_out = np.zeros((*hh.shape, 3))
    for i in range(0 ,3):
        img_out[:,:,i] = ndimage.map_coordinates(select_img[:,:,i], 
                                                 np.array([hh,ww]),output=float,order=1)
    
    img_out = np.hstack((img_out[:,gcp:, :], img_out[:,0:gcp, :]))
    return img_out, mecator_angle
    
if __name__ == '__main__':
    '''
    t = time.time()
    test_out, m2a = mecator_conversion('img/test.JPG', zenith=85, equalize=True)
    print(time.time() - t)
    '''

    t = time.time()
    test_out, m2a = mecator_conversion('raw_imgs/test.JPG', zenith=89, equalize=False, gcp=400)
    print(time.time() - t)
    
    np.savetxt("m2a.csv", m2a, delimiter=",")

    imageio.imwrite('out_89_eq.jpg', test_out)