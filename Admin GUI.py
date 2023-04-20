import getpass
import os
import winreg
import sys
from tkinter import *
from tkinter import messagebox
import pickle
import mysql.connector as mc
import math

username=getpass.getuser()
newpath = r'C:\Users\%s\Desktop\Python'%(username)
    
# Creates unique directory(folder) in the machine
def create_new_directory():
    if not os.path.exists(newpath):
        os.makedirs(newpath)
        
# Direct script start-up while windiows boot-up without .bat and .vbs file using key command=f'"{sys.executable}" "{script_path}"' for process kill
script_path=r'F:\SPi2\SLA\codeathon\Run\App_Restrictor_app.py'
command= f'"{sys.executable}" "{script_path}"'
sub_path=r'Software\Microsoft\Windows\CurrentVersion\Run'
key=winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_path, 0, winreg.KEY_SET_VALUE)
winreg.SetValueEx(key,'App_Restrictor', 0, winreg.REG_SZ, command)
winreg.CloseKey(key)

# Direct script start-up while windiows boot-up without .bat and .vbs file using key command=f'"{sys.executable}" "{script_path}"' for browser control
script_path=r'F:\SPi2\SLA\codeathon\Run\Browser_controller.py'
command= f'"{sys.executable}" "{script_path}"'
sub_path=r'Software\Microsoft\Windows\CurrentVersion\Run'
key=winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_path, 0, winreg.KEY_SET_VALUE)
winreg.SetValueEx(key,'Browser_controller', 0, winreg.REG_SZ, command)
winreg.CloseKey(key)

M_win=Tk()
M_win.title('Anti Procrastinator')
M_win.configure(bg='#7586cc')
M_win.geometry('350x450')
M_win.state('zoomed')

class ProjLabel:
    def __init__(self):
        global banner
        banner=Label(M_win, text='Anti Procrastinator', bg='#FF3399',font=('Polya',50, 'bold', 'italic')).pack(side='top', fill='x')
        
class Login:
    def __init__(self):        
        self.frame=Frame(M_win, relief='raised',bg='#65A8E1', borderwidth=2)        
        self.login=Label(self.frame, text='Login', bg='#FF3399', fg='#FFFFFF', font=('Arial',16)).grid(row=3, column=0, columnspan=2, sticky='news', pady=0)
        self.username=Label(self.frame, text='User name', bg='#65A8E1', fg='#FFFFFF', font=('Arial',10)).grid(row=4, column=0)
        self.username_entry=Entry(self.frame)
        self.username_entry.grid(row=4, column=1, padx=10, pady=20)
        self.password=Label(self.frame, text='Password', bg='#65A8E1', fg='#FFFFFF', font=('Arial',10)).grid(row=5, column=0)
        self.password_entry=Entry(self.frame, show='*')
        self.password_entry.grid(row=5, column=1, pady=5)
        self.login_buttom=Button(self.frame, text='Login', bg='#FF3399', fg='#FFFFFF', font=('Arial',9), cursor="hand2", command=self.EnterLogin).grid(row=6,column=0, columnspan=2, pady=20)
        self.frame.pack(pady=120, anchor='center')

    def EnterLogin(self):
        global e_empy_id
        e_empy_id=self.username_entry.get()
        e_username=self.username_entry.get()
        e_password=self.password_entry.get()
        employee_id=""
        global designation
        designation=""
        
        conn=mc.connect(host='localhost', user='root', password='KMDdharan@25', database="codeathon")
        cur=conn.cursor()
        cur.execute("SELECT emp_id, emp_name, pwd FROM emp_info WHERE emp_id = '{}'".format(e_username))
        record=cur.fetchall()
        cur.close()
        conn.close()
                
        for row in record:
            employee_id=row[0]
            global emp_username
            emp_username=row[1]
            password=row[2]               
        if e_username == employee_id and e_password == password:                    
            self.frame.destroy()
            Logout()
            Admin()                 
        else:
            self.username_entry.delete(0, 'end')
            self.password_entry.delete(0, 'end')
            messagebox.showerror(title='Error', message='Invalid username or password')

class Logout:
    def __init__(self):        
        self.Log_frame=Frame(M_win, bg='white', bd=2, height='5')
        self.label=Label(self.Log_frame, text=emp_username, font=('Times',14,'bold'), bg='white' ).grid(row=0, column=0, sticky=W)
        self.logout_btn=Button(self.Log_frame, text='Logout',bg='white', fg='#ff1717', font=('Arial',8,'bold'), cursor="hand2", command=self.logout).place(relx = 1, rely=0, x =-2, y = 2, anchor = NE)
        self.Log_frame.pack(fill='x', side='top')     
    def logout(self):
        for frm in M_win.winfo_children():
            frm.destroy()
        ProjLabel()
        Login()

class Admin:
    def __init__(self):        
        global EMP_frame
        EMP_frame=Frame(M_win, relief='raised',bg='#65A8E1')
        for i in range(0,6):
             EMP_frame.columnconfigure(i, weight=1)
        for i in range(0,8):
             EMP_frame.rowconfigure(i, weight=1)      
        enroll_btn=Button(EMP_frame, text='Create Initial Blacklist', font=('Cambria',20), bg='#ff80c0', fg='#000000', cursor="hand2", command=self.create).grid(row=2,column=2, padx=10, pady=5, sticky=W+E)
        self.leave_btn=Button(EMP_frame, text='Modify User Privileges', font=('Cambria',20), bg='#ff80c0', fg='#000000', cursor="hand2", command=self.update).grid(row=2,column=3, padx=10, pady=5, sticky=E+W)
        self.atten_btn=Button(EMP_frame, text='Browser Control Panel', font=('Cambria',20), bg='#ff80c0', fg='#000000', cursor="hand2", command=self.browser).grid(row=3,column=2, padx=10, pady=5, sticky=W+E)
        self.org_btn=Button(EMP_frame, text='Web Data Collection', font=('Cambria',20), bg='#ff80c0', fg='#000000', cursor="hand2").grid(row=3,column=3, padx=10, pady=5, sticky=E+W)
        EMP_frame.pack(fill='both', expand='yes')
        
    def create(self):
        EMP_frame.destroy()
        CreateBlacklist()   
    def update(self):
        EMP_frame.destroy()
        UpdatePrivilege()
    def browser(self):
        EMP_frame.destroy()
        BrowserControl()
    def pulling(self):
        EMP_frame.destroy()
        #DataPulling() # WIP

class CreateBlacklist:
    def __init__ (self):
        global create_frame
        create_frame=Frame(M_win, relief='raised',bg='#65A8E1')
        for i in range(0,20):
            create_frame.columnconfigure(i, weight=1)
            create_frame.rowconfigure(i, weight=1)
        home_btn=Button(create_frame, text='Home', bg='#e0801f', fg='white', font=('Arial',12,'bold'), cursor="hand2", command=self.home).grid(row=2, column=3)
        lbl_t=Label(create_frame, text='Create Blacklist', bg='#65A8E1', fg='#000000', font=('Arial',20, 'italic','bold')).grid(row=1, column=4, columnspan=4)
        emp_type_list=[]
        conn=mc.connect(host='localhost', user='root', password='KMDdharan@25', database="codeathon")
        cur=conn.cursor()
        cur.execute("SELECT DISTINCT emp_type FROM emp_info")
        record=cur.fetchall()
        cur.close()
        conn.close()        
        for row in record:
            emp_type_list.append(row[0])
        global team_name
        team_name=StringVar()
        lab1=Label(create_frame, text='Select Emp. Role', bg='#65A8E1', fg='black', font=('Arial',14,'bold')).grid(row=3, column=4, sticky=W)
        lab3=Label(create_frame, text='Enter Team Name', bg='#65A8E1', fg='black', font=('Arial',14,'bold')).grid(row=4, column=4, sticky=W)
        ent=Entry(create_frame, width=15, font=('Times',12), bg = '#dfdfdf',textvariable=team_name).grid(row=4, column=5, sticky=W)
        lab2=Label(create_frame, text='Select Applications', bg='#65A8E1', fg='black', font=('Arial',14,'bold')).grid(row=5, column=4, sticky=W)
        global emp_type
        emp_type=StringVar()
        menu=OptionMenu(create_frame, emp_type, *emp_type_list)
        menu['width']=10
        menu['height']=0
        menu.config(bg="#65A8E1", fg="white")
        menu.grid(row=3, column=5, sticky=W)        
        global total_installed_app
        total_installed_app=dict()
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall') as key:
            for i in range(winreg.QueryInfoKey(key)[0]):
                subkey_name = winreg.EnumKey(key, i)
                subkey = winreg.OpenKey(key, subkey_name)
                try:
                    app_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                    file_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                    if app_name not in total_installed_app.keys() and 'microsoft' not in app_name.lower():
                        total_installed_app[app_name]=file_location.lower()
                except FileNotFoundError:
                    pass
                subkey.Close()
        column_break=math.ceil(len(total_installed_app.keys())/2)
        global total_app
        total_app=[]
        for i in total_installed_app.keys():
            total_app.append((str(i),tkinter.IntVar()))
        k=5
        j=5
        global checkbutton
        for i, (app,var) in enumerate(total_app):
            if i<column_break:
                checkbutton = Checkbutton(create_frame, text=app, bg='#65A8E1', font=('Sitka Tex',12,'bold'), variable=var)
                checkbutton.grid(row=k, column=5, sticky=W)
                k+=1
            else:
                checkbutton = Checkbutton(create_frame, text=app, bg='#65A8E1', font=('Sitka Tex',12,'bold'), variable=var)
                checkbutton.grid(row=j, column=6, sticky=W)
                j+=1
        ent_btn=Button(create_frame, text='Enter', bg='#00a800', fg='black', font=('Arial',12,'bold'), command=self.create_application_blacklist).grid(row=k+1, column=6)
        create_frame.pack(fill='both', expand='yes')
        
    def create_application_blacklist(self):
        i_team_name=team_name.get()
        emp_type_blacklist=dict()
        for i, (app,var) in enumerate(total_app):
            if var.get()==1:
                emp_type_blacklist[app.lower()]=total_installed_app.get(app)
        e_emp_type=emp_type.get()
        user_name=[]
        if e_emp_type != '' and i_team_name == '':
            conn=mc.connect(host='localhost', user='root', password='KMDdharan@25', database="codeathon")
            cur=conn.cursor()
            cur.execute("SELECT emp_id FROM emp_info WHERE emp_type = '%s'"% (e_emp_type))
            record=cur.fetchall()
            cur.close()
            conn.close()
            if len(record)!=0:
                for row in record:
                    user_name.append(row[0])
                for user in user_name:
                    filename=r'%s.pk'%(str(user))
                    with open(filename, "wb") as file:
                        pickle.dump(emp_type_blacklist, file)
                messagebox.showinfo('Create Blacklist', r'Blacklist has been created for %s category' % (e_emp_type))
                create_frame.destroy()
                CreateBlacklist()
            else:
                 messagebox.showinfo('Alert', 'Such employee type does not exit')
        elif e_emp_type == '' and i_team_name != '':
            conn=mc.connect(host='localhost', user='root', password='KMDdharan@25', database="codeathon")
            cur=conn.cursor()
            cur.execute("SELECT emp_id FROM emp_info WHERE emp_dept = '%s'"% (i_team_name))
            record=cur.fetchall()
            cur.close()
            conn.close()
            if len(record)!=0:
                for row in record:
                    user_name.append(row[0])
                for user in user_name:
                    filename=r'%s.pk'%(str(user))
                    with open(filename, "wb") as file:
                        pickle.dump(emp_type_blacklist, file)
                messagebox.showinfo('Create Blacklist', r'Blacklist has been created for %s team' % (i_team_name))
                create_frame.destroy()
                CreateBlacklist()
            else:
                messagebox.showinfo('Alert', 'Such team does not exit')
        elif e_emp_type != '' and i_team_name != '':
            conn=mc.connect(host='localhost', user='root', password='KMDdharan@25', database="codeathon")
            cur=conn.cursor()
            cur.execute("SELECT emp_id FROM emp_info WHERE emp_dept = '%s' and emp_type = '%s'" % (i_team_name, e_emp_type))
            record=cur.fetchall()
            cur.close()
            conn.close()
            if len(record)!=0:
                for row in record:
                    user_name.append(row[0])
                for user in user_name:
                    filename=r'%s.pk'%(str(user))
                    with open(filename, "wb") as file:
                        pickle.dump(emp_type_blacklist, file)
                messagebox.showinfo('Create Blacklist', r'Blacklist has been created for %s team where employee type is %s' % (i_team_name,  e_emp_type))
                create_frame.destroy()
                CreateBlacklist()
            else:
                messagebox.showinfo('Alert', 'Such given combination does not exit')                        
    def home(self):
        create_frame.destroy()
        Admin()        

class UpdatePrivilege:
    def __init__ (self):
        global update_frame
        update_frame=Frame(M_win, relief='raised',bg='#65A8E1')
        emp_list=[]
        conn=mc.connect(host='localhost', user='root', password='KMDdharan@25', database="codeathon")
        cur=conn.cursor()
        cur.execute("SELECT emp_id FROM emp_info")
        record=cur.fetchall()
        cur.close()
        conn.close()        
        for row in record:
            emp_list.append(row[0])
        for i in range(0,20):
            update_frame.columnconfigure(i, weight=1)
        for i in range(0,25):
            update_frame.rowconfigure(i, weight=1)
        lgl_t=Label(update_frame, text='Modify User Privileges', bg='#65A8E1', fg='#000000', font=('Arial',20, 'italic','bold')).grid(row=0, column=4)
        home_btn=Button(update_frame, text='Home', bg='#e0801f', fg='white', font=('Arial',12,'bold'), cursor="hand2", command=self.home).grid(row=1, column=1)
        lab1=Label(update_frame, text='Select Employee ID', bg='#65A8E1', fg='black', font=('Arial',14,'bold')).grid(row=3, column=2, sticky=W)
        global i_Employee_ID
        i_Employee_ID=StringVar()
        entry=Entry(update_frame, width=20, font=('Times',12), bg = '#dfdfdf',textvariable=i_Employee_ID).grid(row=3, column=3, sticky=W)
        ent_btn1=Button(update_frame, text='View List', bg='#65A8E1', fg='black', font=('Arial',12,'bold'), width=10, cursor="hand2", command=self.show_list).grid(row=3, column=4, sticky=W)
        update_frame.pack(fill='both', expand='yes')

    def home(self):
        update_frame.destroy()
        Admin()        
    def show_list(self):
        global checkbutton_b
        global checkbutton_w
        try:
            #checkbutton_b.destroy()
            #checkbutton_w.destroy()
            for child in update_frame.winfo_children():
                if isinstance(child, Button) and child.cget("text") == "Whitelist" or child.cget("text") == 'Blacklist':
                    child.destroy()
                elif isinstance(child, Checkbutton):
                    child.destroy()
        except:
            pass
        global sh_emp_id
        sh_emp_id=i_Employee_ID.get()
        if sh_emp_id != '': 
            global filename
            filename=r'%s.pk'%(sh_emp_id.lower())
            global emp_blacklist
            try:
                with open (filename, 'rb') as file:
                    emp_blacklist= pickle.load(file)
            except FileNotFoundError:
                emp_blacklist=dict()
            global whitelist_app
            whitelist_app=dict()
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall') as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    try:
                        app_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                        file_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                        if app_name.lower() not in emp_blacklist.keys() and 'microsoft' not in app_name.lower():                 
                            whitelist_app[app_name]=file_location.lower()
                    except FileNotFoundError:
                        pass
                    subkey.Close()
            #########
            extra_list={'Google Chrome':'c:\\program files\\google\\chrome\\application', 'Microsoft Edge':'c:\\program files (x86)\\microsoft\\edge\\application', 'AnyDesk':'c:\\program files (x86)\\anydesk', 'PyCharm Community Edition 2022.3.3':'C:\\jetbrains\\pycharm community edition 2022.3.3\\bin', 'Microsoft Visual Studio Code': 'c:\\visual studio\\microsoft vs code'}
            for i in extra_list.keys():
                if i.lower() not in emp_blacklist.keys():
                    whitelist_app[str(i)]=extra_list.get(i)            
            #############
            lab2=Label(update_frame, text='Blacklist Application', bg='#65A8E1', fg='black', font=('Arial',14,'bold')).grid(row=4, column=2, sticky=W)
            global black
            black=[]
            if len(emp_blacklist.keys())!= 0:
                for i in emp_blacklist.keys():
                    if i != 'allow predefined sites' and i != 'allow access on keyword' and i != 'forbidden word restriction':
                        black.append((str(i),tkinter.IntVar()))
            else:
                black.append(('Blacklist were null',tkinter.IntVar()))
            k=5
            for i, (app,var) in enumerate(black):
                if app != 'Blacklist were null':
                    checkbutton_b = Checkbutton(update_frame, text=app.capitalize(), bg='#65A8E1', font=('Sitka Tex',12,'bold'), variable=var)
                    checkbutton_b.grid(row=k, column=2, sticky=W)
                    k+=1
                else:
                    checkbutton_b = Checkbutton(update_frame, text=app, bg='#65A8E1', font=('Sitka Tex',12,'bold'), state="disabled")
                    checkbutton_b.grid(row=k, column=2, sticky=W)
               
            ent_btn2=Button(update_frame, text='Whitelist', bg='#00a800', fg='black', font=('Arial',12,'bold'), cursor="hand2", command=self.whitelist).grid(row=k+1, column=2, sticky=W)
            
            lab3=Label(update_frame, text='Whitelist Apllication', bg='#65A8E1', fg='black', font=('Arial',14,'bold')).grid(row=4, column=4, sticky=W)
            global white
            white=[]
            if len(whitelist_app.keys())!= 0:
                for i in whitelist_app.keys():
                    white.append((str(i),tkinter.IntVar()))
            else:
                white.append(('Whitelist were null',tkinter.IntVar()))
            line_break=math.ceil(len(whitelist_app.keys())/2)
            c1=5
            c2=5
            for i, (app,var) in enumerate(white):
                if app != 'Whitelist were null':
                    if i<9:
                        checkbutton_w = Checkbutton(update_frame, text=app, bg='#65A8E1', font=('Sitka Tex',12,'bold'), variable=var)
                        checkbutton_w.grid(row=c1, column=4, sticky=W)
                        c1+=1
                    else:
                        checkbutton_w = Checkbutton(update_frame, text=app, bg='#65A8E1', font=('Sitka Tex',12,'bold'), variable=var)
                        checkbutton_w.grid(row=c2, column=5, sticky=W)
                        c2+=1
                else:
                    checkbutton_w = Checkbutton(update_frame, text=app, bg='#65A8E1', font=('Sitka Tex',12,'bold'), state="disabled")
                    checkbutton_w.grid(row=c1, column=4, sticky=W)
    
            ent_btn3=Button(update_frame, text='Blacklist', bg='#fd1e2f', fg='black', font=('Arial',12,'bold'), cursor="hand2", command=self.blacklist).grid(row=c1+1, column=4)
        else:
            messagebox.showerror('Select', 'Select employee id')
                
    def whitelist(self):
        try:
            for i, (app,var) in enumerate(black):
                if var.get()==1:
                    emp_blacklist.pop(app.lower())
            with open (filename,'wb') as file:
                pickle.dump(emp_blacklist, file)
            messagebox.showinfo('Message', r'Application whitelisted for %s' % (sh_emp_id))
            update_frame.destroy()
            UpdatePrivilege()
        except:
            messagebox.showerror('Alert', 'No application found/selected from blacklist')               
    def blacklist(self):
        try:
            for i, (app,var) in enumerate(white):
                if var.get()==1:
                    emp_blacklist[app.lower()]=whitelist_app.get(app)
            with open (filename,'wb') as file:
                pickle.dump(emp_blacklist, file)
            messagebox.showinfo('Message', r'Application blacklisted for %s' % (sh_emp_id))
            update_frame.destroy()
            UpdatePrivilege()
        except:
            messagebox.showerror('Alert', 'No application found/selected from whitelist')

class BrowserControl:
    def __init__ (self):
        global browse_frame
        browse_frame=Frame(M_win, relief='raised',bg='#65A8E1')
        for i in range(0,20):
            browse_frame.columnconfigure(i, weight=1)
            browse_frame.rowconfigure(i, weight=1)
        lgl_t=Label(browse_frame, text='Browser Control Panel', bg='#65A8E1', fg='#000000', font=('Arial',20, 'italic','bold')).grid(row=0, column=4)
        home_btn=Button(browse_frame, text='Home', bg='#e0801f', fg='white', font=('Arial',12,'bold'), cursor="hand2", command=self.home).grid(row=1, column=1)
        ### Add ###
        lab_0=Label(browse_frame, text='Add/Update Privileges', bg='#65A8E1', fg='#cb0a5b', font=('Arial',14,'bold')).grid(row=1, column=3, sticky=W)
        lab1=Label(browse_frame, text='Employee ID', bg='#65A8E1', fg='black', font=('Arial',14,'bold')).grid(row=2, column=2, sticky=W)
        global i_Employee_ID
        i_Employee_ID=StringVar()
        entry1=Entry(browse_frame, width=20, font=('Times',12), bg = '#dfdfdf',textvariable=i_Employee_ID).grid(row=2, column=3, sticky=W)
        #lab_or=Label(browse_frame, text='or', bg='#65A8E1', fg='black', font=('Arial',14,'bold')).grid(row=3, column=2, columnspan=2)
        Lbl2=Label(browse_frame, text='Employee Group', bg='#65A8E1', fg='black', font=('Arial',14,'bold')).grid(row=4, column=2, sticky=W)
        global i_Employee_type
        i_Employee_type=StringVar()
        entry2=Entry(browse_frame, width=20, font=('Times',12), bg = '#797979',textvariable=i_Employee_type)
        entry2.configure(state = 'disabled')
        entry2.grid(row=4, column=3, sticky=W)
        Lbl2=Label(browse_frame, text='Search Engine', bg='#65A8E1', fg='black', font=('Arial',14,'bold')).grid(row=5, column=2, sticky=W)
        search_engine=['Google Chrome','Microsoft Edge']
        #search_engine=['None']
        global engine
        engine=StringVar()
        menu1=OptionMenu(browse_frame, engine, *search_engine)
        menu1['width']=19
        #menu1.configure(state="disabled")
        menu1.grid(row=5, column=3, sticky=W)
        Lbl3=Label(browse_frame, text='Access Category', bg='#65A8E1', fg='black', font=('Arial',14,'bold')).grid(row=6, column=2, sticky=W)
        access_catg=['Allow predefined sites','Allow access on keyword', 'Forbidden word restriction']
        global access
        access=StringVar()
        menu2=OptionMenu(browse_frame, access, *access_catg)
        menu2['width']=19
        menu2.grid(row=6, column=3, sticky=W)
        btn1=Button(browse_frame, text='Enter', bg='#65A8E1', fg='black', font=('Arial',12,'bold'), width=10, cursor="hand2", command=self.input).grid(row=7, column=3, sticky=W)
        browse_frame.pack(fill='both', expand='yes')
        
        ##### remove######
        lab_01=Label(browse_frame, text='Remove Category List', bg='#65A8E1', fg='#cb0a5b', font=('Arial',14,'bold')).grid(row=1, column=4)
        #lab11=Label(browse_frame, text='Employee ID', bg='#65A8E1', fg='black', font=('Arial',14,'bold')).grid(row=2, column=4, sticky=W)
        global r_Employee_ID
        r_Employee_ID=StringVar()
        global entry11
        entry11=Entry(browse_frame, width=20, font=('Times',12), bg = '#dfdfdf',textvariable=r_Employee_ID).grid(row=2, column=4)
        #lab_or1=Label(browse_frame, text='or', bg='#65A8E1', fg='black', font=('Arial',14,'bold')).grid(row=3, column=3, columnspan=3)
        #Lbl21=Label(browse_frame, text='Employee Group', bg='#65A8E1', fg='black', font=('Arial',14,'bold')).grid(row=4, column=4, sticky=W)
        global r_Employee_type
        r_Employee_type=StringVar()
        entry21=Entry(browse_frame, width=20, font=('Times',12), bg = '#dfdfdf',textvariable=r_Employee_type)
        entry21.configure(state = 'disabled')
        entry21.grid(row=4, column=4)
        #Lbl21=Label(browse_frame, text='Search Engine', bg='#65A8E1', fg='black', font=('Arial',14,'bold')).grid(row=5, column=4, sticky=W)
        search_engine1=['None']
        global engine1
        engine1=StringVar()
        menu11=OptionMenu(browse_frame, engine1, *search_engine1)
        menu11['width']=19
        menu11.configure(state="disabled")
        menu11.grid(row=5, column=4)
        #Lbl31=Label(browse_frame, text='Access Category', bg='#65A8E1', fg='black', font=('Arial',14,'bold')).grid(row=6, column=4, sticky=W)
        access_catg1=['Allow predefined sites','Allow access on keyword', 'Forbidden word restriction']
        global access1
        access1=StringVar()
        menu21=OptionMenu(browse_frame, access1, *access_catg1)
        menu21['width']=19
        menu21.grid(row=6, column=4)
        btn11=Button(browse_frame, text='Enter', bg='#65A8E1', fg='black', font=('Arial',12,'bold'), width=10, cursor="hand2", command=self.remove).grid(row=7, column=4)
        browse_frame.pack(fill='both', expand='yes')
        
        ### Modify ###
        lab_02=Label(browse_frame, text='Remove Elements Set', bg='#65A8E1', fg='#cb0a5b', font=('Arial',14,'bold')).grid(row=1, column=5, sticky=W)
        #lab12=Label(browse_frame, text='Employee ID', bg='#65A8E1', fg='black', font=('Arial',14,'bold')).grid(row=2, column=6, sticky=W)
        global m_Employee_ID
        m_Employee_ID=StringVar()
        entry12=Entry(browse_frame, width=20, font=('Times',12), bg = '#dfdfdf',textvariable=m_Employee_ID).grid(row=2, column=5, sticky=W)
        #lab_or1=Label(browse_frame, text='or', bg='#65A8E1', fg='black', font=('Arial',14,'bold')).grid(row=3, column=3, columnspan=3)
        #Lbl22=Label(browse_frame, text='Employee Group', bg='#65A8E1', fg='black', font=('Arial',14,'bold')).grid(row=4, column=6, sticky=W)
        global m_Employee_type
        m_Employee_type=StringVar()
        entry22=Entry(browse_frame, width=20, font=('Times',12), bg = '#dfdfdf',textvariable=m_Employee_type)
        entry22.configure(state = 'disabled')
        entry22.grid(row=4, column=5, sticky=W)
        #Lbl22=Label(browse_frame, text='Search Engine', bg='#65A8E1', fg='black', font=('Arial',14,'bold')).grid(row=5, column=6, sticky=W)
        search_engine2=['None']
        global engine2
        engine2=StringVar()
        menu12=OptionMenu(browse_frame, engine2, *search_engine2)
        menu12['width']=19
        menu12.configure(state="disabled")
        menu12.grid(row=5, column=5, sticky=W)
        #Lbl32=Label(browse_frame, text='Access Category', bg='#65A8E1', fg='black', font=('Arial',14,'bold')).grid(row=6, column=6, sticky=W)
        access_catg2=['Allow predefined sites','Allow access on keyword', 'Forbidden word restriction']
        global access2
        access2=StringVar()
        menu22=OptionMenu(browse_frame, access2, *access_catg2)
        menu22['width']=19
        menu22.grid(row=6, column=5, sticky=W)
        btn12=Button(browse_frame, text='Enter', bg='#65A8E1', fg='black', font=('Arial',12,'bold'), width=10, cursor="hand2", command=self.modify).grid(row=7, column=5, sticky=W)
        browse_frame.pack(fill='both', expand='yes')
        
    def home(self):
        browse_frame.destroy()
        Admin()
    def input(self):
        global emp_id
        emp_id=i_Employee_ID.get()
        #b_emp_type=i_Employee_type.get()
        b_app=engine.get()
        global b_access_type
        b_access_type=access.get()
        if emp_id != '' and b_app !='' and b_access_type != '':
            try:
                for child in browse_frame.winfo_children():
                    if isinstance(child, Button) and child.cget("text") == "Enter":
                        child.destroy()
                    elif isinstance(child, Entry):
                        child.destroy()
                    elif isinstance(child, OptionMenu):
                        child.destroy()
                    elif isinstance(child, Label) and child.cget("text") != "Browser Control Panel":
                        child.destroy()
            except:
                pass
            ### remove app from blacklist
            filename=r'%s.pk'%(emp_id.lower())
            try:
                with open (filename, 'rb')as file:
                    emp_blacklist= pickle.load(file)
                    try:
                        existing_list=emp_blacklist[b_access_type.lower()]
                    except:
                        existing_list=['<None>']
                    try:
                        emp_blacklist.pop(b_app.lower())
                        with open(filename, "wb") as file:                    
                            pickle.dump(emp_blacklist, file)
                    except:
                        pass       
            except:
                existing_list=['<None>']
            back_btn=Button(browse_frame, text='Back', bg='#8888ff', fg='white', font=('Arial',12,'bold'), cursor="hand2", command=self.back).grid(row=1, column=2)
            txt=r'Enter %s with comma separator'% (b_access_type.lower())
            lbl4=Label(browse_frame, text=txt, bg='#65A8E1', fg='black', font=('Arial',12)).grid(row=2, column=4)
            global txt_line
            txt_line=Text(browse_frame, width=50, height=10, bg='#dfdfdf')
            txt_line.grid(row=3, column=4)

            existing_text = ", ".join(existing_list)
            lbl41=Label(browse_frame, text='Existing List', bg='#65A8E1', fg='black', font=('Arial',12)).grid(row=2, column=6)
            txt1_line=Text(browse_frame, width=50, height=10, bg='#dfdfdf')
            txt1_line.insert('1.0', existing_text)
            txt1_line.grid(row=3, column=6)
            btn4=Button(browse_frame, text='Enter', bg='#65A8E1', fg='black', font=('Arial',12,'bold'), width=10, cursor="hand2", command=self.load).grid(row=4, column=4) # command
        else:
            messagebox.showerror('Alert','Input parameter missing')
    def load(self):
        input_str=txt_line.get(1.0, END)
        key_list=[x.strip() for x in input_str.split(",")]
        filename=r'%s.pk'%(emp_id.lower())
        key=b_access_type.lower()
        try:
            with open (filename, 'rb')as file:
                emp_blacklist= pickle.load(file)
                try:
                    old_list=emp_blacklist[key]
                    old_list.extend(key_list)
                    emp_blacklist[key]=old_list
                except:
                    emp_blacklist[key]=key_list
        except:
            emp_blacklist=dict()
            emp_blacklist[key]=key_list
        with open (filename, 'wb')as file:
            pickle.dump(emp_blacklist, file)
        txt_line.delete(1.0, END)
        messagebox.showinfo('Info','Permission successfully added')
        browse_frame.destroy()
        BrowserControl()
    def remove(self):
        global r_emp_id
        r_emp_id=r_Employee_ID.get()
        emp=r_emp_id.lower()
        global r_access_type
        r_access_type=access1.get()
        filename=r'%s.pk'%(emp)
        if r_emp_id !='' and r_access_type != '':
            try:
                with open (filename, 'rb')as file:
                    emp_blacklist= pickle.load(file)
                    try:
                        emp_blacklist.pop(r_access_type.lower())
                        with open (filename, 'wb') as file:
                            pickle.dump(emp_blacklist, file)
                        messagebox.showinfo('Remove alert', 'Access category removed')
                        browse_frame.destroy()
                        BrowserControl()
                    except:
                        messagebox.showinfo('Remove alert', 'Such access type not found')
            except:
                messagebox.showinfo('Remove alert', 'Privileges category not found for this employee')
        else:
            meaasgebox.showerror('Error', 'Provide necessary input')
    def modify(self):
        global m_emp_id
        m_emp_id=m_Employee_ID.get()
        global m_access_type
        m_access_type=access2.get()
        filename=r'%s.pk'%(m_emp_id.lower())
        if m_emp_id !='' and m_access_type != '':
            try:
                for child in browse_frame.winfo_children():
                    if isinstance(child, Button) and child.cget("text") == "Enter":
                        child.destroy()
                    elif isinstance(child, Entry):
                        child.destroy()
                    elif isinstance(child, OptionMenu):
                        child.destroy()
                    elif isinstance(child, Label) and child.cget("text") != "Browser Control Panel":
                        child.destroy()
            except:
                pass
            try:
                with open (filename, 'rb')as file:
                    emp_blacklist= pickle.load(file)
                    try:
                        m_old_list=emp_blacklist[m_access_type.lower()]
                    except:
                        m_old_list=['<None>']
            except:
               m_old_list=['<None>']
            back_btn=Button(browse_frame, text='Back', bg='#8888ff', fg='white', font=('Arial',12,'bold'), cursor="hand2", command=self.back).grid(row=1, column=2)
            txt=r'Enter %s with comma separator'% (m_access_type.lower())
            lbl4=Label(browse_frame, text=txt, bg='#65A8E1', fg='black', font=('Arial',12)).grid(row=2, column=4)
            global m_txt_line
            m_txt_line=Text(browse_frame, width=50, height=10, bg='#dfdfdf')
            m_txt_line.grid(row=3, column=4)
            new_text = ", ".join(m_old_list)
            lbl41=Label(browse_frame, text='Existing List', bg='#65A8E1', fg='black', font=('Arial',12)).grid(row=2, column=6)
            m_txt1_line=Text(browse_frame, width=50, height=10, bg='#dfdfdf')
            m_txt1_line.insert('1.0', new_text)
            m_txt1_line.grid(row=3, column=6)
            btn42=Button(browse_frame, text='Enter', bg='#65A8E1', fg='black', font=('Arial',12,'bold'), width=10, cursor="hand2", command=self.update).grid(row=4, column=4) # command
        else:
            messagebox.showerror('Error', 'Provide necessary input')
    def update (self):
        input_str=m_txt_line.get(1.0, END)
        key_list=[x.strip() for x in input_str.split(",")]
        filename=r'%s.pk'%(m_emp_id.lower())
        key=m_access_type.lower()
        try:
            with open (filename, 'rb')as file:
                emp_blacklist= pickle.load(file)
                try:
                    old_list=emp_blacklist[key]
                    new_list=[x for x in old_list if x not in key_list]
                    emp_blacklist[key]=new_list
                except:
                    emp_blacklist[key]=key_list
        except:
            emp_blacklist=dict()
            emp_blacklist[key]=key_list
        with open (filename, 'wb')as file:
            pickle.dump(emp_blacklist, file)
        m_txt_line.delete(1.0, END)
        messagebox.showinfo('Info','Elements successfully removed')
        browse_frame.destroy()
        BrowserControl()
    def back(self):
        browse_frame.destroy()
        BrowserControl()
            
ProjLabel()
Login()
M_win.mainloop()
