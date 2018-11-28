import jieba
import numpy as np


class ClfCore:
    def __init__(self):
        self.matrix=np.ones((4,8),np.int)
        self.loadData()

    def loadData(self):
        filename = 'Data/Data.txt'
        data = open(filename, 'r',encoding='utf-8')
        lines = data.readlines()
        self.KeyWords=[]
        for line in lines:
            line = line.replace('\n','')
            lineItems=line.split(',')
            self.KeyWords.append(lineItems)

    def getClassIndex(self,textKeywords):
        for index in range(8):
            line = self.KeyWords[index]
            for keyword in textKeywords:
                if(keyword in line):
                    return index
        return 0

    def getKewwords(self,text):
        content_seg = jieba.cut(text)
        kewwords=' '.join(content_seg)
        return kewwords.split()

    def predict(self,text):
        keywords = self.getKewwords(text)
        classIndex=self.getClassIndex(keywords)
        proList=self.matrix[:,classIndex]        
        return classIndex,proList
    

    def updateMatrix(self,imgIndex,classIndex):
        self.matrix[imgIndex,classIndex]+=1
        # self.printMatrix()


    def printMatrix(self):
        print(self.matrix)

# clf=ClfCore()
# # ks=clf.getKewwords('高兴赞佩喜悦跃跃欲试')
# clf.updateMatrix(0,5)
# clf.printMatrix()
# print(ks)


