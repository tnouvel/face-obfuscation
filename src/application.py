import sys
import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog
import numpy as np
import cv2


class FactorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Obfuscation Factor')
        self.geometry('300x100')

        self.label = Label(self, text='Choose a factor for obfuscation:')
        self.label.pack()

        self.entry = Entry(self, width=35)
        self.entry.focus_set()
        self.entry.pack()

        self.button = Button(self, text='Confirm',
                             command=lambda: [self.get_value(), self.destroy()])
        self.button.pack()

        self.factor = 0

    def get_value(self):
        self.factor = self.entry.get()

    def get_factor(self):
        return int(self.factor)


class FileApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Open Video')
        self.geometry('400x200')
        # Creating a button to search the file
        b1 = Button(self, text="Open File", command=lambda: [
                    self.open_file(), self.show_file_path()])
        b1.pack()

        self.labelA = tk.Label(self, text="", wraplength=350, justify=LEFT)
        self.labelA.pack()

        exit_button = Button(self, text="Confirm", command=self.destroy)
        exit_button.pack(pady=5)

        self.file_path = ''

    def open_file(self):

        filetypes = (
            ('All files', '*.*'),
            ('mp4 files', '*.mp4'),
            ('jpg files', '*.jpg')
        )
        # Open and return file path
        self.file_path = filedialog.askopenfilename(title="Select A File",
                                                    filetypes=filetypes)

    def show_file_path(self):
        self.labelA['text'] = "Filepath: " + self.file_path

    def get_file_path(self):
        return self.file_path


class OptionApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.choice = ''

        self.title('Obfuscation Options')
        self.geometry('300x100')

        self.label = Label(self, text='Choose type of obfuscation:')
        self.label.pack()

        self.options_list = ["Blur", "Pixelate"]

        self.option = StringVar(self)
        self.option.set("Select a method")

        self.menu = OptionMenu(self, self.option, *self.options_list,
                               command=self.select_option)
        self.menu.pack()

        self.button = Button(self, text='Confirm',
                             command=lambda: [self.destroy()])
        self.button.pack()

    def select_option(self, value):
        self.choice = value

    def get_choice(self):
        return self.choice


class ObfuscationApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.choice = ''
        self.file_path = ''
        self.factor = 0

        self.title('Obfuscation Options')
        self.geometry('500x300')

        # Creating a button to search the file
        b1 = Button(self, text="Open File", command=lambda: [
                    self.open_file(), self.show_file_path()])
        b1.pack()
        # Display file path
        self.labelA = tk.Label(self, text="", wraplength=350, justify=LEFT)
        self.labelA.pack()

        # Option of blur or pixelate
        self.label = Label(self, text='Choose type of obfuscation:')
        self.label.pack()
        self.options_list = ["Blur", "Pixelate"]
        self.option = StringVar(self)
        self.option.set("Select a method")
        self.menu = OptionMenu(self, self.option, *self.options_list,
                               command=self.select_option)
        self.menu.pack()

        # Factor of obfuscation (level of blurring or pixelation)
        self.label = Label(self, text='Choose a factor for obfuscation:')
        self.label.pack()
        self.entry = Entry(self, width=35)
        self.entry.focus_set()
        self.entry.pack()

        # Save output
        self.cb_save = IntVar()
        self.cb = Checkbutton(self, text='Save Output', variable=self.cb_save,
                              onvalue=1, offvalue=0, height=5, width=20).pack()

        self.button = Button(self, text='Confirm',
                             command=lambda: [self.get_value(), self.destroy()])
        self.button.pack()

    def open_file(self):

        filetypes = (
            ('All files', '*.*'),
            ('mp4 files', '*.mp4'),
            ('jpg files', '*.jpg')
        )
        # Open and return file path
        self.file_path = filedialog.askopenfilename(title="Select A File",
                                                    filetypes=filetypes)

    def select_option(self, value):
        self.choice = value

    # def save_value(self):
        #self.cb_save = self.cb.get()

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

    def get_file_path(self):
        return self.file_path

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
