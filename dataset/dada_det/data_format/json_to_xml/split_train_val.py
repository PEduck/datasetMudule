# -*- coding: utf-8 -*-
"""
Created on Wed Jul  7 17:58:50 2021

@author: vinbert
"""


import os
import shutil

tot_labels_path = r"C:\Users\vinbert\Desktop\citrus\train\labels"
val_labels_path = r"C:\Users\vinbert\Desktop\citrus\val\labels"

val_img_path = r"C:\Users\vinbert\Desktop\citrus\val\images"

for img in os.listdir(val_img_path):
    if img.split(".")[-1] == "JPG":
        label_name = img.replace(".JPG", ".txt")
    else:
        label_name = img.replace(".jpg", ".txt")
    shutil.move(os.path.join(tot_labels_path, label_name), 
                os.path.join(val_labels_path, label_name))