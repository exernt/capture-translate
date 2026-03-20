from manga_ocr import MangaOcr

class ocr:
    def __init__(self):
        self.reader = MangaOcr()

    def readImage(self, path):
        return self.reader(path)
