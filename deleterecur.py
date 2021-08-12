from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import style, sqlite3
import datetime
today=datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d')

con = sqlite3.connect("money.db")
cur = con.cursor()

class DeleteRecur(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(400,300,400,600)
        self.setFont(QFont("Times", 13))
        self.setStyleSheet("background-color:black; color:white;") 
        self.setWindowTitle('Delete Recur')
        self.setWindowIcon(QIcon('icons/coin.png'))
        self.setFixedSize(self.size())  #block extending of window
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):

        self.addRevenueTitle = QLabel("DELETE RECUR")
        self.addRevenueTitle.setFont(QFont("Times", 18))
        self.addRevenueTitle.setAlignment(Qt.AlignCenter)

        self.addRevenueImg = QLabel()
        currencypixmap = QPixmap('icons/deleterecur.png')
        self.addRevenueImg.setPixmap(currencypixmap)
        self.addRevenueImg.setAlignment(Qt.AlignCenter)
        self.addRevenueImg.setContentsMargins(0,50,0,0) 

        self.activityEntry = QLineEdit()
        self.activityEntry.setPlaceholderText("Name")
        self.activityEntry.setContentsMargins(20,0,20,20)

        self.submitBtn = QPushButton("Delete")
        self.submitBtn.setStyleSheet(style.addRevenueSubmitBtn())
        self.submitBtn.clicked.connect(self.deleteRevenue)

    def layouts(self):
        self.addRevenueMainLayout = QVBoxLayout()
        self.addRevenueMainLayout.addWidget(self.addRevenueTitle)
        self.addRevenueMainLayout.addWidget(self.addRevenueImg)
        self.addRevenueMainLayout.addStretch()
        self.addRevenueMainLayout.addWidget(self.activityEntry)
        self.addRevenueMainLayout.addWidget(self.submitBtn)

        self.setLayout(self.addRevenueMainLayout)

    def deleteRevenue(self):
        name = self.activityEntry.text()
        if (name!= ""):
            try:
                query = "Delete from recurring where name='{}'".format(name)
                cur.execute(query)
                con.commit()
                QMessageBox.information(self,"Success","Recurring deleted from data base!")
                self.close()
            except:
                QMessageBox.information(self,"Warning","Recurring has not been deleted from data base!")

        else:
            QMessageBox.information(self,"Warning","Fields cannot be empty!")