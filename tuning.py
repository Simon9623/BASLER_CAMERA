import cv2
import numpy as np

def empty(v):
    pass

kernel = np.ones((5, 5), np.uint8)
img = cv2.imread('2.jpg')
if img is None:
    print("Error: Unable to read image. Please check the file path.")
else:
    img = cv2.resize(img, (0, 0), fx=0.4, fy=0.4)

    # 创建滑动条窗口
    cv2.namedWindow('Trackbar')  # 名字
    cv2.resizeWindow('Trackbar', 640, 320)  # 大小

    # 创建 Trackbars
    cv2.createTrackbar('Block Size', 'Trackbar', 11, 50, empty)  # Block Size 一定要是奇数且大于1
    cv2.createTrackbar('C Value', 'Trackbar', 2, 20, empty)
    cv2.createTrackbar('high', 'Trackbar', 100, 300, empty)
    cv2.createTrackbar('low', 'Trackbar', 100, 300, empty)

    # 灰度处理
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 高斯模糊
    blurred_gray = cv2.GaussianBlur(gray, (9, 9), 2)

    while True:
        # 获取 Trackbars 的值
        block_size = cv2.getTrackbarPos('Block Size', 'Trackbar')
        c_value = cv2.getTrackbarPos('C Value', 'Trackbar')
        high = cv2.getTrackbarPos('high', 'Trackbar')
        low = cv2.getTrackbarPos('low', 'Trackbar')
        
        # Block Size 一定要是奇数且大于1，这里确保它是奇数且大于1
        if block_size % 2 == 0:
            block_size += 1
        if block_size <= 1:
            block_size = 3

        # Edge detection
        canny = cv2.Canny(blurred_gray, low, high)
        dilate = cv2.dilate(canny, kernel, iterations=1)
        
        # 自适应阈值处理
        numpy_img = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, c_value)
        numpy_img2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, c_value)
        
        numpy_blur = cv2.adaptiveThreshold(blurred_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, c_value)
        numpy_blur2 = cv2.adaptiveThreshold(blurred_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, c_value)
        
        # 调整各个图像的大小使其一致
        h, w = numpy_img.shape
        gray_resized = cv2.cvtColor(cv2.resize(gray, (w // 2, h // 2)), cv2.COLOR_GRAY2BGR)
        canny_resized = cv2.cvtColor(cv2.resize(canny, (w // 2, h // 2)), cv2.COLOR_GRAY2BGR)
        numpy_img_resized = cv2.cvtColor(cv2.resize(numpy_img, (w // 2, h // 2)), cv2.COLOR_GRAY2BGR)
        numpy_img2_resized = cv2.cvtColor(cv2.resize(numpy_img2, (w // 2, h // 2)), cv2.COLOR_GRAY2BGR)
        numpy_blur_resized = cv2.cvtColor(cv2.resize(numpy_blur, (w // 2, h // 2)), cv2.COLOR_GRAY2BGR)
        numpy_blur2_resized = cv2.cvtColor(cv2.resize(numpy_blur2, (w // 2, h // 2)), cv2.COLOR_GRAY2BGR)

        # 在图像上添加标题
        cv2.putText(gray_resized, 'Gray', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(canny_resized, 'Canny', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(numpy_img_resized, 'GAUSSIAN GRAY', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(numpy_img2_resized, 'MEAN GRAY', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(numpy_blur_resized, 'GAUSSIAN BLUR', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(numpy_blur2_resized, 'MEAN BLUR', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)

        # 将六个图像合并成一个大图像
        top_row = np.hstack((gray_resized, canny_resized, numpy_img_resized))
        bottom_row = np.hstack((numpy_img2_resized, numpy_blur_resized, numpy_blur2_resized))
        combined = np.vstack((top_row, bottom_row))

        # 显示合并的图像
        cv2.imshow('Combined', combined)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

    # 保存图像
    cv2.imwrite('/mnt/data/combined_output.jpg', combined)

