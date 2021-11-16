import os
import json
import argparse

def xywh2cxcywh(x, y, w, h):
    cx = x + w / 2
    cy = y + h / 2
    return cx, cy, w, h

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', type=str, help="source voc directory")
    parser.add_argument('--dst', type=str, help="destination yolo directory")
    parser.add_argument('--stage', type=str, choices=['train', 'val'], help='data split, train or val')
    opts = parser.parse_args()

    if not os.path.exists(opts.dst):
        os.makedirs(opts.dst)

    src_img_dir = os.path.join(opts.src, 'images')
    f = open(os.path.join(opts.src, 'annotations', opts.stage + '.json'), encoding='utf-8')
    coco_labels = json.load(f)
    f.close()
    
    class_names = [category['name'] for category in coco_labels['categories']]
    with open(os.path.join(opts.dst, 'classes.txt'), 'w') as f:
        for class_name in class_names:
            f.write(class_name + '\n')

    images = coco_labels['images']
    annotations = coco_labels['annotations']
    sorted(images, key=lambda x:x['id'])
    sorted(annotations, key=lambda x:x['image_id'])

    save_img_dir = os.path.join(opts.dst, opts.stage, 'images')
    if not os.path.exists(save_img_dir):
        os.makedirs(save_img_dir)
    save_label_dir = os.path.join(opts.dst, opts.stage, 'labels')
    if not os.path.exists(save_label_dir):
        os.makedirs(save_label_dir)

    anno_count = 0
    for image in images:
        fname = image['file_name']
        img_w = image['width']
        img_h = image['height']
        image_id = image['id']
        prefix = os.path.splitext(fname)[0]
        src_img_path = os.path.join(src_img_dir, fname)
        save_img_path = os.path.join(save_img_dir, fname)
        os.symlink(src_img_path, save_img_path)
        save_label_path = os.path.join(save_label_dir, prefix + '.txt')
        label_file = open(save_label_path, 'w')

        while anno_count < len(annotations) and annotations[anno_count]['image_id'] <= image_id:
            if annotations[anno_count]['image_id'] == image_id:
                x, y, w, h = annotations[anno_count]['bbox']
                category = annotations[anno_count]['category_id'] - 1
                cx, cy, w, h = xywh2cxcywh(x, y, w, h)
                cx /= img_w
                cy /= img_h
                w /= img_w
                h /= img_h
                label_file.write("{:d} {:f} {:f} {:f} {:f}\n".format(category, cx, cy, w, h))
            anno_count += 1
        label_file.close()
        if anno_count >= len(annotations):
            break
