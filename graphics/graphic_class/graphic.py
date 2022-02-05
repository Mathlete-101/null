class Graphic:

    def __init__(self, img):
        self.img = img

    def get(self):
        return self.img

    def get_with_edge(self):
        return self.get()

    def get_on(self):
        return self.get()

    def get_off(self):
        return self.get()

    def get_all(self):
        return [self.get()]

    def __len__(self):
        return 1
