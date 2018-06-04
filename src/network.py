import cv2
import pickle
import re
import os

import data as d
import network as n

classes = \
[
    "__BACKGROUND__",
    "Alef",
    "Ayin",
    "Bet",
    "Dalet",
    "Gimel",
    "He",
    "Het",
    "Kaf-medial",
    "Kaf-final",
    "Lamed",
    "Mem-medial",
    "Mem-final",
    "Nun-final",
    "Nun-medial",
    "Pe",
    "Pe-final",
    "Qof",
    "Resh",
    "Samekh",
    "Shin",
    "Taw",
    "Tet",
    "Tsadi-final",
    "Tsadi-medial",
    "Waw",
    "Yod",
    "Zayin"
]

def strip_extention(filename):
    return os.path.splitext(os.path.basename(filename))[0]

def write_image_files(image, folder):
    flat_name = strip_extention(image.filename)
    nameslist = []

    for i in range(0, len(image.lines)):
        cv2.imwrite("{}/{}_line_{}.png".format(folder, flat_name, i), image.lines[i])
        nameslist.append("{}_line_{}".format(flat_name, i))
    
    image.line_names = nameslist
    return nameslist

def write_files(image_list, network_folder = "network", setname="RBA"):
    print("Generating and saving line segments and filelist... ", end="")
    
    # Check / guarantee required folders exists
    image_folder = "{}/{}/Images".format(network_folder, setname)
    names_folder = "{}/{}/Names".format(network_folder, setname)
    
    if not os.path.isdir(image_folder): os.makedirs(image_folder)
    if not os.path.isdir(names_folder): os.makedirs(names_folder)

    nameslist = []
    
    # write image lines
    for image in image_list:
        nameslist = nameslist + write_image_files(image, image_folder)

    # write nameslist
    with open("{}/test.txt".format(names_folder), "w+") as file:
        for name in nameslist:
            file.write("{}\n".format(name))

    print("done")
    return nameslist

#returns a dict with a list of characters per file name
def list_characters(nameslist, pkl_file):
    data = None
    with open(pkl_file, "rb") as file:
        data = pickle.load(file)

    rval = {}

    print("nameslist: {}".format(len(nameslist)))
    print("data: {}".format(len(data)))

    for fname, line in zip(nameslist, data):
        charlist = []
        for rect, name in zip(line[0], line[1]):
            charlist.append(d.Character(rect[:4], rect[4], classes[name]))
        rval[fname] = charlist
    
    for key, val in rval.items():
        rval[key] = sorted(val, key = lambda thing: thing.rect[0])

    return rval

    