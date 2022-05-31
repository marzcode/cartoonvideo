import numpy as np
import glob
import cv2 
import os

bc1 = "ffmpeg -i sample.mp4 -r 24 -f image2 image-%3d.png"
cm1 = os.popen(bc1)
print(cm1.read())

def maincr():
    for name in glob.glob('*.png'):
        
        img = cv2.imread(name)      
        img_gb = cv2.GaussianBlur(img, (7, 7) ,0)
        img_mb = cv2.medianBlur(img_gb, 5)
        img_bf = cv2.bilateralFilter(img_mb, 5, 80, 80)
        img_lp_im = cv2.Laplacian(img, cv2.CV_8U, ksize=5)
        img_lp_gb = cv2.Laplacian(img_gb, cv2.CV_8U, ksize=5)
        img_lp_mb = cv2.Laplacian(img_mb, cv2.CV_8U, ksize=5)
        img_lp_al = cv2.Laplacian(img_bf, cv2.CV_8U, ksize=5)
        img_lp_im_grey = cv2.cvtColor(img_lp_im, cv2.COLOR_BGR2GRAY)
        img_lp_gb_grey = cv2.cvtColor(img_lp_gb, cv2.COLOR_BGR2GRAY)
        img_lp_mb_grey = cv2.cvtColor(img_lp_mb, cv2.COLOR_BGR2GRAY)
        img_lp_al_grey = cv2.cvtColor(img_lp_al, cv2.COLOR_BGR2GRAY)
        _, EdgeImage = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        blur_im = cv2.GaussianBlur(img_lp_im_grey, (5, 5), 0)
        blur_gb = cv2.GaussianBlur(img_lp_gb_grey, (5, 5), 0)
        blur_mb = cv2.GaussianBlur(img_lp_mb_grey, (5, 5), 0)
        blur_al = cv2.GaussianBlur(img_lp_al_grey, (5, 5), 0)
        _, tresh_im = cv2.threshold(blur_im, 245, 255,cv2.THRESH_BINARY +  cv2.THRESH_OTSU)
        _, tresh_gb = cv2.threshold(blur_gb, 245, 255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        _, tresh_mb = cv2.threshold(blur_mb, 245, 255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        _, tresh_al = cv2.threshold(blur_al, 245, 255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        inverted_original = cv2.subtract(255, tresh_im)
        inverted_GaussianBlur = cv2.subtract(255, tresh_gb)
        inverted_MedianBlur = cv2.subtract(255, tresh_mb)
        inverted_Bilateral = cv2.subtract(255, tresh_al)        
        img_reshaped = img.reshape((-1,3))
        img_reshaped = np.float32(img_reshaped)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        K = 8
        _, label, center = cv2.kmeans(img_reshaped, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        res = center[label.flatten()]
        img_Kmeans = res.reshape((img.shape))
        div = 64
        img_bins = img // div * div + div // 2
        inverted_Bilateral = cv2.cvtColor(inverted_Bilateral, cv2.COLOR_GRAY2RGB)
        cartoon_Bilateral = cv2.bitwise_and(inverted_Bilateral, img_bins)
        cv2.imwrite(name, cartoon_Bilateral)
maincr()

bc2 = "ffmpeg -framerate 24 -i image-%03d.png silent.mp4"
cm2 = os.popen(bc2)
print(cm2.read())

bc3 = "ffmpeg -i silent.mp4 -i sample.mp4 -c copy -map 0:0 -map 1:1 -shortest cartoon.mp4"
cm3 = os.popen(bc3)
print(cm3.read())
