from PIL import ExifTags
from PIL import Image
#from GPSPhoto import gpsphoto

def getCamInfo(img_dir):#img=Image.open(Imagedir)
    img = Image.open(img_dir)

    exif_human = {ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS}
    
    #data = gpsphoto.getGPSData(img_dir)
    data = None
    
    with open(img_dir, 'rb') as fd:
        d= fd.read()
        print(d.decode('utf-8', 'ignore'))
        #xmp_start = d.find('<x:xmpmeta')
        #xmp_end = d.find('</x:xmpmeta')
        #xmp_str = d[xmp_start:xmp_end+12]
        #print(xmp_str)
    '''
    # XResolution = exif_human['XResolution'][0]
    # YResolution = exif_human['YResolution'][0]
    if exif_human['FocalLength'][1]==0: # lack data
        FocalLength = 0
    else:
        FocalLength = exif_human['FocalLength'][0]/exif_human['FocalLength'][1] # mm
    if exif_human['FocalPlaneResolutionUnit'] == 2: # inch(default)
        FPX = exif_human['FocalPlaneXResolution'][1] * 2.54/100 # mm
        FPY = exif_human['FocalPlaneYResolution'][1] * 2.54/100 # mm
    else:
        FPX = str(exif_human['FocalPlaneXResolution'][1])+'mm'
        FPY = str(exif_human['FocalPlaneYResolution'][1])+'mm'
    info = {'Size': img.size,
            # 'YResolution': YResolution,
            # 'XResolution': XResolution,
            'FocalLength': FocalLength,
            'FPX':FPX,
            'FPY':FPY,
            'Model': exif_human['Model'],
            }
            '''
    return exif_human, data
    
if __name__ == '__main__':
    info, data = getCamInfo('raw_imgs/test.JPG')
    for key, item in info.items():
        if len(str(item)) <= 200:
            print(key, ':', item)
        else:
            print(key, ':', str(item)[:200]+'...')
            
    for key, item in info['GPSInfo'].items():
        # degree, minuts, sceonds
        # 2 : ((45, 1), (56, 1), (4682, 100))
        # True North direction.
        #16 : T
        #17 : (2700, 10)
        print(key, ':', item)
        
    #print(data)
