from parser.yolo_parser import YOLOParser
from parser.coco_parser import COCOParser
from parser.voc_parser import VOCParser

def get_parser(input_format):
    if input_format == 'yolo':
        return YOLOParser()
    elif input_format == 'coco':
        return COCOParser()
    elif input_format == 'voc':
        return VOCParser()
    else:
        raise NotImplementedError('format {:s} not supported'.format(input_format))

