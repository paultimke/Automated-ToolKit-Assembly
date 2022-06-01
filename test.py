from numpy import ogrid
import Vision as vs
import Global_vars as glob
import cv2

px_cm = vs.calibrate_cam('Images\Calibration\Ref-img_26cm.png',2.73)

image, _ = vs.get_image_from_path('Images\ParaChristian\Ref-img_26cm_31_05_2022__19h-30m-14s.png')
cv2.imshow('og', image)
bn = vs.RGB2binary(image)
cv2.imshow('bn', bn)

_, cnts = vs.count_objects_AnP(bn)
im, sizes = vs.measure_objects(image,cnts,px_cm)
cv2.imshow('cal', im)

cv2.waitKey(0)


cv2.destroyAllWindows()
