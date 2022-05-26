import cv2
import Vision as vs

image = vs.get_image_Vimba()

img, aver= vs.vimba2binary(image)
cv2.imshow('orig',aver)
cv2.imshow('bnw',img)

g, j= vs.count_objects_AnP(img,1,0)
h = vs.print_typNcnt(image,j,)


cv2.waitKey(0)
cv2.destroyAllWindows

#vs.res_vimba()