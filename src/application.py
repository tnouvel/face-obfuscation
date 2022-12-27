from constants import IMAGE_SIZE
import os
from os.path import dirname, join
import tkinter as tk
from tkinter import PhotoImage, filedialog, Label, StringVar, OptionMenu, Entry, IntVar, Checkbutton, Frame
from tkinter.ttk import Style, Button
from PIL import Image, ImageTk
import numpy as np
import cv2



class ObfuscationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.create_widgets()


        self.choice = ''
        self.file_path = ''
        self.file_ext = ''
        self.factor = 0
        self.thumbnail = None

        # Styles
        # Buttons
        style = Style()
        style.configure('Open.TButton', font=(
            'calibri', 10, 'bold'), foreground='blue')
        style.configure('Conf.TButton', font=(
            'calibri', 10, 'bold'), foreground='green')

    def create_widgets(self):
        self.create_window()
        self.create_file_window()
        

    def create_file_window(self):
        self.open_file_button()
        self.obfuscation_options()

        # Save output
        self.cb_save = IntVar()
        self.cb = Checkbutton(self, text='Save Output', variable=self.cb_save,
                              onvalue=1, offvalue=0, height=5, width=20).pack()
        # Confirm
        self.button = Button(self, text='Confirm', style='Conf.TButton',
                             command=lambda: [self.get_value(), self.destroy()])
        self.button.pack()

    def create_window(self):
        self.title('Scator')
        self.geometry('600x500')
        self.minsize(600, 500)
        icon_path = join(dirname(__file__),
                         "ui/images/window_icon.png")
        self.tk.call('wm', 'iconphoto', self._w, tk.PhotoImage(file=icon_path))

    def open_file_button(self):
        self.fileFrame = Frame(self)
        self.fileFrame.pack()
        # Creating a button to search the file
        b1 = Button(self.fileFrame, text="Open File", style='Open.TButton', command=self.open_file)
        b1.pack(pady=(25, 0))
        # Display file path
        self.labelA = tk.Label(self.fileFrame, text="", wraplength=350)
        self.labelA.pack()

    def open_file(self):

        filetypes = (
            ('Compatible Files', '.mp4 .jpg .png'),
            ('Video Files', '*.mp4'),
            ('Image Files', '.jpg .png')
        )
        # Open and return file path
        self.file_path = filedialog.askopenfilename(title="Select A File",
                                                    filetypes=filetypes)
        self.file_ext = os.path.splitext(self.file_path)[1]
        if self.file_path:
            self.show_file_path()

    def obfuscation_options(self):
        # Option of blur or pixelate
        self.method_label = Label(self, text='Choose type of obfuscation:')
        self.method_label.pack()
        self.options_list = ["Blur", "Pixelate"]
        self.option = StringVar(self)
        self.option.set("Select a method")
        self.menu = OptionMenu(self, self.option, *self.options_list,
                               command=self.select_option)
        self.menu.pack()

        # Factor of obfuscation (level of blurring or pixelation)
        self.factor_label = Label(
            self, text='Choose a factor for obfuscation:')
        self.factor_label.pack()
        self.entry = Entry(self, width=35)
        self.entry.focus_set()
        self.entry.pack()

    def select_option(self, value):
        self.choice = value

    def get_save_output(self):
        return self.cb_save.get()

    def get_choice(self):
        return self.choice

    def get_value(self):
        self.factor = self.entry.get()

    def get_factor(self):
        return int(self.factor)

    def show_file_path(self):
        self.labelA['text'] = "Filepath: " + self.file_path
        
        if self.thumbnail: #This makes sure the photo changes
            self.thumbnail.destroy()

        if self.file_ext == ".jpg" or self.file_ext == '.png':
            img = Image.open(self.file_path)
            img.thumbnail(IMAGE_SIZE, Image.ANTIALIAS)
            imgtk = ImageTk.PhotoImage(img)
            self.thumbnail=Label(self.fileFrame, image = imgtk)
            self.thumbnail.image = imgtk
            self.thumbnail.configure(image = imgtk)
            self.thumbnail.pack()

        elif self.file_ext == ".mp4":
            # https://flynnsforge.com/how-to-display-video-from-cv2-in-tkinter-python-3/
            vid = cv2.VideoCapture(self.file_path)
            while True: #Try to figure out way to loop video
                ret, frame = vid.read() #Reads the video
                if self.thumbnail: #Destroy per frame
                    self.thumbnail.destroy()

                if not ret: #unnecessary? makes vid.release() mad without it
                    break

                #Converting the video for Tkinter
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                #Ensure it is within frame
                img.thumbnail(IMAGE_SIZE, Image.ANTIALIAS)
                imgtk = ImageTk.PhotoImage(image=img)
                self.thumbnail=Label(self.fileFrame, image = imgtk)
                #Setting the image on the label
                self.thumbnail.config(image=imgtk)
                self.thumbnail.pack()
                self.update() #Updates the Tkinter window
            vid.release()


    def get_file_path(self):
        return self.file_path

    def get_file_ext(self):
        return self.file_ext
        
# https://stackoverflow.com/questions/35180764/opencv-python-image-too-big-to-display
def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)
