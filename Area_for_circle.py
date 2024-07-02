import cv2
import numpy as np

kernel = np.ones((5, 5), np.uint8)
img = cv2.imread('canny.jpg')
img = cv2.resize(img, (0, 0), fx=0.4, fy=0.4)

# 灰階處理
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# # 高斯模糊
# blurred_gray = cv2.GaussianBlur(gray, (9, 9), 2)
# # 邊緣檢測
# canny = cv2.Canny(blurred_gray, 100, 100)
# canny = cv2.dilate(canny, kernel, iterations=1)

# 找到輪廓
contours = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if len(contours) == 2 else contours[1]

# 初始化圓的計數
circle_count = 0

# 打印所有輪廓的面積
for contour in contours:
    area = cv2.contourArea(contour)
    print("Contour area:", area)
