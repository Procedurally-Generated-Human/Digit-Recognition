from tkinter import *
from tkinter.colorchooser import askcolor

import torch

from PIL import Image
from PIL import ImageGrab
import os

from converter import Converter
from neuralNetwork import NeuralNetwork



class Paint(object):



    def __init__(self):
        self.root = Tk()
        self.c = Canvas(self.root, bg='white', width=28*28, height=28*28)
        self.c.grid(row=1, columnspan=5)
        self.choose_size_button = Button(self.root, text="Done", command=self.set_image)
        self.choose_size_button.grid(row=0, column=4)
        self.setup()
        self.root.mainloop()

    def setup(self):
        self.old_x = None
        self.old_y = None
        self.line_width = 100
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)


    def save_widget_as_image(self, widget, file_name):
        ImageGrab.grab(bbox=(
        widget.winfo_rootx(),
        widget.winfo_rooty(),
        widget.winfo_rootx() + widget.winfo_width(),
        widget.winfo_rooty() + widget.winfo_height()
        )).save(file_name+".png")

    def set_image(self):
        fileName = "number"
        self.save_widget_as_image(self.c, "hi")
        self.c.delete("all")
        img = Image.open('hi.png')
        print(img.size)
        c = Converter(img)
        converted_image = c.complete_convert()
        neural_network = NeuralNetwork()
        neural_network.load_state_dict(torch.load("model.pth"))
        tensor = torch.from_numpy(converted_image)
        guess = neural_network(tensor)
        print(guess)
        print(guess.argmax(1))



    def paint(self, event):
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill="#000000",
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None



