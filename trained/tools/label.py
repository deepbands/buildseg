import os
from typing import Callable, Union, List, Tuple
import cv2
import numpy as np
from PIL import Image


def is_image_file(filename: str) -> bool:
    '''Determine whether the input file name is a valid image file name.'''
    ext = os.path.splitext(filename)[-1].lower()
    return ext in ['.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff']


def get_img_file(dir_name: str) -> List[str]:
    '''Get all image file paths in several directories which have the same parent directory.'''
    images = []
    label = set()
    with open('train2.txt', 'w') as f:
        for parent, _, filenames in os.walk(dir_name):
            for filename in filenames:
                if not is_image_file(filename):
                    continue
                img_path = os.path.join(parent, filename)
                img_id = filename.split('.')[0]
                # img_id = "GID5_G126_GF2_PMS2__L1A0001757484-MSS2"
                mask_path ='/home/aistudio/data/dataset/gt/{}.png'.format(img_id)
                # if not os.path.exists(img_path):
                #     f.write(mask_id +'\n')
                #     print(mask_id)
                instance_mask = np.array(Image.open(mask_path).convert('1'))
                # print(instance_mask.shape)
                instance = list(np.unique(instance_mask))
                if len(instance) == 1:
                    continue
                else:
                    flag = []
                    for index in instance:
                        # print("shape:", instance_mask.shape)
                        contours, _ = cv2.findContours(instance_mask.astype("uint8"), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                        cont_areas = [cv2.contourArea(contour) for contour in contours]
                        area = np.sum(instance_mask==index)
                        # print("instance", index, "area", area)
                        if area > 625 and sorted(cont_areas)[-1] > 256:
                            flag.append(1)
                        else:
                            flag.append(0)
                    # print(flag)
                    # raise Exception("**************")
                    if len(flag) == sum(flag):
                        f.write(img_id+'\n')
                    else:
                        print(img_id)        
    return label


if __name__ == "__main__":
    label = get_img_file('/home/aistudio/data/dataset/img')
    print(label)