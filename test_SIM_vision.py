import Vision as vs
import cv2

px_cm = vs.calibrate_cam('Images\Calibration\Ref-img_26cm.png',2.73)

og, _ = vs.get_image_from_path('Images\ParaChristian\Ref-img_26cm_31_05_2022__19h-27m-41s.png')
bn= vs.RGB2binary(og)
#image = vs.get_image_Vimba()
#bn, og = vs.vimba2binary(image)
#cv2.imshow('bn', bn)
#vs.save_image(og, '3pm', 'Images\ParaChristian')

_, cnts = vs.count_objects_AnP(bn)
im, sizes = vs.measure_objects(og,cnts,px_cm)

cv2.imshow('cal', im)

cv2.waitKey(0)


cv2.destroyAllWindows()