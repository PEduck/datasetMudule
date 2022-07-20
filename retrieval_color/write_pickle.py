import glob
import pandas as pd
import numpy as np
from pathlib import Path
from PIL import Image
from tqdm import tqdm
import cv2
import json


def txt_readlines(feat_p):
    with open(feat_p, 'r') as f:
        feat_data = f.readlines()
    return feat_data

def parse_line(line):
    line_list = line.split('\t')
    crop_path = line_list[0]
    feat_list = line_list[1].split(',')
    return crop_path, feat_list
    # return crop_path
    
    
feat_p = '/nas/chenyi/share/xtc/gallery_crop_features_clothes.txt'
feat_data = txt_readlines(feat_p)

data4parse = feat_data[:]
pathes = []
feat_all_list = []
stem2feat = {}
for line in tqdm(data4parse):
    try:
        crop_path, feat_list = parse_line(line)
        crop_path = Path(crop_path)
        stem = f'{crop_path.parts[-2]}/{crop_path.name}'
        stem2feat[stem] = feat_list
    except:
        print(crop_path)
        
        
import pickle 
with open('./data/stem2feature.pickle', 'wb') as f:
    pickle.dump(stem2feat, f)
