import os
import argparse
import xml.etree.ElementTree as ET

def xyxy2cxcywh(x1, y1, x2, y2):
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2
    w = x2 - x1
    h = y2 - y1
    return cx, cy, w, h

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', type=str, help="source voc directory")
    parser.add_argument('--dst', type=str, help="destination yolo directory")
    parser.add_argument('--class_list', type=str, help="class list file")
    parser.add_argument('--stage', type=str, choices=['train', 'val'], help='data split, train or val')
    opts = parser.parse_args()

    if not os.path.exists(opts.dst):
        os.makedirs(opts.dst)

    # read classes
    class_names = []
    with open(opts.class_list, 'rt') as f:
        names = f.readlines()
        class_names = [name.strip() for name in names]
    print("classes:", class_names)
    with open(os.path.join(opts.dst, 'classes.txt'), 'w') as f:
        for class_name in class_names:
            f.write(class_name + '\n')

    src_img_dir = os.path.join(opts.src, 'JPEGImages', opts.stage)
    src_label_dir = os.path.join(opts.src, 'Annotations', opts.stage)
    src_list = open(os.path.join(opts.src, 'ImageSets', 'Main', opts.stage + '.txt'), 'r')

    dst_img_dir = os.path.join(opts.dst, opts.stage, 'images')
    if not os.path.exists(dst_img_dir):
        os.makedirs(dst_img_dir)
    dst_label_dir = os.path.join(opts.dst, opts.stage, 'labels')
    if not os.path.exists(dst_label_dir):
        os.makedirs(dst_label_dir)

    while True:
        line = src_list.readline()
        if not line:
            break
        prefix = line.strip()
        label_file = open(os.path.join(src_label_dir, prefix + '.xml'))
        tree = ET.parse(label_file)
        label_file.close()
        root = tree.getroot()
        
        img_name = root.find('filename').text
        src_img_path = os.path.join(src_img_dir, img_name)
        dst_img_path = os.path.join(dst_img_dir, img_name)
        os.symlink(src_img_path, dst_img_path)

        save_label_file = open(os.path.join(dst_label_dir, prefix + '.txt'), 'w')
        size = root.find('size')
        img_w = int(size.find('width').text)
        img_h = int(size.find('height').text)

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
            cx, cy, w, h = xyxy2cxcywh(x1, y1, x2, y2)
            cx /= img_w
            cy /= img_h
            w /= img_w
            h /= img_h
            save_label_file.write("{:d} {:f} {:f} {:f} {:f}\n".format(cls_id, cx, cy, w, h))
        save_label_file.close()

    src_list.close()