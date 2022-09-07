from xml.dom.minidom import Document
import os
import cv2
from pathlib import Path
import glob
from tqdm import tqdm



# class XMLWriter:
#     def __init__(self, data):
#         self.data = data
    
#     def write_xml_df(self):
#         xml_write_df = bboxes_df
#         label_name = 'labelimg'
#         xml_write_df['label_xml'] = xml_write_df['labelimg'].values
#         bboxes_gp = xml_write_df.groupby('stem')
#     dataset = 'deploy_manual_sep'
#     xml_write_df['xml_tp'] = xml_write_df['xml_path'].apply(lambda p: Path(str(p).replace('/deploy_manual_sep/xml/', '/deploy_manual_sep/xml_rewrite/')))


for item in tqdm(bboxes_gp):
    stem = item[0]
    rows = item[1]
    path, xml_tp, Pheight, Pwidth, Pdepth = rows.loc[:,['xml_path', 'xml_tp', 'width', 'height']].values[0, :].tolist() + [3]
    path, xml_tp = Path(path), Path(xml_tp)
    name_img = path.name
    bboxes = rows.loc[:,['label_xml', 'bx1', 'bx2', 'bx3', 'bx4']].values
    
    xmlBuilder = Document()
    annotation = xmlBuilder.createElement("annotation")  # 创建annotation标签
    xmlBuilder.appendChild(annotation)
    flag = 0
    for oneline in iter(bboxes):
        flag += 1
        
        folder = xmlBuilder.createElement("folder")  # folder标签
        folderContent = xmlBuilder.createTextNode(dataset)
        folder.appendChild(folderContent)
        annotation.appendChild(folder)
        if flag == 1:
            filename = xmlBuilder.createElement("filename")  # filename标签
            filenameContent = xmlBuilder.createTextNode(name[0:-4]+".jpg")
            filename.appendChild(filenameContent)
            annotation.appendChild(filename)

            size = xmlBuilder.createElement("size")  # size标签
            width = xmlBuilder.createElement("width")  # size子标签width
            widthContent = xmlBuilder.createTextNode(str(Pwidth))
            width.appendChild(widthContent)
            size.appendChild(width)
            height = xmlBuilder.createElement("height")  # size子标签height
            heightContent = xmlBuilder.createTextNode(str(Pheight))
            height.appendChild(heightContent)
            size.appendChild(height)
            depth = xmlBuilder.createElement("depth")  # size子标签depth
            depthContent = xmlBuilder.createTextNode(str(Pdepth))
            depth.appendChild(depthContent)
            size.appendChild(depth)
            annotation.appendChild(size)

        object = xmlBuilder.createElement("object")
        picname = xmlBuilder.createElement("name")
        nameContent = xmlBuilder.createTextNode(oneline[0])
        picname.appendChild(nameContent)
        object.appendChild(picname)
        pose = xmlBuilder.createElement("pose")
        poseContent = xmlBuilder.createTextNode("Unspecified")
        pose.appendChild(poseContent)
        object.appendChild(pose)
        truncated = xmlBuilder.createElement("truncated")
        truncatedContent = xmlBuilder.createTextNode("0")
        truncated.appendChild(truncatedContent)
        object.appendChild(truncated)
        difficult = xmlBuilder.createElement("difficult")
        difficultContent = xmlBuilder.createTextNode("0")
        difficult.appendChild(difficultContent)
        object.appendChild(difficult)
        bndbox = xmlBuilder.createElement("bndbox")
        xmin = xmlBuilder.createElement("xmin")
        mathData=int(oneline[1])
        xminContent = xmlBuilder.createTextNode(str(mathData))
        xmin.appendChild(xminContent)
        bndbox.appendChild(xmin)
        ymin = xmlBuilder.createElement("ymin")
        mathData = int(oneline[2])
        yminContent = xmlBuilder.createTextNode(str(mathData))
        ymin.appendChild(yminContent)
        bndbox.appendChild(ymin)
        xmax = xmlBuilder.createElement("xmax")
        mathData = int(oneline[3])
        xmaxContent = xmlBuilder.createTextNode(str(mathData))
        xmax.appendChild(xmaxContent)
        bndbox.appendChild(xmax)
        ymax = xmlBuilder.createElement("ymax")
        mathData = int(oneline[4])
        ymaxContent = xmlBuilder.createTextNode(str(mathData))
        ymax.appendChild(ymaxContent)
        bndbox.appendChild(ymax)
        object.appendChild(bndbox)

        annotation.appendChild(object)
    
    if xml_tp.is_file(): continue
    if not xml_tp.parent.is_dir(): xml_tp.parent.mkdir(parents=True)
    f = open(xml_tp, 'w')
    xmlBuilder.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
    f.close()
#     break
