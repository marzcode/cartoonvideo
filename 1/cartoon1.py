import cv2 
import glob
import os

bc1 = "ffmpeg -i sample.mp4 -r 24 -f image2 image-%3d.png"
cm1 = os.popen(bc1)
print(cm1.read())

def maincr():
    for name in glob.glob('*.png'):
        img = cv2.imread(name)
        def cartoon(img,blockSize,constant):
	        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	        gray = cv2.medianBlur(gray,1)
	        edges = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,blockSize,constant)
	        color = cv2.bilateralFilter(img,9,250,250)
	        return cv2.bitwise_and(color,color,mask=edges)	
        cv2.imwrite(name,cartoon(img,141,7))
maincr()

bc2 = "ffmpeg -framerate 24 -i image-%03d.png silent.mp4"
cm2 = os.popen(bc2)
print(cm2.read())

bc3 = "ffmpeg -i silent.mp4 -i sample.mp4 -c copy -map 0:0 -map 1:1 -shortest cartoon.mp4"
cm3 = os.popen(bc3)
print(cm3.read())
