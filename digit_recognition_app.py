import keras
from keras.losses import CategoricalCrossentropy
from keras.models import load_model
import numpy as np
from tkinter import *
import tkinter as tk
import win32gui
from PIL import ImageGrab, Image
import PIL.ImageOps

# Load the model
loaded_model = load_model("mnist_model.h5")


def prediction(img):
    img = img.resize((28, 28))

    img = img.convert('L')
    img = PIL.ImageOps.invert(img)
    img = np.array(img)

    img = img.reshape(1, 28, 28, 1)
    img = img / 255
    img2 = img
    img2[0][0] = 0.0
    img2[0][1] = 0.0
    img2[0][:, :4, 0] = 0
    print(repr(img2[0]))

    print(loaded_model.predict([img2]))
    res = loaded_model.predict([img2])[0]
    return np.argmax(res), max(res)


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.x = self.y = 0
        # Creating elements
        self.canvas = tk.Canvas(self, width=600, height=600, bg="white", cursor="cross")
        self.label = tk.Label(self, text="Thinking..", font=("Helvetica", 48))
        self.btn_classify = tk.Button(self, text="Recognise", command=self.classify_handwriting)
        self.clear_button = tk.Button(self, text="Clear", command=self.clear_all)
        self.canvas.grid(row=0, column=0, pady=2, sticky=W, )
        self.label.grid(row=0, column=1, pady=2, padx=2)
        self.btn_classify.grid(row=1, column=1, pady=2, padx=2)
        self.clear_button.grid(row=1, column=0, pady=2)
        self.canvas.bind("<B1-Motion>", self.draw_lines)

    def clear_all(self):
        self.canvas.delete("all")

    def classify_handwriting(self):
        HWND = self.canvas.winfo_id()
        rect = win32gui.GetWindowRect(HWND)
        im = ImageGrab.grab(rect)
        digit, acc = prediction(im)
        self.label.configure(text=str(digit) + ', ' + str(int(acc * 100)) + '%')

    def draw_lines(self, event):
        self.x = event.x
        self.y = event.y
        r = 8
        self.canvas.create_oval(self.x - r, self.y - r, self.x + r, self.y + r, fill='black')


app = App()
mainloop()
