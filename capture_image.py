from pypylon import pylon
import cv2

# 连接到第一个可用的相机
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())

# 连续抓取图像（视频）并最小化延迟
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
converter = pylon.ImageFormatConverter()


converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
i = 0

while camera.IsGrabbing():
    grabResult = camera.RetrieveResult(1000, pylon.TimeoutHandling_ThrowException)

    if grabResult.GrabSucceeded():
        
        image = converter.Convert(grabResult)
        img = image.GetArray()
        cv2.namedWindow('title', cv2.WINDOW_NORMAL)
        cv2.imshow('title', img)
        k = cv2.waitKey(1)
        
        # press 's' to save
        if k == ord('s'):
            # save dir
            cv2.imwrite(f'C:/Users/ston9/Desktop/basler/img/{i}.jpg', img)
            i += 1
        
        elif k == ord('q'):
            break
    grabResult.Release()


camera.StopGrabbing()

cv2.destroyAllWindows()
