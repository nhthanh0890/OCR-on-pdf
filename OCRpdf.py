
#************************************************************************
#                             I N C L U D E S
#*************************************************************************

import os
from os import listdir
import cv2  #opencv library
from PIL import Image #Python Image Library
from wand.image import Image as Img # convert pdf file to image
import numpy as np 
import pytesseract	#OCR on python (Google) 
import csv #Work with CSV file 
import img2pdf #Convert img to pdf file 


path = os.getcwd()
inputPath = path + "/inputdata/" #input data directory
imagePath = inputPath + "/images/" #input image directory
outputPath = path + "/outputdata/" #output data directory
inputFiles = os.listdir(inputPath)


#************************************************************************
#                 F U N C T I O N   D E C L A R A T I O N S
#*************************************************************************

## 	Function name: cvt_pdf2img
##	Description: Convert each page of input pdf file to image, then store it to specified directory
## 	Input: pdf file name
##	Output: image file

def cvt_pdf2img(fileName):
	#Create output image directory
	outputImage = outputPath + fileName + "/images"
	if not os.path.exists(outputImage):
		os.makedirs(outputImage)
	#Create output OCRtext directory
	outputOCRtext = outputPath + fileName + "/OCRtext"
	if not os.path.exists(outputOCRtext):
		os.makedirs(outputOCRtext)
	#Convert pdf to image then store in outputImage directory
	with Img(filename = inputPath + inputFile, resolution=300) as cvt2img:
		cvt2img.compression_quality = 99
		cvt2img.save(filename= outputImage + "/page.jpg")


## 	Function name: OCR_process
##	Description: Get ROI of paragraph on image then get all character by using OCR library "pytesseract"
## 	Input: image file name
##	Output: OCR result of input image

def OCR_process(imageFileName): 

	result = []
	#Read image then cvt to gray
	src = cv2.imread(imageFileName)
	gray = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)

	#Image segmentation using threshold
	ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
	#Morphological image process using image dilation
	kernel = np.ones((30,40), np.uint8)
	img_dilation = cv2.dilate(thresh, kernel, iterations=1)
	#cv2.imshow('img_dilation',img_dilation)

	#Find contours then get ROI of image
	im2,ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

	for i, ctr in enumerate(ctrs):
		x, y, w, h = cv2.boundingRect(ctr)
		# Get ROI of image
		roi = src[y:y+h, x:x+w]
		#Read ROI image as array
		OCRimg = Image.fromarray(roi)
		#Apply pytesseract library for OCR to ROI image
		txt = pytesseract.image_to_string(OCRimg)
		#Save OCR result to text
		result.append(txt)
		# show ROI on output image
		cv2.rectangle(src,(x,y),( x + w, y + h ),(0,255,0),5)
		#font = cv2.FONT_HERSHEY_SIMPLEX
		#cv2.putText(src,str(i),(x,y), font, 3,(255,0,0),2,cv2.LINE_AA)
	cv2.imwrite(imageFileName, src)
	return result



#************************************************************************
#                         M A I N     F U N C T I O N   
#*************************************************************************


#Read each input pdf file then process in inputdata directory
for inputFile in inputFiles:
	#Split file name and it's extension
	fileName, fileExtension = os.path.splitext(inputFile)
	cvt_pdf2img(fileName)
	#Sorting images by pages
	imagelist = sorted(os.listdir(outputPath + fileName + "/images/"))
	#Read input images file which coresponds to pages of pdf file
	for each_file in imagelist:
		#Split filename and it's extension
		pages , pageExtension = os.path.splitext(each_file)
		imagePathfile = outputPath + fileName + "/images/" + each_file 
		#print fileNameList
		result = OCR_process(imagePathfile)
		#Re-order output text list
		result.reverse()
		#Wrire OCR result to text file 
		with open(outputPath + fileName + "/OCRtext/" + pages + '.csv', mode='wb+') as fd:
			writer = csv.writer(fd,delimiter='\n')
			rest_array = [text.encode("utf8") for text in result]
			writer.writerow(rest_array)



















#with open("name.pdf","wb") as f:
	#f.write(img2pdf.convert(fileNameList,dpi=200, x=None, y=None))



