#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from sklearn.naive_bayes import MultinomialNB  # 导入多项式贝叶斯算法
from sklearn import metrics
from sklearn import svm
from Tools import readbunchobj
from Step1_Segment import segment_Line,Step1_Segment
from Step2_ToBunch import seg2Bunch,Step2_ToBunch
from Step3_TFIDFSpace import bunch2Space,Step3_TFIDFSpace
import numpy as np
import cv2
from sklearn.ensemble import RandomForestClassifier

class Helper:
        def __init__(self):
                self.Train()

        def Train(self):
                Step1_Segment()
                Step2_ToBunch()
                Step3_TFIDFSpace()
                trainpath = "train_word_bag/tfdifspace.dat"
                train_set = readbunchobj(trainpath)
                self.vecLen =train_set.tdm.shape[1]


                # clf = svm.SVC()
                self.clf = RandomForestClassifier()
                # clf = MultinomialNB(alpha=0.001)
                self.clf.fit(train_set.tdm, train_set.label)

        def Predict(self,text):
                if(text==''):
                        return ''
                if(len(text)<2):
                        text=text+text
                try:
                        segs = segment_Line(text)
                        bunch=seg2Bunch(segs)
                        space = bunch2Space(bunch)
                        data=space.tdm

                        testData=np.zeros((1,self.vecLen))
                        for i in range(data.shape[1]):
                                testData[0,i]=data[0,i]
                        
                        predicted = self.clf.predict_proba(testData)
                        
                        return predicted[0]
                except Exception as err:
                        print(err)
                        return '0'

        def SaveText(self,fileName,text):
                if(text!=''):
                        textFile = open(fileName, 'a')
                        textFile.write(','+text)
                        textFile.close()

        def ReTrain(self,t0,t1,t2,t3):
                self.SaveText('train_corpus/0/0',t0)
                self.SaveText('train_corpus/1/1',t1)
                self.SaveText('train_corpus/2/2',t2)
                self.SaveText('train_corpus/3/3',t3)
                self.Train()
                

