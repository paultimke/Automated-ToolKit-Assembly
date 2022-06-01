from numpy import ogrid
import Vision as vs
import Global_vars as glob
import cv2

for i in range(5):
    img = vs.get_image_Vimba()
    _, og = vs.vimba2binary(img)

    vs.save_image(og, 'Ref-img_26cm', 'ParaChristian')

    cv2.imshow('cal', og)

    cv2.waitKey(0)


cv2.destroyAllWindows()