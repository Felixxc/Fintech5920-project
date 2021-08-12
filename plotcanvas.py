import sys
import sqlite3
from datetime import datetime
con = sqlite3.connect("money.db")
cur = con.cursor()
 
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon
 
 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random
class PlotCanvas(FigureCanvas):
 
    def __init__(self,parent=None, width=5, height=4, dpi=100,cat='ALL',month='ALL'):
        self.cat=cat
        if month=='ALL' and cat=='ALL':
            query = cur.execute("select date,sum(spendingamount) from spending  group by date order by date")
        elif month=='ALL' and cat!='ALL':
            query = cur.execute("select date,sum(spendingamount) from spending where spendingcategory='{}'  group by date order by date".format(cat))
        elif month!='ALL' and cat=='ALL':
            query = cur.execute("select date,sum(spendingamount) from spending where substr(date,0,8) like '{}' group by date order by date".format(month))
        else:
            query = cur.execute("select date,sum(spendingamount) from spending where spendingcategory='{}' and substr(date,0,8) like '{}' group by date order by date".format(cat,month))
        self.date=[]
        self.spending=[]
        for row_data in query:
            self.date.append(row_data[0])
            self.spending.append(row_data[1])
        self.date=[datetime.strptime(x,"%Y-%m-%d").date() for x in self.date]
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
 
        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()
        
 
    def plot(self):
        # data = [random.random() for i in range(25)]
        ax = self.figure.add_subplot(111)
        ax.plot(self.date,self.spending, 'bo-')
        ax.set_title('Expense Trends of {}'.format(self.cat))
        self.draw()