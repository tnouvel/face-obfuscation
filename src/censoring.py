import cv2
from tkinter import *
import numpy as np


# Draw rectangle around face
def draw_detection(img, faces):

    for(x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 5)
    return img


def blur_image(img, factor=3.0):

    (h, w) = img.shape[:2]

    # kernel width/height
    # larger values = more blur; lower values = less blur
    # decrease factor to increase blur
    kerW = int(w / factor)
    kerH = int(h / factor)

    # make sure kernel width/height are odd to centralize coordinates
    if kerW % 2 == 0:
        kerW -= 1

    if kerH % 2 == 0:
        kerH -= 1

    return cv2.GaussianBlur(img, (kerW, kerH), 0)


# This function pixelates an image
def pixelate_image(img, blocks=30):

    (h, w) = img.shape[:2]
    x_Steps = np.linspace(0, w, blocks + 1, dtype="int")
    y_Steps = np.linspace(0, h, blocks + 1, dtype="int")

    # loop over blocks in both directions
    for i in range(1, len(y_Steps)):
        for j in range(1, len(x_Steps)):
            # find start and end coordinates of x and y for the current block
            start_X = x_Steps[j-1]
            start_Y = y_Steps[i-1]
            end_X = x_Steps[j]
            end_Y = y_Steps[i]

            # get region of interst (roi) with array slicing
            # find the mean
            # draw rectangle with mean RGB values over the roi
            roi = img[start_Y:end_Y, start_X:end_X]
            (b, g, r) = [int(x) for x in cv2.mean(roi)[:3]]
            cv2.rectangle(img, (start_X, start_Y),
                          (end_X, end_Y), (b, g, r), -1)
    return img


# This function performs facial fogging/blurring
# A higher factor will result in less blur
def face_blur(img, model, factor=7):
    h, w = img.shape[:2]
    ker_W = (w//factor) | 1
    ker_H = (h//factor) | 1

    # preprocessing image: resize/mean subtraction
    blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), (104.0, 177.0, 123.0))

    # set img to input of neural network
    model.setInput(blob)

    # inference
    output = np.squeeze(model.forward())

    for i in range(0, output.shape[0]):
        confidence = output[i, 2]

        if confidence > 0.4:

            box = output[i, 3:7] * \
                np.array([img.shape[1], img.shape[0],
                          img.shape[1], img.shape[0]])

            # Convert to integers
            start_X, start_Y, end_X, end_Y = box.astype(np.int32)

            # add to face array
            face = img[start_Y:end_Y, start_X:end_X]
            # blur
            face = cv2.GaussianBlur(face, (ker_W, ker_H), 0)

            img[start_Y:end_Y, start_X:end_X] = face
    return img


# This function pixelates an the face
# More blocks will create more pixelation on targeted frames
def face_pixelate(img, model, blocks=12):

    # preprocessing image: resize/mean subtraction
    blob = cv2.dnn.blobFromImage(img, 1.0, (300, 300), (104.0, 177.0, 123.0))

    # set img to input of neural network
    model.setInput(blob)

    # inference
    output = np.squeeze(model.forward())

    for i in range(0, output.shape[0]):
        confidence = output[i, 2]

        if confidence > 0.4:

            box = output[i, 3:7] * \
                np.array([img.shape[1], img.shape[0],
                          img.shape[1], img.shape[0]])

            # Convert to integers
            start_X, start_Y, end_X, end_Y = box.astype(np.int32)

            # add to face array
            face = img[start_Y:end_Y, start_X:end_X]
            # pixelate
            face = pixelate_image(face, blocks)

            img[start_Y:end_Y, start_X:end_X] = face
    return img
