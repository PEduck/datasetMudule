from lxml import etree


def parse_xml(p):
    trees = etree.parse(str(p))
    width, height = int(trees.find('size/width').text), int(trees.find('size/height').text)
    bboxes = []
    for obj in trees.findall('object'):
        bx = []
        bx.append(p)
        bx.append(int(width))
        bx.append(int(height))
        bdb = obj.find('bndbox')
        bx.append(obj.find('name').text)
        bx.append(int(bdb.find('xmin').text))
        bx.append(int(bdb.find('ymin').text))
        bx.append(int(bdb.find('xmax').text))
        bx.append(int(bdb.find('ymax').text))
        bboxes.append(bx)
    return bboxes

