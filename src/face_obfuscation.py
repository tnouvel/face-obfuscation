import sys
import os
from os.path import dirname, join
import cv2
from tkinter import *
import numpy as np


# User imports
from application import *
from censoring import *


def main(argv):

    # Obfuscation GUI
    obf_app = ObfuscationApp()
    obf_app.mainloop()
    file_path = obf_app.get_file_path()
    file_ext = os.path.splitext(file_path)[1]
    option = obf_app.get_choice()
    factor = obf_app.get_factor()
    save = obf_app.get_save_output()

    # neural network information
    proto_path = join(dirname(__file__), "weights/deploy.prototxt")
    model_path = join(dirname(__file__),
                      "weights/res10_300x300_ssd_iter_140000_fp16.caffemodel")

    # create model from neural info
    model = cv2.dnn.readNetFromCaffe(proto_path, model_path)

    # Image, Video, or unsupported file type separation
    if file_ext == ".jpg" or file_ext == ".png":

        img = cv2.imread(file_path)

        # perform face blurring
        if option == 'Blur':
            img = face_blur(img, model, factor)

        # perform face pixelation
        elif option == 'Pixelate':
            img = face_pixelate(img, model, factor)

        else:
            print("Something went wrong.")
            exit()

        if save:
            base = os.path.basename(file_path)
            out_file = "src/output/" + os.path.splitext(base)[0] + "_obf" + file_ext
            cv2.imwrite(out_file, img)

        else:
            base = os.path.basename(file_path)
            img_name = os.path.splitext(base)[0] + "_obf.jpg"
            resize = ResizeWithAspectRatio(img, width=640)
            cv2.imshow(img_name, resize)
            cv2.waitKey()
            cv2.destroyAllWindows()

    elif os.path.splitext(file_path)[1] == ".mp4":

        cap = cv2.VideoCapture(file_path)
        #cap = cv2.VideoCapture(0)

        if save:
            # Get video information
            size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                    int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            fps = cap.get(cv2.CAP_PROP_FPS)
            # create new file name
            base = os.path.basename(file_path)
            out_file = "output/" + os.path.splitext(base)[0] + "_obf.mp4"
            # set up VideoWriter
            fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
            out = cv2.VideoWriter(out_file, fourcc, fps, size, True)

        while True:
            ret, img = cap.read()

            if not ret:
                break

            if option == 'Blur':  # perform face blurring
                img = face_blur(img, model, factor)
            elif option == 'Pixelate':  # perform face pixelation
                img = face_pixelate(img, model, factor)
            else:
                print("Something went wrong.")
                exit()

            if save:
                out.write(img)

            # show blurring in window
            cv2.imshow("img", img)
            if cv2.waitKey(1) == ord("q"):
                break

        cv2.destroyAllWindows()
        cap.release()
        if save:
            out.release()

    else:
        print("File type not supported.")
        exit()


if __name__ == '__main__':
    main(sys.argv)
