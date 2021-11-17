from generator.yolo_generator import YOLOGenerator
from generator.voc_generator import VOCGenerator
from generator.coco_generator import COCOGenerator

def get_generator(output_format):
    if output_format == 'yolo':
        return YOLOGenerator()
    elif output_format == 'voc':
        return VOCGenerator()
    elif output_format == 'coco':
        return COCOGenerator()
    else:
        raise NotImplementedError('format {:s} not supported'.format(output_format))