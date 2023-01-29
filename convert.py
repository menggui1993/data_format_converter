from parser.get_parser import get_parser
from generator.get_generator import get_generator
import argparse


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--input_format', type=str, choices=['yolo', 'voc', 'coco'], help='input dataset format')
    argparser.add_argument('--input_dir', type=str, help='input dataset root dir')
    argparser.add_argument('--output_format', type=str, choices=['yolo', 'voc', 'coco'], help='output dataset format')
    argparser.add_argument('--output_dir', type=str, help='output dataset root dir')
    argparser.add_argument('--subset', type=str, help='data subset to process')
    argparser.add_argument('--class_file', type=str, default=None, help='file contains class names')
    argparser.add_argument('--copy_img', type=bool, default=False, help='whether to copy images or create soft link of images')
    opts = argparser.parse_args()

    parser = get_parser(opts.input_format)
    generator = get_generator(opts.output_format)
    
    ir = parser.parse(opts.input_dir, opts.subset, opts.class_file)
    generator.generate(ir, opts.output_dir, opts.subset, opts.copy_img)
    