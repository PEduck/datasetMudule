'''
Descripttion: Chen Y's project
version: 1.0
Author: Chen Y
Date: 2022-08-19 11:23:47
LastEditors: Please set LastEditors
LastEditTime: 2022-08-19 18:42:33
'''

import hashlib
from joblib import Parallel, delayed
import pandas as pd
from pathlib import Path
import cv2
from tqdm import tqdm
import re


def data_load(root_origin, depth=2):
    '''加载数据.

    Args:
        root_origin: 原始数据路径。
        depth: 图片文件夹的存储层级深度。

    Returns:
        df: DataFrame,数据信息。

    Raises:
        Error: 图片数据为0。
    '''

    df = pd.DataFrame(columns=['path'])  
    df['path'] = list(Path(root_origin).rglob('*.jpg')) 
    df['eaDir'] = df['path'].apply(lambda x: bool(len(re.findall(r'/@eaDir', str(x)))))
    df = df[~df['eaDir']]
    df = df.drop(columns=['eaDir'])
    assert len(df) > 0, '未找到图片，请核对图片路径。'
    return df


def source_data_clear(df, thres=300):
    '''对原数据进行清洗去重.

    Args:
        thres: 分辨率阈值。

    Returns:
        df: DataFrame,清洗后的图片信息。

    '''

    print('检查图片是否损坏...')
    # 是否调用多线程
    if len(df) > 1e4:
        df['res'] = Parallel(n_jobs=8)(
            delayed(readimg_flag)(path) for path in tqdm(df['path'].values)
        )
    else:
        df['res'] = df['path'].apply(lambda x: readimg_flag(x))

    print('完成图片损坏检查.')
    df['flag'] = [r[2] for r in df['res']]
    df = df[df['flag']].copy()

    # 分辨率大小
    df['height'] = [r[0] for r in df['res']]
    df['width'] = [r[1] for r in df['res']]
    df['width'] = df['width'].astype(int)
    df['height'] = df['height'].astype(int)
    df = df[(df['width'] >= thres) & (df['height'] >= thres)]
    print('完成图片分辨率检查.')

    # 去重
    # 是否调用多线程
    if len(df) > 1e4:
        df['sha256'] = Parallel(n_jobs=8)(
            delayed(sha256sum)(path) for path in tqdm(df['path'].to_numpy())
        )
    else:
        df['sha256'] = df['path'].apply(lambda x: sha256sum(x))

    clred_df = df.drop_duplicates('sha256')
    clred_df = clred_df.drop(columns=['sha256', 'res', 'flag'])
    imgs_num = len(clred_df)
    assert imgs_num > 0, '去重后图片数量不足。'
    print(f'完成图片去重,去重后图片数量是{imgs_num}.')
    return clred_df


def readimg_flag(p):
    try:
        h, w, c = cv2.imread(str(p)).shape
        flag = True if c == 3 else False
    except:
        h, w = None, None
        flag = False
    return h, w, flag


def sha256sum(path):
    sha256 = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def save_crops(save_df, root_result, img_type='', DEBUG=False):
    root_result = Path(root_result)
    save_np = save_df[['img_sp', 'bx1', 'bx2', 'bx3', 'bx4', 'label_pred']].values

    for line in tqdm(save_np):
        p = Path(line[0])
        # print(p, p.is_file())
        label = str(line[-1])
        tp = (
            root_result
            / p.parts[-4]
            / p.parts[-3]
            / p.parts[-2]
            / 'crops'
            / label
            / img_type
            / p.name
        )
        if tp.is_file():
            continue
        img = cv2.imread(str(p))
        if not tp.parent.is_dir():
            tp.parent.mkdir(parents=True, exist_ok=True)
        crops = img[int(line[2]) : int(line[4]), int(line[1]) : int(line[3]), :]
        cv2.imwrite(str(tp), crops)
    crops_num = len(save_np)
    print(f'保存最终裁切的{img_type}小图.数量为:{crops_num}')
