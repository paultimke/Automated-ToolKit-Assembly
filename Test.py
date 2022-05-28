import cv2
import Vision as vs

img = vs.get_image_Vimba()
img, og_img = vs.vimba2binary(img) 
cv2.imshow('gg',og_img)
vs.save_image(og_img,'Tornillos','Ref_imgs',0)

cv2.waitKey(0)
cv2.destroyAllWindows()
#vs.res_vimba()