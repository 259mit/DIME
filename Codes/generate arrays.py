#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def getpaths(path):
    train_path_pcr = path
    train_dcm_pcr = []
    train_dcm_pcr_main = []
    for i in range(1,84):
        if i<10:
            for j in range(0,21):
                if j==0:
                    train_dcm_pcr.append(train_path_pcr+'0'+str(i)+'.dcm')
                else:
                                        
                                train_dcm_pcr.append(train_path_pcr+'0'+str(i)+' '+'('+str(j)+')'+'.dcm')
        else:   
            for j in range(0,21):
                if j==0:
                    train_dcm_pcr.append(train_path_pcr+str(i)+'.dcm')
                else:
                                train_dcm_pcr.append(train_path_pcr+str(i)+' '+'('+str(j)+')'+'.dcm')

    length_to_split = [21]*83
    train_dcm_pcr_main = [list(islice(train_dcm_pcr, elem))
              for elem in length_to_split]

    return train_dcm_pcr_main

def load_scan():
    slices = [dicom.read_file(s) for s in train_dcm_pcr_main[0]]
    slices.sort(key = lambda x: int(x.InstanceNumber))
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
        
    for s in slices:
        s.SliceThickness = slice_thickness
        
    return slices

def get_pixels_hu(scans):
    image = np.stack([s.pixel_array for s in scans])
    # Convert to int16 (from sometimes int16), 
    # should be possible as values should always be low enough (<32k)
    image = image.astype(np.int16)

    # Set outside-of-scan pixels to 1
    # The intercept is usually -1024, so air is approximately 0
    image[image == -2000] = 0
    
    # Convert to Hounsfield units (HU)
    intercept = scans[0].RescaleIntercept
    slope = scans[0].RescaleSlope
    
    if slope != 1:
        image = slope * image.astype(np.float64)
        image = image.astype(np.int16)
        
    image += np.int16(intercept)
    
    return np.array(image, dtype=np.int16)

id=0
patient = load_scan()
imgs = get_pixels_hu(patient)

