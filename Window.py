import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import tkinter.messagebox
from PIL import ImageTk, Image
import random
import time

from Employee import Employee
from Award import Award
from ImgLabel import ImageLabel

class Window:
    
    title = '鈦昇科技年終大摸彩'
    font = '標楷體'
    fullScreenState = True
    xSize = 1280
    ySize = 720
    window = None
    nowPage = None
    
    def __init__(self):
        
        if not os.path.exists('./award_img_import'):
            os.makedirs('./award_img_import')
        if not os.path.exists('./lottery_result'):
            os.makedirs('./lottery_result')
        
        self.window = tk.Tk()
        self.window.title(self.title)
        self.window.geometry('%dx%d' % (self.xSize, self.ySize))
        self.window.minsize(self.xSize, self.ySize)
        
        self.setScreenState()
        self.window.bind("<F11>", self.toggleFullScreen)
        self.window.bind("<Escape>", self.quitFullScreen)
        
        self.backgroundImg = ImageTk.PhotoImage(Image.open('image/BG.png'))
        self.logoImg = ImageTk.PhotoImage(Image.open('image/enr_logo.jpg').resize((186, 56), Image.ANTIALIAS))
    
        #self.setBackGround()
        self.nowPage = StartPage(self)
        self.window.mainloop()
        
    def setScreenState(self):
        self.window.attributes("-fullscreen", self.fullScreenState)
        if type(self.nowPage) == LotteryPage:
            self.nowPage = LotteryPage(self)
        
        
    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.setScreenState()

    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.setScreenState()
            
    def setBackGround(self):
        self.backgroundCanvas = tk.Canvas(self.window, bg='#B00000')
        self.backgroundCanvas.create_image(0, 0, image=self.backgroundImg, anchor=tk.NW)
        self.backgroundCanvas.pack(fill=tk.BOTH, expand=True)
        
    def setLogo(self):
        self.backgroundCanvas.create_image(0, 0, image=self.logoImg, anchor=tk.NW)

    def clearWindow(self, setLogo=True):
        for widget in self.window.winfo_children():
            widget.destroy()
        self.setBackGround()
        if setLogo:
            self.setLogo()

class StartPage():
    
    window = None
    firstTime = True
    
    def __init__(self, w):
        self.window = w
        self.logoImg = ImageTk.PhotoImage(Image.open('image/enr_logo.jpg').resize((558, 168), Image.ANTIALIAS))
        tk.Label(self.window.window, image = self.logoImg).place(relx=0.5, rely=0.45, anchor=tk.CENTER)
        tk.Label(self.window.window, text = self.window.title, font=(self.window.font, 48), fg='#000000').place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        
        titlePlace = {'relx': 0.5, 'rely': 0.8, 'anchor': tk.CENTER}
        titleData = {
            'text': '請按左鍵開始', 
            'font': (self.window.font, 32),
            'fg': '#000000'
        }
        self.lb = tk.Label(self.window.window, **titleData)
        self.lb.place(**titlePlace)
        self.window.window.bind("<Button-1>", lambda x:self.toMainPage())
        
    def toMainPage(self):
        if StartPage.firstTime:
            def nextF():
                self.window.nowPage = MainPage(self.window)
            StartPage.firstTime = False
            self.lb.config(text='載入中 請稍後')
            self.lb.after(100, nextF)

class MainPage():
    
    window = None
    firstTime = True
    
    def __init__(self, w):
        
        if MainPage.firstTime:
            Employee.loadList()
            Award.loadList()
            MainPage.firstTime = False
        
        self.window = w
        self.window.clearWindow()
        
        titlePlace = {'relx': 0.5, 'rely': 0.3, 'anchor': tk.CENTER}
        titleData = {
            'text': self.window.title, 
            'font': (self.window.font, 52, 'bold'),
            'fg': '#FFFF00',
            'bg': '#BB0000'
        }
        goMenuBtnPlace = {'relx': 0.99, 'rely': 0.01, 'anchor': tk.NE}
        goMenuBtnData = {
            'text': '結束程式', 
            'font': (self.window.font, 12), 
            'width': 8, 
            'height': 1,
            'bg': '#FFFFFF', 
            'command': self.window.window.destroy
        }
        BtnListPlace = {'relx': 0.5, 'anchor': tk.CENTER}
        BtnListData = {
            'font': (self.window.font, 20), 
            'width': 15, 
            'height': 1,
            'bg': '#FFFFFF'
        }
        BtnList = [
            {
                'place': {'rely': 0.6},
                'data': {
                    'text': '抽獎', 
                    'command': self.goLotteryPage
                }
            },
            {
                'place': {'rely': 0.72},
                'data': {
                    'text': '員工名單', 
                    'command': self.goEmployeePage
                }
            },
            {
                'place': {'rely': 0.84},
                'data': {
                    'text': '獎項設定', 
                    'command': self.goAwardsPage
                }
            },
        ]
        
        tk.Label(self.window.window, **titleData).place(**titlePlace)
        goMenuBtn = tk.Button(self.window.window, **goMenuBtnData)
        goMenuBtn.place(**goMenuBtnPlace)
        for d in BtnList:
            btn = tk.Button(self.window.window, **BtnListData, **d['data'])
            btn.place(**BtnListPlace, **d['place'])

    def goLotteryPage(self):
        if len(Award.globalList) > 0:
            self.window.nowPage = LotteryPage(self.window)
            del self
        else:
            tk.messagebox.showerror(title='錯誤', message='尚未設定獎項')
    
    def goEmployeePage(self):
        self.window.nowPage = EmployeePage(self.window)
        del self
    
    def goAwardsPage(self):
        self.window.nowPage = AwardPage(self.window)
        del self

class SubPage:
    
    window = None
    
    def __init__(self, w, setLogo=True):
        self.window = w
        self.window.clearWindow(setLogo)
        
        goMenuBtnPlace = {'relx': 0.01, 'rely': 0.99, 'anchor': tk.SW}
        goMenuBtnData = {
            'text': '回首頁', 
            'font': (self.window.font, 12), 
            'width': 8, 
            'height': 1,
            'bg': '#FFFFFF', 
            'command': self.goMainPage
        }
        goMenuBtn = tk.Button(self.window.window, **goMenuBtnData)
        goMenuBtn.place(**goMenuBtnPlace)
        
    def goMainPage(self):
        self.window.nowPage = MainPage(self.window)
        #del self
        
class EmployeePage(SubPage):
    
    def __init__(self, w):
        super().__init__(w)
        self.createTable()
        self.createButtons()
        
    def createTable(self):
        self.listCanvas = tk.Canvas(self.window.window)
        self.listCanvas.place(relx=0.5, rely=0.5, 
                              relheight=0.8, relwidth=0.6, anchor=tk.CENTER)
        self.listFrame = tk.Frame(self.listCanvas)
        
        l = len(Employee.globalList)
        for i, k in enumerate(Employee.keyList):
            lb = tk.Label(self.listFrame, **Employee.showListData[k])
            lb.grid(row=0, column=i, padx=0, pady=0, ipadx=10, ipady=10)
        for i, d in enumerate(Employee.getDictList()):
            for j, k in enumerate(Employee.keyList):
                dd = Employee.showListData[k].copy()
                dd['text'] = d[k]
                lb = tk.Label(self.listFrame, **dd)
                lb.grid(row=i+1, column=j, padx=0, pady=0, ipadx=10, ipady=10)
        
        self.listFrame.configure(height = (l + 1) * 54, width=1145)
        self.listXbar = tk.Scrollbar(self.listCanvas, orient=tk.HORIZONTAL, 
                                     command=self.listCanvas.xview)
        self.listXbar.place(relx=0, rely=1, height=20, relwidth=1, anchor=tk.SW)
        self.listVbar = tk.Scrollbar(self.listCanvas, orient=tk.VERTICAL, 
                                     command=self.listCanvas.yview)
        self.listVbar.place(relx=1, rely=0, width=20, relheight=1, anchor=tk.NE)
        self.listCanvas.create_window(0, 0, anchor=tk.NW, window=self.listFrame)
        self.listCanvas.config(scrollregion=self.listCanvas.bbox('all'), 
                               xscrollcommand=self.listXbar.set, 
                               yscrollcommand=self.listVbar.set)
        
    def recreateTable(self):
        self.listCanvas.destroy()
        self.createTable()
        
    def createButtons(self):
        dd = {'font': (self.window.font, 20), 
             'width': 15,
             'height': 1,
             'bg': '#FFFFFF'}
        btns = [
            {
                'txt': '清空所有得獎',
                'cmd': self.clearAward,
                'y': 0.36
            },
            {
                'txt': '匯入名單試算表',
                'cmd': self.importEmployee,
                'y': 0.48
            },
            {
                'txt': '匯出空白試算表',
                'cmd': self.exportEmpty,
                'y': 0.60
            },
            {
                'txt': '匯出名單試算表',
                'cmd': self.exportEmpoyee,
                'y': 0.72
            },
            {
                'txt': '匯出得獎名單',
                'cmd': self.exportAward,
                'y': 0.84
            }
        ]
        for d in btns:
            btn = tk.Button(self.window.window, **dd, 
                            text=d['txt'], command=d['cmd'])
            btn.place(relx=0.99, rely=d['y'], anchor=tk.E)
           
    def clearAward(self):
        Employee.clearAward()
        self.recreateTable()
    
    def importEmployee(self):
        fn = filedialog.askopenfilename(initialdir='./', 
                                        initialfile='employee_list.xlsx', 
                                        filetypes=(("All","*.xlsx"),
                                                   ("xlsx file","*.xlsx")))
        if len(fn) > 0:
            Employee.importList(fn)
            self.recreateTable()
        
    def exportEmpty(self):
        fn = filedialog.asksaveasfilename(initialdir='./', 
                                          initialfile='employee_list.xlsx', 
                                          defaultextension='.xlsx', 
                                          filetypes=(("All","*.xlsx"),
                                                     ("xlsx file","*.xlsx")))
        if len(fn) > 0:
            Employee.exportEmptyList(fn)
        
    def exportEmpoyee(self):
        fn = filedialog.asksaveasfilename(initialdir='./', 
                                          initialfile='employee_list.xlsx', 
                                          defaultextension='.xlsx', 
                                          filetypes=(("All","*.xlsx"),
                                                     ("xlsx file","*.xlsx")))
        if len(fn) > 0:
            Employee.exportList(fn)
            
    def exportAward(self):
        fn = filedialog.asksaveasfilename(initialdir='./', 
                                          initialfile='award_result.xlsx', 
                                          defaultextension='.xlsx', 
                                          filetypes=(("All","*.xlsx"),
                                                     ("xlsx file","*.xlsx")))
        if len(fn) > 0:
            Employee.exportAward(fn)

class AwardPage(SubPage):
        
    def __init__(self, w):
        super().__init__(w)
        self.createTable()
        self.createButtons()
        
    def createTable(self):
        
        self.listCanvas = tk.Canvas(self.window.window)
        self.listCanvas.place(relx=0.5, rely=0.5, 
                              relheight=0.8, relwidth=0.6, anchor=tk.CENTER)
        self.listFrame = tk.Frame(self.listCanvas)
        
        l = len(Award.globalList)
        for i, k in enumerate(Award.keyList):
            lb = tk.Label(self.listFrame, **Award.showListData[k])
            lb.grid(row=0, column=i, padx=0, pady=0, 
                    ipadx=Award.showListData[k]['width'], ipady=10)

        for i, a in enumerate(Award.globalList):
            lb = tk.Label(self.listFrame, image=a.img200_200, relief=tk.GROOVE)
            lb.grid(row=i+1, column=0, padx=0, pady=0, ipadx=9, ipady=2.5)
            d = a.getDict()
            for j, k in enumerate(Award.keyList[1:]):
                dd = Award.showListData[k].copy()
                dd['text'] = d[k]
                dd['height'] = 7
                lb = tk.Label(self.listFrame, **dd)
                lb.grid(row=i+1, column=j+1, padx=0, pady=0, 
                        ipadx=Award.showListData[k]['width'], ipady=0)

        self.listFrame.configure(height=80 + 195 * (l + 1), width=1145)
        self.listXbar = tk.Scrollbar(self.listCanvas, orient=tk.HORIZONTAL, 
                                     command=self.listCanvas.xview)
        self.listXbar.place(relx=0, rely=1, height=20, relwidth=1, anchor=tk.SW)
        self.listVbar = tk.Scrollbar(self.listCanvas, orient=tk.VERTICAL, 
                                     command=self.listCanvas.yview)
        self.listVbar.place(relx=1, rely=0, width=20, relheight=1, anchor=tk.NE)
        self.listCanvas.create_window(0, 0, anchor=tk.NW, window=self.listFrame)
        self.listCanvas.config(scrollregion=self.listCanvas.bbox('all'), 
                               xscrollcommand=self.listXbar.set,
                               yscrollcommand=self.listVbar.set)
        
    def recreateTable(self):
        self.listCanvas.destroy()
        self.createTable()
        
    def createButtons(self):
        dd = {'font': (self.window.font, 20), 
             'width': 15,
             'height': 1,
             'bg': '#FFFFFF'}
        btns = [
            {
                'txt': '匯入獎項試算表',
                'cmd': self.importAward,
                'y': 0.48
            },
            {
                'txt': '匯出空白試算表',
                'cmd': self.exportEmpty,
                'y': 0.60
            }
        ]
        for d in btns:
            btn = tk.Button(self.window.window, **dd, 
                            text=d['txt'], command=d['cmd'])
            btn.place(relx=0.99, rely=d['y'], anchor=tk.E)
        
    def importAward(self):
        fn = filedialog.askopenfilename(initialdir='./', 
                                        initialfile='award_list.xlsx', 
                                        filetypes=(("All","*.xlsx"),
                                                   ("xlsx file","*.xlsx")))
        if len(fn) > 0:
            Award.importList(fn)
            self.recreateTable()
    
    def exportEmpty(self):
        fn = filedialog.asksaveasfilename(initialdir='./', 
                                          initialfile='award_list.xlsx', 
                                          defaultextension='.xlsx', 
                                          filetypes=(("All","*.xlsx"),
                                                     ("xlsx file","*.xlsx")))
        if len(fn) > 0:
            Award.exportEmptyList(fn)
            
class LotteryPage(SubPage):
    
    nowLottery = 0
    isLotterting = False
    
    def __init__(self, w):
        super().__init__(w, False)
        self.createBG()
        self.window.setLogo()
        self.createStage()
        self.createTable()
        self.createButtons()
        self.updateButtons()
        
    def createBG(self):
        bg = self.window.backgroundCanvas
        self.window.window.update()
        w = bg.winfo_width()
        h = bg.winfo_height()
        self.stageImg = ImageTk.PhotoImage(Image.open('image/stage.png').resize((int(1300 * w / 1920), int(300 * h / 1080)), Image.ANTIALIAS))
        bg.create_image(0, 0, image=self.stageImg, anchor=tk.NW)
        self.rollImg = ImageTk.PhotoImage(Image.open('image/roll.png').resize((int(680 * w / 1920 * 1.5), int(250 * h / 1080 * 1.5)), Image.ANTIALIAS))
        bg.create_image(w * 0.35, h * 0.83, image=self.rollImg, anchor=tk.CENTER)
    
    def createStage(self):
        bg = self.window.backgroundCanvas
        self.window.window.update()
        w = bg.winfo_width()
        h = bg.winfo_height()
        self.showImg = ImageTk.PhotoImage(Image.open(Award.globalList[LotteryPage.nowLottery].img).resize((int(300 * w / 1920), int(300 * h / 1080)), Image.ANTIALIAS))
        bg.create_image(w * 0.35, h * 0.4, image=self.showImg, anchor=tk.CENTER)
        self.awardText = bg.create_text(w * 0.35, h * 0.15, 
                                        text=Award.globalList[LotteryPage.nowLottery].award, 
                                        font=(self.window.font, int(52 * w / 1920), 'bold'), 
                                        fill='#FFFF00', anchor=tk.CENTER)
        self.descText = bg.create_text(w * 0.35, h * 0.62, 
                                       text=Award.globalList[LotteryPage.nowLottery].desc, 
                                       font=(self.window.font, int(46 * w / 1920), 'bold'), 
                                       fill='#FFFF00', anchor=tk.CENTER)
        self.rollTxt1 = bg.create_text(w * 0.20, h * 0.79, text='', 
                                       font=(self.window.font, int(32 * w / 1920), 'bold'),
                                       fill='#000000', anchor=tk.CENTER, justify=tk.CENTER)
        self.rollTxt2 = bg.create_text(w * 0.35, h * 0.79, text='', 
                                       font=(self.window.font, int(32 * w / 1920), 'bold'),
                                       fill='#000000', anchor=tk.CENTER, justify=tk.CENTER)
        self.rollTxt3 = bg.create_text(w * 0.50, h * 0.79, text='', 
                                       font=(self.window.font, int(32 * w / 1920), 'bold'), 
                                       fill='#000000', anchor=tk.CENTER, justify=tk.CENTER)
        
    def createTable(self):
        bg = self.window.backgroundCanvas
        self.window.window.update()
        self.w = bg.winfo_width()
        self.dd = [
            {
                'text': '項次',
                'width': int(2 * self.w / 1920 + 3)
            },
            {
                'text': '員工編號',
                'width': int(5 * self.w / 1920 + 7)
            },
            {
                'text': '部門單位',
                'width': int(3 * self.w / 1920 + 16)
            },
            {
                'text': '中獎人',
                'width': int(3 * self.w / 1920 + 6)
            } 
        ]
        self.ipadxs = [0, 0, 0, 0]
        self.listCanvas = tk.Canvas(self.window.window)
        self.listCanvas.place(relx=1, rely=0, relheight=0.6, relwidth=0.323, anchor=tk.NE)
        self.listFrame = tk.Frame(self.listCanvas)
        for i in range(len(self.dd)):
            lb = tk.Label(self.listFrame, **self.dd[i], 
                          font=(self.window.font, int(18 * self.w / 1920), 'bold'), 
                          height=1, relief=tk.GROOVE)
            lb.grid(row=0, column=i, padx=0, pady=0, ipadx=self.ipadxs[i], ipady=10)
        self.updateTable()
        l=Award.globalList[LotteryPage.nowLottery].num
        self.listFrame.configure(height=65 * (l + 1), width=int(600 * self.w / 1920))
        self.listXbar = tk.Scrollbar(self.listCanvas, orient=tk.HORIZONTAL, 
                                     command=self.listCanvas.xview)
        self.listXbar.place(relx=0, rely=1, height=20, relwidth=1, anchor=tk.SW)
        self.listVbar = tk.Scrollbar(self.listCanvas, orient=tk.VERTICAL, 
                                     command=self.listCanvas.yview)
        self.listVbar.place(relx=1, rely=0, width=20, relheight=1, anchor=tk.NE)
        self.listCanvas.create_window(0, 0, anchor=tk.NW, window=self.listFrame)
        self.listCanvas.config(scrollregion=self.listCanvas.bbox('all'), 
                               xscrollcommand=self.listXbar.set, 
                               yscrollcommand=self.listVbar.set)
        
    def updateTable(self):
        bg = self.window.backgroundCanvas
        lst = Employee.getSearchList(Award.globalList[LotteryPage.nowLottery].award)
        for i in range(Award.globalList[LotteryPage.nowLottery].num):
            t = [str(i + 1), '', '', '']
            if i < len(lst):
                t = [str(i + 1), lst[i]['nid'], lst[i]['apart'], lst[i]['name']]
            for j in range(len(self.dd)):
                d = self.dd[j].copy()
                d['text'] = t[j]
                lb = tk.Label(self.listFrame, **d, 
                              font=(self.window.font, int(18 * self.w / 1920), 'bold'), 
                              height=1, relief=tk.GROOVE)
                lb.grid(row=i+1, column=j, padx=0, pady=0, ipadx=self.ipadxs[j], ipady=10)
        def strNewline(s, n):
            l = []
            if s[0:2].isdigit():
                for i in range(len(s) - 1, 0, -1):
                    if s[0:i].isdigit():
                        l.append(s[0:i])
                        s = s[i:]
                        break
            for i in range(0, len(s), n):
                l.append(s[i:i + n])
            return '\n'.join(l)
        bg.itemconfig(self.rollTxt1, text=str(lst[-1]['nid'] if len(lst) > 0 else ''))
        bg.itemconfig(self.rollTxt2, text=strNewline(lst[-1]['apart'] if len(lst) > 0 else '', 4))
        bg.itemconfig(self.rollTxt3, text=strNewline(lst[-1]['name'] if len(lst) > 0 else '', 4))
    
    def createButtons(self):
        bg = self.window.backgroundCanvas
        self.window.window.update()
        w = bg.winfo_width()
        h = bg.winfo_height()
        self.rollBtnTxt = bg.create_text(w * 0.67, h * 0.93, 
                                         text=Award.globalList[LotteryPage.nowLottery].way, 
                                         font=(self.window.font, int(32 * w / 1920), 'bold'), 
                                         fill='#FFFF00', anchor=tk.CENTER)
        self.rollBtnImg = ImageTk.PhotoImage(Image.open('image/roll_btn.png').resize((int(150 * w / 1920), int(150 * h / 1080)), Image.ANTIALIAS))
        self.rollBtn = bg.create_image(w * 0.67, h * 0.8, image=self.rollBtnImg, anchor=tk.CENTER)
        bg.tag_bind(self.rollBtn, '<Button-1>', lambda x:self.lottery())
        self.window.window.bind("<Return>", lambda x:self.lottery())
        self.lastBtnImg = ImageTk.PhotoImage(Image.open('image/last.png').resize((int(150 * w / 1920), int(150 * h / 1080)), Image.ANTIALIAS))
        self.lastBtn = bg.create_image(w * 0.8, h * 0.85, image=self.lastBtnImg, anchor=tk.CENTER)
        bg.tag_bind(self.lastBtn, '<Button-1>', lambda x:self.goNext(-1))
        self.window.window.bind("<Left>", lambda x:self.goNext(-1))
        self.nextBtnImg = ImageTk.PhotoImage(Image.open('image/next.png').resize((int(150 * w / 1920), int(150 * h / 1080)), Image.ANTIALIAS))
        self.nextBtn = bg.create_image(w * 0.9, h * 0.85, image=self.nextBtnImg, anchor=tk.CENTER)
        bg.tag_bind(self.nextBtn, '<Button-1>', lambda x:self.goNext(1))
        self.window.window.bind("<Right>", lambda x:self.goNext(1))
    
    def lottery(self):
        if LotteryPage.isLotterting:
            return
        LotteryPage.isLotterting = True
        def doLottery():
            ept = Employee.getSearchObjList(None, Award.globalList[LotteryPage.nowLottery].minYear, Award.globalList[LotteryPage.nowLottery].exclude)
            random.shuffle(ept)
            n = 1
            if Award.globalList[LotteryPage.nowLottery].way == '一次抽出':
                n = Award.globalList[LotteryPage.nowLottery].num
                if n > len(ept):
                    n = len(ept)
            for e in ept[:n]:
                e.setAward(Award.globalList[LotteryPage.nowLottery].award)
            self.updateButtons()
            self.updateTable()
            self.rollImg1.destroy()
            self.rollImg2.destroy()
            self.rollImg3.destroy()
            l = Award.globalList[LotteryPage.nowLottery].num
            lst = Employee.getSearchList(Award.globalList[LotteryPage.nowLottery].award)
            ept = Employee.getSearchList(None, Award.globalList[LotteryPage.nowLottery].minYear, Award.globalList[LotteryPage.nowLottery].exclude)
            if (len(lst) >= l) or (len(ept) == 0):
                Employee.exportAward('./lottery_result/' + time.strftime('%Y%m%d_%H%M%S') + '.xlsx')
            LotteryPage.isLotterting = False
        
        bg = self.window.backgroundCanvas
        self.window.window.update()
        w = bg.winfo_width()
        h = bg.winfo_height()
        self.rollImg1 = ImageLabel(self.window.window)
        self.rollImg1.place(relx=0.20, rely=0.79, anchor=tk.CENTER)
        self.rollImg2 = ImageLabel(self.window.window)
        self.rollImg2.place(relx=0.35, rely=0.79, anchor=tk.CENTER)
        self.rollImg3 = ImageLabel(self.window.window)
        self.rollImg3.place(relx=0.50, rely=0.79, anchor=tk.CENTER)
        self.rollImg1.load('./image/rolling1.gif', 200 * w // 1920, 200 * h // 1080)
        self.rollImg2.load('./image/rolling2.gif', 200 * w // 1920, 200 * h // 1080)
        self.rollImg3.load('./image/rolling3.gif', 200 * w // 1920, 200 * h // 1080, endDo=doLottery)
    
    def goNext(self, n):
        LotteryPage.nowLottery += n
        self.window.nowPage = LotteryPage(self.window)
    
    def updateButtons(self):
        bg = self.window.backgroundCanvas
        l = Award.globalList[LotteryPage.nowLottery].num
        lst = Employee.getSearchList(Award.globalList[LotteryPage.nowLottery].award)
        ept = Employee.getSearchList(None, Award.globalList[LotteryPage.nowLottery].minYear, Award.globalList[LotteryPage.nowLottery].exclude)
        if (not len(lst) < l) or (len(ept) == 0):
            bg.delete(self.rollBtn)
            bg.delete(self.rollBtnTxt)
            self.window.window.unbind("<Return>")
        if not LotteryPage.nowLottery > 0:
            bg.delete(self.lastBtn)
            self.window.window.unbind("<Left>")
        if not LotteryPage.nowLottery + 1 < len(Award.globalList):
            bg.delete(self.nextBtn)
            self.window.window.unbind("<Right>")