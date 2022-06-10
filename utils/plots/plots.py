import cv2


def draw_bbox(img_np, box_coco, fontScale=1):
    id_ = str(box_coco[0])
    x1 = int(box_coco[1])
    y1 = int(box_coco[2])
    x2 = int(box_coco[3])
    y2 = int(box_coco[4])
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.rectangle(img_np,(x1, y1),(x2, y2),(0,0,255),thickness=2)
    f = cv2.putText(img_np, text=str(id_), org=(x1 + 5, y1 + 5), fontFace=font, fontScale=fontScale, 
        thickness=2, lineType=cv2.LINE_AA, color=(0, 255, 0))
    return img_np