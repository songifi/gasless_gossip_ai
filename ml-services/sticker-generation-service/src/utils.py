"""Utils Module for Sticker Generation Service"""

import cv2
import numpy as np
from PIL import Image


def extract_alpha_channel(img):
    '''Extracts the alpha channel from an image'''
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    _, _, _, a = img.split()
    alpha_array = np.array(a)
    return alpha_array

def get_largest_contour(alpha_channel):
    '''Get the largest contour from an alpha channel'''
    # Smoothing using GaussianBlur
    smoothed = cv2.GaussianBlur(alpha_channel, (15, 15), 0)
    contours_smoothed = cv2.findContours(
        smoothed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_smoothed = contours_smoothed[0] if len(
        contours_smoothed) == 2 else contours_smoothed[1]
    big_contours_smoothed = max(contours_smoothed, key=cv2.contourArea)
    peri = cv2.arcLength(big_contours_smoothed, True)
    return cv2.approxPolyDP(big_contours_smoothed, 0.001 * peri, True)


def draw_filled_contour_on_black_background(big_contour, shape):
    '''Draw a filled contour on the black background.'''
    contour_img = np.zeros(shape)
    cv2.drawContours(contour_img, [big_contour], 0, 255, -1)
    return contour_img  


def apply_dilation(img):
    '''Apply dilation to an image'''
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (30, 30))
    return cv2.morphologyEx(img, cv2.MORPH_DILATE, kernel)


def apply_overlays(canvas, img, dilate):
    '''Apply overlays to an image'''
    if img.shape[2] == 3:  # Convert RGB → RGBA
        img = np.dstack([img, np.ones(img.shape[:2], dtype=np.uint8) * 255])
    alpha = img[:, :, 3]
    alpha = np.expand_dims(alpha, 2)
    alpha = np.repeat(alpha, 3, 2)
    alpha = alpha / 255

    canvas[dilate == 255] = (255, 255, 255, 255)
    canvas[:, :, 0:3] = canvas[:, :, 0:3] * (1 - alpha) + alpha * img[:, :, 0:3]

    return canvas


def create_sticker(img):
    '''Create a sticker from an image'''
    img_array = np.array(img)
    alpha = extract_alpha_channel(img)
    big_contour = get_largest_contour(alpha)
    contour_img = draw_filled_contour_on_black_background(
        big_contour, alpha.shape)
    dilate = apply_dilation(contour_img)

    canvas = np.zeros((img_array.shape[0], img_array.shape[1], 4),dtype=np.uint8)
    canvas = apply_overlays(canvas, img_array, dilate)

    return canvas.astype(np.uint8)

def show_sticker_from_image(image,text):
    '''Show the sticker from an image'''
    sticker = Image.fromarray(image)
    sticker.save(f"{text}.png")
    print(f"Sticker saved as {text}.png")