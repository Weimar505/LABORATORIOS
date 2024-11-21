#con esto habilitamos el entorno virtual :  source env/bin/activate
import cv2
def resize_img(img, width, height):
    up_points = (width, height)
    img_resize = cv2.resize(img, up_points)
    return img_resize

img = cv2.imread("wall-e.jpg")
rimg = resize_img(img, 500, 500)
cv2.imshow("resize image", rimg)
cv2.waitKey(0)