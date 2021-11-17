class IR:
    def __init__(self, class_names, img_lists=[]):
        self.class_names = class_names
        self.img_lists = img_lists
    
    def add_img(self, size, img_path, bboxes):
        self.img_lists.append((size, img_path, bboxes))