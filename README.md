# OCR-on-pdf

# How does it work?

This's my program which process input pdf file then give all the characters and each character’s bounding box coordinates found in a single page of a pdf document
In this approach, i will process each page of pdf file as an image. I will apply a simple segmentation method based on binary threshold method.
I will explain my approach by the following steps:
- Step 1: Download research paper in pdf format from https://arxiv.org/ then store in "inputdata" directory
- Step 2: Based on filename of each pdf file, create directory with name corresponding to pdf filename
- Step 3: Convert all pages of the pdf file to images and save it in "images" folder inside above directory
- Step 4: Threshold the image to binary then apply morphological processing for the binary image. In here i will using image dilation to expand ROI of image
- Step 5: Find boundary of ROI and draw rectangle for each finding out ROI.
- Step 6: Apply OCR library pytesseract to each ROI. The output results will be saved to "outputdata" directory under text format

