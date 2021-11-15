class Graphic:

    def __init__(self, img):
        self.img = img

    def get(self):
        return self.img

    def get_with_edge(self):
        return self.get()

    def __len__(self):
        return 1
