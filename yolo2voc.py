import os
import cv2
import argparse
from xml.dom.minidom import Document

from yolo2coco import cxcywh2xywh

def cxcywh2xyxy(cx, cy, w, h):
    x1 = cx - w / 2
    y1 = cy - h / 2
    x2 = cx + w / 2
    y2 = cy + h / 2
    return x1, y1, x2, y2

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', type=str, help="source voc directory")
    parser.add_argument('--dst', type=str, help="destination yolo directory")
    parser.add_argument('--class_list', type=str, help="class list file")
    parser.add_argument('--stage', type=str, choices=['train', 'val'], help='data split, train or val')
    opts = parser.parse_args()

    # read classes
    class_names = []
    with open(opts.class_list, 'rt') as f:
        names = f.readlines()
        class_names = [name.strip() for name in names]
    print("classes:", class_names)

    src_img_dir = os.path.join(opts.src, opts.stage, 'images')
    src_label_dir = os.path.join(opts.src, opts.stage, 'labels')

    if not os.path.exists(os.path.join(opts.dst, 'ImageSets', 'Main')):
        os.makedirs(os.path.join(opts.dst, 'ImageSets', 'Main'), exist_ok=True)
    if not os.path.exists(os.path.join(opts.dst, 'JPEGImages', opts.stage)):
        os.makedirs(os.path.join(opts.dst, 'JPEGImages', opts.stage))
    if not os.path.exists(os.path.join(opts.dst, 'Annotations', opts.stage)):
        os.makedirs(os.path.join(opts.dst, 'Annotations', opts.stage))

    list_file = open(os.path.join(opts.dst, 'ImageSets', 'Main', opts.stage + '.txt'), 'w')
    save_img_dir = os.path.join(opts.dst, 'JPEGImages', opts.stage)
    save_label_dir = os.path.join(opts.dst, 'Annotations', opts.stage)

    for _, _, files in os.walk(src_img_dir):
        for fname in files:
            prefix = os.path.splitext(fname)[0]
            src_img_path = os.path.join(src_img_dir, fname)
            src_label_path = os.path.join(src_label_dir, prefix + '.txt')

            # get img info
            img = cv2.imread(src_img_path)
            img_h, img_w = img.shape[:2]
            dst_img_path = os.path.join(save_img_dir, fname)
            os.symlink(src_img_path, dst_img_path)      # use symbolic link instead of copying

            list_file.write(prefix + '\n')

            doc = Document()
            annotation = doc.createElement('annotation')
            doc.appendChild(annotation)

            folder = doc.createElement('folder')
            folder.appendChild(doc.createTextNode('fabric'))
            annotation.appendChild(folder)

            filename = doc.createElement('filename')
            filename.appendChild(doc.createTextNode(fname))
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

            # read annotation
            with open(src_label_path, 'rt') as f:
                lines = f.readlines()
                for line in lines:
                    data = line.strip().split(' ')
                    category = int(data[0])
                    cx = float(data[1]) * img_w
                    cy = float(data[2]) * img_h
                    w = float(data[3]) * img_w
                    h = float(data[4]) * img_h
                    x1, y1, x2, y2 = cxcywh2xywh(cx, cy, w, h)
                    x1 = round(x1)
                    y1 = round(y1)
                    x2 = round(x2)
                    y2 = round(y2)

                    obj = doc.createElement('object')
                    name = doc.createElement('name')

                    name.appendChild(doc.createTextNode(class_names[category]))
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

            save_label_path = os.path.join(save_label_dir, prefix + '.xml')
            with open(save_label_path, 'w') as f:
                f.write(doc.toprettyxml(indent='    '))
    
    list_file.close()