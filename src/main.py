import cv2
import os
import pickle
import sys

import numpy

import data
import network as n
import preprocessing as pp
import linesegment as ls

testnames = ["ffilled", "ffilled_crop", "seg0", "seg1", "seg2", "seg3",
            "seg4", "seg5", "seg6", "seg7", "seg8", "seg9", "seg10", "seg11"]
test_pkl = "../outputs/TEST_detections.pkl"
easy_pkl = "../outputs/TEST_boxes_classes.pkl"


def list_files(directory):
    if not os.path.isdir(directory):
        print("{} is not a valid directory")
        sys.exit(-2)
    
    return os.listdir(directory)

if __name__ == "__main__2":
    dat = n.list_characters(testnames, easy_pkl)
    
    for name, chars in dat.items():
        print("File: {}\n    ".format(name), end="")
        for c in chars:
            print("{} ".format(c.name), end="")
        print()
        

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
    
    images = [data.Image(directory, f) for f in files]
    for img in images:
        img.load_processed()
        #cv2.imshow('img', img.image)
        #cv2.waitKey(0)
        img.segment_lines()

    n.write_files(images)

    print("Network rval: {}".format(n.run_network()))