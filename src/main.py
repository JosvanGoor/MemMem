import cv2
import os
import sys

import preprocessing as pp

def list_files(directory):
    if not os.path.isdir(directory):
        print("{} is not a valid directory")
        sys.exit(-2)
    
    return os.listdir(directory)

def preprocess_page(filename):
    image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    image2 = pp.get_gauss_otsu(image)

    rect, mask = pp.get_page_rect_mask(image2)

    image = (image * (mask // 255))
    image = pp.subimage(image, rect)
    image2 = pp.get_gauss_otsu(image)
    image2 = pp.fill_white(image2)

    return image2

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
    
    files = ["{}/{}".format(directory, f) for f in files]
    images = [preprocess_page(f) for f in files]