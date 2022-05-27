import cv2
import Vision as vs


for i in range(7):
    img, sizes = vs.img_detectSizes()
    cv2.waitKey(0)

cv2.destroyAllWindows()