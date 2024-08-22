from ast import Try
from cProfile import label
from faulthandler import disable
from inspect import Parameter
from logging import root
from math import fabs
from select import select
from tabnanny import check
from time import sleep
import tkinter as tk
from tkinter import CENTER, END, NO, StringVar, ttk as ttk
import sys
from tracemalloc import stop
from turtle import back, color, width
from xml.etree.ElementTree import C14NWriterTarget
from colorama import Cursor
from cv2 import findFundamentalMat
from numpy import equal, true_divide
from psutil import users
import pyodbc as odbc
from tkinter import W, Grid, messagebox

flageLogedIn = False
flageLogedInDataEntry = False

#Making connection to the Database of MS SQL SERVER

DRIVER_NAME = 'SQL SERVER'
SERVER_NAME = 'DESKTOP-9RNCLNJ'
DATABASE_NAME = 'SchoolManagementSystem'
connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connefction=yes;
"""


userSignInUserNameGlobal = ''

show_face = '😃'
hide_face = '😁'

root = tk.Tk()
root.geometry("700x900")
root.title("School Management System")
#root.config(bg="#447c84")
#root.state('zoomed')

frame = tk.Frame(root,pady=20)
frame.pack(expand=True,pady=20)
#frame.propagate(False)
frame.config(width=1000,height=1000)
#bg='#179094'



class Windows:


    def show_hide_password(self):
        if self.passwordEntry['show'] == '●':
            self.passwordEntry.configure(show='')
            self.showHideBtn.configure(text=show_face)
        else:
            self.passwordEntry.configure(show='●')
            self.showHideBtn.configure(text=hide_face)




    def mainWindow(self):
        #sign in lable
        self.signInLabel = tk.Label(frame, text="School Management System",font=("bold",15))
        self.signInLabel.grid(pady=10,row=0)
        #username Label
        self.userNameLabel = tk.Label(frame, width=15,text="username",font=("Times", "13","bold"))
        self.userNameLabel.grid(pady=10,ipady=5,row=1)
        #Underline:
        self.userName_undrline = tk.Label(frame,text='________________',font=("bold",15),fg='#d6d6d6')
        #userName_undrline.grid(row=2)
        self.userName_undrline.place(x=37,y=123)
        #username Entry
        self.userNameEntry = tk.Entry(frame, font=("Calibri","13","bold"),bd=0)
        self.userNameEntry.grid(pady=10, ipady=5,row=2)
        self.userNameEntry.bind('<FocusIn>', lambda e: self.userName_undrline.configure(fg='#158aff'))
        self.userNameEntry.bind('<FocusOut>', lambda e: self.userName_undrline.configure(fg='#d6d6d6'))
        #password Label
        self.passwordLabel = tk.Label(frame, width=15,text="password",font=("Times", "13","bold"))
        self.passwordLabel.grid(pady=10,ipady=5,row=3)
        #Underline:
        self.password_undrline = tk.Label(frame,text='________________',font=("bold",15),fg='#d6d6d6')
        #userName_undrline.grid(row=2)
        self.password_undrline.place(x=37,y=232)
        #password Entry
        self.passwordEntry = tk.Entry(frame,font=("Calibri","13","bold"),bd=0,show='●')
        self.passwordEntry.grid(pady=10, ipady=5,row=4)
        self.passwordEntry.bind('<FocusIn>', lambda e: self.password_undrline.configure(fg='#158aff'))
        self.passwordEntry.bind('<FocusOut>', lambda e: self.password_undrline.configure(fg='#d6d6d6'))
        #show hide button:
        self.showHideBtn = tk.Button(frame,text=hide_face,font=("bold",15),bd=0,command=self.show_hide_password)
        self.showHideBtn.grid(row=4,column=0,sticky=tk.E)
        #showHideBtn.place(x=290,y=166)
        #sign in button
        self.signInBtn = tk.Button(frame, text="Sign IN",relief=tk.SOLID,width=16,font=("bold",15),bd=0,bg='#158aff',fg='white', command=self.signIN)
        self.registerBtn = tk.Button(frame, text="Register",relief=tk.SOLID,width=16,font=("bold",15),bd=0,bg='#158aff',fg='white', command=self.register)
        self.signInBtn.grid(pady=20,row=5)
        self.registerBtn.grid(pady=20,row=6)




    def destropyMainLablesAndButtons(self):
        self.userNameEntry.delete(0, tk.END)
        self.passwordEntry.delete(0,tk.END)
        self.signInLabel.destroy()
        self.userNameLabel.destroy()
        self.userName_undrline.destroy()
        self.userNameEntry.destroy()
        self.passwordLabel.destroy()
        self.password_undrline.destroy()
        self.passwordEntry.destroy()
        self.showHideBtn.destroy()
        self.signInBtn.destroy()
        self.registerBtn.destroy()







    def signIN(self):
        #check in the database
        #take the input from database
        #check weather the user is register or not if not then
        #nevigate the thread to the main loop and print a wanring window
        try:
            conn = odbc.connect(connection_string)
            print(conn)
        except Exception as e:
            print(e)
            print("Server did not connected so task is terminated: ")
            return False
        myCursor = conn.cursor()
        myCursor.execute("SELECT * FROM SignIn")
        allUserNames = myCursor.fetchall()
        for row in allUserNames:
            print(row)
        userNameFlage = False
        passwordFlage = False
        val = self.userNameEntry.get()
        passw = self.passwordEntry.get()
        #loop for the verification of the user: 
        for record in allUserNames:
            #for verification i am trying to print ther usernames and passwords:
            print('userName: ',record[0],'   password: ', record[1])
            if record[2] == val:
                userNameFlage = True
                if record[3] == passw:
                    passwordFlage = True
                    break
                else:
                    break
        #check condition that the user is registered or not:
        if not userNameFlage and not passwordFlage:
            self.passwordEntry.delete(0,tk.END)
            messagebox.showerror('','User is not Register!\nPlease Register First!')
        elif userNameFlage and not passwordFlage:
            self.passwordEntry.delete(0,tk.END)
            messagebox.showerror('','Incorrect Password!')
        elif userNameFlage and passwordFlage:
            global userSignInUserNameGlobal
            userSignInUserNameGlobal = self.userNameEntry.get()
            print('Global value: ',userSignInUserNameGlobal)
            self.destropyMainLablesAndButtons()
            self.welcomeLabel = tk.Label(frame, text="Welcome "+record[0],font=("Times", "24", "bold"),fg='Blue')
            self.welcomeLabel.grid(pady=20,row=0,columnspan=3)
            myCursor.commit()
            myCursor.close()
            self.Home()



    def Home(self):
        try:
            conn = odbc.connect(connection_string)
            print(conn)
        except Exception as e:
            print(e)
            print("Server did not connected so task is terminated: ")
            return False
        myCursor = conn.cursor()
        self.logOutSignIn = tk.Button(frame, text="Log out",relief=tk.SOLID,width=16,font=("bold",15),bd=0,bg='#158aff',fg='white', command=self.logoutSignedIn)
        #//////////////////////////////////////////////
        #self.logOutSignIn.grid(pady=20,row=5, columnspan=3)
        self.attendance = tk.Button(frame, text="Attendance",relief=tk.SOLID,width=16,font=("bold",15),bd=0,bg='#158aff',fg='white',command=self.attendanceView)
        self.attendance.grid(pady=20,row=1,column=0)
        self.marks = tk.Button(frame, text="Marks",relief=tk.SOLID,width=16,font=("bold",15),bd=0,bg='#158aff',fg='white',command=self.marksView)
        self.marks.grid(pady=20,row=2,column=0)
        self.transcript = tk.Button(frame, text="Transcript",relief=tk.SOLID,width=16,font=("bold",15),bd=0,bg='#158aff',fg='white',command=self.transcriptView)
        self.transcript.grid(pady=20,row=3,column=0)
        self.cources = tk.Button(frame, text="Cources",relief=tk.SOLID,width=16,font=("bold",15),bd=0,bg='#158aff',fg='white', command=self.courseView)
        self.cources.grid(pady=20,row=1,column=2)
        self.timeTable = tk.Button(frame, text="Time Table",relief=tk.SOLID,width=16,font=("bold",15),bd=0,bg='#158aff',fg='white',command=self.timeTableView)
        self.timeTable.grid(pady=20,row=2,column=2)
        self.payments = tk.Button(frame, text="Payments",relief=tk.SOLID,width=16,font=("bold",15),bd=0,bg='#158aff',fg='white',command=self.paymentsView)
        self.payments.grid(pady=20,row=3,column=2)
        # self.enterData = tk.Button(frame, text="Enter Student Data",relief=tk.SOLID,width=35,font=("bold",15),bd=0,bg='#FF4C3D',fg='white',command=self.enterStudentDataView)
        # self.RegisteredUserSuccefully = tk.Label(frame,text='Enter Student Data First',relief=tk.SOLID,font=("bold",15),bd=0,fg='#FF4C3D')
        # self.RegisteredUserSuccefully.grid(pady=10,ipady=5,row=6,columnspan=3)
        # self.enterData.grid(pady=20,row=5,columnspan=3)
        self.logOutSignIn.grid(pady=20,row=7, columnspan=3)
        
        self.row = tk.Button(frame, text="",width=2,bd=0)
        self.row.grid(pady=20,row=8,column=1)
        myCursor = conn.cursor()
        userNameParamerter = [userSignInUserNameGlobal]
        query = "SELECT studentID FROM Student where studentID = ?"
        print("from Home: ",userSignInUserNameGlobal)
        myCursor.execute(query,userNameParamerter)
        UserNameAll = myCursor.fetchall()
        flageExist = False
        for userName in UserNameAll:
            print("UserName: ",userName[0])
            if userName[0] == userSignInUserNameGlobal:
                print("Got it::")
                global flageLogedIn
                flageLogedIn = True
                flageExist = True
                break
        if not flageExist:
            self.enterData = tk.Button(frame, text="Enter Student Data",relief=tk.SOLID,width=35,font=("bold",15),bd=0,bg='#FF4C3D',fg='white',command=self.enterStudentDataView)
            self.enterData.grid(pady=20,row=5,columnspan=3)
            self.RegisteredUserSuccefully = tk.Label(frame,text='Enter Student Data First',relief=tk.SOLID,font=("bold",15),bd=0,fg='#FF4C3D')
            self.RegisteredUserSuccefully.grid(pady=10,ipady=5,row=6,columnspan=3)




    #/////////////////////////////////////////////////////////////////////////

    def createAccount(self):
        try:
            conn = odbc.connect(connection_string)
            print(conn)
        except Exception as e:
            print(e)
            print("Server did not connected so task is terminated: ")
            return False
        myCursor = conn.cursor()
        #sqlQueryRegister = "INSERT INTO SignIn(firstName,lastName,UserName,password_) VALUES (?,?,?,?),  self.firstNameEntry.get(), self.lastNameEntry.get(), self.userNameEntry.get(), self.passwordEntry.get()"
        #valuesRegister = ()
        dataRowRegister = [self.firstNameEntry.get(),self.lastNameEntry.get(),self.userNameEntry.get(), self.passwordEntry.get()]
        
        if self.passwordEntry.get() != self.confirmPasswordEntry.get():
            messagebox.showerror('','Confirm password does not match\nPlease confirm your Password!')
            return False
        elif self.passwordEntry.get() == self.confirmPasswordEntry.get():
            myCursor.execute("SELECT UserName FROM SignIn")
            allRecordsForRegister = myCursor.fetchall()
            i = 0
            flagRegisteration = False
            for registerRow in allRecordsForRegister:
                print('UserNames: ',i,' = ',registerRow[0])
                i = i+1
                if dataRowRegister[2] == registerRow[0]:
                    flagRegisteration = True
                    self.passwordEntry.delete(0,tk.END)
                    self.confirmPasswordEntry.delete(0,tk.END)
                    messagebox.showerror('','User already Registered\nPlease choose another username!')
                    break
            if not flagRegisteration:
                sqlResiterQuery = "INSERT INTO SignIn(firstName,lastName,UserName,password_) VALUES (?,?,?,?)"
                myCursor.execute(sqlResiterQuery,dataRowRegister)
                self.RegisteredUserSuccefully = tk.Label(frame,text='User registered Successfully',relief=tk.SOLID,font=("bold",15),bd=0,fg='green')
                self.RegisteredUserSuccefully.grid(pady=10,ipady=5,row=0,columnspan=2)
                self.registerDestroy()
                myCursor.commit()
                myCursor.close()
        else:
            myCursor.commit()
            myCursor.close()





    def show_hide_password_regiser(self):
        if self.passwordEntry['show'] == '●' or self.confirmPasswordEntry['show'] =='●':
            self.passwordEntry.configure(show='')
            self.confirmPasswordEntry.configure(show='')
            self.showHideRegisterBtn.configure(text=show_face)
        else:
            self.passwordEntry.configure(show='●')
            self.confirmPasswordEntry.configure(show='●')
            self.showHideRegisterBtn.configure(text=hide_face)





    #//////////////////////////////////////////////////////////////////////////

    def registeredSuccefullyDestoy(self):
        self.signInBtn.destroy()
        self.RegisteredUserSuccefully.destroy()
        self.mainWindow()



    def registerDestroy(self):
        self.mainLabel.destroy()
        self.firstNameLabel.destroy()
        self.lastNameLabel.destroy()
        self.userNameLabel.destroy()
        self.passwordLebel.destroy()
        self.confirmPasswordLebel.destroy()
        self.firstName_undrline.destroy()
        self.lastName_undrline.destroy()
        self.userName_undrline.destroy()
        self.password_undrline.destroy()
        self.confirm_password_undrline.destroy()
        self.firstNameEntry.delete(0,tk.END)
        self.lastNameEntry.delete(0,tk.END)
        self.userNameEntry.delete(0,tk.END)
        self.passwordEntry.delete(0,tk.END)
        self.firstNameEntry.destroy()
        self.lastNameEntry.destroy()
        self.userNameEntry.destroy()
        self.passwordEntry.destroy()
        self.confirmPasswordEntry.destroy()
        self.showHideRegisterBtn.destroy()
        self.showPassword.destroy()
        self.registerBtn.destroy()
        self.cancelationBtn.destroy()
        self.signInBtn = tk.Button(frame, text="Sign IN",relief=tk.SOLID,width=16,font=("bold",15),bd=0,bg='#158aff',fg='white', command=self.registeredSuccefullyDestoy)
        self.signInBtn.grid(pady=20,row=1)
        




    def cancleRegisteration(self):
        self.mainLabel.destroy()
        self.firstNameLabel.destroy()
        self.lastNameLabel.destroy()
        self.userNameLabel.destroy()
        self.passwordLebel.destroy()
        self.confirmPasswordLebel.destroy()
        self.firstName_undrline.destroy()
        self.lastName_undrline.destroy()
        self.userName_undrline.destroy()
        self.password_undrline.destroy()
        self.confirm_password_undrline.destroy()
        self.firstNameEntry.delete(0,tk.END)
        self.lastNameEntry.delete(0,tk.END)
        self.userNameEntry.delete(0,tk.END)
        self.passwordEntry.delete(0,tk.END)
        self.firstNameEntry.destroy()
        self.lastNameEntry.destroy()
        self.userNameEntry.destroy()
        self.passwordEntry.destroy()
        self.confirmPasswordEntry.destroy()
        self.showHideRegisterBtn.destroy()
        self.showPassword.destroy()
        self.registerBtn.destroy()
        self.cancelationBtn.destroy()
        self.mainWindow()



    def register(self):
        windows.destropyMainLablesAndButtons()
        #::::::::LABELS::::::::
        # mainLabel
        self.mainLabel = tk.Label(frame, text="Create New Account",font=("bold",15))
        self.mainLabel.grid(pady=10,row=0,columnspan=2)
        #first Name Label
        self.firstNameLabel = tk.Label(frame, width=15,text="First Name",font=("Times", "13","bold"))
        self.firstNameLabel.grid(pady=10,ipady=5,row=1,column=0)
        #last Name Label
        self.lastNameLabel = tk.Label(frame, width=15,text="Last Name",font=("Times", "13","bold"))
        self.lastNameLabel.grid(pady=10,ipady=5,row=2,column=0)
        #userName Label
        self.userNameLabel = tk.Label(frame, width=15,text="Username",font=("Times", "13","bold"))
        self.userNameLabel.grid(pady=10,ipady=5,row=3,column=0)
        #password Lebel
        self.passwordLebel = tk.Label(frame, width=15,text="Password",font=("Times", "13","bold"))
        self.passwordLebel.grid(pady=10,ipady=5,row=4,column=0)
        #confirm password Lebel
        self.confirmPasswordLebel = tk.Label(frame, width=15,text="Confirm password",font=("Times", "13","bold"))
        self.confirmPasswordLebel.grid(pady=10,ipady=5,row=5,column=0)
        #::::::::UNDERLINES::::::::
        #Underline firstName_undrline:
        self.firstName_undrline = tk.Label(frame,text='________________',font=("bold",15),fg='#d6d6d6')
        self.firstName_undrline.place(x=155,y=69)
        #Underline lastName_undrline:
        self.lastName_undrline = tk.Label(frame,text='________________',font=("bold",15),fg='#d6d6d6')
        self.lastName_undrline.place(x=155,y=124)
        #Underline userName_undrline:
        self.userName_undrline = tk.Label(frame,text='________________',font=("bold",15),fg='#d6d6d6')
        self.userName_undrline.place(x=155,y=179)
        #Underline password_undrline:
        self.password_undrline = tk.Label(frame,text='________________',font=("bold",15),fg='#d6d6d6')
        self.password_undrline.place(x=155,y=234)
        #Underline confirm password_undrline:
        self.confirm_password_undrline = tk.Label(frame,text='________________',font=("bold",15),fg='#d6d6d6')
        self.confirm_password_undrline.place(x=155,y=289)
        #::::::::ENTRIES::::::::
        #FIRST NAME ENTRY
        self.firstNameEntry = tk.Entry(frame, font=("Calibri","13","bold"),bd=0)
        self.firstNameEntry.grid(pady=10, ipady=5,row=1,column=1)
        self.firstNameEntry.bind('<FocusIn>', lambda e: self.firstName_undrline.configure(fg='#158aff'))
        self.firstNameEntry.bind('<FocusOut>', lambda e: self.firstName_undrline.configure(fg='#d6d6d6'))
        #LAST NAME ENTRY
        self.lastNameEntry = tk.Entry(frame, font=("Calibri","13","bold"),bd=0)
        self.lastNameEntry.grid(pady=10, ipady=5,row=2,column=1)
        self.lastNameEntry.bind('<FocusIn>', lambda e: self.lastName_undrline.configure(fg='#158aff'))
        self.lastNameEntry.bind('<FocusOut>', lambda e: self.lastName_undrline.configure(fg='#d6d6d6'))
        #USERNAME Entry
        self.userNameEntry = tk.Entry(frame, font=("Calibri","13","bold"),bd=0)
        self.userNameEntry.grid(pady=10, ipady=5,row=3,column=1)
        self.userNameEntry.bind('<FocusIn>', lambda e: self.userName_undrline.configure(fg='#158aff'))
        self.userNameEntry.bind('<FocusOut>', lambda e: self.userName_undrline.configure(fg='#d6d6d6'))
        #PASSWORD Entry
        self.passwordEntry = tk.Entry(frame,font=("Calibri","13","bold"),bd=0,show='●')
        self.passwordEntry.grid(pady=10, ipady=5,row=4,column=1)
        self.passwordEntry.bind('<FocusIn>', lambda e: self.password_undrline.configure(fg='#158aff'))
        self.passwordEntry.bind('<FocusOut>', lambda e: self.password_undrline.configure(fg='#d6d6d6'))
        #CONFIRM PASSWORD ENTRY
        self.confirmPasswordEntry = tk.Entry(frame,font=("Calibri","13","bold"),bd=0,show='●')
        self.confirmPasswordEntry.grid(pady=10, ipady=5,row=5,column=1)
        self.confirmPasswordEntry.bind('<FocusIn>', lambda e: self.confirm_password_undrline.configure(fg='#158aff'))
        self.confirmPasswordEntry.bind('<FocusOut>', lambda e: self.confirm_password_undrline.configure(fg='#d6d6d6'))
        #show hide button:
        self.showHideRegisterBtn = tk.Button(frame,text=hide_face,font=("bold",15),bd=0,command=self.show_hide_password_regiser)
        self.showHideRegisterBtn.grid(row=6,column=0,sticky=tk.E)
        #show Show password:
        self.showPassword = tk.Label(frame, width=15,text="Show password",font=("Times", "13","bold"),justify=tk.LEFT)
        self.showPassword.grid(pady=10,ipady=5,row=6,column=1,sticky=tk.W)
        #::::::::BUTTONS::::::::
        #REGISTER BUTTON
        self.registerBtn = tk.Button(frame, text="Create",relief=tk.SOLID,width=16,font=("bold",15),bd=0,bg='#158aff',fg='white',command=self.createAccount)
        self.registerBtn.grid(pady=20,row=7,columnspan=2)
        #CANCLE BUTTON
        self.cancelationBtn = tk.Button(frame, text="Cancel",relief=tk.SOLID,width=16,font=("bold",15),bd=0,bg='#158aff',fg='white', command=self.cancleRegisteration)
        self.cancelationBtn.grid(pady=20,row=8,columnspan=2)


        
    def logoutSignedIn(self):
        self.destroyFromHome()
        userSignInUserNameGlobal = ''
        self.mainWindow()

    def destroyFromHome(self):
        self.welcomeLabel.destroy()
        self.logOutSignIn.destroy()
        self.attendance.destroy()
        self.marks.destroy()
        self.transcript.destroy()
        self.cources.destroy()
        self.timeTable.destroy()
        self.payments.destroy()
        self.row.destroy()
        if not flageLogedIn:    
            self.RegisteredUserSuccefully.destroy()
            self.enterData.destroy()
        
    def back(self,Label,backBtn,homeBtn,logout,treeView):
        Label.destroy()
        treeView.destroy()
        logout.destroy()
        backBtn.destroy()
        homeBtn.destroy()
        self.Home()

    
    def logout(self,Label,backBtn,homeBtn,logoutBtn,treeView):
        logoutBtn.destroy()
        treeView.destroy()
        Label.destroy()
        backBtn.destroy()
        homeBtn.destroy()
        self.mainWindow()




    def attendanceView(self):
        self.destroyFromHome()
        try:
            conn = odbc.connect(connection_string)
            print(conn)
        except Exception as e:
            print(e)
            print("Server did not connected so task is terminated: ")
            return False
        myCursor = conn.cursor()
        
        if not flageLogedIn:
            messagebox.showerror('','Student Data does not Exist\nPlease Enter Student data first')
            self.Home()
        else:
            self.destroyFromHome()
            self.backBtn = tk.Button(frame, text="🔙",justify=tk.LEFT,relief=tk.SOLID,width=1,font=("bold",25),bd=0,fg='#158aff', command= lambda: self.back( self.attendanceLabel,self.backBtn, self.homeBtn,self.logoutBtn,self.treeView))
            self.backBtn.grid(pady=20,row=0,column=1,sticky=tk.W)
            self.homeBtn = tk.Button(frame, text="🏠",justify=tk.LEFT,relief=tk.SOLID,width=1,font=("bold",25),bd=0,fg='#158aff', command= lambda: self.back( self.attendanceLabel,self.backBtn, self.homeBtn,self.logoutBtn,self.treeView))
            self.homeBtn.grid(pady=20,row=0,column=0,sticky=tk.W)
            self.logoutBtn = tk.Button(frame, text="Logout",justify=tk.LEFT,relief=tk.SOLID,width=8,font=("bold",13),bg='#158aff',bd=0,fg='white', command= lambda: self.logout( self.attendanceLabel,self.backBtn, self.homeBtn,self.logoutBtn,self.treeView))
            self.logoutBtn.grid(pady=10,row=0,column=3,sticky=tk.E)
            self.attendanceLabel = tk.Label(frame, text="Attendance",font=("Times", "24", "bold"),fg='Blue')
            self.attendanceLabel.grid(pady=20,row=1,columnspan=4)
            self.treeView = ttk.Treeview(frame,height=30)
            self.treeView.grid(row=2,columnspan=4)
            self.treeView['columns'] = ("CourseID","Lecture no.","Attendance","Date","Teacher")
            #self.treeView.column("#0",width=0,stretch=NO)
            self.treeView.column("#0",width=100,minwidth=25)
            self.treeView.column("CourseID",width=120,minwidth=25,anchor=CENTER)
            self.treeView.column("Lecture no.",width=120,minwidth=25,anchor=CENTER)
            self.treeView.column("Attendance",width=120,minwidth=25,anchor=CENTER)
            self.treeView.column("Date",width=120,minwidth=25,anchor=CENTER)
            self.treeView.column("Teacher",width=120,minwidth=25,anchor=CENTER)

            self.treeView.heading("#0",text="Course",anchor=CENTER)
            self.treeView.heading("CourseID",text="CourseID",anchor=CENTER)
            self.treeView.heading("Lecture no.",text="Lecture no#",anchor=CENTER)
            self.treeView.heading("Attendance",text="Attendance",anchor=CENTER)
            self.treeView.heading("Date",text="Date",anchor=CENTER)
            self.treeView.heading("Teacher",text="Teacher",anchor=CENTER)
            
            # # add a scrollbar
            # scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.treeView.yview)
            # self.treeView.configure(yscroll=scrollbar.set)
            # scrollbar.grid(row=0, column=1, sticky='NS')
            perameter = [userSignInUserNameGlobal]
            query = "Select CourseID, crsName from Course where StudentID = ?"
            myCursor.execute(query,perameter)
            print('User: ',userSignInUserNameGlobal)
            courseID_ = myCursor.fetchall()
            myCursor.commit()
            myCursor.close()
            count = 0
            for cour in courseID_:
                print('count: ',count, '  :cour: ',cour[0])
                self.treeView.insert(parent='',index='end',iid=count,text=cour[1],values=())
                count = count +1

            myCursor = conn.cursor()
            query = "Select CourseID,lecNum,attendance,attDate,teacherName from Attendance where studentID = ?"
            myCursor.execute(query,perameter)
            attendacnceValue = myCursor.fetchall()
            myCursor.commit()
            myCursor.close()
            index = 100
            print('count: ',count)
            print('index: ',index)
            mark = "✅"
            for valu in attendacnceValue:
                courCount = 0
                for course in courseID_:
                    if course[0] == valu[0]:
                        if valu[2]=="Present":
                            mark = "✅"
                        else:
                            mark = "❌"
                        break
                    courCount = courCount +1
                self.treeView.insert(parent='',index='end',iid=count,text=mark,values=(valu[0],valu[1],valu[2],valu[3],valu[4]))
                self.treeView.move(count,courCount,index)
                index = index+1
                count = count+1



    def courseView(self):
        self.destroyFromHome()
        try:
            conn = odbc.connect(connection_string)
            print(conn)
        except Exception as e:
            print(e)
            print("Server did not connected so task is terminated: ")
            return False
        myCursor = conn.cursor()
        query = "Select studentID From Student where studentID = ?"
        perameter = [userSignInUserNameGlobal]
        myCursor.execute(query,perameter)
        courseUserName = myCursor.fetchall()
        myCursor.commit()
        myCursor.close()
        flageCourseUsername = False
        for username in courseUserName:
            print("UserName: ",username[0])
            if username[0]==userSignInUserNameGlobal:
                print('Got Attendance: ')
                flageCourseUsername = True
                break
        
        if not flageCourseUsername:
            messagebox.showerror('','Student Data does not Exist\nPlease Enter Student data first')
            self.Home()
        else:
            self.destroyFromHome()
            self.backBtn = tk.Button(frame, text="🔙",justify=tk.LEFT,relief=tk.SOLID,width=1,font=("bold",25),bd=0,fg='#158aff', command= lambda: self.back( self.courseLabel,self.backBtn, self.homeBtn,self.logoutBtn,self.treeView))
            self.backBtn.grid(pady=20,row=0,column=1,sticky=tk.W)
            self.homeBtn = tk.Button(frame, text="🏠",justify=tk.LEFT,relief=tk.SOLID,width=1,font=("bold",25),bd=0,fg='#158aff', command= lambda: self.back( self.courseLabel,self.backBtn, self.homeBtn,self.logoutBtn,self.treeView))
            self.homeBtn.grid(pady=20,row=0,column=0,sticky=tk.W)
            self.logoutBtn = tk.Button(frame, text="Logout",justify=tk.LEFT,relief=tk.SOLID,width=8,font=("bold",13),bg='#158aff',bd=0,fg='white', command= lambda: self.logout( self.courseLabel,self.backBtn, self.homeBtn,self.logoutBtn,self.treeView))
            self.logoutBtn.grid(pady=10,row=0,column=3,sticky=tk.E)
            self.courseLabel = tk.Label(frame, text="Course",font=("Times", "24", "bold"),fg='Blue')
            self.courseLabel.grid(pady=20,row=1,columnspan=4)
            self.treeView = ttk.Treeview(frame,height=15)
            self.treeView.grid(row=2,columnspan=4)
            self.treeView['columns'] = ("CourseID","crsName","section","teacherName","teacherEmail","crsCreditHrs","bookName")
            self.treeView.column("#0",width=0,stretch=NO)
            self.treeView.column("CourseID",width=120,minwidth=25,anchor=CENTER)
            self.treeView.column("crsName",width=120,minwidth=25,anchor=CENTER)
            self.treeView.column("section",width=120,minwidth=25,anchor=CENTER)
            self.treeView.column("teacherName",width=120,minwidth=25,anchor=CENTER)
            self.treeView.column("teacherEmail",width=120,minwidth=25,anchor=CENTER)
            self.treeView.column("crsCreditHrs",width=120,minwidth=25,anchor=CENTER)
            self.treeView.column("bookName",width=120,minwidth=25,anchor=CENTER)

            self.treeView.heading("#0",text="",anchor=CENTER)
            self.treeView.heading("CourseID",text="CourseID",anchor=CENTER)
            self.treeView.heading("crsName",text="Name",anchor=CENTER)
            self.treeView.heading("section",text="Section",anchor=CENTER)
            self.treeView.heading("teacherName",text="Teacher",anchor=CENTER)
            self.treeView.heading("teacherEmail",text="Teacher Email",anchor=CENTER)
            self.treeView.heading("crsCreditHrs",text="CH",anchor=CENTER)
            self.treeView.heading("bookName",text="Book",anchor=CENTER)


            # # add a scrollbar
            # scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=self.treeView.yview)
            # self.treeView.configure(yscroll=scrollbar.set)
            # scrollbar.grid(row=0, column=1, sticky='ns')
            myCursor = conn.cursor()
            query = "Select CourseID, crsName,section,teacherName,teacherEmail,crsCreditHrs,bookName from Course where StudentID = ?"
            myCursor.execute(query,perameter)
            courseID = myCursor.fetchall()
            myCursor.commit()
            myCursor.close()
            count = 0
            for cour in courseID:
                self.treeView.insert(parent='',index='end',iid=count,text=cour[1],values=(cour[0],cour[1],cour[2],cour[3],cour[4],cour[5],cour[6]))
                count +=1







    def marksView(self):
        self.destroyFromHome()

        
        try:
            conn = odbc.connect(connection_string)
            print(conn)
        except Exception as e:
            print(e)
            print("Server did not connected so task is terminated: ")
            return False
        myCursor = conn.cursor()
        query = "Select studentID From Student where studentID = ?"
        perameter = [userSignInUserNameGlobal]
        myCursor.execute(query,perameter)
        marksUserName = myCursor.fetchall()
        myCursor.commit()
        myCursor.close()
        flageMarksUsername = False
        for username in marksUserName:
            print("UserName: ",username[0])
            if username[0]==userSignInUserNameGlobal:
                print('Got Attendance: ')
                flageMarksUsername = True
                break
        
        if not flageMarksUsername:
            messagebox.showerror('','Student Data does not Exist\nPlease Enter Student data first')
            self.Home()
        else:
            self.backBtn = tk.Button(frame, text="🔙",justify=tk.LEFT,relief=tk.SOLID,width=1,font=("bold",25),bd=0,fg='#158aff', command= lambda: self.back( self.marksLabel,self.backBtn, self.homeBtn,self.logoutBtn,self.treeView))
            self.backBtn.grid(pady=20,row=0,column=1,sticky=tk.W)
            self.homeBtn = tk.Button(frame, text="🏠",justify=tk.LEFT,relief=tk.SOLID,width=1,font=("bold",25),bd=0,fg='#158aff', command= lambda: self.back( self.marksLabel,self.backBtn, self.homeBtn,self.logoutBtn,self.treeView))
            self.homeBtn.grid(pady=20,row=0,column=0,sticky=tk.W)
            self.logoutBtn = tk.Button(frame, text="Logout",justify=tk.LEFT,relief=tk.SOLID,width=8,font=("bold",13),bg='#158aff',bd=0,fg='white', command= lambda: self.logout( self.marksLabel,self.backBtn, self.homeBtn,self.logoutBtn,self.treeView))
            self.logoutBtn.grid(pady=10,row=0,column=3,sticky=tk.E)
            self.marksLabel = tk.Label(frame, text="Marks",font=("Times", "24", "bold"),fg='Blue')
            self.marksLabel.grid(pady=20,row=1,columnspan=4)
            

            self.treeView = ttk.Treeview(frame,height=30)
            self.treeView.grid(row=2,columnspan=4)
            self.treeView['columns'] = ("CourseID","examName","totalMarks","obtaindedMarks")
            #self.treeView.column("#0",width=0,stretch=NO)
            self.treeView.column("#0",width=100,minwidth=25)
            self.treeView.column("CourseID",width=120,minwidth=25,anchor=CENTER)
            self.treeView.column("examName",width=120,minwidth=25,anchor=CENTER)
            self.treeView.column("totalMarks",width=120,minwidth=25,anchor=CENTER)
            self.treeView.column("obtaindedMarks",width=120,minwidth=25,anchor=CENTER)

            self.treeView.heading("#0",text="Course",anchor=CENTER)
            self.treeView.heading("CourseID",text="CourseID",anchor=CENTER)
            self.treeView.heading("examName",text="Exam",anchor=CENTER)
            self.treeView.heading("totalMarks",text="Tolal Marks",anchor=CENTER)
            self.treeView.heading("obtaindedMarks",text="Obtainded Marks",anchor=CENTER)
            
            # # add a scrollbar
            # scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=self.treeView.yview)
            # self.treeView.configure(yscroll=scrollbar.set)
            # scrollbar.grid(row=0, column=1, sticky='ns')
            myCursor = conn.cursor()
            query = "Select CourseID,crsName  from Course where StudentID = ?"
            myCursor.execute(query,perameter)
            courseID_ = myCursor.fetchall()
            myCursor.commit()
            myCursor.close()
            count = 0
            for cour in courseID_:
                self.treeView.insert(parent='',index='end',iid=count,text=cour[1],values=())
                count +=1

            myCursor = conn.cursor()
            query = "Select CourseID, examName, totalMarks,obtaindedMarks from Exam where StudentID = ?"
            myCursor.execute(query,perameter)
            marksValue = myCursor.fetchall()
            myCursor.commit()
            myCursor.close()
            index = 100
            print('count: ',count)
            print('index: ',index)
            for valu in marksValue:
                courCount = 0
                for course in courseID_:
                    if course[0] == valu[0]:
                        print('Yes:')
                        break
                    courCount = courCount +1
                self.treeView.insert(parent='',index='end',iid=count,text="",values=(valu[0],valu[1],valu[2],valu[3]))
                self.treeView.move(count,courCount,index)
                index = index+1
                count = count+1









    def timeTableView(self):
        self.destroyFromHome()
        try:
            conn = odbc.connect(connection_string)
            print(conn)
        except Exception as e:
            print(e)
            print("Server did not connected so task is terminated: ")
            return False
        myCursor = conn.cursor()
        query = "Select studentID From Student where studentID = ?"
        perameter = [userSignInUserNameGlobal]
        myCursor.execute(query,perameter)
        marksUserName = myCursor.fetchall()
        myCursor.commit()
        myCursor.close()
        flageMarksUsername = False
        for username in marksUserName:
            print("UserName: ",username[0])
            if username[0]==userSignInUserNameGlobal:
                print('Got Time Table: ')
                flageMarksUsername = True
                break
        
        if not flageMarksUsername:
            messagebox.showerror('','Student Data does not Exist\nPlease Enter Student data first')
            self.Home()
        else:
            
            self.backBtn = tk.Button(frame, text="🔙",justify=tk.LEFT,relief=tk.SOLID,width=1,font=("bold",25),bd=0,fg='#158aff', command= lambda: self.back( self.timeTableLabel,self.backBtn, self.homeBtn,self.logoutBtn,self.treeView))
            self.backBtn.grid(pady=20,row=0,column=1,sticky=tk.W)
            self.homeBtn = tk.Button(frame, text="🏠",justify=tk.LEFT,relief=tk.SOLID,width=1,font=("bold",25),bd=0,fg='#158aff', command= lambda: self.back( self.timeTableLabel,self.backBtn, self.homeBtn,self.logoutBtn,self.treeView))
            self.homeBtn.grid(pady=20,row=0,column=0,sticky=tk.W)
            self.logoutBtn = tk.Button(frame, text="Logout",justify=tk.LEFT,relief=tk.SOLID,width=8,font=("bold",13),bg='#158aff',bd=0,fg='white', command= lambda: self.logout( self.timeTableLabel,self.backBtn, self.homeBtn,self.logoutBtn,self.treeView))
            self.logoutBtn.grid(pady=10,row=0,column=3,sticky=tk.E)
            self.timeTableLabel = tk.Label(frame, text="Time Table",font=("Times", "24", "bold"),fg='Blue')
            self.timeTableLabel.grid(pady=20,row=1,columnspan=3)
            self.treeView = ttk.Treeview(frame,height=30)
            self.treeView.grid(row=2,columnspan=4)
            self.treeView.grid(row=2,columnspan=4)
            self.treeView['columns'] = ("classDay","CourseID","crsName","teacherName","classSrartTime","classEndTime","room")
            self.treeView.column("#0",width=0,stretch=NO)
            self.treeView.column("classDay",width=60,minwidth=25,anchor=W)
            self.treeView.column("CourseID",width=50,minwidth=25,anchor=CENTER)
            self.treeView.column("crsName",width=100,minwidth=25,anchor=W)
            self.treeView.column("teacherName",width=120,minwidth=25,anchor=W)
            self.treeView.column("classSrartTime",width=80,minwidth=25,anchor=W)
            self.treeView.column("classEndTime",width=80,minwidth=25,anchor=W)
            self.treeView.column("room",width=50,minwidth=30,anchor=W)

            self.treeView.heading("#0",text="",anchor=CENTER)
            self.treeView.heading("classDay",text="Day",anchor=CENTER)
            self.treeView.heading("CourseID",text="C.Code",anchor=CENTER)
            self.treeView.heading("crsName",text="Name",anchor=CENTER)
            self.treeView.heading("teacherName",text="Faculty",anchor=CENTER)
            self.treeView.heading("classSrartTime",text="Start Time",anchor=CENTER)
            self.treeView.heading("classEndTime",text="End Time",anchor=CENTER)
            self.treeView.heading("room",text="C.Room",anchor=CENTER)
            
            # # add a scrollbar
            # scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=self.treeView.yview)
            # self.treeView.configure(yscroll=scrollbar.set)
            # scrollbar.grid(row=0, column=1, sticky=tk.NS)
            myCursor = conn.cursor()
            query = "Select classDay,CourseID,crsName,teacherName,classSrartTime,classEndTime,room  from TimeTable where StudentID = ?"
            myCursor.execute(query,perameter)
            timeTableValue = myCursor.fetchall()
            myCursor.commit()
            myCursor.close()
            count = 0
            for cour in timeTableValue:
                self.treeView.insert(parent='',index='end',iid=count,text=cour[1],values=(cour[0],cour[1],cour[2],cour[3],cour[4],cour[5],cour[6]))
                count +=1




    def transcriptView(self):
        self.destroyFromHome()
        self.backBtn = tk.Button(frame, text="🔙",justify=tk.LEFT,relief=tk.SOLID,width=1,font=("bold",25),bd=0,fg='#158aff', command= lambda: self.back( self.transcriptLabel,self.backBtn, self.homeBtn,self.logoutBtn,self.treeView))
        self.backBtn.grid(pady=20,row=0,column=1,sticky=tk.W)
        self.homeBtn = tk.Button(frame, text="🏠",justify=tk.LEFT,relief=tk.SOLID,width=1,font=("bold",25),bd=0,fg='#158aff', command= lambda: self.back( self.transcriptLabel,self.backBtn, self.homeBtn,self.logoutBtn,self.treeView))
        self.homeBtn.grid(pady=20,row=0,column=0,sticky=tk.W)
        self.logoutBtn = tk.Button(frame, text="Logout",justify=tk.LEFT,relief=tk.SOLID,width=8,font=("bold",13),bg='#158aff',bd=0,fg='white', command= lambda: self.logout( self.transcriptLabel,self.backBtn, self.homeBtn,self.logoutBtn,self.treeView))
        self.logoutBtn.grid(pady=10,row=0,column=3,sticky=tk.E)
        self.transcriptLabel = tk.Label(frame, text="Transcript",font=("Times", "24", "bold"),fg='Blue')
        self.transcriptLabel.grid(pady=20,row=1,columnspan=3)
        self.treeView = ttk.Treeview(frame,height=30)
        self.treeView.grid(row=2,columnspan=4)




    def paymentsView(self):
        self.destroyFromHome()
        self.backBtn = tk.Button(frame, text="🔙",justify=tk.LEFT,relief=tk.SOLID,width=1,font=("bold",25),bd=0,fg='#158aff', command= lambda: self.back( self.paymentsLabel,self.backBtn, self.homeBtn,self.logoutBtn,self.treeView))
        self.backBtn.grid(pady=20,row=0,column=1,sticky=tk.W)
        self.homeBtn = tk.Button(frame, text="🏠",justify=tk.LEFT,relief=tk.SOLID,width=1,font=("bold",25),bd=0,fg='#158aff', command= lambda: self.back( self.paymentsLabel,self.backBtn, self.homeBtn,self.logoutBtn,self.treeView))
        self.homeBtn.grid(pady=20,row=0,column=0,sticky=tk.W)
        self.logoutBtn = tk.Button(frame, text="Logout",justify=tk.LEFT,relief=tk.SOLID,width=8,font=("bold",13),bg='#158aff',bd=0,fg='white', command= lambda: self.logout( self.paymentsLabel,self.backBtn, self.homeBtn,self.logoutBtn,self.treeView))
        self.logoutBtn.grid(pady=10,row=0,column=3,sticky=tk.E)
        self.paymentsLabel = tk.Label(frame, text="Payments",font=("Times", "24", "bold"),fg='Blue')
        self.paymentsLabel.grid(pady=20,row=1,columnspan=3)
        self.treeView = ttk.Treeview(frame,height=30)
        self.treeView.grid(row=2,columnspan=4)


    def destroyRegisteredUserSuccefullyLable(self):
        self.homeBtn.destroy()
        self.RegisteredUserSuccefully.destroy()
        self.Home()
    
    def crossLogout(self):
        print('Cross:')
        self.backBtn.destroy()
        self.homeBtn.destroy()
        self.crossBtn.destroy()
        self.logoutBtn.destroy()
        self.rawColumn.destroy()
        self.enterStudentDataLabel.destroy()
        self.userLabel.destroy()
        self.userNameEntry.delete(0,tk.END)
        self.userNameEntry.destroy()
        self.semesterDropMenuLable.destroy()
        self.semesterDropMenu.destroy()
        self.fistNameLabel.destroy()
        self.firstNameEntry.delete(0,tk.END)
        self.firstNameEntry.destroy()
        self.lastNameLabel.destroy()
        self.lastNameEntry.delete(0,tk.END)
        self.lastNameEntry.destroy()
        self.fatherNameLabel.destroy()
        self.fatherNameEntry.delete(0,tk.END)
        self.fatherNameEntry.destroy()
        self.genderDropMenuLable.destroy()
        self.genderDropMenu.destroy()
        self.emailLabel.destroy()
        self.emailEntry.delete(0,tk.END)
        self.emailEntry.destroy()
        self.dobLabel.destroy()
        self.dobEntry.delete(0,tk.END)
        self.dobEntry.destroy()
        self.sMajorLabel.destroy()
        self.sMajorEntry.delete(0,tk.END)
        self.sMajorEntry.destroy()
        self.sLevelLabel.destroy()
        self.YOELabel.destroy()
        self.YOEEntry.delete(0,tk.END)
        self.YOEEntry.destroy()
        self.addressLabel.destroy()
        self.addressEntry.delete(0,tk.END)
        self.addressEntry.destroy()
        self.doneBtn.destroy()
        self.sLevelEntry.delete(0,tk.END)
        self.sLevelEntry.destroy()
        self.mainWindow()

    def enterStudentDataViewDestroy(self):
        self.backBtn.destroy()
        self.homeBtn.destroy()
        self.crossBtn.destroy()
        self.logoutBtn.destroy()
        self.rawColumn.destroy()
        self.enterStudentDataLabel.destroy()
        self.userLabel.destroy()
        self.userNameEntry.delete(0,tk.END)
        self.userNameEntry.destroy()
        self.semesterDropMenuLable.destroy()
        self.semesterDropMenu.destroy()
        self.fistNameLabel.destroy()
        self.firstNameEntry.delete(0,tk.END)
        self.firstNameEntry.destroy()
        self.lastNameLabel.destroy()
        self.lastNameEntry.delete(0,tk.END)
        self.lastNameEntry.destroy()
        self.fatherNameLabel.destroy()
        self.fatherNameEntry.delete(0,tk.END)
        self.fatherNameEntry.destroy()
        self.genderDropMenuLable.destroy()
        self.genderDropMenu.destroy()
        self.emailLabel.destroy()
        self.emailEntry.delete(0,tk.END)
        self.emailEntry.destroy()
        self.dobLabel.destroy()
        self.dobEntry.delete(0,tk.END)
        self.dobEntry.destroy()
        self.sMajorLabel.destroy()
        self.sMajorEntry.delete(0,tk.END)
        self.sMajorEntry.destroy()
        self.sLevelLabel.destroy()
        self.YOELabel.destroy()
        self.YOEEntry.delete(0,tk.END)
        self.YOEEntry.destroy()
        self.addressLabel.destroy()
        self.addressEntry.delete(0,tk.END)
        self.addressEntry.destroy()
        self.doneBtn.destroy()
        self.sLevelEntry.delete(0,tk.END)
        self.sLevelEntry.destroy()
        if flageLogedInDataEntry:
            self.homeBtn = tk.Button(frame, text="🏠",justify=tk.LEFT,relief=tk.SOLID,width=20,font=("bold",50),bd=0,fg='#158aff', command= self.destroyRegisteredUserSuccefullyLable)
            self.homeBtn.grid(pady=30)
        else:
            self.Home()


    def doneUserEntry(self):
	# semester VARCHAR(6) CHECK(semester IN('Fall','Spring','Summer')) NOT NULL,
	# gender VARCHAR(8) CHECK(gender IN('Male','Female','Bisexual')) NOT NULL,

        try:
            conn = odbc.connect(connection_string)
            print(conn)
        except Exception as e:
            print(e)
            print("Server did not connected so task is terminated: ")
            return False
        else:
            check_countFlage = True
            myCursor = conn.cursor()
                
            if userSignInUserNameGlobal == "":
                check_countFlage = False
                warn = "UserName can't be Empty!"
            elif self.fatherNameEntry.get() == "":
                check_countFlage = False
                warn = "Father Name can't be Empty!"
            elif self.firstNameEntry.get() == "":
                check_countFlage = False
                warn = "First name can't be empty!"
            elif self.lastNameEntry.get() =="":
                check_countFlage = False
                warn = "Last Name can't be empty!"
            elif self.emailEntry.get() == "":
                check_countFlage = False
                warn = "Email can't be empty!"
            elif self.dobEntry.get() =="":
                check_countFlage = False
                warn = "Date Of Birth can't be empty!"
            elif self.sMajorEntry.get() == "":
                check_countFlage = False
                warn = "Semester Major can't be empty!"
            elif self.sLevelEntry.get() =="":
                check_countFlage = False
                warn = "Semester Level can't be empty!"
            elif self.YOEEntry.get() == "":
                check_countFlage = False
                warn = "Year of Enrolled can't be empty!"
            elif self.addressEntry.get()=="":
                check_countFlage = False
                warn = "Address can't be empty!"
            elif self.clickedSemester.get()=="Choose":
                check_countFlage = False
                warn = "Semester can't be empty!\nPlease select semeset!"
            elif self.clickedGender.get()=="Choose":
                check_countFlage = False
                warn = "Semester can't be empty!\nPlease select semeset!"
            else:
                perameter = [userSignInUserNameGlobal,
                            self.clickedSemester.get(),
                            self.firstNameEntry.get(),
                            self.lastNameEntry.get(),
                            self.fatherNameEntry.get(),
                            self.clickedGender.get(),
                            self.emailEntry.get(),
                            self.dobEntry.get(),
                            self.sMajorEntry.get(),
                            self.sLevelEntry.get(),
                            int(self.YOEEntry.get()),
                            self.addressEntry.get()
                            ]
                for val in perameter:
                    print("val: ",val)
                query = "insert into Student Values(?,?,?,?,?,?,?,?,?,?,?,?)"
                myCursor.execute(query,perameter)
                myCursor.commit()
                myCursor.close()
                self.RegisteredUserSuccefully = tk.Label(frame,text='Data Entered Successfully',relief=tk.SOLID,font=("bold",15),bd=0,fg='#2CD34D')
                self.RegisteredUserSuccefully.grid(pady=10,ipady=5,row=1)
                global flageLogedInDataEntry
                flageLogedInDataEntry = True
                self.enterStudentDataViewDestroy()
            if not check_countFlage:
                messagebox.showerror('', warn)


    def enterStudentDataView(self):
        self.destroyFromHome()
        self.backBtn = tk.Button(frame, text="🔙",justify=tk.LEFT,relief=tk.SOLID,width=1,font=("bold",25),bd=0,fg='#158aff', command= self.enterStudentDataViewDestroy)
        self.backBtn.grid(pady=20,row=0,column=1,sticky=tk.W)
        self.homeBtn = tk.Button(frame, text="🏠",justify=tk.LEFT,relief=tk.SOLID,width=1,font=("bold",25),bd=0,fg='#158aff', command= self.enterStudentDataViewDestroy)
        self.homeBtn.grid(pady=20,row=0,column=0,sticky=tk.W)
        self.crossBtn = tk.Button(frame, text="❌",justify=tk.LEFT,relief=tk.SOLID,width=1,font=("bold",20),bd=0,fg='#158aff', command= self.enterStudentDataViewDestroy)
        self.crossBtn.grid(pady=20,row=0,column=2,sticky=tk.W)
        self.logoutBtn = tk.Button(frame, text="Logout",justify=tk.LEFT,relief=tk.SOLID,width=8,font=("bold",13),bg='#158aff',bd=0,fg='white', command=self.crossLogout)
        self.logoutBtn.grid(pady=10,row=0,column=4,sticky=tk.E)
        self.rawColumn = tk.Label(frame, text="",width=12)
        self.rawColumn.grid(pady=20,row=0,column=3)
        self.enterStudentDataLabel = tk.Label(frame, text="Enter Student Data",font=("Times", "24", "bold"),fg='Blue')
        self.enterStudentDataLabel.grid(pady=20,row=1,columnspan=6)
        

        
        self.userLabel = tk.Label(frame, width=15,text="username",font=("Times", "13","bold"))
        self.userLabel.grid(pady=10,ipady=5,row=2,column=0,sticky=tk.W)

        self.userNameEntry = tk.Entry(frame,relief=tk.SOLID,font=("Calibri", "13", "bold"),fg="grey",bd=0)
        self.userNameEntry.insert(0,userSignInUserNameGlobal)
        self.userNameEntry.grid(pady=10,ipady=5,row=2,column=1)
        #semester menu
        semester = ['Fall','Spring','Summer']
        
        # datatype of menu text
        self.clickedSemester = StringVar()
        
        # initial menu text
        self.clickedSemester.set( "Choose" )
        self.semesterDropMenuLable = tk.Label(frame, width=15,text="Semester",font=("Times", "13","bold"))
        self.semesterDropMenuLable.grid(pady=10,ipady=5,row=3,column=0,sticky=tk.W)
        self.semesterDropMenu = tk.OptionMenu(frame,self.clickedSemester,*semester)
        self.semesterDropMenu.grid(pady=10,ipady=5,row=3,column=1,sticky=tk.W)

        self.fistNameLabel = tk.Label(frame, width=15,text="First Name",font=("Times", "13","bold"))
        self.fistNameLabel.grid(pady=10,ipady=5,row=4,column=0,sticky=tk.W)
        
        self.firstNameEntry = tk.Entry(frame,relief=tk.SOLID,font=("Calibri", "13", "bold"),fg="grey",bd=0)
        self.firstNameEntry.grid(pady=10,ipady=5,row=4,column=1)

        
        self.lastNameLabel = tk.Label(frame, width=15,text="Last Name",font=("Times", "13","bold"))
        self.lastNameLabel.grid(pady=10,ipady=5,row=5,column=0,sticky=tk.W)
        
        self.lastNameEntry = tk.Entry(frame,relief=tk.SOLID,font=("Calibri", "13", "bold"),fg="grey",bd=0)
        self.lastNameEntry.grid(pady=10,ipady=5,row=5,column=1)


        
        self.fatherNameLabel = tk.Label(frame, width=15,text="Father Name",font=("Times", "13","bold"))
        self.fatherNameLabel.grid(pady=10,ipady=5,row=6,column=0,sticky=tk.W)
        
        self.fatherNameEntry = tk.Entry(frame,relief=tk.SOLID,font=("Calibri", "13", "bold"),fg="grey",bd=0)
        self.fatherNameEntry.grid(pady=10,ipady=5,row=6,column=1)


        
        gender = ['Male','Female','Bisexual']
        
        # datatype of menu text
        self.clickedGender = StringVar()
        
        # initial menu text
        self.clickedGender.set( "Choose" )
        self.genderDropMenuLable = tk.Label(frame, width=15,text="Gender",font=("Times", "13","bold"))
        self.genderDropMenuLable.grid(pady=10,ipady=5,row=7,column=0,sticky=tk.W)
        self.genderDropMenu = tk.OptionMenu(frame,self.clickedGender,*gender)
        self.genderDropMenu.grid(pady=10,ipady=5,row=7,column=1,sticky=tk.W)

        
        
        self.emailLabel = tk.Label(frame, width=15,text="Email",font=("Times", "13","bold"))
        self.emailLabel.grid(pady=10,ipady=5,row=8,column=0,sticky=tk.W)
        
        self.emailEntry = tk.Entry(frame,relief=tk.SOLID,font=("Calibri", "13", "bold"),fg="grey",bd=0)
        self.emailEntry.grid(pady=10,ipady=5,row=8,column=1)

        
        self.dobLabel = tk.Label(frame, width=30,text="Date Of Birth(YYYY-MM-DD)",font=("Times", "13","bold"))
        self.dobLabel.grid(pady=10,ipady=5,row=9,column=0)
        
        self.dobEntry = tk.Entry(frame,relief=tk.SOLID,font=("Calibri", "13", "bold"),fg="grey",bd=0)
        self.dobEntry.grid(pady=10,ipady=5,row=9,column=1,sticky=tk.W)
        self.dobEntry.insert(0,"YYYY-MM-DD")

        
        self.sMajorLabel = tk.Label(frame, width=15,text="Semester Major",font=("Times", "13","bold"))
        self.sMajorLabel.grid(pady=10,ipady=5,row=10,column=0,sticky=tk.W)
        
        self.sMajorEntry = tk.Entry(frame,relief=tk.SOLID,font=("Calibri", "13", "bold"),fg="grey",bd=0)
        self.sMajorEntry.grid(pady=10,ipady=5,row=10,column=1)

        
        self.sLevelLabel = tk.Label(frame, width=15,text="Semester Level",font=("Times", "13","bold"))
        self.sLevelLabel.grid(pady=10,ipady=5,row=11,column=0,sticky=tk.W)
        
        self.sLevelEntry = tk.Entry(frame,relief=tk.SOLID,font=("Calibri", "13", "bold"),fg="grey",bd=0)
        self.sLevelEntry.grid(pady=10,ipady=5,row=11,column=1)


        
        self.YOELabel = tk.Label(frame, width=15,text="Year Of Enrolled",font=("Times", "13","bold"))
        self.YOELabel.grid(pady=10,ipady=5,row=12,column=0,sticky=tk.W)
        
        self.YOEEntry = tk.Entry(frame,relief=tk.SOLID,font=("Calibri", "13", "bold"),fg="grey",bd=0)
        self.YOEEntry.grid(pady=10,ipady=5,row=12,column=1)


        
        self.addressLabel = tk.Label(frame, width=15,text="Address",font=("Times", "13","bold"))
        self.addressLabel.grid(pady=10,ipady=5,row=13,column=0,sticky=tk.W)
        
        self.addressEntry = tk.Entry(frame,relief=tk.SOLID,font=("Calibri", "13", "bold"),fg="grey",bd=0)
        self.addressEntry.grid(pady=10,ipady=5,row=13,column=1)

        self.doneBtn = tk.Button(frame, text="Done",relief=tk.SOLID,width=25,font=("bold",15),bd=0,bg='#158aff',fg='white', command=self.doneUserEntry)
        self.doneBtn.grid(pady=20,row=14,columnspan=4)        





    # def Try(self):
    #     # try:
    #     #     conn = odbc.connect(connection_string)
    #     #     print(conn)
    #     # except Exception as e:
    #     #     print(e)
    #     #     print("Server did not connected so task is terminated: ")
    #     #     return False
    #     # myCursor = conn.cursor()
    #     #self.destropyMainLablesAndButtons()
    #     self.welcomeLabel = tk.Label(frame, text="Welcome ",font=("Times", "24", "bold"),fg='Blue')
    #     self.welcomeLabel.grid(pady=20,row=0,columnspan=3)
    #     # myCursor.commit()
    #     # myCursor.close()
    #     self.logOutSignIn = tk.Button(frame, text="Log out",relief=tk.SOLID,width=16,font=("bold",15),bd=0,bg='#158aff',fg='white', command=self.logoutSignedIn)
    #     #//////////////////////////////////////////////
    #     #self.logOutSignIn.grid(pady=20,row=5, columnspan=3)
    #     self.attendance = tk.Button(frame, text="Attendance",relief=tk.SOLID,width=16,font=("bold",15),bd=0,bg='#158aff',fg='white',command=self.attendanceView)
    #     self.attendance.grid(pady=20,row=1,column=0)
    #     self.marks = tk.Button(frame, text="Marks",relief=tk.SOLID,width=16,font=("bold",15),bd=0,bg='#158aff',fg='white',command=self.marksView)
    #     self.marks.grid(pady=20,row=2,column=0)
    #     self.transcript = tk.Button(frame, text="Transcript",relief=tk.SOLID,width=16,font=("bold",15),bd=0,bg='#158aff',fg='white',command=self.transcriptView)
    #     self.transcript.grid(pady=20,row=3,column=0)
    #     self.cources = tk.Button(frame, text="Cources",relief=tk.SOLID,width=16,font=("bold",15),bd=0,bg='#158aff',fg='white', command=self.courseView)
    #     self.cources.grid(pady=20,row=1,column=2)
    #     self.timeTable = tk.Button(frame, text="Time Table",relief=tk.SOLID,width=16,font=("bold",15),bd=0,bg='#158aff',fg='white',command=self.timeTableView)
    #     self.timeTable.grid(pady=20,row=2,column=2)
    #     self.payments = tk.Button(frame, text="Payments",relief=tk.SOLID,width=16,font=("bold",15),bd=0,bg='#158aff',fg='white',command=self.paymentsView)
    #     self.payments.grid(pady=20,row=3,column=2)
    #     self.enterData = tk.Button(frame, text="Enter Student Data",relief=tk.SOLID,width=35,font=("bold",15),bd=0,bg='#FF4C3D',fg='white',command=self.enterStudentDataView)
    #     self.RegisteredUserSuccefully = tk.Label(frame,text='Enter Student Data First',relief=tk.SOLID,font=("bold",15),bd=0,fg='#FF4C3D')
    #     self.RegisteredUserSuccefully.grid(pady=10,ipady=5,row=6,columnspan=3)
    #     self.enterData.grid(pady=20,row=5,columnspan=3)
    #     self.logOutSignIn.grid(pady=20,row=7, columnspan=3)
        
    #     self.row = tk.Button(frame, text="",width=2,bd=0)
    #     self.row.grid(pady=20,row=8,column=1)
    #     # # myCursor = conn.cursor()
    #     # userNameParamerter = [userSignInUserNameGlobal]
    #     # query = "SELECT studentID FROM Student where studentID = ?"
    #     # myCursor.execute(query,userNameParamerter)
    #     # UserNameAll = myCursor.fetchall()
    #     # flageExist = False
    #     # for userName in UserNameAll:
    #     #     print("UserName: ",userName[0])
    #     #     if userName[0] == userSignInUserNameGlobal:
    #     #         print("Got it::")
    #     #         flageExist = True
    #     #         break
    #     # if not flageExist:
    #     #     self.enterData.grid(pady=20,row=5)
    #     #     self.RegisteredUserSuccefully.grid(pady=10,ipady=5,row=6,columnspan=2)
    #     #     self.logOutSignIn.grid(pady=20,row=7, columnspan=3)
    #     # else:
    #     #     self.logOutSignIn.grid(pady=20,row=5, columnspan=3)


windows = Windows()
windows.mainWindow()
# windows.Try() 864
# windows.enterStudentDataView()


root.mainloop()