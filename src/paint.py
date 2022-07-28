from tkinter import *
from tkinter.colorchooser import askcolor

from PIL import Image
import os

from converter import Converter



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
        self.line_width = 75
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)

    def set_image(self):
        fileName = "number"
        self.c.postscript(file = fileName + '.eps') 
        img = Image.open(fileName + '.eps')
        os.remove("number.eps")
        img.save(fileName + '.png', 'png') 
        self.c.delete("all")
        c = Converter(img)
        c.complete_convert()


    def paint(self, event):
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, event.x, event.y,
                               width=self.line_width, fill="#000000",
                               capstyle=ROUND, smooth=TRUE, splinesteps=36)
        self.old_x = event.x
        self.old_y = event.y

    def reset(self, event):
        self.old_x, self.old_y = None, None



