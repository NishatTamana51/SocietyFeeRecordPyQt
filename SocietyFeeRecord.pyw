from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from fpdf import FPDF
import sys
import sqlite3
import time
import os
import datetime


class InsertDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(InsertDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Register")

        self.setWindowTitle("Add Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        self.QBtn.clicked.connect(self.addstudent)

        layout = QVBoxLayout()

        self.reg_noinput = QLineEdit()
        self.reg_noinput.setPlaceholderText("Registration No.")
        layout.addWidget(self.reg_noinput)

        self.nameinput = QLineEdit()
        self.nameinput.setPlaceholderText("Name")
        layout.addWidget(self.nameinput)

        self.semesterinput = QComboBox()
        self.semesterinput.addItem("1/1")
        self.semesterinput.addItem("1/2")
        self.semesterinput.addItem("2/1")
        self.semesterinput.addItem("2/2")
        self.semesterinput.addItem("3/1")
        self.semesterinput.addItem("3/2")
        self.semesterinput.addItem("4/1")
        self.semesterinput.addItem("4/2")
        self.semesterinput.addItem("M/1")
        self.semesterinput.addItem("M/2")
        self.semesterinput.addItem("M/3")
        layout.addWidget(self.semesterinput)

        self.yearinput = QLineEdit()
        self.yearinput.setPlaceholderText("Examination Year")
        layout.addWidget(self.yearinput)
        
        self.mobileinput = QLineEdit()
        self.mobileinput.setPlaceholderText("Mobile No.")
        layout.addWidget(self.mobileinput)

        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def addstudent(self):

        reg_no = ""
        name = ""
        semester = ""
        year = ""
        mobile = ""
        
        reg_no = self.reg_noinput.text()
        name = self.nameinput.text()
        semester = self.semesterinput.itemText(self.semesterinput.currentIndex())
        year = self.yearinput.text ()
        mobile = self.mobileinput.text()
        
        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            self.c.execute("INSERT INTO socRecord(reg_no,name,semester,year,mobile) VALUES (?,?,?,?,?)",(reg_no,name,semester,year,mobile))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'SUCCESS!','Student has been added to the database.')
            self.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'ERROR!', 'Could not add student to the database.')

class SearchDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(SearchDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Search")

        self.setWindowTitle("Search Entry")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.searchstudent)
        layout = QVBoxLayout()

        self.searchinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.searchinput.setValidator(self.onlyInt)
        self.searchinput.setPlaceholderText("Registration No.")
        layout.addWidget(self.searchinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def searchstudent(self):

        searchreg = ""
        searchreg = self.searchinput.text()
        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            result = self.c.execute("WITH cte AS (SELECT ROW_NUMBER() OVER (ORDER BY reg_no) AS serial,reg_no,name,semester,year,mobile FROM socRecord)SELECT serial,reg_no,name,semester,year,mobile FROM cte WHERE reg_no = "+str(searchreg))#changed
            row = result.fetchone()
            searchresult = "Serial no : "+str(row[0])+'\n'+"Registration No. : "+str(row[1])+'\n'+"Name: "+str(row[2])+'\n'+"Semester : "+str(row[3])+'\n'+"Mobile : "+str(row[5])+'\n'#changed
            QMessageBox.information(QMessageBox(), 'SUCCESSFUL!', searchresult)
            self.conn.commit()
            self.c.close()
            self.conn.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'ERROR!', 'Could not find student in the database.')

class DeleteDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(DeleteDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Delete")

        self.setWindowTitle("Delete Student")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.QBtn.clicked.connect(self.deletestudent)
        layout = QVBoxLayout()

        self.deleteinput = QLineEdit()
        self.onlyInt = QIntValidator()
        self.deleteinput.setValidator(self.onlyInt)
        self.deleteinput.setPlaceholderText("Registration No.")
        layout.addWidget(self.deleteinput)
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def deletestudent(self):

        delreg = ""
        delreg = self.deleteinput.text()

        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            self.c.execute("DELETE from socRecord WHERE reg_no="+str(delreg))#changed
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'SUCCESS!','Deletion from table successful')
            self.close()
        except Exception:
            QMessageBox.warning(QMessageBox(), 'ERROR!', 'Could not Delete student from the database.')



class AboutDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(AboutDialog, self).__init__(*args, **kwargs)

        self.setFixedWidth(500)
        self.setFixedHeight(500)

        QBtn = QDialogButtonBox.Ok  
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        
        self.setWindowTitle("About")
        title = QLabel("BMB SOCIETY FEE RECORD")
        font = title.font()
        font.setPointSize(20)
        title.setFont(font)

        labelpic = QLabel()
        pixmap = QPixmap('icon/sust.png')
        pixmap = pixmap.scaledToWidth(250)
        labelpic.setPixmap(pixmap)
        labelpic.setFixedHeight(275)

        layout.addWidget(title)

        layout.addWidget(QLabel("v1.0"))
        layout.addWidget(QLabel("This program is done as a project work under the supervision of\n"
                                "Tanvir Hossain, Lecturer, Department of Biochemistry and Molecular Biology, SUST.\n\n"
                                "Authors:\nNishat Tamanna (Masters 1st semester, Session: 2019-20, BMB, SUST)\n"
                                "Firoz Mahmud (Masters 1st semester, Session: 2019-20, BMB, SUST)"))
        layout.addWidget(labelpic)


        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
        
class ExportDialog(QDialog):
    def __init__(self, *args, **kwargs):
        super(ExportDialog, self).__init__(*args, **kwargs)

        self.QBtn = QPushButton()
        self.QBtn.setText("Get a PDF Copy")

        self.setWindowTitle("Export as PDF")
        self.setFixedWidth(300)
        self.setFixedHeight(200)
        self.QBtn.clicked.connect(self.createPdf)
        layout = QVBoxLayout()

        self.pdfNameinput = QLineEdit()
        self.pdfNameinput.setPlaceholderText("PDF file name")
        layout.addWidget(self.pdfNameinput)

        self.takeinput = QComboBox()
        self.takeinput.addItem("1/1")
        self.takeinput.addItem("1/2")
        self.takeinput.addItem("2/1")
        self.takeinput.addItem("2/2")
        self.takeinput.addItem("3/1")
        self.takeinput.addItem("3/2")
        self.takeinput.addItem("4/1")
        self.takeinput.addItem("4/2")
        self.takeinput.addItem("M/1")
        self.takeinput.addItem("M/2")
        self.takeinput.addItem("M/3")
        layout.addWidget(self.takeinput)

        self.yearinput = QLineEdit()
        self.yearinput.setPlaceholderText("Examination Year")
        layout.addWidget(self.yearinput)
        
        layout.addWidget(self.QBtn)
        self.setLayout(layout)

    def createPdf(self):
        year = ""
        year = self.yearinput.text ()
        pdfName = ""
        pdfName = self.pdfNameinput.text() + '.pdf' 
        name_of_semester = ""
        name_of_semester = self.takeinput.itemText(self.takeinput.currentIndex())
        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            result = self.c.execute("SELECT row_number() OVER (ORDER BY reg_no) AS serial,reg_no,name FROM socRecord WHERE semester = ? AND year = ?",(name_of_semester,year,),)#changed
            
            ###########Exporting as Pdf Using fpdf #################
            pdf = FPDF(format='A4', unit='in')
            pdf.add_page()
            pdf.set_font('Times','',10.0)
            epw = pdf.w - 2*pdf.l_margin
            col_width = epw/4
            pdf.set_font('Times','B',14.0)
            title = 'Society Fee Record of ' + str(name_of_semester) + ' (' + str(year) + ')'
            pdf.cell(epw, 0.0, title , align='C')
            pdf.set_font('Times','',10.0) 
            pdf.ln(0.5)
            th = pdf.font_size
            header = ['Serial No.','Registration No.', 'Name']
            pdf.cell(0.7)
            for i in header:
                if i == header[0]:
                    pdf.cell( col_width/2.3, 2*th, i, border=1, align='C')
                elif i == header[1]:
                    pdf.cell(col_width/1.5, 2*th, i, border=1, align='C')
                else:
                    pdf.cell(col_width/0.5, 2*th, i, border=1, align='C')
            pdf.ln(2*th)    
            for row in result:
                x = list(row)
                pdf.cell(0.7)
                for each in x:
                    if each == x[0]:
                        pdf.cell(col_width/2.3, 2*th, str(each), border=1, align = 'C')
                    elif each == x[1]:
                        pdf.cell(col_width/1.5, 2*th, str(each), border=1, align='C')    
                    else:            
                        pdf.cell(col_width/0.5, 2*th, str(each), border=1, align='C')
                pdf.ln(2*th)
            pdf.ln(4*th)
            pdf.output(pdfName,'F')


            #######For Exporting as csv file#################
            '''with open(pdfName, 'w', newline='') as file:
                writer = csv.writer(file)
                
                writer.writerow(["Serial","Registration No","Name"])
                for row_number, row_data in enumerate(result):
                    writer.writerow([row_number, row_data[1], row_data[2]])'''
            
            self.conn.close()
            QMessageBox.information(QMessageBox(),'SUCCESSFUL!','Check your folder for the PDF')
            self.close()
            
        except Exception:
            QMessageBox.warning(QMessageBox(), 'ERROR!', 'Could not create the PDF.')
            

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowIcon(QIcon('icon/intro.png'))

        self.conn = sqlite3.connect("database.db")
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS socRecord(serial INTEGER, reg_no TEXT NOT NULL PRIMARY KEY, name TEXT, semester TEXT, year TEXT, mobile TEXT)")#changed
        self.c.close()

        file_menu = self.menuBar().addMenu("&File")
        export_menu = self.menuBar().addMenu("&Export as PDF")
        help_menu = self.menuBar().addMenu("&About")
        self.setWindowTitle("BMB SOCIETY FEE RECORD")
        self.setMinimumSize(800, 600)

        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget.setHorizontalHeaderLabels(("Serial No.", "Registration No.", "Name", "Semester", "Examination Year", "Mobile No."))

        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        statusbar = QStatusBar()
        self.setStatusBar(statusbar)

        btn_ac_adduser = QAction(QIcon("icon/add.jpg"), "Add Student", self)
        btn_ac_adduser.triggered.connect(self.insert)
        btn_ac_adduser.setStatusTip("Add Student")
        toolbar.addAction(btn_ac_adduser)

        btn_ac_refresh = QAction(QIcon("icon/refresh.png"),"Refresh",self)
        btn_ac_refresh.triggered.connect(self.loaddata)
        btn_ac_refresh.setStatusTip("Refresh Table")
        toolbar.addAction(btn_ac_refresh)

        btn_ac_search = QAction(QIcon("icon/search.png"), "Search", self)
        btn_ac_search.triggered.connect(self.search)
        btn_ac_search.setStatusTip("Search User")
        toolbar.addAction(btn_ac_search)

        btn_ac_delete = QAction(QIcon("icon/delete.png"), "Delete", self)
        btn_ac_delete.triggered.connect(self.delete)
        btn_ac_delete.setStatusTip("Delete User")
        toolbar.addAction(btn_ac_delete)

        adduser_action = QAction(QIcon("icon/add.jpg"),"Insert Student", self)
        adduser_action.triggered.connect(self.insert)
        file_menu.addAction(adduser_action)

        searchuser_action = QAction(QIcon("icon/search.png"), "Search Student", self)
        searchuser_action.triggered.connect(self.search)
        file_menu.addAction(searchuser_action)

        deluser_action = QAction(QIcon("icon/delete.png"), "Delete Student", self)
        deluser_action.triggered.connect(self.delete)
        file_menu.addAction(deluser_action)

        deleteTable_action = QAction(QIcon("icon/add.jpg"),"Delete Table", self)
        deleteTable_action.triggered.connect(self.deleteTable)
        file_menu.addAction(deleteTable_action)


        about_action = QAction(QIcon("icon/developer.png"),"Developer", self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)

        export_as_pdf_action = QAction(QIcon("icon/pdf.png"),"Create a PDF", self)
        export_as_pdf_action.triggered.connect(self.export)
        export_menu.addAction(export_as_pdf_action)

    def loaddata(self):
        self.connection = sqlite3.connect("database.db")
        query = "SELECT row_number() OVER (ORDER BY reg_no) AS serial,reg_no,name,semester,year,mobile FROM socRecord"
        result = self.connection.execute(query)
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number,QTableWidgetItem(str(data)))
        self.connection.close()

    def handlePaintRequest(self, printer):
        document = QTextDocument()
        cursor = QTextCursor(document)
        model = self.table.model()
        table = cursor.insertTable(
            model.rowCount(), model.columnCount())
        for row in range(table.rows()):
            for column in range(table.columns()):
                cursor.insertText(model.item(row, column).text())
                cursor.movePosition(QTextCursor.NextCell)
        document.print_(printer)

    def insert(self):
        dlg = InsertDialog()
        dlg.exec_()

    def delete(self):
        dlg = DeleteDialog()
        dlg.exec_()

    def search(self):
        dlg = SearchDialog()
        dlg.exec_()

    def about(self):
        dlg = AboutDialog()
        dlg.exec_()

    def export(self):
        dlg = ExportDialog()
        dlg.exec_()
        
    def deleteTable(self):
        msg = QMessageBox()
        msg.setWindowTitle("CAUTION!")
        msg.setText("You will lose all data.")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.deleteTable2)
        x = msg.exec_()
    

    def deleteTable2(self):
        msg2 = QMessageBox()
        msg2.setWindowTitle("SUCCESSFUL!")
        msg2.setText("All data deleted. Close the program.")
        msg2.setIcon(QMessageBox.Question)
        msg2.setStandardButtons(QMessageBox.Ok)
        msg2.buttonClicked.connect(self.dropTable)
        x = msg2.exec_()

    def dropTable(self):
        try:
            self.conn = sqlite3.connect("database.db")
            self.c = self.conn.cursor()
            self.c.execute("DROP TABLE IF EXISTS socRecord")
            self.conn.close()

        except Exception:
            QMessageBox.warning(QMessageBox(), 'ERROR!', 'Could not Delete  entire table.')
        


app = QApplication(sys.argv)
if(QDialog.Accepted == True):
    window = MainWindow()
    window.show()
    window.loaddata()
sys.exit(app.exec_())

