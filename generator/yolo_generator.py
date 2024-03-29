from generator.generator import Generator
from ir import IR
import os
import shutil

def xywh2cxcywh(x, y, w, h):
    cx = x + w / 2
    cy = y + h / 2
    return cx, cy, w, h

class YOLOGenerator(Generator):
    def __init__(self):
        super(YOLOGenerator, self).__init__()

    def generate(self, ir, out_dir, subset, copy_img):
        out_img_dir = os.path.join(out_dir, subset)
        out_anno_dir = os.path.join(out_dir, subset)
        out_class_file = os.path.join(out_dir, 'classes.txt')
        out_list_file = os.path.join(out_dir, subset + ".txt")

        if not os.path.exists(out_img_dir):
            os.makedirs(out_img_dir)
        if not os.path.exists(out_anno_dir):
            os.makedirs(out_anno_dir)

        # write class list
        with open(out_class_file, 'w') as f:
            for class_name in ir.class_names:
                f.write(class_name + '\n')
        
        out_list = open(out_list_file, 'w')
        for img_info in ir.img_lists:
            img_w, img_h = img_info[0]
            src_img_path = img_info[1]
            bboxes = img_info[2]
            img_name = os.path.split(src_img_path)[-1]
            out_img_path = os.path.join(out_img_dir, img_name)
            if copy_img:
                shutil.copyfile(src_img_path, out_img_path)
            else:
                os.symlink(src_img_path, out_img_path)

            anno_name = os.path.splitext(img_name)[0] + '.txt'
            out_anno_path = os.path.join(out_anno_dir, anno_name)
            with open(out_anno_path, 'w') as f:
                for category, x, y, w, h in bboxes:
                    cx, cy, w, h = xywh2cxcywh(x, y, w, h)
                    cx /= img_w
                    cy /= img_h
                    w /= img_w
                    h /= img_h
                    f.write('{:d} {:f} {:f} {:f} {:f}\n'.format(category, cx, cy, w, h))
            out_list.write(out_img_path + '\n')
        out_list.close()