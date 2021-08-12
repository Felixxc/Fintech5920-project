import style, addrevenue, addspending,addrecur,deleterecur
import subprocess   #restart func
import sqlite3, sys
import matplotlib.pyplot as plt     #generate figure
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from plotcanvas import PlotCanvas
from plotcanvas_inv import PlotCanvas_inv
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

con = sqlite3.connect("money.db")
cur = con.cursor()

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.homespending = 0.0
        self.busspending = 0.0
        self.clothesspending = 0.0
        self.eatspending = 0.0
        self.phonespending = 0.0
        self.creditspending = 0.0
        self.others = 0.0
        self.salary = 0.0
        self.investment=0.0
        self.spend = 0.0
        self.trend_month='ALL'
        self.trend_cat='ALL'
        self.setGeometry(250,150,1000,800)
        self.setWindowTitle(' Expense Tracker')
        self.setWindowIcon(QIcon('icons/coin.png'))
        self.setFixedSize(self.size())  #block extending of window
        self.UI()
        self.show()

    def UI(self):
        self.toolBar()
        self.tabWidget()
        self.widgets()
        self.layouts()
        self.tabChanged()


    def toolBar(self):
        self.tb = self.addToolBar("Tool Bar")
        self.tb.setStyleSheet("font: 11pt Arial; color: black; background-color: #FFFFFF;")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.logo=QLabel()
        logopixmap=QPixmap("icons/logo.png")
        self.logo.setPixmap(logopixmap)
        self.tb.addWidget(self.logo)
        self.toolbarBanner=QLabel("     Expense Tracker                                     ")
        self.toolbarBanner.setStyleSheet("font-size: 25pt;  background-color: white; color:black;")
        self.tb.addWidget(self.toolbarBanner)
        ######################################################################toolbar buttons
        ###################################generate figure
        # self.generateFigure = QAction(QIcon('icons/generatefigure.png'), "GENERATE FIGURE", self)
        # self.generateFigure.triggered.connect(self.funcGenerateFigure)
        # self.tb.addAction(self.generateFigure)
        # self.tb.addSeparator()
        ###################################delete datas (new month)
        self.deleteDatas = QAction(QIcon('icons/reset.png'), "RESET", self)
        self.deleteDatas.triggered.connect(self.funcDeleteDatas)
        self.tb.addAction(self.deleteDatas)
        self.tb.addSeparator()


    def tabWidget(self):
        self.tabs = QTabWidget()
        self.tabs.blockSignals(True)    #first thing to refresh window automatically
        self.tabs.currentChanged.connect(self.tabChanged)   #third thing to refresh window automatically
        self.setCentralWidget(self.tabs)    #thanks that we can see tables
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4=QWidget()
        self.tab5=QWidget()
        self.tab6=QWidget()
        self.tabs.addTab(self.tab1, "Main")
        self.tabs.addTab(self.tab2, "Income")
        self.tabs.addTab(self.tab3, "Spendings")
        self.tabs.addTab(self.tab4,"Recurring Expense")
        self.tabs.addTab(self.tab5,"Trends")
        self.tabs.addTab(self.tab6,"Assets")
        self.tabs.setFont(QFont("Arial", 15))
        self.tabs.setStyleSheet("font: Arial;color: #13227a; background-color: #FFFFFF;")

    def get_month_list(self):
        query="select DISTINCT SUBSTR(date,0,8) from spending union select DISTINCT SUBSTR(date,0,8) from revenue"
        monthlist=cur.execute(query)
        month_list=[]
        for item in monthlist:
            month_list.append(item[0])
        return month_list
    
    def get_cat_list_in(self):
        query="select DISTINCT category from  investment"
        inlist=cur.execute(query)
        in_list=[]
        for item in inlist:
            in_list.append(item[0])
        return in_list

    def widgets(self):


        ############################################tab1 widgets
        #left
        self.monthselector=QComboBox()
        self.monthselector.addItems(['ALL']+self.get_month_list())
        self.monthselector.activated[str].connect(self.getValues_bymonth)
        self.monthselector.setStyleSheet("border:1px solid gray;font: 10pt Arial;  background-color: white; color:black;")
        self.automaticBanner=QLabel("Automatic categories")
        self.automaticBanner.setStyleSheet("font-size: 12pt Arial;  background-color: white; color:black;")
        self.manualBanner=QLabel(r"Manual catergories")
        self.manualBanner.setStyleSheet("font-size: 12pt Arial;  background-color: white; color:black;")

        self.hometitle=QLabel("Household           ")
        self.hometitle.setStyleSheet("color:white;background-color:#412BFF")
        self.hometitle.setFont(QFont("Arial", 20))
        self.homeImg = QLabel()
        homepixmap = QPixmap('icons/home.png')
        self.homeImg.setPixmap(homepixmap)
        self.homeImg.setStyleSheet("background-color:#412BFF")
        self.homeSpending = QLabel(f"{self.homespending} HKD")
        self.homeSpending.setFont(QFont("Arial", 20))
        self.homeSpending.setStyleSheet("background-color:#412BFF; color: white;")

        self.transporttitle=QLabel("Transport                   ")
        self.transporttitle.setStyleSheet("color:white;background-color:#412BFF;qproperty-alignment: AlignLeft")
        self.transporttitle.setFont(QFont("Arial", 20))
        self.busImg = QLabel()
        buspixmap = QPixmap('icons/bus.png')
        self.busImg.setPixmap(buspixmap)
        self.busImg.setStyleSheet("background-color:#412BFF;")
        self.busSpending = QLabel(f"{self.busspending} HKD")
        self.busSpending.setFont(QFont("Arial", 20))
        self.busSpending.setStyleSheet("background-color:#412BFF; color: white;")

        self.clothestitle=QLabel("Clothes                  ")
        self.clothestitle.setStyleSheet("color:white;background-color:#FF0D0D")
        self.clothestitle.setFont(QFont("Arial", 20))
        self.clothesImg = QLabel()
        clothespixmap = QPixmap('icons/clothes.png')
        self.clothesImg.setPixmap(clothespixmap)
        self.clothesImg.setStyleSheet("background-color:#FF0D0D")
        self.clothesSpending = QLabel(f"{self.clothesspending} HKD")
        self.clothesSpending.setFont(QFont("Arial", 20))
        self.clothesSpending.setStyleSheet("background-color:#FF0D0D; color: white;")

        self.eattitle=QLabel("Food                    ")
        self.eattitle.setStyleSheet("color:white;background-color:#FF0D0D")
        self.eattitle.setFont(QFont("Arial", 20))
        self.eatImg = QLabel()
        eatpixmap = QPixmap('icons/eat.png')
        self.eatImg.setPixmap(eatpixmap)
        self.eatImg.setStyleSheet("background-color:#FF0D0D")
        self.eatSpending = QLabel(f"{self.eatspending} HKD")
        self.eatSpending.setFont(QFont("Arial", 20))
        self.eatSpending.setStyleSheet("background-color:#FF0D0D; color: white;")
        
        self.phonetitle=QLabel("Phone                ")
        self.phonetitle.setStyleSheet("color:white;background-color:#412BFF")
        self.phonetitle.setFont(QFont("Arial", 20))
        self.phoneImg = QLabel()
        phonepixmap = QPixmap('icons/phone.png')
        self.phoneImg.setPixmap(phonepixmap)
        self.phoneImg.setStyleSheet("background-color:#412BFF")
        self.phoneSpending = QLabel(f"{self.phonespending} HKD")
        self.phoneSpending.setFont(QFont("Arial", 20))
        self.phoneSpending.setStyleSheet("background-color:#412BFF; color: white;")

        self.credittitle=QLabel("Credit Card                ")
        self.credittitle.setStyleSheet("color:white;background-color:#412BFF")
        self.credittitle.setFont(QFont("Arial", 20))
        self.carImg = QLabel()
        carpixmap = QPixmap('icons/creditcard.png')
        self.carImg.setPixmap(carpixmap)
        self.carImg.setStyleSheet("background-color:#412BFF")
        self.creditSpending = QLabel(f"{self.creditspending} HKD")
        self.creditSpending.setFont(QFont("Arial", 20))
        self.creditSpending.setStyleSheet("background-color:#412BFF; color: white;")

        self.investmenttitle=QLabel("Others                ")
        self.investmenttitle.setStyleSheet("color:white;background-color:#FF0D0D")
        self.investmenttitle.setFont(QFont("Arial", 20))
        self.othersImg = QLabel()
        otherspixmap = QPixmap('icons/box.png')
        self.othersImg.setPixmap(otherspixmap)
        self.othersImg.setStyleSheet("background-color:#FF0D0D")
        self.othersSpending = QLabel(f"{self.others} HKD") 
        self.othersSpending.setFont(QFont("Arial", 20))
        self.othersSpending.setStyleSheet("background-color:#FF0D0D; color: white;")
        #right
        self.addRevenue = QPushButton("     Add Income")
        self.addRevenue.setIcon(QIcon('icons/good.png'))
        self.addRevenue.setStyleSheet(style.addRevenueButton())
        self.addRevenue.clicked.connect(self.funcAddRevenue)

        self.addSpending = QPushButton("    Add Spending")
        self.addSpending.setIcon(QIcon('icons/wrong.png'))
        self.addSpending.setStyleSheet(style.addSpendingButton())
        self.addSpending.clicked.connect(self.funcAddSpending)

        self.Salary = QLabel(f"Income: {round(self.salary, 2)} HKD")
        self.Salary.setContentsMargins(25,25,25,25)
        self.Salary.setStyleSheet("font: 20pt Arial; border: 2px solid green; background-color: white; color:black;")
        self.Spend = QLabel(f"Investment: {round(self.investment, 2)} HKD")
        self.Spend.setContentsMargins(25,25,25,25)
        self.Spend.setStyleSheet("font: 20pt Arial; color: red; border: 2px solid red; background-color: white; color:black;")
        self.Investment = QLabel(f"Investment: {round(self.investment, 2)} HKD")
        self.Investment.setContentsMargins(25,25,25,25)
        self.Investment.setStyleSheet("font: 20pt Arial; border: 2px solid blue; background-color: white; color:black;")
        self.Balance = QLabel(f"Balance: {round(self.salary - self.spend - self.investment, 2)} HKD")
        self.Balance.setContentsMargins(25,25,25,25)
        self.Balance.setStyleSheet("font: 20pt Arial; border: 2px solid green; background-color: white; color:black;")
        self.BalanceButton = QPushButton("  Spending details")
        self.BalanceButton.setIcon(QIcon('icons/detail.png'))
        self.BalanceButton.clicked.connect(self.funcBalanceFigure)
        self.BalanceButton.setStyleSheet(style.GenerateFigureBalanceButton())

        ############################################tab2 widgets
        self.revenueTable = QTableWidget()
        self.revenueTable.setColumnCount(3)
        self.revenueTable.setHorizontalHeaderItem(0, QTableWidgetItem("Date"))
        self.revenueTable.setHorizontalHeaderItem(1, QTableWidgetItem("Income amount"))
        self.revenueTable.setHorizontalHeaderItem(2, QTableWidgetItem("Income name"))
        self.revenueTable.setStyleSheet(style.Tablestyle())
        self.revenueTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.revenueTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.revenueTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)


        ############################################tab3 widgets
        ###table
        self.spendingTable = QTableWidget()
        self.spendingTable.setColumnCount(4)
        self.spendingTable.setHorizontalHeaderItem(0,QTableWidgetItem("Date"))
        self.spendingTable.setHorizontalHeaderItem(1, QTableWidgetItem("Spend amount"))
        self.spendingTable.setHorizontalHeaderItem(2, QTableWidgetItem("Spend name"))
        self.spendingTable.setHorizontalHeaderItem(3, QTableWidgetItem("Spend category"))
        self.spendingTable.setStyleSheet(style.Tablestyle())
        self.spendingTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.spendingTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.spendingTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.spendingTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        ###buttons to look for
        self.searchSpendEntry = QLineEdit()
        self.searchSpendEntry.setPlaceholderText("Look for spend...")
        self.lookforSpendBtn = QPushButton("Search")
        self.lookforSpendBtn.setStyleSheet(style.LookForSpendBtn())
        self.lookforSpendBtn.clicked.connect(self.funcLookforSpend)
        ######################################tab4 widgets
        self.recurringTable = QTableWidget()
        self.recurringTable.setColumnCount(5)
        self.recurringTable.setHorizontalHeaderItem(0,QTableWidgetItem("Name"))
        self.recurringTable.setHorizontalHeaderItem(1,QTableWidgetItem("Category"))
        self.recurringTable.setHorizontalHeaderItem(2,QTableWidgetItem("Frequency"))
        self.recurringTable.setHorizontalHeaderItem(3,QTableWidgetItem("Amount"))
        self.recurringTable.setHorizontalHeaderItem(4,QTableWidgetItem("Start Date"))
        self.recurringTable.setStyleSheet(style.Tablestyle())
        self.recurringTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.recurringTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.recurringTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.recurringTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.recurringTable.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.addRecur=QPushButton("Add recurring")
        self.addRecur.clicked.connect(self.funcAddRecur)
        self.addRecur.setStyleSheet(style.AddRecurBtn())
        self.deleteRecur=QPushButton("Delete recurring")
        self.deleteRecur.clicked.connect(self.funcDeleteRecur)
        self.deleteRecur.setStyleSheet(style.DeleteRecurBtn())
        ###################################tab5
        self.catbanner=QLabel("Select Category:")
        self.catbanner.setStyleSheet("border:0px solid gray;font: 12pt Arial;  background-color: white; color:black;")
        self.categoryList=QComboBox(self)
        self.categoryList.addItems(['ALL','Household','Transport','Phone','Credit Card','Food','Clothes','Others']) 
        self.categoryList.setStyleSheet("border:1px solid gray;font: 10pt Arial;  background-color: white; color:black;")
        self.categoryList.activated[str].connect(self.set_trend_cat)

        self.monthbanner=QLabel("Select Month:")
        self.monthbanner.setStyleSheet("border:0px solid gray;font: 12pt Arial;  background-color: white; color:black;")    
        self.monthselector1=QComboBox()
        self.monthselector1.addItems(['ALL']+self.get_month_list())
        self.monthselector1.setStyleSheet("border:1px solid gray;font: 10pt Arial;  background-color: white; color:black;")
        self.monthselector1.activated[str].connect(self.set_trend_month)
        self.projectIncomeGraph=PlotCanvas(self, width=5, height=4)

        #########################tab6
        self.investmentbanner=QLabel("              Select category of assets:")
        self.investmentbanner.setStyleSheet("border:0px solid gray;font: 15pt Arial;  background-color: white; color:black;")   
        self.invcatselector=QComboBox()
        self.invcatselector.addItems(self.get_cat_list_in())
        self.invcatselector.setStyleSheet("border:1px solid gray;font: 10pt Arial;  background-color: white; color:black;")
        self.invcatselector.activated[str].connect(self.set_inv_cat)
        self.invGraph=PlotCanvas_inv(self,width=5,height=4)
        
    def set_trend_month(self,month):
        self.trend_month=month
        self.displayProjectIncome()
    def set_trend_cat(self,cat):
        self.trend_cat=cat
        self.displayProjectIncome()
    def set_inv_cat(self,cat):
        self.inv_cat=cat
        self.displayInvestment()
        
        

    def layouts(self):
        ############################################tab1
        self.mainLayout = QHBoxLayout()
        self.mainLeftLayout = QFormLayout()
        self.mainRightLayout = QVBoxLayout()

        #thanks group box we can make some stylesheet
        # self.leftLayout00=QHBoxLayout()
        # self.leftGB00=QGroupBox()
        self.leftLayout0=QHBoxLayout()
        self.leftGB0=QGroupBox()
        self.leftLayout1 = QHBoxLayout()
        self.leftGB1 = QGroupBox()
        self.leftGB1.setStyleSheet(style.leftGroup1())
        self.leftLayout2 = QHBoxLayout()
        self.leftGB2 = QGroupBox()
        self.leftGB2.setStyleSheet(style.leftGroup2())
        self.leftLayout3 = QHBoxLayout()
        self.leftGB3 = QGroupBox()
        self.leftGB3.setStyleSheet(style.leftGroup3())
        self.leftLayout4 = QHBoxLayout()
        self.leftGB4 = QGroupBox()
        self.leftGB4.setStyleSheet(style.leftGroup4())
        self.leftLayout5 = QHBoxLayout()
        self.leftGB5 = QGroupBox()
        self.leftGB5.setStyleSheet(style.leftGroup5())
        self.leftLayout6 = QHBoxLayout()
        self.leftGB6 = QGroupBox()
        self.leftGB6.setStyleSheet(style.leftGroup6())
        self.leftLayout7 = QHBoxLayout()
        self.leftGB7 = QGroupBox()
        self.leftGB7.setStyleSheet(style.leftGroup7())
        self.leftLayout00=QHBoxLayout()
        self.leftGB00=QGroupBox()

        #adding widgets to layouts
        self.leftLayout0.addWidget(self.automaticBanner)
        self.leftLayout00.addWidget(self.manualBanner)
        self.leftLayout1.addWidget(self.homeImg)
        self.leftLayout1.addWidget(self.hometitle)
        self.leftLayout1.addWidget(self.homeSpending)   
        self.leftLayout2.addWidget(self.busImg)
        self.leftLayout2.addWidget(self.transporttitle)
        self.leftLayout2.addWidget(self.busSpending) 
        self.leftLayout3.addWidget(self.clothesImg)
        self.leftLayout3.addWidget(self.clothestitle)
        self.leftLayout3.addWidget(self.clothesSpending)
        self.leftLayout4.addWidget(self.eatImg)
        self.leftLayout4.addWidget(self.eattitle)
        self.leftLayout4.addWidget(self.eatSpending)
        self.leftLayout5.addWidget(self.phoneImg)
        self.leftLayout5.addWidget(self.phonetitle)
        self.leftLayout5.addWidget(self.phoneSpending)
        self.leftLayout6.addWidget(self.carImg)
        self.leftLayout6.addWidget(self.credittitle)
        self.leftLayout6.addWidget(self.creditSpending)
        self.leftLayout7.addWidget(self.othersImg)
        self.leftLayout7.addWidget(self.investmenttitle)
        self.leftLayout7.addWidget(self.othersSpending)
        

        self.leftGB0.setLayout(self.leftLayout0)
        self.leftGB00.setLayout(self.leftLayout00)
        self.leftGB1.setLayout(self.leftLayout1)
        self.leftGB2.setLayout(self.leftLayout2)
        self.leftGB3.setLayout(self.leftLayout3)
        self.leftGB4.setLayout(self.leftLayout4)
        self.leftGB5.setLayout(self.leftLayout5)
        self.leftGB6.setLayout(self.leftLayout6)
        self.leftGB7.setLayout(self.leftLayout7)

        
        self.mainLeftLayout.addWidget(self.leftGB0)
        self.mainLeftLayout.addWidget(self.leftGB1)
        self.mainLeftLayout.addWidget(self.leftGB2)
        self.mainLeftLayout.addWidget(self.leftGB5)
        self.mainLeftLayout.addWidget(self.leftGB6)
        self.mainLeftLayout.addWidget(self.leftGB00)
        self.mainLeftLayout.addWidget(self.leftGB4)
        self.mainLeftLayout.addWidget(self.leftGB3)
        self.mainLeftLayout.addWidget(self.leftGB7)
        self.mainLeftLayout.addWidget(self.BalanceButton)

        self.toprightLayout = QVBoxLayout()
        self.toprightLayout.addWidget(self.monthselector)
        self.toprightLayout.addWidget(self.Salary)
        self.toprightLayout.addWidget(self.Spend)
        self.toprightLayout.addWidget(self.Investment)
        self.toprightLayout.addWidget(self.Balance)

        self.bottomrightLayout = QVBoxLayout()
        self.bottomrightLayout.addWidget(self.addRevenue)
        self.bottomrightLayout.addWidget(self.addSpending)
        
   
        self.mainRightLayout.addLayout(self.toprightLayout, 40)
        self.mainRightLayout.addLayout(self.bottomrightLayout, 60)

        self.mainLayout.addLayout(self.mainLeftLayout, 60)
        self.mainLayout.addLayout(self.mainRightLayout, 40)
        self.tab1.setLayout(self.mainLayout)

        ############################################tab2
        self.mainRevenueLayout = QVBoxLayout()
        self.mainRevenueLayout.addWidget(self.revenueTable)
        self.tab2.setLayout(self.mainRevenueLayout)
        ############################################tab3
        self.mainSpendingLayout = QVBoxLayout()
        self.mainSpendingLayout.addWidget(self.spendingTable)
        self.mainSpendingLayout.addWidget(self.searchSpendEntry)
        self.mainSpendingLayout.addWidget(self.lookforSpendBtn)
        self.tab3.setLayout(self.mainSpendingLayout)
        ###################################tab4
        self.mainRecurringLayout = QVBoxLayout()
        self.mainRecurringLayout.addWidget(self.recurringTable)
        self.buttonBox=QHBoxLayout()
        self.buttonBox.addWidget(self.addRecur)
        self.buttonBox.addWidget(self.deleteRecur)
        self.mainRecurringLayout.addLayout(self.buttonBox)
        self.tab4.setLayout(self.mainRecurringLayout)
        ################################tab5
        self.mainProjectLayout=QVBoxLayout()
        self.comboxLayout=QHBoxLayout()
        self.leftcomboboxLayout=QVBoxLayout()
        self.rightcomboboxLayout=QVBoxLayout()
        self.leftcomboboxLayout.addWidget(self.catbanner)
        self.leftcomboboxLayout.addWidget(self.categoryList)
        self.rightcomboboxLayout.addWidget(self.monthbanner)
        self.rightcomboboxLayout.addWidget(self.monthselector1)
        self.comboxLayout.addLayout(self.leftcomboboxLayout)
        self.comboxLayout.addLayout(self.rightcomboboxLayout)
        self.mainProjectLayout.addLayout(self.comboxLayout)
        self.mainProjectLayout.addWidget(self.projectIncomeGraph)
        self.tab5.setLayout(self.mainProjectLayout)
        ###############tab6
        self.mainInvestmentLayout=QVBoxLayout()
        self.invBannerLayout=QHBoxLayout()
        self.invBannerLayout.addWidget(self.investmentbanner)
        self.invBannerLayout.addWidget(self.invcatselector)
        self.mainInvestmentLayout.addLayout(self.invBannerLayout)
        self.mainInvestmentLayout.addWidget(self.invGraph)
        self.tab6.setLayout(self.mainInvestmentLayout)

        ###
        self.tabs.blockSignals(False)   #second thing to refresh window automatically

    def displayRevenues(self):
        self.revenueTable.setFont(QFont("Arial",11))
        for i in reversed(range(self.revenueTable.rowCount())):
            self.revenueTable.removeRow(i)

        query = cur.execute("SELECT date,revenueamount, revenuename FROM revenue")   #displaying only this field
        for row_data in query:
            row_number = self.revenueTable.rowCount()
            self.revenueTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.revenueTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.revenueTable.setEditTriggers(QAbstractItemView.NoEditTriggers)    #cannot change value of elements in table

    def displaySpending(self):
        self.spendingTable.setFont(QFont("Arial",11))
        for i in reversed(range(self.spendingTable.rowCount())):
            self.spendingTable.removeRow(i)

        query = cur.execute("SELECT date,spendingamount, spendingname, spendingcategory FROM spending order by date desc")  #displaying only this field
        for row_data in query:
            row_number = self.spendingTable.rowCount()
            self.spendingTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.spendingTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.spendingTable.setEditTriggers(QAbstractItemView.NoEditTriggers)    #cannot change value of elements in table
    
    def displayRecurring(self):
        self.recurringTable.setFont(QFont("Arial",11))
        for i in reversed(range(self.recurringTable.rowCount())):
            self.recurringTable.removeRow(i)

        query = cur.execute("SELECT name,category, frequency, per,start_date FROM recurring")  #displaying only this field
        for row_data in query:
            row_number = self.recurringTable.rowCount()
            self.recurringTable.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.recurringTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.recurringTable.setEditTriggers(QAbstractItemView.NoEditTriggers)    #cannot change value of elements in table

    def displayProjectIncome(self):
        self.mainProjectLayout.removeWidget(self.projectIncomeGraph)
        self.projectIncomeGraph=PlotCanvas(cat=self.trend_cat,month=self.trend_month)
        self.mainProjectLayout.addWidget(self.projectIncomeGraph)
        # print(1)
    
    def displayInvestment(self):
        self.mainInvestmentLayout.removeWidget(self.invGraph)
        self.invGraph=PlotCanvas_inv(cat=self.inv_cat)
        self.mainInvestmentLayout.addWidget(self.invGraph)
    
    

    def funcBalanceFigure(self):
        if self.spend != 0.0:
            slices = [self.homespending,self.busspending, self.clothesspending ,self.eatspending,self.phonespending ,self.creditspending, self.others]
            parts = ["Household", 'Transport', 'Clothes','Food','Phone','Credit Card','Others']  #cash we have ("revenue" or "cash"), cash we spend, cash we save
            colours = ['#1F8F36','#E30000','#3EE807','#006030','#844200','#484891','#336666']
            plt.rcParams['font.size'] = 12
            plt.rcParams['figure.facecolor'] = 'gray'
            plt.rcParams['text.color'] = 'white'
            plt.rcParams['toolbar'] = 'None'
            plt.pie(slices, labels = parts, startangle = 90, shadow = True, explode = (0.1, 0.1, 0.1,0.1, 0.1, 0.1,0.1), autopct = '%1.1f%%', colors = colours)
            plt.title("Detail Figure for {}".format(self.monthselector.currentText()))
            
            plt.show()
        else:
            QMessageBox.information(self, "Warning!", "To create figure you must have something on account!")


    def funcDeleteDatas(self):
        mbox = QMessageBox.question(self,"Warning","Are you sure to delete data? This option will reset the database.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if mbox == QMessageBox.Yes:
            try:
                query1 = cur.execute("DELETE FROM revenue")
                query2 = cur.execute("DELETE FROM spending")
                query3 = cur.execute("DELETE FROM spendingcategories")
                query4 = cur.execute("DELETE FROM investment")
                query5 = cur.execute("DELETE FROM recurring")
                con.commit()
                QMessageBox.information(self,"Success","Data deleted! You can start with clean slate! I will restart aplication!")
                self.close()
                subprocess.call("python" + " main.py", shell=True)  #restart because after deleting data you cannot see revenues/spends tabels it will crash application
                con.close()
            except:
                QMessageBox.information(self,"Warning","Data have not been deleted!")

    def funcGenerateFigure(self):
        if self.spend > 0:   
            ###option with circle diagram
            #slices = [self.homespending, self.busspending, self.clothesspending, self.eatspending, self.phonespending, self.carspending]
            #parts = ["home", 'public transport', 'clothes', 'eat', 'gadgets', 'car'] 
            #colours = ['#7DFBFF', '#FF0D0D', '#FF00E6', '#3BFF5B', '#412BFF', '#B17DFF']
            #plt.rcParams['font.size'] = 12
            #plt.rcParams['figure.facecolor'] = 'gray'
            #plt.rcParams['text.color'] = 'white'
            #plt.pie(slices, labels = parts, startangle = 90, shadow = True, explode = (0.1, 0.1, 0.1, 0.1, 0.1, 0.1), autopct = '%1.1f%%', colors = colours)
            #plt.title("Categories Figure")
            #plt.show()

            ###option with bar diagram
            parts = {'Home': self.homespending, 'Transport': self.busspending, 'Clothes': self.clothesspending,'Food': self.eatspending, 'Phone': self.phonespending, 'Credit Card': self.creditspending}
            colours = ['#7DFBFF', '#FF0D0D', '#FF00E6', '#3BFF5B', '#412BFF', '#B17DFF']
            courses = list(parts.keys())
            values = list(parts.values())
            plt.rcParams['figure.facecolor'] = 'white'
            plt.bar(courses, values, color=colours, width=0.6)
            plt.title("Spends category") 
            plt.show()
        else:
            QMessageBox.information(self,"Warning","You must spend something to create spending categories figure!")



    def getValues(self):
        allRevenues = cur.execute("SELECT SUM(revenueamount) FROM revenue").fetchall()
        if allRevenues[0][0] != None:
            self.salary = allRevenues[0][0]
        self.Salary.setText(f"Income: {round(self.salary, 2)} HKD")

        allSpending = cur.execute("SELECT SUM(spendingamount) FROM spending").fetchall()
        if allSpending[0][0] != None:
            self.spend = allSpending[0][0]
        self.Spend.setText(f"Spendings: {round(self.spend, 2)} HKD")

        self.Balance.setText(f"Balance: {round(self.salary - self.spend, 2)} HKD")

        allInvestment = cur.execute("select sum(value)from(select value,category,rank()over(partition by category order by date desc)as rk from investment) where rk=1").fetchall()
        if allInvestment[0][0] != None:
            self.investment = allInvestment[0][0]
        self.Investment.setText(f"Investment: {round(self.investment, 2)} HKD")
        

        allHomeSpending = cur.execute("SELECT SUM(spendingamount) FROM spending where spendingcategory='Household'").fetchall()
        if allHomeSpending[0][0] != None:
            self.homespending = allHomeSpending[0][0]
        self.homeSpending.setText(f"{round(self.homespending, 2)} HKD")
        allBusSpending = cur.execute("SELECT SUM(spendingamount) FROM spending where spendingcategory='Transport'").fetchall()
        if allBusSpending[0][0] != None:
            self.busspending = allBusSpending[0][0]
        self.busSpending.setText(f"{round(self.busspending, 2)} HKD")
        allClothesSpending = cur.execute("SELECT SUM(spendingamount) FROM spending where spendingcategory='Clothes'").fetchall()
        if allClothesSpending[0][0] != None:
            self.clothesspending = allClothesSpending[0][0]
        self.clothesSpending.setText(f"{round(self.clothesspending, 2)} HKD")
        allFoodSpending = cur.execute("SELECT SUM(spendingamount) FROM spending where spendingcategory='Food'").fetchall()
        if allFoodSpending[0][0] != None:
            self.eatspending = allFoodSpending[0][0]
        self.eatSpending.setText(f"{round(self.eatspending, 2)} HKD")
        allPhoneSpending = cur.execute("SELECT SUM(spendingamount) FROM spending where spendingcategory='Phone'").fetchall()
        if allPhoneSpending[0][0] != None:
            self.phonespending = allPhoneSpending[0][0]
        self.phoneSpending.setText(f"{round(self.phonespending, 2)} HKD")
        allCreditSpending = cur.execute("SELECT SUM(spendingamount) FROM spending where spendingcategory='Credit Card'").fetchall()
        if allCreditSpending[0][0] != None:
            self.creditspending = allCreditSpending[0][0]
        self.creditSpending.setText(f"{round(self.creditspending, 2)} HKD")
        allEconomy = cur.execute("SELECT SUM(spendingamount) FROM spending where spendingcategory='Others'").fetchall()
        if allEconomy[0][0] != None:
            self.others = allEconomy[0][0]
        self.othersSpending.setText(f"{round(self.others, 2)} HKD")

    def funcLookforSpend(self): #looking spend in table 3
        value = self.searchSpendEntry.text()
        if value == "":
            QMessageBox.information(self,"Warning","Search entry is empty!")
        else:
            self.searchSpendEntry.setText("")
            query = ("SELECT date,spendingamount, spendingname, spendingcategory FROM spending WHERE spendingname LIKE ?")
            results = cur.execute(query, ('%'+value+'%',)).fetchall()

            if results == []:
                QMessageBox.information(self,"Warning","There is not such spend!")
            else:
                for i in reversed(range(self.spendingTable.rowCount())):
                    self.spendingTable.removeRow(i)

                for row_data in results:
                    row_number = self.spendingTable.rowCount()
                    self.spendingTable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.spendingTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def getValues_bymonth(self,month):
        if month=='ALL':
            self.getValues()
        else:
            self.homespending = 0.0
            self.busspending = 0.0
            self.clothesspending = 0.0
            self.eatspending = 0.0
            self.phonespending = 0.0
            self.creditspending = 0.0
            self.others = 0.0
            self.salary = 0.0
            self.investment=0.0
            self.spend = 0.0
            allRevenues = cur.execute("SELECT SUM(revenueamount) FROM revenue where substr(date,0,8) like '{}'".format(month)).fetchall()
            if allRevenues[0][0] != None:
                self.salary = allRevenues[0][0]
            self.Salary.setText(f"Income: {round(self.salary, 2)} HKD")

            allSpending = cur.execute("SELECT SUM(spendingamount) FROM spending where substr(date,0,8) like '{}'".format(month)).fetchall()
            if allSpending[0][0] != None:
                self.spend = allSpending[0][0]
            self.Spend.setText(f"Spendings: {round(self.spend, 2)} HKD")

            self.Balance.setText(f"Balance: {round(self.salary - self.spend, 2)} HKD")

            allHomeSpending = cur.execute("SELECT SUM(spendingamount) FROM spending where spendingcategory='Household' and substr(date,0,8) like '{}'".format(month)).fetchall()
            if allHomeSpending[0][0] != None:
                self.homespending = allHomeSpending[0][0]
            self.homeSpending.setText(f"{round(self.homespending, 2)} HKD")
            allBusSpending = cur.execute("SELECT SUM(spendingamount) FROM spending where spendingcategory='Transport' and substr(date,0,8) like '{}'".format(month)).fetchall()
            if allBusSpending[0][0] != None:
                self.busspending = allBusSpending[0][0]
            self.busSpending.setText(f"{round(self.busspending, 2)} HKD")
            allClothesSpending = cur.execute("SELECT SUM(spendingamount) FROM spending where spendingcategory='Clothes' and substr(date,0,8) like '{}'".format(month)).fetchall()
            if allClothesSpending[0][0] != None:
                self.clothesspending = allClothesSpending[0][0]
            self.clothesSpending.setText(f"{round(self.clothesspending, 2)} HKD")
            allFoodSpending = cur.execute("SELECT SUM(spendingamount) FROM spending where spendingcategory='Food' and substr(date,0,8) like '{}'".format(month)).fetchall()
            if allFoodSpending[0][0] != None:
                self.eatspending = allFoodSpending[0][0]
            self.eatSpending.setText(f"{round(self.eatspending, 2)} HKD")
            allPhoneSpending = cur.execute("SELECT SUM(spendingamount) FROM spending where spendingcategory='Phone' and substr(date,0,8) like '{}'".format(month)).fetchall()
            if allPhoneSpending[0][0] != None:
                self.phonespending = allPhoneSpending[0][0]
            self.phoneSpending.setText(f"{round(self.phonespending, 2)} HKD")
            allCreditSpending = cur.execute("SELECT SUM(spendingamount) FROM spending where spendingcategory='Credit Card' and substr(date,0,8) like '{}'".format(month)).fetchall()
            if allCreditSpending[0][0] != None:
                self.creditspending = allCreditSpending[0][0]
            self.creditSpending.setText(f"{round(self.creditspending, 2)} HKD")
            allEconomy = cur.execute("SELECT SUM(spendingamount) FROM spending where spendingcategory='Others' and substr(date,0,8) like '{}'".format(month)).fetchall()
            if allEconomy[0][0] != None:
                self.others = allEconomy[0][0]
            self.othersSpending.setText(f"{round(self.others, 2)} HKD")

    def month_selected(self,month):
        pass


    def tabChanged(self):   #fourth thing to refresh window automatically
        self.getValues()
        self.displayRevenues()
        self.displaySpending()
        self.displayRecurring()


    def funcAddRevenue(self):
        self.addrevenue = addrevenue.AddRevenue()

    def funcAddSpending(self):
        # if (self.salary > 0.0 and self.salary > self.spend):  #we cant add spending without money
        #     self.addspending = addspending.AddSpending(self.salary, self.spend)
        # else:
        #     QMessageBox.information(self, "Warning!", "You do not have money!")
        self.addspending = addspending.AddSpending(self.salary, self.spend)

    def funcAddRecur(self):
        self.addrecur=addrecur.AddRecur()
    
    def funcDeleteRecur(self):
        self.deleterecur=deleterecur.DeleteRecur()

def main():
    app = QApplication(sys.argv)
    window = Window()
    app.exec_()

if __name__ == '__main__':
    main()