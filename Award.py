import os
import tkinter as tk
from PIL import ImageTk, Image
import FileIO

class Award:
    
    font = '標楷體'
    globalList = []
    
    img = None
    award = ''
    desc = ''
    num = 0
    way = None
    minYear = 0
    
    img200_200 = None
    
    keyList = ['img', 'award', 'desc', 'num', 'way', 'minYear', 'exclude']
    
    showListData = {
        'img': {
            'text': '獎品圖片', 
            'font': (font, 20), 
            'width': 13, 
            'height': 1,
            'relief': tk.GROOVE
        },
        'award': {
            'text': '獎項', 
            'font': (font, 20), 
            'width': 12, 
            'height': 1,
            'relief': tk.GROOVE
        },
        'desc': {
            'text': '獎品名稱', 
            'font': (font, 20), 
            'width': 18, 
            'height': 1,
            'relief': tk.GROOVE
        },
        'num': {
            'text': '數量', 
            'font': (font, 20), 
            'width': 5, 
            'height': 1,
            'relief': tk.GROOVE
        },
        'way': {
            'text': '抽取方式', 
            'font': (font, 20), 
            'width': 8, 
            'height': 1,
            'relief': tk.GROOVE
        },
        'minYear': {
            'text': '最小年資', 
            'font': (font, 20), 
            'width': 8, 
            'height': 1,
            'relief': tk.GROOVE
        },
        'exclude': {
            'text': '備註', 
            'font': (font, 20), 
            'width': 4, 
            'height': 1,
            'relief': tk.GROOVE
        }
    }
    
    def __init__(self, img, award, desc, num, way, minYear, exclude, ind = -1):
        award = str(award)
        self.award = award
        self.desc = desc
        self.num = num
        self.way = '一次抽出' if way != None and '一次' in way else '逐次抽出'
        self.minYear = minYear if minYear != None else 0
        self.exclude = exclude if type(exclude) == bool else (exclude == 'Y')
        
        if not os.path.exists('./data/award_img'):
            os.makedirs('./data/award_img')
        try:
            iTmp = Image.open(img)
        except:
            iTmp = Image.open('./image/default.png')
        
        try:
            iTmp.save('./data/award_img/' + award + '.png')
        except:
            iTmp.convert('RGB').save('./data/award_img/' + award + '.png')
            
        self.img = './data/award_img/' + award + '.png'
        self.img200_200 = ImageTk.PhotoImage(iTmp.resize((190, 185), Image.ANTIALIAS))
        
        
        if ind == -1:
            Award.globalList.append(self)
        else:
            Award.globalList.insert(ind, self)
        
    @staticmethod
    def getDesc(award):
        for d in Award.globalList:
            if d.award == award:
                return d.desc
        return None
    
    def getDict(self):
        d = {'img': self.img,
             'award': self.award,
             'desc': self.desc,
             'num': self.num,
             'way': self.way,
             'minYear': self.minYear,
             'exclude': self.exclude}
        return d
     
    @staticmethod
    def getDictList():
        lst = [a.getDict() for a in Award.globalList]
        return lst
    
    @staticmethod
    def importList(fn):
        lst = FileIO.loadXlsx(fn, '獎項', 7)
        Award.globalList = []
        for i in lst:
            Award('./award_img_import/' + i[5], i[0], i[1], i[2], i[3], i[4], i[6])
        Award.saveList()
    
    @staticmethod
    def exportEmptyList(fn):
        k = ['獎項', '獎品名稱', '數量', '抽取方式(逐次抽出/一次抽出)', '最小年資', '圖片檔案名稱(檔名與附檔名，路徑在"./award_img_import")', '備註']
        w = [12, 20, 8, 16, 10, 20, 8]
        FileIO.dumpXlsx(fn, '獎項', k, w)
    
    @staticmethod
    def loadList():
        lst = FileIO.loadJsonData('award.json')
        Award.globalList = []
        for i in lst:
            Award(i['img'], 
                  i['award'], 
                  i['desc'], 
                  i['num'], 
                  i['way'], 
                  i['minYear'],
                  i['exclude'])
            
    @staticmethod
    def saveList():
        d = Award.getDictList()
        FileIO.dumpJsonData('award.json', d)