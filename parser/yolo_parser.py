from parser.parser import Parser
from ir import IR
import os
import cv2

def cxcywh2xywh(cx, cy, w, h):
    x = cx - w / 2
    y = cy - h / 2
    return x, y, w, h

class YOLOParser(Parser):
    def __init__(self):
        super(YOLOParser, self).__init__()

    def parse(self, src_dir, subset, class_file=None):
        src_img_dir = os.path.join(src_dir, subset)
        src_anno_dir = os.path.join(src_dir, subset)

        if not os.path.exists(src_img_dir):
            raise FileNotFoundError
        if not os.path.exists(src_anno_dir):
            raise FileNotFoundError
        if not os.path.exists(class_file):
            raise FileNotFoundError(class_file)
        
        # read classes
        class_names = []
        with open(class_file, 'rt') as f:
            names = f.readlines()
            class_names = [name.strip() for name in names]
        # print("classes:", class_names)
        
        ir = IR(class_names)    # intermediate representation
        
        for _, _, files in os.walk(src_img_dir):
            for img_name in files:
                prefix = os.path.splitext(img_name)[0]
                src_img_path = os.path.join(src_img_dir, img_name)
                src_anno_path = os.path.join(src_anno_dir, prefix + '.txt')

                # get img info
                img = cv2.imread(src_img_path)
                img_h, img_w = img.shape[:2]

                bboxes = []
                # read annotation
                with open(src_anno_path, 'rt') as f:
                    lines = f.readlines()
                    for line in lines:
                        data = line.strip().split(' ')
                        category = int(data[0])
                        cx = float(data[1]) * img_w
                        cy = float(data[2]) * img_h
                        w = float(data[3]) * img_w
                        h = float(data[4]) * img_h
                        x, y, w, h = cxcywh2xywh(cx, cy, w, h)
                        bbox = [category, x, y, w, h]
                        bboxes.append(bbox)
                
                ir.add_img((img_w, img_h), src_img_path, bboxes)

        return ir