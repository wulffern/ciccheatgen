#!/usr/bin/env python3

import reportlab as rl
import yaml
import glob
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape

class PdfGen():

    def __init__(self,fname):
        with open(fname) as fi:
            obj = yaml.safe_load(fi)

        foname = fname.replace(".yaml",".pdf").replace("sheets","pdf")
        width, height = landscape(A4)
        print(width,height)
        self.c = canvas.Canvas(foname,pagesize=landscape(A4),bottomup=1)

        self.textHeight = 12

        self.c.setFont('Courier', self.textHeight)
        self.x = 0
        self.y = height - self.textHeight

        self.pageHeight = height
        self.columWidth = width/4
        self.obj = obj
        self.indent = 0
        self.step  = 10

    def generate(self):
        self.addObj(self.obj)

    def addObj(self,obj):

        if obj is None:
            return
        for k in obj:
            self.addText(k)
            if(type(obj) is dict):
                o = obj[k]
                self.indent += self.step
                self.addObj(o)
                self.indent -= self.step



    def save(self):
        self.c.save()

    def addHeader(self,txt):

        self.addText(txt + ":")
        self.c.setFont('Helvetica', 12)

    def addText(self,txt):
        self.c.drawString(self.x + self.indent,self.y,txt)
        self.y -= self.textHeight + 2
        if((self.y - self.textHeight) <= 0):
            self.x += self.columWidth
            self.y = 0

files = glob.glob("sheets/*.yaml")
for f in files:
    pg = PdfGen(f)
    pg.generate()
    pg.save()
