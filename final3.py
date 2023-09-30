# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from tkinter import *
import tkinter as tk
from tkinter import colorchooser, ttk,filedialog,Entry
from PIL import ImageTk,Image,ImageDraw,ImageOps
import cv2
import io
import subprocess
import os
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier


class main(object):

    def __init__(self, master):
        self.master = master
        self.master.title="Button Example"
        self.color_fg = "black"
        self.color_bg = "white"
        self.old_x = None
        self.old_y = None
        self.pen_width = 20
        self.darwWidget()
        self.c.bind()
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind("<ButtonRelease-1>", self.reset)
        # self.button1=tk.Button(master,text="clear",command=self.clearcanvas)
        # self.button1.pack()
        # self.button2=tk.Button(master,text="exit",command=self.master.destroy)
        # self.button2.pack()
        self.button3=tk.Button(master,text="learn",command=self.savefile)
        self.label = tk.Label(master, text="Enter answer:")
        self.label.pack()
        self.lrn_input=Entry(master)
        self.lrn_input.pack()
        self.button3.pack()
        self.button5=tk.Button(master,text="pridict",command=self.pridict)
        self.button5.pack()
        self.button4=tk.Button(master,text="result",command=self.show_digits)
        self.button4.pack()
        self.digits=0
        self.tcells=[]
        self.tcells_array=0
        self.targets=[]
        self.df=""
        self.result=0
        self.targets_array=0
        self.X_array=0
        self.y_array=0
        self.data=pd.read_csv("mydf.csv")
        # self.data=self.data.drop("Unnamed: 0",axis=1)
        
    def paint(self, e):
        if self.old_x and self.old_y:
            # print("draw")
            self.c.create_line(self.old_x, self.old_y, e.x, e.y, width=self.pen_width,fill=self.color_fg, capstyle="round", smoot=True)
        self.old_x = e.x
        self.old_y = e.y

    def reset(self, e):
        self.old_x = None
        self.old_y = None

    def changedW(self, width):      
        self.pen_width=width
    
    def clearcanvas(self):
        self.c.delete(ALL)

    def change_fg(self):
        self.color_fg = colorchooser.askcolor(color=self.color_fg)[1]

    def change_bg(self):
        self.color_bg = colorchooser.askcolor(color=self.color_bg)[1]
        self.c['bg']=self.color_bg
            

    def darwWidget(self):
        self.controls=Frame(self.master,padx=5,pady=5)
        # textpw=Label(self.controls,text="pen Width",font="Georgia 16")
        # textpw.grid(row=0,column=0)
        # self.slider=ttk.Scale(self.controls,from_=5 , to=100, command=self.changedW,orient="vertical" )
        # self.slider.set(self.pen_width)
        # self.slider.grid(row=0,column=1)
        # self.controls.pack(side="left")
        self.c=Canvas(self.master,width=500,height=400,bg=self.color_bg)
        self.c.pack(fill=BOTH,expand=True)
        
        menu=Menu(self.master)
        self.master.config(menu=menu)
        optionmenu=Menu(menu)
        menu.add_cascade(label="Menu",menu=optionmenu)
        optionmenu.add_command(label='brush color',command=self.change_fg)
        optionmenu.add_command(label='backgrond color',command=self.change_bg)
        optionmenu.add_command(label='clear convas',command=self.clearcanvas)                     
        optionmenu.add_command(label='Exit',command=self.master.destroy)
        
        
    def savefile(self):
        target=self.lrn_input.get()
       
        
        if target=="":
            print("do nothing")
        else:
            ps = self.c.postscript(colormode='gray')
            img = Image.open(io.BytesIO(ps.encode('utf-8')))
            img=ImageOps.invert(img)
            img=img.resize((40, 40), Image.ANTIALIAS)
            img.save('test.png')
            self.digits=cv2.imread("test.png",cv2.IMREAD_GRAYSCALE)
            self.tcells.append(self.digits.flatten())
            print(target)
            self.targets.append(target)
            self.clearcanvas()
            self. lrn_input.delete(0,"end")
            self.tcells_array=np.array(self.tcells,dtype=np.float32)
            self.targets_array=np.array(self.targets,dtype=np.float32)
            self.df=pd.DataFrame(self.tcells_array)
            self.df['target']=self.targets_array
            # self.df.to_csv("mydf.csv",index=False)
            print(self.df)
            result=pd.concat([self.data,self.df],axis=0)
            # print(result)
            result.to_csv("mydf.csv",index=False)
            
    def show_digits(self):
        print(self.digits)
        digits=self.digits
     
        self.tcells_array=np.array(self.tcells,dtype=np.float32)
        self.targets_array=np.array(self.targets,dtype=np.float32)
        self.master.destroy()
        # test_digits=cv2.imread("test_digits2.png",cv2.IMREAD_GRAYSCALE)
        
        
    def pridict(self):

        X=self.df.loc[:,self.df.columns!="target"]
        y=self.df.loc[:,self.df.columns=="target"]
        self.X_array=np.array(X,dtype=np.float32)
        self.y_array=np.array(y,dtype=np.float32)
        
        knn=cv2.ml.KNearest_create()
        knn.train(self.X_array,cv2.ml.ROW_SAMPLE,self.y_array)
        ret,self.result,neighbours,dist=knn.findNearest(self.X_array,k=3)
        message =neighbours 
        text = self.c.create_text(10, 100, text=message, font=("Helvetica", 10))
        print(self.result)
        
        
        
win = Tk()

win.title("my app")
paint=main(win)
win.mainloop()
# mydf=paint.df
# data=paint.data

