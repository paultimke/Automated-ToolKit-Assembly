from array import array
from typing import Tuple
from pymba import Vimba, VimbaException
from pymba import Frame
from cv2 import Mat
import cv2
from datetime import datetime
import os
import numpy as np
import imutils
from imutils import perspective
from imutils import contours
from scipy.spatial import distance as dist

# todo add more colours
PIXEL_FORMATS_CONVERSIONS = {
    'BayerRG8': cv2.COLOR_BAYER_RG2RGB,
}

def get_image_path(path:str) -> None:
    """ Get Image from specified Path Function.
    Return image Mat and image size (pixels)
    
    @path parameter has to be a string
    """
    image = cv2.imread(path)
    size = image.shape 

    return image, size

def get_image_cam(source:int) -> None:
    """ Get image from camera source Function.
    Return image Mat and image size (pixels)
    
    @source parameter int, 0-default(webcam), 1..n-next source
    """
    capture = cv2.VideoCapture(source)
    ret, frame = capture.read()

    return frame

def get_image_Vimba() -> Frame:
    """ Get image from Vimba Function.
    
    Use Vimba functions to take picture from Allied Vision cameras 
    """
    with Vimba() as vimba:
        #init camera
        camera = vimba.camera(0)
        camera.open()
        camera.arm('SingleFrame')

        # capture a single frame, more than once if desired
        try:
            #take picture
            frame = camera.acquire_frame()
            #foto = get_frame(frame)
        except VimbaException as e:
            # rearm camera upon frame timeout
            if e.error_code == VimbaException.ERR_TIMEOUT:
                print(e)
                camera.disarm()
                camera.arm('SingleFrame')
            else:
                raise
        camera.disarm()
        camera.close()

    return frame

def crop_image(img:Mat, Xi:int, Xf:int, Yi:int, Yf:int) -> Mat:
    """ Crop image Function.
    Crop an image into specified rectangle coords (0,0 at uper left corner)

    @Xi parameter X starting pixel
    @Xf parameter X finishing pixel
    @Yi parameter Y starting pixel
    @Yf parameter Y finishing pixel
    """
    img = img[Xi:Xf, Yi:Yf]

    return img

def save_image(image:Mat, name:str, folder:str, show:bool) ->None:
    """ Save Image Function.
    Get the date and time from computer, then save the 
    given image with an specific name and path folder

    @image parameter
    @name parameter as desired 
    @folder parameter name of desired folder
    @show parameter if True print date and time and Aknowledge
     """

    #Get Date
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y__%Hh-%Mm-%Ss")
    if show:
        print("date and time =", dt_string)

    #Save image to folder
    status=cv2.imwrite(f'{folder}/{name}_{dt_string}.png',image)
    if status and show:
        print("Image written to file-system : ",status)
    elif not status:
        os.mkdir(folder)
        status=cv2.imwrite(f'{folder}/{name}_{dt_string}.png',image)
        if show:
            print("Image written to file-system : ",status)
    


def RGB2binary(img:Mat) -> Mat:
    """ RGB to Binary Function.
    Process an RGB image with morphology techniques to convert
    it into a binary array 
    @img parameter image (3 dimensions Mat)"""
    #blur image
    img = cv2.medianBlur(img,7)
    #gray scale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #treshhold over 1st value will covert to 2nd value
    image_res ,img = cv2.threshold(img,50,255,cv2.THRESH_BINARY)
    #arreglo chiquito para hacer operaciones morfologicas
    kernel = np.ones((3,3),np.uint8)
    #filtro de morfología abierto
    img = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel) 
    #transformación NO SE
    #img = cv2.distanceTransform(img,cv2.DIST_L2,5)
    #reducir tamaño de objetos por factor
    _, img =  cv2.threshold(img, 0.06*img.max(),255,0)

    #cambiar formato de u32 a u8
    img = np.uint8(img)

    return img
    
def vimba2binary(img: Frame) ->Mat:
    """ Gray to Binary Function. Allied Vision Camera
    Process a grayscale Vimba image with morphology techniques to convert
    it into a binary array 
    @img parameter image (3 dimensions Mat)"""

    #pymba image to numpy array
    img = img.buffer_data_numpy()
    #blur image
    aver = cv2.medianBlur(img,1)
    img = cv2.medianBlur(img,9)
    #treshhold over 1st value will covert to 2nd value
    image_res ,img = cv2.threshold(img,40,255,cv2.THRESH_BINARY)
    #arreglo chiquito para hacer operaciones morfologicas
    kernel = np.ones((3,3),np.uint8)
    #filtro de morfología abierto
    img = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel) 
    #transformación NO SE
    img = cv2.distanceTransform(img,cv2.DIST_L2,5)
    #reducir tamaño de objetos por factor
    ret, img =  cv2.threshold(img, 0.06*img.max(),255,0)
    #cambiar formato de u32 a u8
    img = np.uint8(img)

    return img, aver

def count_objects_AnP(image:Mat, show:bool, show_more:bool) -> Mat:
    """ Count objects: Area and Perimeter Function.
    Count how many objects are detected in the given image, then shows 
    the info for each object: Area and Perimeter 
    Return an array with all info
    
    @image parameter Mat
    @show parameter Bool, if true prints values for all objects
    """
    cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    finalContours = []
    i = 0    #contador interno
    # for each contour found
    for cnt in contours:
        # find its area in pixel
        area = cv2.contourArea(cnt)
        # minimum area value is to be fixed
        if (area > 100):
            i = i +1
            perimeter = cv2.arcLength(cnt, True)
            #print(len(approx))
            finalContours.append([area, perimeter])
            if show_more:
                print("Area",i,"= ", area)
                print("Perim",i,"= ", round(perimeter,2),"\n")
        
    cnts = imutils.grab_contours(cnts)
    if show:
        print("Objects in the image : ", i)

    return finalContours, cnts

def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

def measure_objects(image: Mat, cnts: array, reference: float) -> Tuple[Mat, list]:
    # sort the contours from left-to-right and initialize the
    # 'pixels per metric' calibration variable
    (cnts, _) = contours.sort_contours(cnts)
    pixelsPerMetric = None
    sizes=[]
    for c in cnts:
        # min object size
        if cv2.contourArea(c) < 100:
            continue

        # calculate the rotated box of the contour
        orig = image
        box = cv2.minAreaRect(c)
        box = cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        # order the points in the contour such that they appear
        # in top-left, top-right, bottom-right, and bottom-left
        # order, then draw the outline of the rotated bounding
        # box
        box = perspective.order_points(box)
        cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 1)
        # loop over the original points and draw them
        for (x, y) in box:
            cv2.circle(orig, (int(x), int(y)), 2, (0, 0, 255), -1)
        # unpack the ordered bounding box, then compute the midpoint
        # between the top-left and top-right coordinates, followed by
        # the midpoint between bottom-left and bottom-right coordinates
        (tl, tr, br, bl) = box
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)
        # compute the midpoint between the top-left and top-right points,
        # followed by the midpoint between the top-right and bottom-right
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)
        # draw the midpoints on the image
        cv2.circle(orig, (int(tltrX), int(tltrY)), 1, (255, 0, 0), -1)
        cv2.circle(orig, (int(blbrX), int(blbrY)), 1, (255, 0, 0), -1)
        cv2.circle(orig, (int(tlblX), int(tlblY)), 1, (255, 0, 0), -1)
        cv2.circle(orig, (int(trbrX), int(trbrY)), 1, (255, 0, 0), -1)
        # draw lines between the midpoints
        cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
            (255, 0, 255), 1)
        cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
            (255, 0, 255), 1)
        # compute the distance between midpoints
        dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
        # if the pixels per metric has not been initialized, then
        # calculate pixels per metric (in this case cm)
        if pixelsPerMetric is None:
            pixelsPerMetric = dB / reference
        # compute the size of the object
        dimA = dA / pixelsPerMetric
        dimB = dB / pixelsPerMetric
        # draw the object sizes on the image
        cv2.putText(orig, "{:.1f}cm".format(dimA),
            (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
            0.3, (255, 255, 255), 1)
        cv2.putText(orig, "{:.1f}cm".format(dimB),
            (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
            0.3, (255, 255, 255), 1)
        # show the output image

        sizes.append((dimA, dimB))

    return orig, sizes

def img_detectSizes() -> Tuple[Mat, list]:
    #image = vs.get_image_cam(1)
    image = cv2.imread('tst_img3.png')
    img = RGB2binary(image)
    _, contours = count_objects_AnP(img,0,0)
    img, sizes = measure_objects(image, contours,2.7)
    
    # Cut the head off the list because it's the reference object
    return (img, sizes[1:])

def print_typNcnt(img:Mat, objects:int, types:list) -> Mat:
    # sort the contours from left-to-right and initialize the
    # 'pixels per metric' calibration variable
    (objects, _) = contours.sort_contours(objects)
    #poner contornos y numeración
    for (i, c) in enumerate(objects):
        ((x, y), _) = cv2.minEnclosingCircle(c)
        cv2.putText(img, "{}".format(i + 1), (int(x) - 41, int(y)+20),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(img, types[i][1], (int(x) - 20, int(y)+40),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 1)
    
    return img


def res_vimba()-> None:
    """ Restart Vimba Viewer settings to continous 
    frame adquisition """
    with Vimba() as vimba:
        #init camera
        camera = vimba.camera(0)
        camera.open()
        camera.arm('Continuous')
        print('Ready')
        camera.disarm()
        camera.close()

