from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import style, sqlite3
import datetime
today=datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d')

con = sqlite3.connect("money.db")
cur = con.cursor()

class AddRecur(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(400,300,400,600)
        self.setFont(QFont("Times", 13))
        self.setStyleSheet("background-color:black; color:white;") 
        self.setWindowTitle('Add Recur')
        self.setWindowIcon(QIcon('icons/coin.png'))
        self.setFixedSize(self.size())  #block extending of window
        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):

        self.addRevenueTitle = QLabel("ADD RECUR")
        self.addRevenueTitle.setFont(QFont("Times", 18))
        self.addRevenueTitle.setAlignment(Qt.AlignCenter)

        self.addRevenueImg = QLabel()
        currencypixmap = QPixmap('icons/addrecur.png')
        self.addRevenueImg.setPixmap(currencypixmap)
        self.addRevenueImg.setAlignment(Qt.AlignCenter)
        self.addRevenueImg.setContentsMargins(0,50,0,0) 

        self.amountEntry = QLineEdit()
        self.amountEntry.setPlaceholderText("Amount")
        self.amountEntry.setContentsMargins(20,0,20,0)
        self.activityEntry = QLineEdit()
        self.activityEntry.setPlaceholderText("Name")
        self.activityEntry.setContentsMargins(20,0,20,20)
        self.frequencyEntry = QLineEdit()
        self.frequencyEntry.setPlaceholderText("Frequency(measured by days)")
        self.frequencyEntry.setContentsMargins(20,0,20,20)
        self.dateEntry = QLineEdit()
        self.dateEntry.setPlaceholderText("Start date")
        self.dateEntry.setContentsMargins(20,0,20,20)


        self.chooseCategoryLabel = QLabel("CHOOSE CATEGORY")
        self.chooseCategoryLabel.setAlignment(Qt.AlignCenter)
        self.chooseCategory = QComboBox()
        self.chooseCategory.addItems(["Household", "Transport", "Phone", "Food", "Clothes", "Credit Card", "Others"])

        self.submitBtn = QPushButton("Submit")
        self.submitBtn.setStyleSheet(style.addRevenueSubmitBtn())
        self.submitBtn.clicked.connect(self.addRevenue)

    def layouts(self):
        self.addRevenueMainLayout = QVBoxLayout()
        self.addRevenueMainLayout.addWidget(self.addRevenueTitle)
        self.addRevenueMainLayout.addWidget(self.addRevenueImg)
        self.addRevenueMainLayout.addStretch()
        self.addRevenueMainLayout.addWidget(self.activityEntry)
        self.addRevenueMainLayout.addWidget(self.amountEntry)
        self.addRevenueMainLayout.addWidget(self.frequencyEntry)
        self.addRevenueMainLayout.addWidget(self.dateEntry)
        self.addRevenueMainLayout.addWidget(self.chooseCategoryLabel)
        self.addRevenueMainLayout.addWidget(self.chooseCategory)
        self.addRevenueMainLayout.addWidget(self.submitBtn)

        self.setLayout(self.addRevenueMainLayout)

    def addRevenue(self):
        amount = self.amountEntry.text()
        name = self.activityEntry.text()
        frequency=self.frequencyEntry.text()
        start_date=self.dateEntry.text()
        category = self.chooseCategory.currentText()
        if (name and amount and frequency and start_date and category != ""):
            try:
                query = "INSERT INTO recurring (id,name,category,frequency,per,start_date) VALUES(NULL,?,?,?,?,?)"
                cur.execute(query, (name, category,frequency,amount,start_date))
                con.commit()
                QMessageBox.information(self,"Success","Recurring added to data base!")
                self.close()
            except Exception as e:
                QMessageBox.information(self,"Warning","Recurring has not been added to data base!")

        else:
            QMessageBox.information(self,"Warning","Fields cannot be empty!")