


def bbox_yolo2voc(bx, w, h):
    x_c = float(bx[0])*w
    y_c = float(bx[1])*h
    wbbox = float(bx[2])*w
    hbbox = float(bx[3])*h
    x1 = int(x_c - wbbox/2)
    y1 = int(y_c - hbbox/2)
    x2 = int(x_c + wbbox/2)
    y2 = int(y_c + hbbox/2)
    bbox = [x1, y1, x2, y2]
    return bbox


def bbox_voc2yolo(bx, w, h):
    x1 = bx[0]
    y1 = bx[1]
    x2 = bx[2]
    y2 = bx[3]
    w_bbox = x2 - x1
    h_bbox = y2 - y1
    x_c = x1 + w_bbox/2
    y_c = y1 + h_bbox/2
    bbox = [x_c/w, y_c/h, w_bbox/w, h_bbox/h]
    return bbox


def bbox_coco2voc(bbox):
    bbox[2] = bbox[0] + bbox[2]
    bbox[3] = bbox[1] + bbox[3]
    return bbox


def bbox_voc2yolo_df(df):
    w =  df['width'].values
    h =  df['height'].values
    w_bbox = df['bx3'].values - df['bx1'].values
    h_bbox = df['bx4'].values - df['bx2'].values
    x_c = df['bx1'].values + w_bbox/2
    y_c = df['bx2'].values + h_bbox/2
    df.loc[:, 'bx1'] = x_c/w
    df.loc[:, 'bx2'] = y_c/h
    df.loc[:, 'bx3'] = w_bbox/w
    df.loc[:, 'bx4'] = h_bbox/h    
    return df

