import numpy as np
import h5py
import os, sys, traceback
import os.path as osp
import wget, tarfile
import cv2
from PIL import Image

def get_data(path):
    return h5py.File(path, 'r')


def add_more_data_into_dset(DB_FNAME, more_img_file_path, more_depth_path, more_seg_path):
    db = h5py.File(DB_FNAME, 'w')
    depth_db = get_data(more_depth_path)
    print(len(depth_db.keys()))
    seg_db = get_data(more_seg_path)
    print(len(seg_db['mask'].keys()))
    db.create_group('image')
    db.create_group('depth')
    db.create_group('seg')
    for imname in os.listdir(more_img_file_path):
        if imname.endswith('.jpg'):
            full_path = more_img_file_path + imname
            print(full_path, imname)

            j = Image.open(full_path)
            imgSize = j.size
            rawData = j.tostring()
            img = Image.fromstring('RGB', imgSize, rawData)
            # img = img.astype('uint16')
            db['image'].create_dataset(imname, data=img)
            db['depth'].create_dataset(imname, data=depth_db[imname])
            db['seg'].create_dataset(imname, data=seg_db['mask'][imname])
            db['seg'][imname].attrs['area'] = seg_db['mask'][imname].attrs['area']
            db['seg'][imname].attrs['label'] = seg_db['mask'][imname].attrs['label']
    db.close()
    depth_db.close()
    seg_db.close()


# path to the data-file, containing image, depth and segmentation:
DB_FNAME = 'dset_8000.h5'

# add more data into the dset
more_depth_path = 'depth.h5'
more_seg_path = 'seg.h5'
more_img_file_path = 'bg_img/'

add_more_data_into_dset(DB_FNAME, more_img_file_path, more_depth_path, more_seg_path)
