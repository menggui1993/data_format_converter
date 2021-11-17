from abc import abstractmethod

class Generator:
    def __init__(self):
        pass
    
    @abstractmethod
    def generate(self, ir, out_dir, subset):
        pass