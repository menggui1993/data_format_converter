from generator.generator import Generator
from ir import IR
import os
import shutil
import json

class COCOGenerator(Generator):
    def __init__(self):
        super(COCOGenerator, self).__init__()
    
    def generate(self, ir, out_dir, subset):
        out_img_dir = os.path.join(out_dir, 'images')
        out_anno_dir = os.path.join(out_dir, 'annotations')

        if not os.path.exists(out_img_dir):
            os.makedirs(out_img_dir)
        if not os.path.exists(out_anno_dir):
            os.makedirs(out_anno_dir)

        coco_data = {'images': [], 'annotations': [], "categories": []}

        for i, category in enumerate(ir.class_names):
            coco_data['categories'].append({'name': category, 'id': i + 1})
        
        img_count = 0
        for img_info in ir.img_lists:
            img_count += 1
            img_w, img_h = img_info[0]
            src_img_path = img_info[1]
            bboxes = img_info[2]
            img_name = os.path.split(src_img_path)[-1]
            out_img_path = os.path.join(out_img_dir, img_name)
            if copy_img:
                shutil.copyfile(src_img_path. out_img_path)
            else:
                os.symlink(src_img_path, out_img_path)

            img_data = {'file_name': img_name, 'id': img_count, 'height': img_h, 'width': img_w}
            coco_data['images'].append(img_data)

            for category, x, y, w, h in bboxes:
                bbox = [round(val, 2) for val in [x, y, w, h]]
                annotation = {'image_id': img_count,
                              'id': int(len(coco_data['annotations']) + 1),
                              'category_id': category + 1,
                              'bbox': bbox}
                coco_data['annotations'].append(annotation)

        out_anno_file = open(os.path.join(out_anno_dir, subset + '.json'), 'w')
        json.dump(coco_data, out_anno_file)