import glob


crops_troot = '/nas/chenyi/datasets_cls/gallery_detect/gallery_oss/dadetv4/gall_dadetv4_all/crops_oss'
crop_list = glob.glob(crops_troot + '/*/*/*.jpg')
print(len(crop_list))


