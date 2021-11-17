from abc import abstractmethod


class Parser:
    def __init__(self):
        pass
    
    @abstractmethod
    def parse(self, src_dir, subset, class_file=None):
        pass

    
