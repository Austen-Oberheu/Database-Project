import sys
import re
import PyQt5
from PyQt5.QtWidgets import (QApplication, qApp, QAction, QDesktopWidget, QToolTip, 
							 QPushButton, QMessageBox, QMainWindow, QMenu, QTextEdit,
							 QHBoxLayout, QVBoxLayout, QLineEdit, QTableWidget, 
							 QTableWidgetItem, QLabel, QWidget, QComboBox, QDateEdit,
							 QCheckBox)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot, QDate, QTimer
from PyQt5.QtSql import *

	
def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		pass
	try:
		import unicodedata
		unicodedata.numeric(s)
		return True
	except (TypeError, ValueError):
		pass

	return False

class SalaryWindow(QWidget):
    
	def __init__(self, employeeNum):
		super().__init__()
		self.initUI()
		self.initInfo(employeeNum)
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.updatePay)
		self.timer.start(1000)


	def initInfo(self, employeeNum):
		query = QSqlQuery()
		ok = query.exec('SELECT employee_num, first_name, last_name, s.dept_name, e.position, pay_rate, hours, payment '
						'FROM employee e '
						'LEFT JOIN '
						'salary as s on e.employee_num = s.emp_num '
						'WHERE e.employee_num = {0}'.format(int(employeeNum)))
		if (ok == False):
			print(query.lastQuery())
			print(query.lastError().number())
			print(query.lastError().databaseText())
		else:
			print('Successful')
	
		while (query.next()):
			firstName = query.value(1)
			lastName = query.value(2)
			deptNum = query.value(3)
			salary = str(query.value(4))
			payRate = query.value(5)
			hours = query.value(6)
			payment = query.value(7)
			

		self.firstNameBox.insert(firstName)
		self.lastNameBox.insert(lastName)
		self.idBox.insert(employeeNum)
		self.deptbox.insert(str(deptNum))

		self.payRatBox.insert(str(payRate))

		isSalary = None
		if (re.search('Manager', salary)):
				isSalary = True
		else:
				isSalary = False

		print(isSalary)

		self.salaryCheckBox.setChecked(isSalary)
		self.hoursBox.insert(str(hours))

		if (isSalary):
			self.paymentBox.insert(str((payRate / 12) / 2))
		else:
			self.paymentBox.insert(str(hours * payRate))

	def initUI(self):
		self.setGeometry(300, 300, 600, 300)
		self.setWindowTitle('Employee Pay')

		self.deptlabel = QLabel(self)
		self.deptlabel.setText('Department')
		self.deptlabel.move(25, 20)
		self.deptbox = QLineEdit(self)
		self.deptbox.move(25, 45)
		self.deptbox.resize(125, 20)
		self.deptbox.setMaxLength(25) 
		self.deptbox.setReadOnly(True)

		self.idLabel = QLabel(self)
		self.idLabel.setText('ID')
		self.idLabel.move(165, 20)
		self.idBox = QLineEdit(self)
		self.idBox.move(165, 45)
		self.idBox.resize(40, 20)
		self.idBox.setReadOnly(True)

		self.firstNameLable = QLabel(self)
		self.firstNameLable.setText('First Name')
		self.firstNameLable.move(215, 20)
		self.firstNameBox = QLineEdit(self)
		self.firstNameBox.move(215, 45)
		self.firstNameBox.resize(80, 20)
		self.firstNameBox.setReadOnly(True)
		#Create the box for Last Name results
		self.lastNameLable = QLabel(self)
		self.lastNameLable.setText('Last Name')
		self.lastNameLable.move(315, 20)
		self.lastNameBox = QLineEdit(self)
		self.lastNameBox.move(315, 45)
		self.lastNameBox.resize(80, 20)
		self.lastNameBox.setReadOnly(True)
		
		self.payRateLabel = QLabel(self)
		self.payRateLabel.setText('Pay Rate')
		self.payRateLabel.move(25, 75)
		self.payRatBox = QLineEdit(self)
		self.payRatBox.move(25, 95)
		self.payRatBox.resize(80, 20)

		self.salaryLabel = QLabel(self)
		self.salaryLabel.setText('Salary')
		self.salaryLabel.move(125, 75)
		self.salaryCheckBox = QCheckBox(self)
		self.salaryCheckBox.move(125, 95)

		self.hoursLabel = QLabel(self)
		self.hoursLabel.setText('Hours')
		self.hoursLabel.move(165, 75)
		self.hoursBox = QLineEdit(self)
		self.hoursBox.move(165, 95)
		self.hoursBox.resize(80, 20)

		self.paymentLabel = QLabel(self)
		self.paymentLabel.setText('Payment')
		self.paymentLabel.move(265, 75)
		self.paymentBox = QLineEdit(self)
		self.paymentBox.move(265, 95)
		self.paymentBox.resize(80, 20)

		self.dbLabel = QLabel(self)
		self.dbLabel.setText('						')
		self.dbLabel.move(165, 155)		
		self.button = QPushButton('Save Changes', self)
		self.button.resize(120, 20)
		self.button.move(25, 150)
		self.button.clicked.connect(self.save_click)
		#Create the box for returned results and the label that goes above them
		
		#self.deptbox = QLineEdit(self)
		#self.deptbox.move(125, 100)
		#self.deptbox.resize(125, 20)
		#self.deptbox.setMaxLength(25)
		
		self.show()

	@pyqtSlot()

	
	def save_click(self):
		query = QSqlQuery()
		ok = query.exec('UPDATE s '
						'SET pay_rate = {0}0, hours = {1}0, payment = {2}0 '
						'FROM salary s '
						'WHERE emp_num = {3}'
						.format(round(float(self.payRatBox.text()), 2), round(float(self.hoursBox.text()), 2), round(float(self.paymentBox.text()), 2), int(self.idBox.text())))
		
		if (ok == False):
			self.dbLabel.setText('Employee Pay Save Failed')
			print(query.lastQuery())
			print(query.lastError().number())
			print(query.lastError().databaseText())
		else:
			self.dbLabel.setText('Employee Pay Saved')
			
	def updatePay(self):
		hours = float(self.hoursBox.text())
		payRate = float(self.payRatBox.text())
		self.paymentBox.clear()
		if (self.salaryCheckBox.isChecked()):
			self.paymentBox.insert(str(round(((payRate / 12) / 2), 2)))
		else:
			self.paymentBox.insert(str(hours * payRate))

class AddEmployeeWindow(QWidget):
    
	def __init__(self):
		super().__init__()

		self.initUI()


	def initUI(self):
		self.setGeometry(300, 300, 600, 300)
		self.setWindowTitle('Add Employee')

		self.deptlabel = QLabel(self)
		self.deptlabel.setText('Department')
		self.deptlabel.move(25, 20)
		
		self.deptbox = QComboBox(self)
		self.deptbox.move(25, 45)
		self.deptbox.resize(125, 20)
		self.deptbox.addItem('Production', 3)
		self.deptbox.addItem('Sales', 4)
		self.deptbox.addItem('Human Resources', 5)
		self.deptbox.addItem('Warehouse', 6)
		self.deptbox.addItem('IT', 7)
		self.deptbox.activated.connect(self.sliderEvent)

		self.idLabel = QLabel(self)
		self.idLabel.setText('ID')
		self.idLabel.move(165, 20)
		self.idBox = QLineEdit(self)
		self.idBox.move(165, 45)
		self.idBox.resize(40, 20)
		self.idBox.setReadOnly(True)

		self.firstNameLable = QLabel(self)
		self.firstNameLable.setText('First Name')
		self.firstNameLable.move(215, 20)
		self.firstNameBox = QLineEdit(self)
		self.firstNameBox.move(215, 45)
		self.firstNameBox.resize(80, 20)
		#Create the box for Last Name results
		self.lastNameLable = QLabel(self)
		self.lastNameLable.setText('Last Name')
		self.lastNameLable.move(315, 20)
		self.lastNameBox = QLineEdit(self)
		self.lastNameBox.move(315, 45)
		self.lastNameBox.resize(80, 20)
		#Create the box for returned results and the label that goes above them
		self.dobLabel = QLabel(self)
		self.dobLabel.setText('Date of Birth')
		self.dobLabel.move(415, 20)
		self.dobbox = QDateEdit(QDate.currentDate(), self)
		self.dobbox.move(415, 45)
		self.dobbox.resize(80, 20)
		#Create the box for returned results and the label that goes above them
		self.genderlabel = QLabel(self)
		self.genderlabel.setText('Gender')
		self.genderlabel.move(515, 20)
		self.genderbox = QLineEdit(self)
		self.genderbox.move(515, 45)
		self.genderbox.resize(20, 20)
		#Create the box for returned results and the label that goes above them
		self.doslable = QLabel(self)
		self.doslable.setText('Start Date')
		self.doslable.move(25, 75)
		self.dosbox = QDateEdit(QDate.currentDate(), self)
		self.dosbox.move(25, 100)

		self.dbLabel = QLabel(self)
		self.dbLabel.setText('						')
		self.dbLabel.move(165, 155)		
		self.button = QPushButton('Create Employee', self)
		self.button.resize(120, 20)
		self.button.move(25, 150)
		self.button.clicked.connect(self.create_click)
		#Create the box for returned results and the label that goes above them
		
		#self.deptbox = QLineEdit(self)
		#self.deptbox.move(125, 100)
		#self.deptbox.resize(125, 20)
		#self.deptbox.setMaxLength(25)

		
		self.show()

	@pyqtSlot()

	def sliderEvent(self):
		query = QSqlQuery()
		ok = query.exec('SELECT employee_num FROM employee LEFT JOIN department ON employee.dept_num = department.dept_num WHERE dept_name = \'{0}\' '.format(str(self.deptbox.currentText())))
		
		while (query.next()):
			id = query.value(0)
		self.idBox.clear()
		self.idBox.insert(str(int(id)+1))

		if (ok == False):
			print(query.lastError().number())
			print(query.lastError().databaseText())
	
	def create_click(self):
		query = QSqlQuery()
		ok = query.exec('INSERT INTO employee ' 
			'VALUES ({0}, \'{1}\', \'{2}\', \'{3}\', \'{4}\', \'{5}\', {6}, \'{7}\')'
			.format(int(self.idBox.text()), str(self.dobbox.date().toString("yyyy-MM-dd")), self.firstNameBox.text(), self.lastNameBox.text(), self.genderbox.text(), str(self.dosbox.date().toString("yyyy-MM-dd")), self.deptbox.currentData(), 'Employee'))
		
		if (ok == False):
			self.dbLabel.setText('Create Employee Failed')
			print(query.lastQuery())
			print(query.lastError().number())
			print(query.lastError().databaseText())
		else:
			self.dbLabel.setText('Create Employee Successful')
			

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
		self.textbox = QLineEdit(self)
		self.textbox.move(20, 45)
		self.textbox.resize(280, 20)
		self.textbox.setPlaceholderText('Enter First Name, Last Name, or ID Number')
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

		self.queryButton = QPushButton('Delete', self)
		self.queryButton.resize(90, 20)
		self.queryButton.move(455, 140)
		self.queryButton.clicked.connect(self.deleteEvent)

		self.addButton = QPushButton('Add', self)
		self.addButton.resize(90, 20)
		self.addButton.move(655, 140)
		self.addButton.clicked.connect(self.addEvent)

		self.addButton = QPushButton('Pay', self)
		self.addButton.resize(90, 20)
		self.addButton.move(555, 140)
		self.addButton.clicked.connect(self.payEvent)

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
		if(self.dbLabel.close() is None):
			self.db.close()


#Connects to the database with the credentials below when the button is clicked
	@pyqtSlot()

	def deleteEvent(self):
		if(self.idBox.text() == ''):
			return
		choice = QMessageBox.question(self, 'Extract!',
                                            "Delete the Entry?",
                                            QMessageBox.Yes | QMessageBox.No)
		if (choice == QMessageBox.Yes):
			query = QSqlQuery()
			ok = query.exec('DELETE FROM employee WHERE employee_num = {0}'.format(int(self.idBox.text())))
			if (ok):
				self.firstNameBox.clear()
				self.lastNameBox.clear()
				self.dobbox.clear()
				self.idBox.clear()
				self.genderbox.clear()
				self.dosbox.clear()
				self.deptbox.clear()
				self.updatelabel.setText('Query Successful')
			else:
				self.updatelabel.setText('Query Failed')
				print(query.lastError().number())
				print(query.lastError().databaseText())

	def addEvent(self):
		self.window = AddEmployeeWindow()

	def payEvent(self):
		if(self.idBox.text() == ''):
			return
		employeeNum = self.idBox.text()
		self.window = SalaryWindow(employeeNum)

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
		queryInput = self.textbox.text()
		if(is_number(queryInput) == True):
			ok = query.exec('SELECT first_name, last_name, bday, employee_num, gender, date_started, department.dept_name FROM employee LEFT JOIN department ON employee.dept_num = department.dept_num WHERE employee_num = \'{0}\' '.format(queryInput))
		else:
			ok = query.exec('SELECT first_name, last_name, bday, employee_num, gender, date_started, department.dept_name FROM employee LEFT JOIN department ON employee.dept_num = department.dept_num WHERE first_name = \'{0}\' or last_name = \'{0}\' '.format(queryInput))
		
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
		if (ok == False):
			self.updatelabel.setText('Query Failed')
			print(query.lastError().number())
			print(query.lastError().databaseText())
		else:
			self.updatelabel.setText('Query Successful')

	def update_click(self):
		if(self.idBox.text() == ''):
			return
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
	db = QSqlDatabase
	app = QApplication(sys.argv)
	ex = SQL()
	
	sys.exit(app.exec_())  

