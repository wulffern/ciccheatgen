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

        print(self.c.getAvailableFonts())

        self.c.setFont('Courier', self.textHeight)
        self.margin = 10
        self.width = width
        self.height = height
        self.x = self.margin
        self.y = height - self.textHeight - self.margin
        self.pageHeight = height
        self.columWidth = width/3
        self.obj = obj
        self.indent = 0
        self.step  = 10
        self.fontheader = "Times-Bold"
        self.fontsizeheader = 13
        self.font = "Times-Roman"
        self.fontsize = 9
        self.rightmargin = 120

    def generate(self):

        if "title" in self.obj:
            self.addTitle(self.obj["title"])

        if "content" in self.obj:
            self.addObj(self.obj["content"])


    def addTitle(self,text):
        self.x += self.margin
        self.addText(text,self.fontheader,self.fontsizeheader)
        self.y -= self.fontsizeheader
        self.x -= self.margin

    def addObj(self,obj):

        if obj is None:
            return

        t = type(obj)

        if(t is dict):
            for k in obj:
                if(k is not ""):
                    self.addHeader(k)
                o = obj[k]
                #self.indent += self.step
                self.addObj(o)
                #self.indent -= self.step
        elif(t is list):
            for k in obj:
                #self.indent += self.step
                self.addText(k)
                #self.indent -= self.step
        self.y -= self.textHeight

    def save(self):
        self.c.save()

    def addHeader(self,txt):

        self.addText(txt,self.fontheader,self.fontsizeheader)


    def addText(self,txt,font=None,fontsize=None):

        if(txt == None):
            txt = ""
        if(font == None):
            font = self.font
        if(fontsize == None):
            fontsize = self.fontsize

        self.c.setFont(font,fontsize)

        #- Split if the string contains ;
        if(";" in txt):
            (t,bindkey) = txt.split(";")
            self.c.drawString(self.x + self.indent,self.y,t)
            self.indent += self.columWidth - self.rightmargin
            self.c.setFont("Courier-Bold",self.fontsize-1)
            self.c.drawString(self.x + self.indent,self.y,bindkey)
            self.c.setFont(self.font,self.fontsize)
            self.indent -= self.columWidth - self.rightmargin
        else:
            self.c.drawString(self.x + self.indent,self.y,txt)
        self.y -= fontsize + 3
        if((self.y - fontsize- self.margin) <= 0):
            self.x += self.columWidth + self.margin
            self.y = self.height - self.margin - self.fontsize
        self.c.setFont(self.font,self.fontsize)

files = glob.glob("sheets/*.yaml")
for f in files:
    pg = PdfGen(f)
    pg.generate()
    pg.save()
