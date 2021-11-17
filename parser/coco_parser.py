from parser.parser import Parser
from ir import IR
import os
import json

class COCOParser(Parser):
    def __init__(self):
        super(COCOParser, self).__init__()
    
    def parse(self, src_dir, subset, class_file=None):
        src_img_dir = os.path.join(src_dir, 'images')
        src_anno_path = os.path.join(src_dir, 'annotations', subset + '.json')

        if not os.path.exists(src_img_dir):
            raise FileNotFoundError
        if not os.path.exists(src_anno_path):
            raise FileNotFoundError

        label_file = open(src_anno_path, encoding='utf-8')
        coco_data = json.load(label_file)
        label_file.close()

        class_names = []
        category_id2name = {}
        for category in coco_data['categories']:
            category_id2name[category['id']] = category['name']
            class_names.append(category['name'])
        # print("classes:", class_names)
        
        ir = IR(class_names)    # intermediate representation

        images = coco_data['images']
        annotations = coco_data['annotations']
        sorted(images, key=lambda x:x['id'])
        sorted(annotations, key=lambda x:x['image_id'])

        anno_count = 0
        for image in images:
            img_name = image['file_name']
            img_w = image['width']
            img_h = image['height']
            image_id = image['id']

            src_img_path = os.path.join(src_img_dir, img_name)
            bboxes = []
            while anno_count < len(annotations) and annotations[anno_count]['image_id'] <= image_id:
                if annotations[anno_count]['image_id'] == image_id:
                    x, y, w, h = annotations[anno_count]['bbox']
                    category = class_names.index(category_id2name[annotations[anno_count]['category_id']])
                    bbox = [category, x, y, w, h]
                    bboxes.append(bbox)
                anno_count += 1
            ir.add_img((img_w, img_h), src_img_path, bboxes)
        
        return ir