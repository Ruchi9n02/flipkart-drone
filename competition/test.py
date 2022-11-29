import cv2
import numpy as np
  
# Reading an image
img = cv2.imread('image.png')
  
# The kernel to be used for dilation purpose
kernel = np.ones((5, 5), np.uint8)
  
# converting the image to HSV format
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  
# defining the lower and upper values of HSV,
# yellow colour
Lower_hsv = np.array([20, 70, 100])
Upper_hsv = np.array([50, 255, 255])
#blue
Lower_hsv = np.array([90, 50, 70])
Upper_hsv = np.array([128, 255, 255])
#red
Lower_hsv = np.array( [0, 50, 70])
Upper_hsv = np.array([9, 255, 255])
#green
Lower_hsv = np.array([36, 50, 70])
Upper_hsv = np.array([89, 255, 255])
# #pink
Lower_hsv = np.array( [159, 50, 70])
Upper_hsv = np.array([180, 255, 255])
  
# creating the mask by eroding,morphing,
# dilating process
Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
Mask = cv2.erode(Mask, kernel, iterations=1)
Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
Mask = cv2.dilate(Mask, kernel, iterations=1)
  
# Inverting the mask by
# performing bitwise-not operation
# Mask = cv2.bitwise_not(Mask)
  
# Displaying the image
cv2.imshow('Mask', Mask)
  
# waits for user to press any key
# (this is necessary to avoid Python
# kernel form crashing)
cv2.waitKey(0)
  
# closing all open windows
cv2.destroyAllWindows()