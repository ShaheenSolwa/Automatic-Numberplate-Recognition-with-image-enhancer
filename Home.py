import os
import easyocr
import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np
import cv2
import pytesseract
import imutils

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def load_image(img):
    im = Image.open(img)
    return im

def ocr_image(img):
        original_image = cv2.imread(img)

        original_image = imutils.resize(original_image, width=500)
        gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)

        edged_image = cv2.Canny(gray_image, 30, 200)

        contours, new = cv2.findContours(edged_image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        img1 = original_image.copy()
        cv2.drawContours(img1, contours, -1, (0, 255, 0), 3)

        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:200]

        # stores the license plate contour
        screenCnt = None
        img2 = original_image.copy()

        # draws top 30 contours
        cv2.drawContours(img2, contours, -1, (0, 255, 0), 3)

        count = 0
        idx = 7

        for c in contours:
            # approximate the license plate contour
            contour_perimeter = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * contour_perimeter, True)

            # Look for contours with 4 corners
            if len(approx) == 4:
                screenCnt = approx

                # find the coordinates of the license plate contour
                x, y, w, h = cv2.boundingRect(c)
                new_img = original_image[y: y + h, x: x + w]

                # stores the new image
                cv2.imwrite('./' + str(idx) + '.png', new_img)
                idx += 1
                break

        # draws the license plate contour on original image
        cv2.drawContours(original_image, [screenCnt], -1, (0, 255, 0), 3)

        # filename of the cropped license plate image
        cropped_License_Plate = './7.png'

        # converts the license plate characters to string
        text_tess = pytesseract.image_to_string(cropped_License_Plate, lang='eng')

        reader = easyocr.Reader(['en'])  # specify the language
        result = reader.readtext(cropped_License_Plate)
        for (bbox, text_easy, prob) in result:
            pass

        if os.path.exists(r"C:\Users\ssolwa001\PycharmProjects\PwC_ANPR\7.png"):
            os.remove(r"C:\Users\ssolwa001\PycharmProjects\PwC_ANPR\7.png")

        return text_tess, text_easy




modification_dict = {}
with st.sidebar:
    st.subheader("Choose an image transform")
    transforms = ["None", "Brightness", "Contrast", "Sharpening", "Noise Reduction", "Resize", "Crop", "Equalize", "Deblur"]
    transform_select = st.selectbox("", options=transforms)
    try_ocr = st.checkbox("Do you want to try OCR the image?")
    if transform_select.lower() == "brightness":
        brightness = st.slider("Select Brightness Level", 0, 100)
        modification_dict['brightness'] = int(brightness)
    elif transform_select.lower() == "contrast":
        contrast = st.slider("Select Contrast Level", -100, 100)
        modification_dict['contrast'] = int(contrast)
    elif transform_select.lower() == "sharpening":
        sharpen = st.slider("Select Sharpening Level", -100 , 100)
        modification_dict['sharpen'] = int(sharpen)
    elif transform_select.lower() == "noise reduction":
        noise_reduction = st.slider("Select how much of Noise should be removed", 0, 100)
        modification_dict['noise_reduction'] = int(noise_reduction)
    elif transform_select.lower() == "resize":
        crop_width = st.number_input("Select Width Size", min_value=1)
        crop_height = st.number_input("Select Height Size", min_value=1)
        modification_dict['resize'] = (crop_width, crop_height)
    elif transform_select.lower() == 'crop':
        im = Image.open(r"C:\Users\ssolwa001\PycharmProjects\PwC_ANPR\uploads\upload.jpg")
        width, height = im.size
        w = st.number_input("Left Crop", min_value=0, key='w')
        x = st.number_input("Top Crop", min_value=0, key='x')
        y = st.number_input("Right Crop", min_value=width, key='y')
        z = st.number_input("Bottom Crop", min_value=height, key='z')

        modification_dict['crop'] = (w,    x,   y,     z)
    elif transform_select.lower() == 'equalize':
        modification_dict['equalize'] = 'equalize'
    elif transform_select.lower() == 'none':
        modification_dict['none'] = 'none'
    elif transform_select.lower() == 'deblur':
        modification_dict['deblur'] = 'deblur'



st.title("Automatic Number Plate Recognition System")
st.write("\n")
file = st.file_uploader("Upload your image", type=['jpg', 'jpeg', 'png'])
st.write("\n")


col1, col2 = st.columns(2)

with col1:
    st.subheader("Original Image")
    if file is not None:
        # Perform your Manupilations (In my Case applying Filters)
        img = load_image(file)
        st.image(img)
        img.save(r"C:\Users\ssolwa001\PycharmProjects\PwC_ANPR\uploads\upload.jpg")
    else:
        st.write("Make sure you image is in JPG/PNG Format.")
    st.write("\n")

with col2:
    st.subheader("Modified Image")
    new_img = Image.new('1', (500, 500))
    if file is not None:
        if len(modification_dict.keys()) > 0:
            for x, y in modification_dict.items():
                if x == 'resize':
                    width, height = y
                    new_img = img.resize(y)
                    st.image(new_img)
                    new_img.save(r"C:\Users\ssolwa001\PycharmProjects\PwC_ANPR\modified_images\modified.jpg")
                elif x == 'brightness':
                    new_img = ImageEnhance.Brightness(img)
                    new_img = new_img.enhance(y)
                    st.image(new_img)
                    new_img.save(r"C:\Users\ssolwa001\PycharmProjects\PwC_ANPR\modified_images\modified.jpg")
                elif x == 'contrast':
                    new_img = ImageEnhance.Contrast(img)
                    new_img = new_img.enhance(y)
                    st.image(new_img)
                    new_img.save(r"C:\Users\ssolwa001\PycharmProjects\PwC_ANPR\modified_images\modified.jpg")
                elif x == 'sharpen':
                    new_img = ImageEnhance.Sharpness(img)
                    new_img = new_img.enhance(y)
                    st.image(new_img)
                    new_img.save(r"C:\Users\ssolwa001\PycharmProjects\PwC_ANPR\modified_images\modified.jpg")
                elif x == 'noise_reduction':
                    new_img = img.filter(ImageFilter.BLUR)
                    new_img = new_img.filter(ImageFilter.MinFilter(3))
                    new_img = new_img.filter(ImageFilter.MinFilter)
                    st.image(new_img)
                    new_img.save(r"C:\Users\ssolwa001\PycharmProjects\PwC_ANPR\modified_images\modified.jpg")
                elif x == 'crop':
                    cropped_img = img.crop(y)
                    st.image(cropped_img)
                    cropped_img.save(r"C:\Users\ssolwa001\PycharmProjects\PwC_ANPR\modified_images\modified.jpg")
                elif x == 'equalize':
                    equalzied_image = ImageOps.equalize(img, mask=None)
                    st.image(equalzied_image)
                    equalzied_image.save(r"C:\Users\ssolwa001\PycharmProjects\PwC_ANPR\modified_images\modified.jpg")
                elif x == 'none':
                    st.image(img)
                    img.save(r"C:\Users\ssolwa001\PycharmProjects\PwC_ANPR\modified_images\modified.jpg")
                elif x == 'deblur':
                    img = cv2.imread(r"C:\Users\ssolwa001\PycharmProjects\PwC_ANPR\uploads\upload.jpg")
                    sharpen_filter = np.array([[0, -1, 0],
                                              [-2, 9, -1],
                                              [0, -1.5, -1]])
                    sharpen = cv2.filter2D(img, -1, sharpen_filter)
                    st.image(sharpen)
                    new_img = Image.fromarray(sharpen)
                    new_img.save(r"C:\Users\ssolwa001\PycharmProjects\PwC_ANPR\modified_images\modified.jpg")
                    #sharpen.save(r"C:\Users\ssolwa001\PycharmProjects\PwC_ANPR\modified_images\modified.jpg")
    else:
        st.write("Make sure you image is in JPG/PNG Format.")

    st.write("\n")
    st.write("\n")


if try_ocr:
    st.text("The ocr text is: ")
    try:
        text_tess, text_easy = ocr_image(r"C:\Users\ssolwa001\PycharmProjects\PwC_ANPR\modified_images\modified.jpg")
        symbols = r"!@#$%^&*()_+-={}[]|\:;\"\'<>,.?/~`"
        for symbol in symbols:
            text_tess = text_tess.replace(symbol, "")
            text_easy = text_easy.replace(symbol, "")
        st.text(f"Tesseract OCR Result: {text_tess}")
        st.text(f"Easy OCR Result: {text_easy}")
    except Exception as e:
        st.warning("Failed to OCR the image!")
