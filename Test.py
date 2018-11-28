from tkinter import *
import time
from PIL import Image, ImageTk
from Step4_Train import Helper
import numpy as np
import os
import random
from Processing import ClfCore


class MainUI(Frame):
    def __init__(self,master, **kwargs):
        # Frame.__init__(self,self.master) #设置框架类的父类（基于master<主窗体>），frame可以是看做控件的父容器
        # self.pack() #显示frame控件
        self.clfCore=ClfCore()
        self.master = master
        self.createWidgets()
        self.selectedImgIndex=0
        self.classIndex=0
        self.predictResult=[]
        self.predictArgSort=[]
        # self.helper=Helper()

    def createWidgets(self):    #用于创建控件（是frame的子）
        self.frameL1 = Frame(self.master,width=500, height=120,bg='lightgray')
        self.frameL2 = Frame(self.master,width=500, height=40,bg='lightgray')
        self.frameL3 = Frame(self.master,width=500, height=120,bg='lightgray')
        self.frameL4 = Frame(self.master,width=500, height=35,bg='lightgray')

        self.frameL1.grid(row=0, column=0,padx=1,pady=1)
        self.frameL2.grid(row=1, column=0,padx=1,pady=1)
        self.frameL3.grid(row=2, column=0,padx=1,pady=1)
        self.frameL4.grid(row=3, column=0,padx=1,pady=1)

        self.image_0 = self.getOrderedImage(0,0)
        self.image_1 = self.getOrderedImage(1,0)
        self.image_2 = self.getOrderedImage(2,0)
        self.image_3 = self.getOrderedImage(3,0)
        self.selectedImage=self.image_0


        #添加按钮
        self.btnSend = Button(self.frameL4, text='发 送', width = 8,command=self.onSendMsg)#在frmLB容器中添加
        self.btnSend.grid(row=0,column=0,sticky=N+S)
        

        self.btnCancel = Button(self.frameL4, text='取消', width = 8)
        self.btnCancel.grid(row=0,column=1,sticky=N+S)

        self.lblImage0 = Button(self.frameL2,command=lambda:self.onImageBtn(0))
        self.lblImage1 = Button(self.frameL2,command=lambda:self.onImageBtn(1))
        self.lblImage2 = Button(self.frameL2,command=lambda:self.onImageBtn(2))
        self.lblImage3 = Button(self.frameL2,command=lambda:self.onImageBtn(3))
        

        self.lblImage0.grid(row=0,column=0,padx=40)
        self.lblImage1.grid(row=0,column=1,padx=40)
        self.lblImage2.grid(row=0,column=2,padx=40)
        self.lblImage3.grid(row=0,column=3,padx=40)

        self.setButtonImages()


        # lblImage.grid(sticky=W+E+N+S)

        self.sendMsgContent = Text(self.frameL3,bg='white')
        self.sendMsgContent.grid()
        self.sendMsgContent.bind('<Key-Tab>',self.onTabKeyHandler)
        # self.sendMsgContent.image_create(END,image=self.imgInfo)

        self.receivedMsgContent = Text(self.frameL1,bg='darkgray')        
        self.receivedMsgContent.grid()
        # self.receivedMsgContent.insert(END,'text')
        self.receivedMsgContent.config(state=DISABLED)

        self.frameL1.grid_propagate(0)
        self.frameL2.grid_propagate(0)
        self.frameL3.grid_propagate(0)
        self.frameL4.grid_propagate(0)


    def onSendMsg(self):
        msg=self.sendMsgContent.get(1.0,END)
        self.receivedMsgContent.config(state=NORMAL)
        self.receivedMsgContent.insert(END,msg)
        self.receivedMsgContent.config(state=DISABLED)
        self.sendMsgContent.delete(1.0,END)

        self.clfCore.updateMatrix(self.selectedImgIndex,self.classIndex)

    # def getImage(self,fileName):
    #     img = ImageTk.PhotoImage(Image.open('Images/'+fileName))
    #     return img

    def getOrderedImage(self,folderIndex,imgIndex):
        img = ImageTk.PhotoImage(Image.open(os.path.join('Imgs',str(folderIndex),str(imgIndex+1)+'.jpg')))
        return img

    def setSelectedImage(self,index):
        if(index==0):
            self.selectedImage=self.image_0
        elif(index==1):
            self.selectedImage=self.image_1
        elif(index==2):
            self.selectedImage=self.image_2
        elif(index==3):
            self.selectedImage=self.image_3

        self.selectedImgIndex = self.predictArgSort[index]
        self.sendMsgContent.image_create(INSERT,image=self.selectedImage)

    def setButtonImages(self):
        self.lblImage0.config(image=self.image_0)
        self.lblImage0.image=self.image_0

        self.lblImage1.config(image=self.image_1)
        self.lblImage1.image=self.image_1

        self.lblImage2.config(image=self.image_2)
        self.lblImage2.image=self.image_2

        self.lblImage3.config(image=self.image_3)
        self.lblImage3.image=self.image_3

    # def getSortedIndex(data):

    
    def onTabKeyHandler(self,event):
        # self.image_0=self.getImage('o.ico')
        # self.lblImage0.config(image=self.image_0)
        # self.lblImage0.image=self.image_0
        text=self.sendMsgContent.get(1.0,END)
        if(text==''):
            return
        
        # result=self.helper.Predict(text)
        # result=np.argsort(result)

        imgIndex,proList = self.clfCore.predict(text)
        self.classIndex = imgIndex

        self.predictResult = proList
        self.predictArgSort=np.argsort(-proList,axis=-1, kind='quicksort', order=None)        
        

        self.image_0=self.getOrderedImage(self.predictArgSort[0],self.classIndex)
        self.image_1=self.getOrderedImage(self.predictArgSort[1],self.classIndex)
        self.image_2=self.getOrderedImage(self.predictArgSort[2],self.classIndex)
        self.image_3=self.getOrderedImage(self.predictArgSort[3],self.classIndex)

        self.selectedImgIndex=self.predictArgSort[0]
        self.setButtonImages()

        self.selectedImage=self.image_0
        self.sendMsgContent.image_create(INSERT,image=self.image_0)

    # def onBtnImage0(self):
    #     self.selectedIndex=0
    #     self.sendMsgContent.image_create(INSERT,image=self.image_0)
        # data=self.sendMsgContent.get(1.0,END)[:-2]
        # self.sendMsgContent.delete(1.0,END)
        # self.sendMsgContent.insert(END,data)

    # def onBtnImage1(self):
    #     self.tmp=self.getImage('Icon.jpg')
    #     self.sendMsgContent.image_create(INSERT,image=self.tmp)
    #     self.selectedIndex=1

    def onImageBtn(self,index):
        self.setSelectedImage(index)


if __name__ == '__main__':    
    root = Tk()
    root.resizable(0,0)
    root.title('Messager')

    mainUI = MainUI(root)
    root.mainloop()