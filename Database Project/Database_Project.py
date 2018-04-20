import sys
import PyQt5
from PyQt5.QtWidgets import (QApplication, qApp, QAction, QDesktopWidget, QToolTip, 
							 QPushButton, QMessageBox, QMainWindow, QMenu, QTextEdit,
							 QHBoxLayout, QVBoxLayout, QLineEdit, QTableWidget, 
							 QTableWidgetItem, QLabel)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtSql import *


class SQL(QMainWindow):

	def __init__(self):
		super().__init__()
		self.left = 100
		self.top = 100
		self.width = 800
		self.height = 400
		self.initUI()
		
	def initUI(self):
#Set window size and position
		self.setGeometry(self.left, self.top, self.width, self.height)
#Create the connect to database button
		self.dbLabel = QLabel(self)
		self.dbLabel.setText('Not Connected')
		self.dbLabel.move(205, 15)		
		self.button = QPushButton('Connect to Database', self)
		self.button.resize(180, 20)
		self.button.move(20, 20)
		self.button.clicked.connect(self.on_click)
#Create the textbox for searches
		self.textbox = QTextEdit(self)
		self.textbox.move(20, 45)
		self.textbox.resize(280, 180)
#Employee ID Box
		self.idLabel = QLabel(self)
		self.idLabel.setText('ID')
		self.idLabel.move(355, 20)
		self.idBox = QLineEdit(self)
		self.idBox.move(355, 45)
		self.idBox.resize(40, 20)
		self.idBox.setReadOnly(True)
#Create the box for returned results and the label that goes above them
		self.firstNameLable = QLabel(self)
		self.firstNameLable.setText('First Name')
		self.firstNameLable.move(400, 20)
		self.firstNameBox = QLineEdit(self)
		self.firstNameBox.move(400, 45)
		self.firstNameBox.resize(80, 20)
#Create the box for Last Name results
		self.lastNameLable = QLabel(self)
		self.lastNameLable.setText('Last Name')
		self.lastNameLable.move(485, 20)
		self.lastNameBox = QLineEdit(self)
		self.lastNameBox.move(485, 45)
		self.lastNameBox.resize(80, 20)
#Create the box for returned results and the label that goes above them
		self.paylabel = QLabel(self)
		self.paylabel.setText('Date of Birth')
		self.paylabel.move(575, 20)
		self.paybox = QLineEdit(self)
		self.paybox.move(575, 45)
		self.paybox.resize(80, 20)
#Create the run Query button 
		self.queryButton = QPushButton('Run Query', self)
		self.queryButton.resize(180, 20)
		self.queryButton.move(20, 240)
		self.queryButton.clicked.connect(self.query_click)		
#Create the update button
		self.queryButton = QPushButton('Update', self)
		self.queryButton.resize(90, 20)
		self.queryButton.move(550, 80)
		self.queryButton.clicked.connect(self.update_click)
#Exit from the menu
		exitAct = QAction(QIcon('Exit.png'), '&Exit', self)
		exitAct.setShortcut('Crtl+Q')
		exitAct.setStatusTip('Exit Application')
		exitAct.triggered.connect(qApp.quit)
		
		self.statusBar()
#Adds the menu at the top of the window and a file option that currently does nothing
		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(exitAct)

		
		self.setWindowTitle('SQL App')
		self.setWindowIcon(QIcon('web.png'))
		self.show()
#Connects to the database with the credentials below when the button is clicked
	@pyqtSlot()
	def on_click(self):
		db = QSqlDatabase.addDatabase('QODBC')
		db.setDatabaseName('DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s;'
                        % ('98.103.60.67,49172',
                           'DamajjAuto',
                           'damajjauto',
                           '12345'))
		ok = db.open()
		print(ok)
		if(ok == False):
			error = db.lastError()
			print(error)
		else:
			self.dbLabel.setText('Connected')
#Runs a query searching for a row that matches the first or last name, currently not sure how it would handle multiple rows returning		
	def query_click(self):
		query = QSqlQuery()
		query.exec('SELECT first_name, last_name, bday, employee_num FROM employee WHERE first_name = \'{0}\' or last_name = \'{0}\' '.format(self.textbox.toPlainText()))
		while (query.next()):
			firstName = query.value(0)
			lastName = query.value(1)
			pay = query.value(2)
			id = query.value(3)
			self.firstNameBox.clear()
			self.lastNameBox.clear()
			self.paybox.clear()
			self.idBox.clear()
			self.firstNameBox.insert(firstName)
			self.lastNameBox.insert(lastName)
			self.paybox.insert(str(pay))
			self.idBox.insert(str(id))

	def update_click(self):
		query = QSqlQuery()
		error = QSqlError()
		query.exec('UPDATE employee' 
			 ' SET first_name = \'{0}\', last_Name = \'{1}\', bday = {2} '
			'WHERE employee_num = {3}'.format(self.firstNameBox.text(), self.lastNameBox.text(), int(self.paybox.text()), int(self.idBox.text())))
		

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = SQL()
	
	sys.exit(app.exec_())  