import numpy as np
import pandas as pd
import glob
import re
from tqdm import tqdm
from pathlib import Path
import sys,os
import shutil


root = Path('/home/chenyi/workspace/dataset/haowei34k/')
save_root = Path('/home/chenyi/workspace/dataset/haowei34k_folders/')
if Path.is_dir(save_root):
    shutil.rmtree(save_root)
else:
    Path.mkdir(save_root, parents=True, exist_ok=True)

imgs_list = glob.glob(str(root /'images/*/*.jpg'))
# labels_list = glob.glob(str(root /'labels/*/*.txt'))
data_info = pd.DataFrame(columns=['img_path', 'label_path'])
data_info['img_path'] = imgs_list
data_info['label_path'] = data_info['img_path'].apply(lambda x: x.replace('images', 'labels'))
data_info['label_path'] = data_info['label_path'].apply(lambda x: x.replace('.jpg', '.txt'))
data_info['img_fname'] = data_info['img_path'].apply(lambda x: 
                                                     re.findall(r'/images/(train|val)/(.*.jpg)', x)[0][1])
data_info['label_fname'] = data_info['img_fname'].apply(lambda x: x.replace('.jpg', '.txt'))

iter_num = 200
for ind, row in tqdm(data_info.iterrows()):
    folder_ind = ind//iter_num
    imgs_froot = save_root / f'images/{folder_ind}/'
    labels_froot = save_root / f'labels/{folder_ind}/'
    if not Path.is_dir(imgs_froot):
        Path.mkdir(imgs_froot, parents=True, exist_ok=True)
    
    if not Path.is_dir(labels_froot):
        Path.mkdir(labels_froot, parents=True, exist_ok=True)
    
    img_fname = row['img_fname']
    label_fname = row['label_fname']
    img_tp = imgs_froot /img_fname
    label_tp = labels_froot /label_fname
    shutil.copyfile(row['img_path'], img_tp)
    shutil.copyfile(row['label_path'], label_tp)

    
    