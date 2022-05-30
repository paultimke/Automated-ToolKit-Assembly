from array import array
from typing import Tuple
import cv2
from cv2 import Mat
from datetime import datetime
import os
import numpy as np
import imutils
from imutils import perspective
from imutils import contours
from scipy.spatial import distance as dist
import Global_vars as glob

try:
    from pymba import Vimba, VimbaException
    from pymba import Frame
except:
    pass

# CONSTANTS
DEBUG = False


def get_image_from_path(path:str) -> None:
    """ Get Image from specified Path Function.
    Return image Mat and image size (pixels)
    
    @path parameter has to be a string
    """
    image = cv2.imread(path)
    size = image.shape 

    return image, size

def get_image_Vimba():
    """ Get image from Vimba Function.
    
    Use Vimba functions to take picture from Allied Vision cameras 
    @return Vimba Frame
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

def save_image(image:Mat, name:str, folder:str) ->None:
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
    if DEBUG:
        print("date and time =", dt_string)

    #Save image to folder
    status=cv2.imwrite(f'{folder}/{name}_{dt_string}.png',image)
    if status and DEBUG:
        print("Image written to file-system : ",status)
    elif not status:
        os.mkdir(folder)
        status=cv2.imwrite(f'{folder}/{name}_{dt_string}.png',image)
        if DEBUG:
            print("Image written to file-system : ",status)
    


def RGB2binary(img: Mat) -> Mat:
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

def vimba2binary(img) ->Mat:
    """ Gray to Binary Function. Allied Vision Camera
    Process a grayscale Vimba image with morphology techniques to convert
    it into a binary array 
    @img parameter image (3 dimensions Mat) - Vimba Frame"""

    #pymba image to numpy array
    img = img.buffer_data_numpy()
    #blur image
    og_img = cv2.medianBlur(img,1)
    img = cv2.medianBlur(img,7)
    #treshhold over 1st value will covert to 2nd value
    _ ,img = cv2.threshold(img,45,255,cv2.THRESH_BINARY)
    #arreglo chiquito para hacer operaciones morfologicas
    kernel = np.ones((3,3),np.uint8)
    #filtro de morfología abierto
    img = cv2.morphologyEx(img,cv2.MORPH_OPEN,kernel) 
    #transformación NO SE
    img = cv2.distanceTransform(img,cv2.DIST_L2,5)
    #reducir tamaño de objetos por factor
    _, img =  cv2.threshold(img, 0.05*img.max(),255,0)
    #cambiar formato de u32 a u8
    img = np.uint8(img)

    return img, og_img

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
    

def count_objects_AnP(image:Mat) -> Mat:
    """ Count objects: Area and Perimeter Function.
    Count how many objects are detected in the given image, then shows 
    the info for each object: Area and Perimeter 
    Return an array with all info
    
    @image parameter Mat
    @show parameter Bool, if true prints values for all objects
    """
    cnts = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    contourss, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    (contourss, _) = contours.sort_contours(contourss)

    finalContours = []
    i = 0    #contador interno
    # for each contour found
    for cnt in contourss:
        # find its area in pixel
        area = cv2.contourArea(cnt)
        # minimum area value is to be fixed
        if (area > 100):
            i = i +1
            perimeter = cv2.arcLength(cnt, True)
            #print(len(approx))
            finalContours.append([area, perimeter])
            if DEBUG:
                print("Area",i,"= ", area)
                print("Perim",i,"= ", round(perimeter,2),"\n")
        
    cnts = imutils.grab_contours(cnts)
    if DEBUG:
        print("Objects in the image : ", i)

    return finalContours, cnts


def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


def measure_reference(cnts:array, reference:int) -> Mat:
    # sort the contours from left-to-right and initialize the
    # 'pixels per metric' calibration variable
    (cnts, _) = contours.sort_contours(cnts)
    for c in cnts:
        # min object size
        if cv2.contourArea(c) < 100:
            continue

        # calculate the rotated box of the contour
        box = cv2.minAreaRect(c)
        box = cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        # order the points in the contour such that they appear
        # in top-left, top-right, bottom-right, and bottom-left
        # order, then draw the outline of the rotated bounding
        # box
        box = perspective.order_points(box)
        # unpack the ordered bounding box, then compute the midpoint
        # between the top-left and top-right coordinates, followed by
        # the midpoint between bottom-left and bottom-right coordinates
        (tl, tr, br, bl) = box
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)
        # compute the midpoint between the top-left and top-right points,
        # followed by the midpoint between the top-righ and bottom-right
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)
        # compute the distance between midpoints
        dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
        # if the pixels per metric has not been initialized, then
        # calculate pixels per metric (in this case cm)
        pixelsPerMetric = (dB / reference)

    return pixelsPerMetric


def measure_objects(image:Mat, cnts:array, px_cm:int) -> Mat:
    # sort the contours from left-to-right and initialize the
    # 'pixels per metric' calibration variable
    (cnts, _) = contours.sort_contours(cnts)
    pixelsPerMetric = px_cm #None
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
        # followed by the midpoint between the top-righ and bottom-right
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
        #if pixelsPerMetric is None:
            #pixelsPerMetric = dB / reference
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

        DimA = round(dimA,4)
        DimB = round(dimB,4)

        # Populate the sizes list with detected dimensions
        sizes.append([DimA,DimB])

    return orig, sizes

def img_detectSizes() -> Tuple[Mat, list]:
    """ Image Detect Sizes Function.
    Takes a picture, processes it and returns a list of tuples representing
    the sizes of each screw detected in the image

    @Mat return -> Processed image
    @sizes -> list of each screw's dimensions (length and width)
    """
    ref_size = glob.Calibration_size

    #img = get_image_Vimba()
    #img = vimba2binary(img)
    img,_ = get_image_from_path("Images/Test_Imgs/tst_img2.png")
    img = RGB2binary(img)

    _, contours = count_objects_AnP(img)
    img, sizes = measure_objects(img, contours, ref_size)
    return (img, sizes)


def calibrate_cam(path_to_img: str, reference: int) -> int:
    img,_ = get_image_from_path(path_to_img)
    img = RGB2binary(img)
    _, cnts = count_objects_AnP(img)
    px_m = measure_reference(cnts,reference)

    return px_m


