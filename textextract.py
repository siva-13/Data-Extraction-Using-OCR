import cv2
from pytesseract import pytesseract
import numpy as np
from PIL import Image
import argparse
import os
import re

def main(imgpath="test1.jpg"):
    # Path Allocation
    img = cv2.imread(imgpath)

    imgsharp = r'C:\Users\hp\PycharmProjects\Flask-work\ImgSharp\sharp.png'
    imgtotxt = r"C:\Users\hp\PycharmProjects\Flask-work\Image2text\text.txt"
    facepath = r'C:\Users\hp\PycharmProjects\Flask-work\static\img.png'
    face_cas = cv2.CascadeClassifier(r'C:\Users\hp\anaconda3\Library\etc\haarcascades\haarcascade_frontalface_default.xml')
    path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    #cv2.imshow('img_name',img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    # Face Dedection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cas.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=15)
    for x, y, w, h in faces:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
        faces = img[y:y + h, x:x + w]
    #     cv2.imshow("face",faces)
    #     cv2.imwrite('face.jpg', faces)
    cv2.imwrite(facepath, faces)
    # cv2.imshow('siva', faces)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


    # pytesseract.image_to_string(img, config=custom_config)
    # img = cv2.imread(r'C:\Users\hp\Music\.ipynb_checkpoints\samp1.jpeg')
    def get_grayscale(image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    # thresholding
    def thresholding(image):
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


    gray = get_grayscale(img)
    thresh = thresholding(gray)

    # cv2.imshow('sample' ,thresh)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cv2.imwrite(imgsharp, thresh)

    # path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    # image_path = path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    # image_path = r'C:\Users\hp\Music\.ipynb_checkpoints\sharp.png'

    # Opening the image & storing it in an image object
    img = Image.open(imgsharp)

    # Providing the tesseract
    # executable location to pytesseract library
    pytesseract.tesseract_cmd = path_to_tesseract

    # extract the text from the image
    text = pytesseract.image_to_string(img)

    # Displaying the extracted text
    # print(text[:-1])
    file1 = open(imgtotxt, "w+")
    file1.writelines(text)
    file1.close()

    # Check if any line in the file contains string
    def check_if_string_in_file(file_name, string_to_search):
        with open(file_name, 'r') as read_obj:
            for line in read_obj:
                # For each line, check if line contains the string
                if string_to_search in line:
                    return True
        return False

    # If given document is PanCard
    def panExtract(textfile):
        file = open(textfile)
        print("PANCARD DOCUMENTS!!!!")
        # read the content of the file opened
        content = file.readlines()
        listToStr = ' '.join([str(elem) for elem in content])
        lines = listToStr.split("\n")
        non_empty_lines = [line for line in lines if line.strip() != ""]
        dobreg = re.compile(r'\d\d\/\d\d/\d\d\d\d')
        dobr = dobreg.search(listToStr)
        panreg = re.compile(r'[A-Z][A-Z][A-Z][A-Z][A-Z]\d\d\d\d[A-Z]')
        pan = panreg.search(listToStr)
        RNAME="NAME : " + non_empty_lines[2]
        RFATHER_NAME="FATHER NAME : " + non_empty_lines[3]
        RDOB="DOB : " + dobr.group()

        RPAN_NUMBER="PAN NUMBER : " + pan.group()
        #print("NAME : " + non_empty_lines[2])
        #print("FATHER NAME : " + non_empty_lines[3])
        #print("DOB : " + dobr.group())
        #print("PAN NUMBER : " + pan.group())
        file.close()
        return RNAME,RFATHER_NAME,RDOB,RPAN_NUMBER
    # if given docment is driving license
    def drivingExtract(textfile):
        file = open(textfile)
        print("India Driving Licence!!!!")
        # read the content of the file opened
        content = file.readlines()
        listToStr = ' '.join([str(elem) for elem in content])
        lines = listToStr.split("\n")
        non_empty_lines = [line for line in lines if line.strip() != ""]
        panreg = re.compile(r'\d\d\/\d\d/\d\d\d\d')
        pan = panreg.search(listToStr)
        TNm = re.compile(r'[A-Z][A-Z]\d\d\s\d\d\d\d\d\d\d\d\d\d')
        TN = TNm.search(listToStr)
        DOIse = re.compile(r'\d\d/\d\d/\d\d\d\d')
        DOI = DOIse.search(listToStr)
        DObs = re.compile(r'[A-z][A-Z][A-Z]\s\d\d/\d\d/\d\d\d\d')
        DOB = DObs.search(listToStr)
        RDOI='DATE OF ISSUE : ' + DOI.group()
        RDL='D.L.No : ' + TN.group()
        RNAME="NAME : " + non_empty_lines[3].strip()[4:]
        RADDRESS="ADDRESS : " + non_empty_lines[6] + '\n\t  ' + non_empty_lines[7] + '\n\t  ' + non_empty_lines[8] + '.'
        #print('Date Of Issue : ' + DOI.group())
        #print('D.L.No : ' + TN.group())
        #print("NAME : " + non_empty_lines[3].strip()[4:])
        #print("ADDRESS : " + non_empty_lines[6] + '\n\t  ' + non_empty_lines[7] + '\n\t  ' + non_empty_lines[8] + '.')
        file.close()
        return RDOI,RNAME,RADDRESS,RDL

    # To check the type of Document
    pan_array = ['INCOMETAX', 'Account', 'DEPARTMENT']
    driving_lic = ['D.L.No', 'Indian', 'Driving', 'Licence']
    
    for pan_check in pan_array:
        if ((check_if_string_in_file(imgtotxt, pan_check) == True)):
            a,b,c,d=panExtract(imgtotxt)
            print(a,"\n",b,"\n",c,"\n",d,"\n")
            #break
            return a,b,c,d,"TYPE : PANCARD DOCUMENT"
    for driv_check in driving_lic:
        if ((check_if_string_in_file(imgtotxt, driv_check) == True)):
            a,b,c,d=drivingExtract(imgtotxt)
            print(a,"\n",b,"\n",c,"\n",d,"\n")
            #break
            return a,b,c,d,"TYPE : DRIVING DOCUMENT"



if __name__ == "__main__":
    main()