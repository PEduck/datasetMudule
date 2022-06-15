import glob
import pandas as pd
import os


def check_syslink(root, mode='images'):
    subfix = '.txt' if mode=='labels' else '.jpg'
    flag_list = [os.path.isfile(os.readlink(p)) for p in glob.glob(f'{root}/{mode}/*/*{subfix}')]
    txt_df = pd.DataFrame()
    txt_df['flag'] = flag_list
    return txt_df.value_counts('flag')


