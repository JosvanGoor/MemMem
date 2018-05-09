import cv2
import numpy
import math

def fill_white(image):
    h, w = image.shape
    seed = (1, 1)

    mask = numpy.zeros((h+2, w+2), numpy.uint8)
    floodflags = 4
    floodflags |= cv2.FLOODFILL_MASK_ONLY
    floodflags |= (255 << 8)

    num,img,mask,rect = cv2.floodFill(image, mask, seed, 255)
    num,img,mask,rect = cv2.floodFill(img, mask, (w-2, h-2), 255)
    num,img,mask,rect = cv2.floodFill(img, mask, (0, h-2), 255)
    num,img,mask,rect = cv2.floodFill(img, mask, (w-2, 0), 255)
    return img

def get_gauss_otsu(image):
    blurred = cv2.GaussianBlur(image, (5,5), 0)
    otsu = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return otsu[1]

# expects B&W image
def get_letter_rects(image, minw = 15, minh = 15):
    image, contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    hierarchy = hierarchy[0]

    rects = []
    for component in zip(contours, hierarchy):
        cur_cont = component[0]
        cur_hier = component[1]
        x, y, w, h = cv2.boundingRect(cur_cont)
        if(cur_hier[2]) < 0:
            if w < minw or h < minh: continue
            rects.append([x,y,w,h])

    return rects

# expects B&W image
def get_page_rect_mask(image):
    image_rect = [0, 0, image.shape[0], image.shape[1]]
    image_2, contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    hierarchy = hierarchy[0]

    rects = []
    for component in zip(contours, hierarchy):
        cur_cont = component[0]
        cur_hier = component[1]
        x,y,w,h = cv2.boundingRect(cur_cont)

        if cur_hier[3] < 0: #toplvl component
            if w < 300 or h < 300: continue #too small
            print('[{}, {}, {}, {}]'.format(x,y,w,h))
            rects.append([x,y,w,h, cur_cont])
    
    middle = [0, 0, 1, 1]
    mindist = image_rect[3] * 10
    for r in rects:
        if(r == image_rect): continue
        d = pythagoras(rect_middle(image_rect), rect_middle(r))
        if d < mindist:
            mindist = d
            middle = r

    mask = numpy.zeros(image.shape, numpy.uint8)
    cv2.drawContours(mask, [middle[4]], 0, 255, -1)

    return middle, mask

def pythagoras(p1, p2):
    dx = (p1[0] - p2[0]) ** 2
    dy = (p1[1] - p1[1]) ** 2
    return math.sqrt(dx + dy)

def rect_middle(rect):
    return [rect[0] + (rect[2] // 2), rect[1] + (rect[3] // 2)]

def resize(image, proportion):
    return cv2.resize(image, (0,0), fx=proportion, fy=proportion)

def subimage(image, rect):
    x = rect[0]
    y = rect[1]
    w = rect[2]
    h = rect[3]
    return numpy.copy(image[y:y+h, x:x+w])