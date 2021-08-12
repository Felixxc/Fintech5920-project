from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sqlite3, style
import datetime
today=datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d')

con = sqlite3.connect("money.db")
cur = con.cursor()

class AddSpending(QWidget):
    def __init__(self, salary, spend):
        super().__init__()
        self.salary = salary
        self.spend = spend
        self.setGeometry(350,200,350,550)
        self.setFont(QFont("Times", 13))
        self.setStyleSheet("background-color:black; color:white;") 
        self.setWindowTitle('Add Spending')
        self.setWindowIcon(QIcon('icons/coin.png'))
        self.setFixedSize(self.size())
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):

        self.addSpendingTitle = QLabel("ADD SPENDING")
        self.addSpendingTitle.setFont(QFont("Times", 18))
        self.addSpendingTitle.setAlignment(Qt.AlignCenter)

        self.addSpendingImg = QLabel()
        currencypixmap = QPixmap('icons/buy.png')
        self.addSpendingImg.setPixmap(currencypixmap)
        self.addSpendingImg.setAlignment(Qt.AlignCenter)
        self.addSpendingImg.setContentsMargins(0,50,0,0) #(left, top, right, bottom)

        self.amountEntry = QLineEdit()
        self.amountEntry.setPlaceholderText("Amount")
        self.amountEntry.setContentsMargins(20,0,20,0)
        self.amountEntry.setStyleSheet("color:white; font-size:15pt;")
        self.activityEntry = QLineEdit()
        self.activityEntry.setPlaceholderText("Marker")
        self.activityEntry.setContentsMargins(20,0,20,20)
        self.activityEntry.setStyleSheet("color:white; font-size:15pt;")

        self.submitBtn = QPushButton("Submit")
        self.submitBtn.setStyleSheet(style.addSpendingSubmitBtn())
        self.submitBtn.clicked.connect(self.addSpending)

        self.chooseCategoryLabel = QLabel("CHOOSE CATEGORY")
        self.chooseCategoryLabel.setAlignment(Qt.AlignCenter)
        self.chooseCategory = QComboBox()
        self.chooseCategory.addItems(["Household", "Transport", "Phone", "Food", "Clothes", "Credit Card", "Others"])

    def layouts(self):
        self.addSpendingMainLayout = QVBoxLayout()
        self.addSpendingForm = QVBoxLayout()

        self.addSpendingMainLayout.addWidget(self.addSpendingTitle)
        self.addSpendingMainLayout.addWidget(self.addSpendingImg)
        self.addSpendingMainLayout.addStretch()

        self.addSpendingForm.addWidget(self.amountEntry)
        self.addSpendingForm.addWidget(self.activityEntry)
        self.addSpendingForm.addWidget(self.chooseCategoryLabel)
        self.addSpendingForm.addWidget(self.chooseCategory)
        self.addSpendingMainLayout.addLayout(self.addSpendingForm)
        self.addSpendingForm.setAlignment(Qt.AlignCenter)

        self.addSpendingMainLayout.addWidget(self.submitBtn)

        self.setLayout(self.addSpendingMainLayout)

    def addSpending(self):
        amount = self.amountEntry.text()
        name = self.activityEntry.text()
        category = self.chooseCategory.currentText()

        # if float(amount) <= (self.salary - self.spend):
        self.homespending = 0.0
        self.busspending = 0.0
        self.clothesspending = 0.0
        self.eatspending = 0.0
        self.phonespending = 0.0
        self.creditspending = 0.0
        self.othersspending = 0.0
        if category == "Household":
            self.homespending += float(amount)
        elif category == "Transport":
            self.busspending += float(amount)
        elif category == "Clothes":
            self.clothesspending += float(amount)
        elif category == "Food":
            self.eatspending += float(amount)
        elif category == "Phone":
            self.phonespending += float(amount)
        elif category == "Credit Card":
            self.creditspending += float(amount)
        elif category == "Others":
            self.othersspending += float(amount)

        if (name and amount != ""):
            try:
                query1 = "INSERT INTO 'spending' (spendingamount, spendingname, spendingcategory,date) VALUES(?,?,?,?)"
                cur.execute(query1, (amount, name, category,today))
                con.commit()

                query2 = "INSERT INTO 'spendingcategories' (homespending, busspending, clothesspending, eatspending, phonespending, creditspending, othersspending) VALUES(?,?,?,?,?,?,?)"
                cur.execute(query2, (self.homespending, self.busspending, self.clothesspending, self.eatspending, self.phonespending, self.creditspending, self.othersspending ))
                con.commit()
                QMessageBox.information(self,"Warning","Spend has been added to data base!")
                self.close()
            except:
                QMessageBox.information(self,"Warning","Spend has not been added to data base!")

        else:
            QMessageBox.information(self,"Warning","Fields cannot be empty!")
        # else:
        #     QMessageBox.information(self,"Warning","You do not have as much money!")