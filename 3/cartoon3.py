import numpy as np
import cv2
import glob
import os

bc1 = "ffmpeg -i sample.mp4 -r 24 -f image2 image-%3d.png"
cm1 = os.popen(bc1)
print(cm1.read())

def maincr():
    for name in glob.glob('*.png'):

        img = cv2.imread(name)
        def edge_mask(img, line_size, blur_value):
          gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
          gray_blur = cv2.medianBlur(gray, blur_value)
          edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)
          return edges
        edges = edge_mask(img, 25, 3)
        def color_quantization(img, k):
          data = np.float32(img).reshape((-1, 3))
          criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
          ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
          center = np.uint8(center)
          result = center[label.flatten()]
          result = result.reshape(img.shape)
          return result
        total_color = 12
        img = color_quantization(img, total_color)
        blurred = cv2.bilateralFilter(img, d=7, sigmaColor=200,sigmaSpace=200)
        cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)
        cv2.imwrite(name, cartoon)

maincr()

bc2 = "ffmpeg -framerate 24 -i image-%03d.png silent.mp4"
cm2 = os.popen(bc2)
print(cm2.read())

bc3 = "ffmpeg -i silent.mp4 -i sample.mp4 -c copy -map 0:0 -map 1:1 -shortest cartoon.mp4"
cm3 = os.popen(bc3)
print(cm3.read())




