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

		db = QSqlDatabase

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
		self.textbox.resize(280, 25)
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
		self.dobLabel = QLabel(self)
		self.dobLabel.setText('Date of Birth')
		self.dobLabel.move(575, 20)
		self.dobbox = QLineEdit(self)
		self.dobbox.move(575, 45)
		self.dobbox.resize(80, 20)
#Create the box for returned results and the label that goes above them
		self.genderlabel = QLabel(self)
		self.genderlabel.setText('Gender')
		self.genderlabel.move(665, 20)
		self.genderbox = QLineEdit(self)
		self.genderbox.move(665, 45)
		self.genderbox.resize(20, 20)
#Create the box for returned results and the label that goes above them
		self.doslable = QLabel(self)
		self.doslable.setText('Start Date')
		self.doslable.move(355, 75)
		self.dosbox = QLineEdit(self)
		self.dosbox.move(355, 100)
		self.dosbox.resize(80, 20)
#Create the box for returned results and the label that goes above them
		self.deptlabel = QLabel(self)
		self.deptlabel.setText('Department')
		self.deptlabel.move(440, 75)
		self.deptbox = QLineEdit(self)
		self.deptbox.move(440, 100)
		self.deptbox.resize(125, 20)
		self.deptbox.setMaxLength(25) 
#Create the run Query button 
		self.queryButton = QPushButton('Run Query', self)
		self.queryButton.resize(180, 20)
		self.queryButton.move(20, 80)
		self.queryButton.clicked.connect(self.query_click)
#Create the update button
		self.queryButton = QPushButton('Update', self)
		self.queryButton.resize(90, 20)
		self.queryButton.move(355, 140)
		self.queryButton.clicked.connect(self.update_click)

		self.updatelabel = QLabel(self)
		self.updatelabel.setText('')
		self.updatelabel.move(355, 160)

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

	def closeEvent(self, event):
		self.db.close()

#Connects to the database with the credentials below when the button is clicked
	@pyqtSlot()
	def on_click(self):
		self.db = QSqlDatabase.addDatabase('QODBC')
		self.db.setDatabaseName('DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s;'
                        % ('98.103.60.67,49172',
                           'DamajjAuto',
                           'damajjauto',
                           '12345'))
		ok = self.db.open()
		print(ok)
		if(ok == False):
			error = self.db.lastError()
			print(error)
		else:
			self.dbLabel.setText('Connected')
#Runs a query searching for a row that matches the first or last name, currently not sure how it would handle multiple rows returning		
	def query_click(self):
		query = QSqlQuery()
		query.exec('SELECT first_name, last_name, bday, employee_num, gender, date_started, department.dept_name FROM employee LEFT JOIN department ON employee.dept_num = department.dept_num WHERE first_name = \'{0}\' or last_name = \'{0}\' or employee_num = \'{1}\' '.format(self.textbox.toPlainText(), int(self.textbox.toPlainText())))
		while (query.next()):
			firstName = query.value(0)
			lastName = query.value(1)
			dateOfBirth = query.value(2)
			id = query.value(3)
			gender = query.value(4)
			startDate = query.value(5)
			department = query.value(6)
			self.firstNameBox.clear()
			self.lastNameBox.clear()
			self.dobbox.clear()
			self.idBox.clear()
			self.genderbox.clear()
			self.dosbox.clear()
			self.deptbox.clear()
			self.firstNameBox.insert(firstName)
			self.lastNameBox.insert(lastName)
			self.dobbox.insert(str(dateOfBirth))
			self.idBox.insert(str(id))
			self.genderbox.insert(str(gender))
			self.dosbox.insert(str(startDate))
			self.deptbox.insert(str(department))

	def update_click(self):
		query = QSqlQuery()
		ok = query.exec('UPDATE e ' 
			'SET first_name = \'{0}\', last_name = \'{1}\', bday = \'{2}\', employee_num = \'{3}\', gender = \'{4}\', date_started = \'{5}\' , dept_num = (SELECT dept_num FROM department WHERE dept_name = \'{6}\') '
			'from employee e '
			'WHERE employee_num = {3}'.format(self.firstNameBox.text(), self.lastNameBox.text(), self.dobbox.text(), int(self.idBox.text()), self.genderbox.text(), self.dosbox.text(), self.deptbox.text()))
		
		if (ok == False):
			self.updatelabel.setText('Update Failed')
			print(query.lastError().number())
			print(query.lastError().databaseText())
		else:
			self.updatelabel.setText('Update Successful')

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = SQL()
	
	sys.exit(app.exec_())  
