import numpy as np
import cv2
import glob

bc1 = "ffmpeg -i sample.mp4 -r 24 -f image2 image-%3d.png"
cm1 = os.popen(bc1)
print(cm1.read())

def maincr():
    for name in glob.glob('*.png'):
        filename = name
        
        def resizeImage(image):
            scale_ratio = 1
            width = int(image.shape[1] * scale_ratio)
            height = int(image.shape[0] * scale_ratio)
            new_dimensions = (width, height)
            resized = cv2.resize(image, new_dimensions, interpolation = cv2.INTER_AREA)
            return resized
        
        def findCountours(image):
        
            contoured_image = image
            gray = cv2.cvtColor(contoured_image, cv2.COLOR_BGR2GRAY) 
            edged = cv2.Canny(gray, 90, 180)
            contours, hierarchy = cv2.findContours(edged, 
            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(contoured_image, contours, contourIdx=-1, color=1, thickness=1)
            #cv2.imshow('Image after countouring', contoured_image)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            return contoured_image
        
        def ColorQuantization(image, K=4):
            Z = image.reshape((-1, 3)) 
            Z = np.float32(Z) 
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.0001)
            compactness, label, center = cv2.kmeans(Z, K, None, criteria, 1, cv2.KMEANS_RANDOM_CENTERS)
            center = np.uint8(center)
            res = center[label.flatten()]
            res2 = res.reshape((image.shape))
            return res2
        
        if __name__ == "__main__":
            image = cv2.imread(filename)
            resized_image = resizeImage(image)
            coloured = ColorQuantization(resized_image)
            contoured = findCountours(coloured)
            final_image = contoured
            save_q = "y"
            if save_q == "y":
                cv2.imwrite(filename, final_image)
maincr()

bc2 = "ffmpeg -framerate 24 -i image-%03d.png silent.mp4"
cm2 = os.popen(bc2)
print(cm2.read())

bc3 = "ffmpeg -i silent.mp4 -i sample.mp4 -c copy -map 0:0 -map 1:1 -shortest cartoon.mp4"
cm3 = os.popen(bc3)
print(cm3.read())