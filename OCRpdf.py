import os
from os import listdir
from os.path import isfile, join 
import cv2
from PIL import Image
import numpy as np
import img2pdf
import pytesseract

path = os.getcwd()
inputDataPath = path + "/inputdata/"
inputImagePath = inputDataPath + "/images"
outputDataPath = path + "/outputdata/"
inputFiles = os.listdir(inputDataPath)

def cvt_pdf2img():
	for inputFile in inputFiles:
		fileName, file_extension = os.path.splitext(inputFile)
		outputImagePath = outputDataPath + fileName
		if not os.path.exists(outputImagePath):
			os.makedirs(outputImagePath)
		with Img(filename = inputDataPath + inputFile, resolution=300) as cvt2img:
			cvt2img.compression_quality = 99
			cvt2img.save(filename= outputImagePath + "/page.jpg")

imagelist = sorted(os.listdir(outputDataPath + "/test/"))
fileNameList = []
for each_file in imagelist:
	imagePathfile = outputDataPath + "test/" + each_file
	fileNameList.append(imagePathfile)

def OCR_process():
	result = []
	src = cv2.imread(fileNameList[1])
	gray = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)

	#binary
	ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)

	kernel = np.ones((30,40), np.uint8)
	img_dilation = cv2.dilate(thresh, kernel, iterations=1)

	#find contours
	im2,ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for i, ctr in enumerate(ctrs):
		x, y, w, h = cv2.boundingRect(ctr)
		# Getting ROI
		roi = src[y:y+h, x:x+w]
		OCRimg = Image.fromarray(roi)
		txt = pytesseract.image_to_string(OCRimg)
		result.append(txt)
		# show ROI
		cv2.rectangle(src,(x,y),( x + w, y + h ),(0,255,0),5)
		#font = cv2.FONT_HERSHEY_SIMPLEX
		#cv2.putText(src,str(i),(x,y), font, 3,(255,0,0),2,cv2.LINE_AA)
	cv2.imwrite("test1.jpg", src)
	return result


result = OCR_process()
n = len(result)

for i in range(n -1,-1,-1):
	print result[i]
	print "\n"








#with open("name.pdf","wb") as f:
	#f.write(img2pdf.convert(fileNameList,dpi=200, x=None, y=None))



