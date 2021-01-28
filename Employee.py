import tkinter as tk
import FileIO
from Award import Award

class Employee:
    
    font = '標楷體'
    globalList = []
    globalAwardCount = 0
    
    nid = ''
    name = ''
    apart = ''
    year = 0
    award = None
    awardNum = 0
    keyList = ['nid', 'apart', 'name', 'year', 'award']
    showListData = {
        'nid': {
            'text': '員工編號', 
            'font': (font, 20), 
            'width': 15, 
            'height': 1,
            'relief': tk.GROOVE
        },
        'apart': {
            'text': '部門單位', 
            'font': (font, 20), 
            'width': 20, 
            'height': 1,
            'relief': tk.GROOVE
        },
        'name': {
            'text': '姓名', 
            'font': (font, 20), 
            'width': 15, 
            'height': 1,
            'relief': tk.GROOVE
        },
        'year': {
            'text': '年資', 
            'font': (font, 20), 
            'width': 6, 
            'height': 1,
            'relief': tk.GROOVE
        },
        'award': {
            'text': '得獎', 
            'font': (font, 20), 
            'width': 15, 
            'height': 1,
            'relief': tk.GROOVE
        }
    }
    
    def __init__(self, nid, apart, name, year, award=None, awardNum=None):
        self.nid = nid
        self.name = name
        self.apart = apart
        self.year = year
        self.award = award
        self.awardNum = awardNum
        if awardNum != None and awardNum > Employee.globalAwardCount:
            Employee.globalAwardCount = awardNum
        Employee.globalList.append(self)
        
    def setAward(self, award):
        Employee.globalAwardCount = Employee.globalAwardCount + 1
        self.award = award
        self.awardNum = Employee.globalAwardCount
        Employee.saveList()
        
    def getDict(self):
        d = {'nid': self.nid,
             'name': self.name,
             'apart': self.apart,
             'year': self.year,
             'award': '' if self.award == None else self.award}
        return d
     
    def getFullDict(self):
        d = {'nid': self.nid,
             'name': self.name,
             'apart': self.apart,
             'year': self.year,
             'award': self.award,
             'awardNum': self.awardNum}
        return d

    def getList(self):
        l = [self.nid,
             self.name,
             self.apart,
             self.year,
             '' if self.award == None else self.award]
        return l
    
    @staticmethod
    def getDictList():
        lst = [e.getDict() for e in Employee.globalList]
        return lst
    
    @staticmethod
    def getFullDictList():
        lst = [e.getFullDict() for e in Employee.globalList]
        return lst
    
    @staticmethod
    def getListList():
        lst = [e.getList() for e in Employee.globalList]
        return lst
    
    @staticmethod
    def importList(fn):
        lst = FileIO.loadXlsx(fn, '員工名單', 4)
        Employee.globalList = []
        for i in lst:
            Employee(i[0], i[1], i[2], i[3])
        Employee.saveList()
    
    @staticmethod
    def exportList(fn):
        k = ['員工編號', '部門單位', '姓名', '年資', '得獎']
        w = [15, 24, 12, 5, 20]
        lst = Employee.getListList()
        FileIO.dumpXlsx(fn, '員工名單', k, w, lst)
        
    @staticmethod
    def exportEmptyList(fn):
        k = ['員工編號', '部門單位', '姓名', '年資']
        w = [15, 24, 12, 5]
        FileIO.dumpXlsx(fn, '員工名單', k, w)
    
    @staticmethod
    def exportAward(fn):
        l = Employee.getFullDictList()
        l = sorted(l, key = lambda s: s['awardNum'] if s['awardNum'] != None else 0)
        l = [i for i in l if i['awardNum'] != None]
        k = ['流水號', '獎項', '獎品名稱', '員工編號', '部門單位', '姓名']
        w = [10, 35, 35, 12, 24, 10]
        lst = []
        for i in l:
            lst.append([i['awardNum'], 
                        i['award'], 
                        Award.getDesc(i['award']), 
                        i['nid'], 
                        i['apart'], 
                        i['name']])
        FileIO.dumpXlsx(fn, '得獎名單', k, w, lst)
    
    @staticmethod
    def loadList():
        lst = FileIO.loadJsonData('employee.json')
        Employee.globalList = []
        for i in lst:
            Employee(i['nid'], 
                     i['apart'], 
                     i['name'], 
                     i['year'], 
                     i['award'], 
                     i['awardNum'])
            
    @staticmethod
    def saveList():
        d = Employee.getFullDictList()
        FileIO.dumpJsonData('employee.json', d)
    
    @staticmethod
    def clearAward():
        for i in Employee.globalList:
            i.award = None
            i.awardNum = None
        Employee.globalAwardCount = 0
        Employee.saveList()
    
    @staticmethod
    def getSearchList(award=None, minYear=0):
        l = Employee.getFullDictList()
        l = sorted(l, key = lambda s: s['awardNum'] if s['awardNum'] != None else 0)
        l = [i for i in l if i['award'] == award and i['year'] >= minYear]
        return l
    
    @staticmethod
    def getSearchObjList(award=None, minYear=0):
        l = Employee.globalList.copy()
        l = sorted(l, key = lambda s: s.awardNum if s.awardNum != None else 0)
        l = [i for i in l if i.award == award and i.year >= minYear]
        return l