# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 13:34:33 2021

@author: vinbert
"""



import os
import shutil
from tqdm import tqdm
 
from read_json_anno import ReadAnno
from create_xml_anno import CreateAnno

def move_file(old_path, new_path, file_type="json"):
    for filename in os.listdir(old_path):
        if filename.split(".")[-1] == file_type:
            old_path_name = os.path.join(old_path, filename)
            new_path_name = os.path.join(new_path, filename)
            shutil.move(old_path_name, new_path_name)
 
def json_transform_xml(json_path, xml_path, process_mode="rectangle"):
    json_path = json_path
    json_anno = ReadAnno(json_path, process_mode=process_mode)
    width, height = json_anno.get_width_height()
    filename = json_anno.get_filename()
    coordis = json_anno.get_coordis()
 
    xml_anno = CreateAnno()
    xml_anno.add_filename(filename)
    xml_anno.add_pic_size(width_text_str=str(width), height_text_str=str(height), depth_text_str=str(3))
    for xmin,ymin,xmax,ymax,label in coordis:
        xml_anno.add_object(name_text_str=str(label),
                            xmin_text_str=str(int(xmin)),
                            ymin_text_str=str(int(ymin)),
                            xmax_text_str=str(int(xmax)),
                            ymax_text_str=str(int(ymax)))
 
    xml_anno.save_doc(xml_path)
 
if __name__ == "__main__":
    
    # youcha_img_data = r"C:\Users\vinbert\Desktop\youcha_data\images"
    # if not os.path.exists(youcha_img_data):
    #     os.makedirs(youcha_img_data)
    # youcha_json_data = r"C:\Users\vinbert\Desktop\youcha_data\json_data"
    # if not os.path.exists(youcha_json_data):
    #     os.makedirs(youcha_json_data)
    # filename_list = ["DJI_0525", "DJI_0606"]
    # root_path = r"C:\Users\vinbert\Desktop"
    # for f in filename_list:
    #     subfile_path = os.path.join(root_path, f)
    #     move_file(subfile_path, youcha_img_data, file_type="jpg")
    #     move_file(subfile_path, youcha_json_data, file_type="json")
    
    root_json_dir = r"C:\Users\vinbert\Desktop\youcha_all\json_file"
    root_save_xml_dir = r"C:\Users\vinbert\Desktop\youcha_all\annotations"
    if not os.path.exists(root_save_xml_dir):
        os.makedirs(root_save_xml_dir)
    for json_filename in tqdm(os.listdir(root_json_dir)):
        json_path = os.path.join(root_json_dir, json_filename)
        save_xml_path = os.path.join(root_save_xml_dir, json_filename.replace(".json", ".xml"))
        json_transform_xml(json_path, save_xml_path, process_mode="rectangle")

