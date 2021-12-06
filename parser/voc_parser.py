from parser.parser import Parser
from ir import IR
import os
import xml.etree.ElementTree as ET

def xyxy2xywh(x1, y1, x2, y2):
    w = x2 - x1
    h = y2 - y1
    return x1, y1, w, h

class VOCParser(Parser):
    def __init__(self):
        super(VOCParser, self).__init__()

    def parse(self, src_dir, subset, class_file=None):
        src_img_dir = os.path.join(src_dir, 'JPEGImages')
        src_anno_dir = os.path.join(src_dir, 'Annotations')
        src_list_file = os.path.join(src_dir, 'ImageSets', 'Main', subset + '.txt')

        if not os.path.exists(src_img_dir):
            raise FileNotFoundError
        if not os.path.exists(src_anno_dir):
            raise FileNotFoundError
        if not os.path.exists(src_list_file):
            raise FileNotFoundError
        if not os.path.exists(class_file):
            raise FileNotFoundError(class_file)
        
        # read classes
        class_names = []
        with open(class_file, 'rt') as f:
            names = f.readlines()
            class_names = [name.strip() for name in names]
        # print("classes:", class_names)

        src_list = open(src_list_file, 'r')
        ir = IR(class_names)    # intermediate representation

        while True:
            line = src_list.readline()
            if not line:
                break
            prefix = line.strip()
            label_file = open(os.path.join(src_anno_dir, prefix + '.xml'))
            tree = ET.parse(label_file)
            label_file.close()
            root = tree.getroot()
            
            img_name = root.find('filename').text
            src_img_path = os.path.join(src_img_dir, img_name)

            size = root.find('size')
            img_w = int(size.find('width').text)
            img_h = int(size.find('height').text)

            bboxes = []
            for obj in root.iter('object'):
                category = obj.find('name').text
                if category not in class_names:
                    continue
                cls_id = class_names.index(category)
                xmlbox = obj.find('bndbox')
                x1 = float(xmlbox.find('xmin').text)
                y1 = float(xmlbox.find('ymin').text)
                x2 = float(xmlbox.find('xmax').text)
                y2 = float(xmlbox.find('ymax').text)
                x, y, w, h = xyxy2xywh(x1, y1, x2, y2)
                bbox = [cls_id, x, y, w, h]
                bboxes.append(bbox)
            ir.add_img((img_w, img_h), src_img_path, bboxes)

        src_list.close()
        return ir