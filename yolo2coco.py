import os
import json
json.encoder.FLOAT_REPR = lambda x: format(x, '.2f')
import cv2
import argparse

def cxcywh2xywh(cx, cy, w, h):
    x = cx - w / 2
    y = cy - h / 2
    return x, y, w, h

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
    
    # init coco dataset
    coco_result = {'images': [], 'annotations': [], "categories": []}
    save_img_dir = os.path.join(opts.dst, 'images')
    if not os.path.exists(save_img_dir):
        os.makedirs(save_img_dir)
    img_count = 0
    # add category info
    for i, category in enumerate(class_names):
        coco_result['categories'].append({'name': category, 'id': i + 1})

    # traverse yolo format dataset
    for _, _, files in os.walk(src_img_dir):
        for fname in files:
            img_count += 1
            prefix = os.path.splitext(fname)[0]
            src_img_path = os.path.join(src_img_dir, fname)
            src_label_path = os.path.join(src_label_dir, prefix + '.txt')

            # get img info
            img = cv2.imread(src_img_path)
            img_h, img_w = img.shape[:2]
            dst_img_path = os.path.join(save_img_dir, fname)
            os.symlink(src_img_path, dst_img_path)      # use symbolic link instead of copying

            img_info = {'file_name': fname, 'id': img_count, 'height': img_h, 'width': img_w}
            coco_result['images'].append(img_info)

            # read annotation
            with open(src_label_path, 'rt') as f:
                lines = f.readlines()
                for line in lines:
                    data = line.strip().split(' ')
                    category = int(data[0]) + 1
                    cx = float(data[1]) * img_w
                    cy = float(data[2]) * img_h
                    w = float(data[3]) * img_w
                    h = float(data[4]) * img_h
                    x, y, w, h = cxcywh2xywh(cx, cy, w, h)
                    bbox = [round(val, 2) for val in [x, y, w, h]]
                    annotation = {'image_id': img_count,
                                  'id': int(len(coco_result['annotations']) + 1),
                                  'category_id': category,
                                  'bbox': bbox}
                    coco_result['annotations'].append(annotation)

    print("number of images: ", len(coco_result['images']))
    print("number of bboxes: ", len(coco_result['annotations']))
    save_label_dir = os.path.join(opts.dst, "annotations")
    if not os.path.exists(save_label_dir):
        os.mkdir(save_label_dir)
    save_label_path = os.path.join(save_label_dir, opts.stage + '.json')
    json.dump(coco_result, open(save_label_path, 'w'))