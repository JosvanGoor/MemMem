import cv2
import os
import sys

import preprocessing as pp
import linesegment as ls

class Image:
    
    def __init__(self, folder, filename):
        self.folder = folder
        self.filename = filename

        self.image = None
        self.lines = []

    def load_processed(self):
        print("Loading {}/{}... ".format(self.folder, self.filename), end="")
        filename = "{}/{}".format(self.folder, self.filename)
        image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        image2 = pp.get_gauss_otsu(image)

        rect, mask = pp.get_page_rect_mask(image2)

        image = (image * (mask // 255))
        image = pp.subimage(image, rect)
        image2 = pp.get_gauss_otsu(image)
        self.image = pp.fill_white(image2)
        print("done!")

    def segment_lines(self):
        print("Segmenting {}/{}... ".format(self.folder, self.filename), end="")
        self.lines = ls.segmentLine(self.image)
        self.lines = [ls.getSeg(self.image, x, y) for x, y in self.lines]
        print("done!")

def list_files(directory):
    if not os.path.isdir(directory):
        print("{} is not a valid directory")
        sys.exit(-2)
    
    return os.listdir(directory)

if __name__ == "__main__":
    if sys.version_info[0] < 3:
        print("Please use python 3...")
        print("    Example usage: python3 path/to/directory/")
        sys.exit(-1)

    if not len(sys.argv) == 2:
        print("Incorrect ammount of arguments, required: 1")
        print("    Example usage: python3 path/to/directory/")
        sys.exit(-1)

    directory = sys.argv[1]
    files = list_files(directory)
    
    images = [Image(directory, f) for f in files]
    for img in images:
        img.load_processed()
        img.segment_lines()

    for x in images[0].lines:
        cv2.imshow("abc", x)