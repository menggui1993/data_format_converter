from generator.generator import Generator
from ir import IR
import os
import shutil
from xml.dom.minidom import Document

def xywh2xyxy(x, y, w, h):
    x1 = x
    y1 = y
    x2 = x + w
    y2 = y + h
    return x1, y1, x2, y2

class VOCGenerator(Generator):
    def __init__(self):
        super(VOCGenerator, self).__init__()
    
    def generate(self, ir, out_dir, subset, copy_img):
        out_img_dir = os.path.join(out_dir, 'JPEGImages')
        out_anno_dir = os.path.join(out_dir, 'Annotations')
        out_list_file = os.path.join(out_dir, 'ImageSets', 'Main', subset + '.txt')

        if not os.path.exists(out_img_dir):
            os.makedirs(out_img_dir)
        if not os.path.exists(out_anno_dir):
            os.makedirs(out_anno_dir)
        if not os.path.exists(os.path.join(out_dir, 'ImageSets', 'Main')):
            os.makedirs(os.path.join(out_dir, 'ImageSets', 'Main'))

        with open(out_list_file, 'w') as list_file:
            for img_info in ir.img_lists:
                img_w, img_h = img_info[0]
                src_img_path = img_info[1]
                bboxes = img_info[2]
                img_name = os.path.split(src_img_path)[-1]
                fname = os.path.splitext(img_name)[0]
                out_img_path = os.path.join(out_img_dir, img_name)
                if copy_img:
                    shutil.copyfile(src_img_path. out_img_path)
                else:
                    os.symlink(src_img_path, out_img_path)
                list_file.write(fname + '\n')

                anno_name = fname + '.xml'
                out_anno_path = os.path.join(out_anno_dir, anno_name)
                
                doc = Document()
                annotation = doc.createElement('annotation')
                doc.appendChild(annotation)

                filename = doc.createElement('filename')
                filename.appendChild(doc.createTextNode(img_name))
                annotation.appendChild(filename)

                size = doc.createElement('size')
                width = doc.createElement('width')
                width.appendChild(doc.createTextNode(str(img_w)))
                size.appendChild(width)
                height = doc.createElement('height')
                height.appendChild(doc.createTextNode(str(img_h)))
                size.appendChild(height)
                depth = doc.createElement('depth')
                depth.appendChild(doc.createTextNode(str(3)))
                size.appendChild(depth)
                annotation.appendChild(size)

                for category, x, y, w, h in bboxes:
                    x1, y1, x2, y2 = xywh2xyxy(x, y, w, h)
                    x1 = round(x1)
                    y1 = round(y1)
                    x2 = round(x2)
                    y2 = round(y2)

                    obj = doc.createElement('object')
                    name = doc.createElement('name')

                    name.appendChild(doc.createTextNode(ir.class_names[category]))
                    obj.appendChild(name)
                    bndbox = doc.createElement('bndbox')
                    xmin = doc.createElement('xmin')
                    xmin.appendChild(doc.createTextNode(str(x1)))
                    bndbox.appendChild(xmin)
                    ymin = doc.createElement('ymin')
                    ymin.appendChild(doc.createTextNode(str(y1)))
                    bndbox.appendChild(ymin)
                    xmax = doc.createElement('xmax')
                    xmax.appendChild(doc.createTextNode(str(x2)))
                    bndbox.appendChild(xmax)
                    ymax = doc.createElement('ymax')
                    ymax.appendChild(doc.createTextNode(str(y2)))
                    bndbox.appendChild(ymax)
                    obj.appendChild(bndbox)
                    annotation.appendChild(obj)

                with open(out_anno_path, 'w') as f:
                    f.write(doc.toprettyxml(indent='    '))