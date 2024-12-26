from tkinter import Tk,Label,Frame,Entry,Button,messagebox,filedialog
from tkinter.ttk import Combobox
from tkintertable import TableCanvas, TableModel
import time
import random
import project_tables
import sqlite3
import gmail
from PIL import Image,ImageTk
import os
import shutil
import re

file=open("gmail_login.txt")
email,apppass=file.read().split(",")
file.close

win=Tk() #window create
win.state("zoomed") #full screen window
win.resizable(width=False, height=False)
win.configure(bg="#F0F0F0")

tittle=Label(win,text="Banking Automation",font=("arial",35,"bold"),bg="#002855",fg="#FFFFFF")
#tittle=Label(win,text="Banking Automation",font=("arial",40,"bold"),bg="#ADD8E6",fg="#000000")
tittle.pack()

date=time.strftime("%d-%B-%Y")
currdate=Label(win,text=date,font=("arial",20,"bold"),bg="#F0F0F0")
currdate.pack(pady=10) 
img=Image.open("logo.jpg").resize((200,120))
bitmap_img=ImageTk.PhotoImage(img,master=win)
logo_lbl=Label(win,image=bitmap_img)
logo_lbl.place(relx=0,rely=0) 
footer=Label(win,text="By Umair Ahmad @7827106729\nducat noida",font=("arial",20,"bold"),bg="#F0F0F0",fg="#1A2A42")
footer.pack(side="bottom")

def main_screen():
    frm=Frame(win,highlightbackground="black",highlightthickness=2)
    frm.configure(bg="#D3D3D3")
    frm.place(relx=0,rely=.13,relwidth=1,relheight=.79)

    code_cap=""
    for i in range(3):
        i = random.randint(65,90)
        c = chr(i)
        j = random.randint(0,9)
        code_cap = code_cap + c + str(j)

    def forgot_pass():
        frm.destroy()
        forgotpass_screen()

    def login():
        acn_type=cb_type.get()
        acno=e_acn.get()
        pwd=e_pass.get()
        user_cap=e_captcha.get()

        if acno=="" or pwd=="" or user_cap=="":
            messagebox.showerror(title="login",message="Empty fields are not allowed")
            return
        if acn_type=="admin" and acno=="0" and pwd=="admin" and code_cap==user_cap:
            if user_cap==code_cap:

                frm.destroy()
                welcome_admin_screen()
            else:
                messagebox.showerror(title="invalid",message="invalid captcha")
        elif acn_type=="user":
            if user_cap==code_cap:
                conobj=sqlite3.connect("bank.sqlite")
                curobj=conobj.cursor()
                curobj.execute("select * from users where users_acnno=? and users_pass=?",(acno,pwd)) 
                tup=curobj.fetchone()
                if tup==None:
                    messagebox.showerror("login","Invalid Acn/Pass")
                    return
                else:
                    global welcome_user,user_acno
                    welcome_user=tup[1]
                    user_acno=tup[0]
                    frm.destroy()
                    welcome_user_screen()
            else:
                messagebox.showerror("login","invalid captcha")
        else:
            messagebox.showerror(title="login",message="invalid acn or password")

    def refresh():
        cap=""
        for i in range(3):
            i = random.randint(65,90)
            c = chr(i)
            j = random.randint(0,9)
            cap = cap + c + str(j)

            


    lbl_type=Label(frm,text="ACN Type",font=("arial",20,"bold"),bg="#F5F5F5",fg="#333333")
    lbl_type.place(relx=.3,rely=.15)


    cb_type=Combobox(frm,values=["----select an acn type----","user","admin"],font=("arial",20,"bold"))
    cb_type.current(0)
    cb_type.place(relx=.45,rely=.15)

    lbl_acn=Label(frm,text="ACN No",font=("arial",20,"bold"),bg="#F5F5F5",fg="#333333")
    lbl_acn.place(relx=.3,rely=.25)

    e_acn=Entry(frm,font=("arial",20,"bold"),bd=5,bg="#FFFFFF",fg="#000000",highlightthickness=2,highlightbackground="#DCDCDC")
    e_acn.place(relx=.45,rely=.25)
    e_acn.focus()

    lbl_pass=Label(frm,text="Password",font=("arial",20,"bold"),bg="#F5F5F5",fg="#333333")
    lbl_pass.place(relx=.3,rely=.35)

    e_pass=Entry(frm,font=("arial",20,"bold"),bd=5,bg="#FFFFFF",fg="#000000",highlightthickness=2,highlightbackground="#DCDCDC",show="*")
    e_pass.place(relx=.45,rely=.35)


    def refresh():
        e_acn.delete(0,"end")
        e_pass.delete(0,"end")
        e_captcha.delete(0,"end")
        e_acn.focus()

    lbl_captcha=Label(frm,text=f"Captcha\t{code_cap}",font=("arial",20,"bold"),bg="#F5F5F5",fg="#333333")
    lbl_captcha.place(relx=.45,rely=.45)

    btn_refresh=Button(frm,text="Refresh",font=("arial",12,"bold"),bd=5,bg="#90EE90",fg="#000000",command=refresh)
    btn_refresh.place(relx=.6,rely=.45,relheight=.05,relwidth=.05 )

    lbl_captcha2=Label(frm,text="Enter Captcha",font=("arial",20,"bold"),bg="#F5F5F5",fg="#333333")
    lbl_captcha2.place(relx=.3,rely=.55)

    e_captcha=Entry(frm,font=("arial",20,"bold"),bd=5,bg="#FFFFFF",fg="#000000",highlightthickness=2,highlightbackground="#DCDCDC")
    e_captcha.place(relx=.45,rely=.55)

    btn_login=Button(frm,text="login",font=("arial",20,"bold"),bd=5,bg="#90EE90",fg="#000000",command=login)
    btn_login.place(relx=.47,rely=.75)

    btn_reset=Button(frm,text="reset",font=("arial",20,"bold"),bd=5,bg="#F08080",fg="#000000",command=refresh)
    btn_reset.place(relx=.58,rely=.75)

    btn_forgotpass=Button(frm,text="forgot Password",font=("arial",20,"bold"),bd=5,command=forgot_pass,bg="#17A2B8",fg="#FFFFFF")
    btn_forgotpass.place(relx=.45,rely=.87,relwidth=.21)

def forgotpass_screen():
    frm=Frame(win,highlightbackground="black",highlightthickness=2)
    frm.configure(bg="#D3D3D3")
    frm.place(relx=0,rely=.13,relwidth=1,relheight=.79)

    frm_tittle=Label(win,text="Password Recovery Screen",font=("arial",20,"bold"),fg="#333333")
    frm_tittle.pack(pady=50)

    def back():
        frm.destroy()
        main_screen()

    def reset():
        e_acn.delete(0,"end")
        e_email.delete(0,"end")
        e_mob.delete(0,"end")
        e_acn.focus()

    
    def forgotpass_db():
        uacno=e_acn.get()
        umob=e_mob.get()
        uemail=e_email.get()

        def is_email_vaild():
            email_pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9-.]+$"
            if re.match(email_pattern,e_email.get()):
                return True
            else:
                return False

        if is_email_vaild() is True:

            conobj=sqlite3.connect("bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select users_name,users_pass from users where users_acnno=? and users_email=? and users_mob=?",(uacno,uemail,umob)) 
            tup=curobj.fetchone()
            if tup==None:
                messagebox.showerror("Forgot pass","Invalid Details")
                return
            else:
                global upass
                uname=tup[0]
                upass=tup[1]
                #code to generate otp
                otp=random.randint(1000,9999)

            try:
                con=gmail.GMail(email,apppass)
                utext=f"""Hello,{uname},
                OTP to recover password is {otp}
            

                Thanks
                ABC Bank Corp
                """
                
                msg=gmail.Message(to=uemail,subject="OTP for password recovery",text=utext)
                con.send(msg)
                messagebox.showinfo("New User","Mail sent successfully")

                lbl_otp=Label(frm,text="OTP",font=("arial",20,"bold"),bg="#F5F5F5",fg="#333333")
                lbl_otp.place(relx=.35,rely=.7)

                e_otp=Entry(frm,font=("arial",20,"bold"),bd=5,bg="#FFFFFF",fg="#000000",highlightthickness=2,highlightbackground="#DCDCDC")
                e_otp.place(relx=.4,rely=.7)

                def verify_otp():
                    if otp==int(e_otp.get()):
                        messagebox.showinfo("forgot pass",f"Your Pass is:\t{upass}")
                    else:
                        messagebox.showerror("forgot pass",f"Invalid Otp")
                btn_otp=Button(frm,text="verify",font=("arial",20,"bold"),bd=5,bg="#90EE90",fg="#000000",command=verify_otp)
                btn_otp.place(relx=.6,rely=.7 )
                
            except:
                messagebox.showerror("Network Problem","Something went wrong with network")
        else:
            messagebox.showerror("invald","invalid email format")
                    
                         
    btn_back=Button(frm,text="back",font=("arial",20,"bold"),bd=5,command=back,bg="#007BFF",fg="#FFFFFF")
    btn_back.place(relx=0,rely=0)

    lbl_acn=Label(frm,text="ACN No",font=("arial",20,"bold"),bg="#F5F5F5",fg="#333333")
    lbl_acn.place(relx=.3,rely=.25)

    e_acn=Entry(frm,font=("arial",20,"bold"),bd=5,bg="#FFFFFF",fg="#000000",highlightthickness=2,highlightbackground="#DCDCDC")
    e_acn.place(relx=.45,rely=.25)
    e_acn.focus()

    lbl_mob=Label(frm,text="Mob",font=("arial",20,"bold"),bg="#F5F5F5",fg="#333333")
    lbl_mob.place(relx=.3,rely=.35)

    e_mob=Entry(frm,font=("arial",20,"bold"),bd=5,bg="#FFFFFF",fg="#000000",highlightthickness=2,highlightbackground="#DCDCDC")
    e_mob.place(relx=.45,rely=.35)

    lbl_email=Label(frm,text="Email",font=("arial",20,"bold"),bg="#F5F5F5",fg="#333333")
    lbl_email.place(relx=.3,rely=.45)

    e_email=Entry(frm,font=("arial",20,"bold"),bd=5,bg="#FFFFFF",fg="#000000",highlightthickness=2,highlightbackground="#DCDCDC")
    e_email.place(relx=.45,rely=.45)

    btn_submit=Button(frm,text="submit",font=("arial",20,"bold"),bd=5,bg="#90EE90",fg="#000000",command=forgotpass_db)
    btn_submit.place(relx=.48,rely=.6 )
   
    btn_reset=Button(frm,text="reset",font=("arial",20,"bold"),bd=5,bg="#F08080",fg="#000000",command=reset)
    btn_reset.place(relx=.58,rely=.6)

def welcome_admin_screen():
    frm=Frame(win,highlightbackground="black",highlightthickness=2)
    frm.configure(bg="#D3D3D3")
    frm.place(relx=0,rely=.13,relwidth=1,relheight=.79)

    frm2_tittle=Label(frm,text="Admin Home Screen",font=("arial",20,"bold"),fg="#333333")
    frm2_tittle.pack()    

    def logout():
        frm.destroy()
        main_screen()
    
    def newuser():
        frm.destroy
        newuser_screen()

    def deleteuser():
        frm.destroy
        deleteuser_screen()

    def viewuser():
        frm.destroy
        viewuser_screen()

    btn_logout=Button(frm,text="logout",font=("arial",20,"bold"),bd=5,command=logout,bg="#007BFF",fg="#FFFFFF")
    btn_logout.place(relx=.9,rely=0)

    btn_newuser=Button(frm,text="Open user acn",font=("arial",20,"bold"),bd=5,command=newuser,bg="#90EE90",fg="#000000")
    btn_newuser.place(relx=0,rely=.1,relwidth=.2)

    btn_deleteuser=Button(frm,text="Delete User",font=("arial",20,"bold"),bd=5,command=deleteuser,bg="#F08080",fg="#000000")
    btn_deleteuser.place(relx=0,rely=.3,relwidth=.2)

    btn_viewuser=Button(frm,text="View User",font=("arial",20,"bold"),bd=5,command=viewuser,bg="#F05680",fg="#000000")
    btn_viewuser.place(relx=0,rely=.5,relwidth=.2)

def newuser_screen():
    frm=Frame(win,highlightbackground="black",highlightthickness=2)
    frm.configure(bg="#D3D3D3")
    frm.place(relx=0,rely=.13,relwidth=1,relheight=.79)

    frm2_tittle=Label(frm,text="Open New Account Screen",font=("arial",20,"bold"),fg="#333333")
    frm2_tittle.pack()    

    def logout():
        frm.destroy()
        main_screen()
    
    def back():
        frm.destroy
        welcome_admin_screen()
     
    def reset():
        e_name.delete(0,"end")
        e_mob.delete(0,"end")
        e_email.delete(0,"end")
        e_adhar.delete(0,"end")

    def newuser_db():
        uname=e_name.get()
        umob=e_mob.get()
        umail=e_email.get()
        uadhar=e_adhar.get()
        ubal=0
        upass=""
        for i in range(3):
            i = random.randint(65,90)
            c = chr(i)
            j = random.randint(0,9)
            upass = upass + str(j) + c 

        conobj=sqlite3.connect("bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("insert into users(users_name,users_pass,users_mob,users_email,users_bal,users_adhar,users_opendate) values(?,?,?,?,?,?,?)",(uname,upass,umob,umail,ubal,uadhar,date))
        conobj.commit()
        conobj.close()
       
        conobj=sqlite3.connect("bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select max(users_acnno) from users")
        uacn=curobj.fetchone()[0]
        conobj.close()
        messagebox.showinfo("New User",f"ACN created with ACN:{uacn} & PASS:{upass}")
        try:
            con=gmail.GMail(email,apppass)
            utext=f"""Hello,{uname},
            Your account has been opened successfully with ABC Bank
            Your Account no is {uacn}
            Your Password is {upass}

            Kindly change your Password when you login to app


            Thanks
            ABC Bank Corp
            """
            msg=gmail.Message(to=umail,subject="Account opened successfully",text=utext)
            con.send(msg)
            messagebox.showinfo("New User","Mail sent successfully")

        except:
            messagebox.showerror("Network Problem","Something went wrong with network")
    btn_logout=Button(frm,text="logout",font=("arial",20,"bold"),bd=5,command=logout,bg="#007BFF",fg="#FFFFFF")
    btn_logout.place(relx=.9,rely=0)

    btn_back=Button(frm,text="back",font=("arial",20,"bold"),bd=5,command=back,bg="#007BFF",fg="#FFFFFF")
    btn_back.place(relx=0,rely=0)

    lbl_name=Label(frm,text="Name",font=("arial",20,"bold"),bg="#F5F5F5",fg="#333333")
    lbl_name.place(relx=.3,rely=.25)

    e_name=Entry(frm,font=("arial",20,"bold"),bd=5,bg="#FFFFFF",fg="#000000",highlightthickness=2,highlightbackground="#DCDCDC")
    e_name.place(relx=.45,rely=.25)
    e_name.focus()

    lbl_mob=Label(frm,text="Mob",font=("arial",20,"bold"),bg="#F5F5F5",fg="#333333")
    lbl_mob.place(relx=.3,rely=.35)

    e_mob=Entry(frm,font=("arial",20,"bold"),bd=5,bg="#FFFFFF",fg="#000000",highlightthickness=2,highlightbackground="#DCDCDC")
    e_mob.place(relx=.45,rely=.35)

    lbl_email=Label(frm,text="Email",font=("arial",20,"bold"),bg="#F5F5F5",fg="#333333")
    lbl_email.place(relx=.3,rely=.45)

    e_email=Entry(frm,font=("arial",20,"bold"),bd=5,bg="#FFFFFF",fg="#000000",highlightthickness=2,highlightbackground="#DCDCDC")
    e_email.place(relx=.45,rely=.45)

    lbl_adhar=Label(frm,text="Adhar no",font=("arial",20,"bold"),bg="#F5F5F5",fg="#333333")
    lbl_adhar.place(relx=.3,rely=.55)

    e_adhar=Entry(frm,font=("arial",20,"bold"),bd=5,bg="#FFFFFF",fg="#000000",highlightthickness=2,highlightbackground="#DCDCDC")
    e_adhar.place(relx=.45,rely=.55)

    btn_submit=Button(frm,text="submit",font=("arial",20,"bold"),bd=5,bg="#90EE90",fg="#000000",command=newuser_db)
    btn_submit.place(relx=.48,rely=.7 )
   
    btn_reset=Button(frm,text="reset",font=("arial",20,"bold"),bd=5,bg="#F08080",fg="#000000",command=reset)
    btn_reset.place(relx=.58,rely=.7)

def deleteuser_screen():
    frm=Frame(win,highlightbackground="black",highlightthickness=2)
    frm.configure(bg="#D3D3D3")
    frm.place(relx=0,rely=.13,relwidth=1,relheight=.79)

    frm2_tittle=Label(frm,text="Delete User Account Screen",font=("arial",20,"bold"),fg="#333333")
    frm2_tittle.pack()    

    def logout():
        frm.destroy()
        main_screen()
    
    def back():
        frm.destroy
        welcome_admin_screen()
    
    def reset():
        e_acn.delete(0,"end")
        e_adhar.delete(0,"end")

    def delete():
        try:
            uacn=int(e_acn.get())        #get the account number from entry 
            uadhar=e_adhar.get().strip()    #get the Aadhar from entry 
            #connect to the database
            conobj=sqlite3.connect("bank.sqlite")
            curobj=conobj.cursor()

            #check if the account and adhar exist
            curobj.execute("select * from users where users_acnno=? and users_adhar=?",(uacn,uadhar))
            user=curobj.fetchone()
            if user is not None:
                uname=user[1]
                umail=user[4]
                curobj.execute("delete from users where users_acnno=? and users_adhar=?",(uacn,uadhar))
                curobj.execute("delete from txn where txn_acno=?",(uacn,))   
                conobj.commit()
                messagebox.showinfo("Delete User","account deleted succesfully")
                try:
                    con=gmail.GMail(email,apppass)
                    utext=f"""Hello,{uname},
                    Your account has been deleted successfully with ABC Bank

                    Thanks
                    ABC Bank Corp
                    """
                    msg=gmail.Message(to=umail,subject="Account deleted successfully",text=utext)
                    con.send(msg)
                    messagebox.showinfo("User","Mail sent successfully")

                except:
                    messagebox.showerror("Network Problem","Something went wrong with network")
            else:
                messagebox.showerror("delete","Invalid ACN No or Adhar No")
            
        except Exception as e:
            messagebox.showerror("Erorr",f"An error occurred: {e}")
        finally:
            conobj.close()

     
    btn_logout=Button(frm,text="logout",font=("arial",20,"bold"),bd=5,command=logout,bg="#007BFF",fg="#FFFFFF")
    btn_logout.place(relx=.9,rely=0)

    btn_back=Button(frm,text="back",font=("arial",20,"bold"),bd=5,command=back,bg="#007BFF",fg="#FFFFFF")
    btn_back.place(relx=0,rely=0)

    lbl_acn=Label(frm,text="Account No",font=("arial",20,"bold"),bg="#F5F5F5",fg="#333333")
    lbl_acn.place(relx=.3,rely=.25)

    e_acn=Entry(frm,font=("arial",20,"bold"),bd=5,bg="#FFFFFF",fg="#000000",highlightthickness=2,highlightbackground="#DCDCDC")
    e_acn.place(relx=.45,rely=.25)

    lbl_adhar=Label(frm,text="Adhar no",font=("arial",20,"bold"),bg="#F5F5F5",fg="#333333")
    lbl_adhar.place(relx=.3,rely=.35)

    e_adhar=Entry(frm,font=("arial",20,"bold"),bd=5,bg="#FFFFFF",fg="#000000",highlightthickness=2,highlightbackground="#DCDCDC")
    e_adhar.place(relx=.45,rely=.35)

    btn_submit=Button(frm,text="submit",font=("arial",20,"bold"),bd=5,bg="#90EE90",fg="#000000",command=delete)
    btn_submit.place(relx=.48,rely=.5 )
   
    btn_reset=Button(frm,text="reset",font=("arial",20,"bold"),bd=5,bg="#F08080",fg="#000000",command=reset)
    btn_reset.place(relx=.58,rely=.5)

def viewuser_screen():
    frm=Frame(win,highlightbackground="black",highlightthickness=2)
    frm.configure(bg="#D3D3D3")
    frm.place(relx=0,rely=.13,relwidth=1,relheight=.79)

    frm2_tittle=Label(frm,text="View User Account Screen",font=("arial",20,"bold"),fg="#333333")
    frm2_tittle.pack()    

    def logout():
        frm.destroy()
        main_screen()
    
    def back():
        frm.destroy
        welcome_admin_screen()
    
    def view():
        uacn=e_acn.get()
        conobj=sqlite3.connect("bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select * from users where users_acnno=?",(uacn,))
        tup=curobj.fetchone()
        conobj.close()
        if tup == None:
            messagebox.showerror("view", "account does not exist")
            return

        lbl_acn=Label(frm,text="Acn No",font=("arial",20,"bold"),fg="#333333")
        lbl_acn.place(relx=.1,rely=.25)

        lbl_acn_val=Label(frm,text=tup[0],font=("arial",20,"bold"),fg="#336773")
        lbl_acn_val.place(relx=.2,rely=.25)

        lbl_name=Label(frm,text="Name",font=("arial",20,"bold"),fg="#333333")
        lbl_name.place(relx=.7,rely=.25)

        lbl_name_val=Label(frm,text=tup[1],font=("arial",20,"bold"),fg="#333333")
        lbl_name_val.place(relx=.83,rely=.25)
        
        lbl_mob=Label(frm,text="Mob No",font=("arial",20,"bold"),fg="#333333")
        lbl_mob.place(relx=.1,rely=.45)

        lbl_mob_val=Label(frm,text=tup[3],font=("arial",20,"bold"),fg="#333333")
        lbl_mob_val.place(relx=.2,rely=.45)

        lbl_adhar=Label(frm,text=
        "Adhar",font=("arial",20,"bold"),fg="#333333")
        lbl_adhar.place(relx=.7,rely=.45)

        lbl_adhar_val=Label(frm,text=tup[6],font=("arial",20,"bold"),fg="#333333")
        lbl_adhar_val.place(relx=.83,rely=.45)

        lbl_opendate=Label(frm,text="Open Date",font=("arial",20,"bold"),fg="#333333")
        lbl_opendate.place(relx=.1,rely=.65)

        lbl_opendate_val=Label(frm,text=tup[7],font=("arial",20,"bold"),fg="#333333")
        lbl_opendate_val.place(relx=.2,rely=.65)

        lbl_bal=Label(frm,text="Available Bal",font=("arial",20,"bold"),fg="#333333")
        lbl_bal.place(relx=.7,rely=.65)

        lbl_bal_val=Label(frm,text=tup[5],font=("arial",20,"bold"),fg="#333333")
        lbl_bal_val.place(relx=.83,rely=.65)
         
     
    btn_logout=Button(frm,text="logout",font=("arial",20,"bold"),bd=5,command=logout,bg="#007BFF",fg="#FFFFFF")
    btn_logout.place(relx=.9,rely=0)

    btn_back=Button(frm,text="back",font=("arial",20,"bold"),bd=5,command=back,bg="#007BFF",fg="#FFFFFF")
    btn_back.place(relx=0,rely=0)

    lbl_acn=Label(frm,text="Account no",font=("arial",20,"bold"),bg="#F5F5F5",fg="#333333")
    lbl_acn.place(relx=.25,rely=.15)

    e_acn=Entry(frm,font=("arial",20,"bold"),bd=5,bg="#FFFFFF",fg="#000000",highlightthickness=2,highlightbackground="#DCDCDC")
    e_acn.place(relx=.4,rely=.15)

    btn_search=Button(frm,text="search",font=("arial",20,"bold"),bd=5,bg="#90EE90",fg="#000000",command=view)
    btn_search.place(relx=.65,rely=.15 )

def welcome_user_screen():
    frm=Frame(win,highlightbackground="black",highlightthickness=2)
    frm.configure(bg="#D3D3D3")
    frm.place(relx=0,rely=.13,relwidth=1,relheight=.79)

    screen_title="USer Home Screen"
    frm_tittle=Label(frm,text=screen_title,font=("arial",20,"bold"),fg="#333333")
    frm_tittle.place(relx=.45,rely=.1)    

    lbl_wel=Label(frm,text=f"Welcome,{welcome_user}",font=("arial",20,"bold"),fg="#333333")
    lbl_wel.place(relx=0,rely=0)  

    def logout():
        frm.destroy()
        main_screen()

    def details_screen():
        screen_title="User Details Screen"
        frm_tittle.configure(text=screen_title)

        ifrm=Frame(frm,highlightbackground="black",highlightthickness=2)
        ifrm.configure(bg="#6493D3")
        ifrm.place(relx=.25,rely=.15,relwidth=.7,relheight=.7)

        conobj=sqlite3.connect("bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select * from users where users_acnno=?",(user_acno,))
        tup=curobj.fetchone()
        conobj.close()

        lbl_acn=Label(ifrm,text=f"Acn No",font=("arial",20,"bold"),fg="#333333")
        lbl_acn.place(relx=.05,rely=.15)

        lbl_acn_val=Label(ifrm,text=tup[0],font=("arial",20,"bold"),fg="#336773")
        lbl_acn_val.place(relx=.2,rely=.15)

        lbl_name=Label(ifrm,text="Name",font=("arial",20,"bold"),fg="#333333")
        lbl_name.place(relx=.6,rely=.15)

        lbl_name_val=Label(ifrm,text=tup[1],font=("arial",20,"bold"),fg="#333333")
        lbl_name_val.place(relx=.83,rely=.15)
        
        lbl_mob=Label(ifrm,text="Mob No",font=("arial",20,"bold"),fg="#333333")
        lbl_mob.place(relx=.05,rely=.35)

        lbl_mob_val=Label(ifrm,text=tup[3],font=("arial",20,"bold"),fg="#333333")
        lbl_mob_val.place(relx=.2,rely=.35)

        lbl_adhar=Label(ifrm,text=
        "Adhar",font=("arial",20,"bold"),fg="#333333")
        lbl_adhar.place(relx=.6,rely=.35)

        lbl_adhar_val=Label(ifrm,text=tup[6],font=("arial",20,"bold"),fg="#333333")
        lbl_adhar_val.place(relx=.83,rely=.35)

        lbl_opendate=Label(ifrm,text="Open Date",font=("arial",20,"bold"),fg="#333333")
        lbl_opendate.place(relx=.05,rely=.55)

        lbl_opendate_val=Label(ifrm,text=tup[7],font=("arial",20,"bold"),fg="#333333")
        lbl_opendate_val.place(relx=.2,rely=.55)

        lbl_bal=Label(ifrm,text="Available Bal",font=("arial",20,"bold"),fg="#333333")
        lbl_bal.place(relx=.6,rely=.55)

        lbl_bal_val=Label(ifrm,text=tup[5],font=("arial",20,"bold"),fg="#333333")
        lbl_bal_val.place(relx=.83,rely=.55)

    def deposit_screen():
        screen_title="deposit Screen"
        frm_tittle.configure(text=screen_title)
        def deposit():
            uamt=int(e_amt.get())
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("update users set users_bal=users_bal+? where users_acnno=?",(uamt,user_acno))
            conobj.commit()
            conobj.close()


            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select users_bal from users where users_acnno=?",(user_acno,))
            ubal=curobj.fetchone()[0]
            conobj.close()

            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("insert into txn(txn_acno,txn_type,txn_amt,txt_bal,txn_date)values(?,?,?,?,?)",(user_acno,"credit",uamt,ubal,date))
            conobj.commit()
            conobj.close()

            messagebox.showinfo("Deposit",f"{uamt}deposited,Updated Bal:{ubal}")

        ifrm=Frame(frm,highlightbackground="black",highlightthickness=2)
        ifrm.configure(bg="#6493D3")
        ifrm.place(relx=.25,rely=.15,relwidth=.7,relheight=.7)

        lbl_amt=Label(ifrm,text="Amount",font=("arial",20,"bold"),bg="#F5F5F5",fg="#333333")
        lbl_amt.place(relx=.25,rely=.25)

        e_amt=Entry(ifrm,font=("arial",20,"bold"),bd=5,bg="#FFFFFF",fg="#000000",highlightthickness=2,highlightbackground="#DCDCDC")
        e_amt.place(relx=.4,rely=.25)

        btn_submit=Button(ifrm,text="submit",font=("arial",20,"bold"),bd=5,bg="#90EE90",fg="#000000",command=deposit)
        btn_submit.place(relx=.6,rely=.4 )

    def withdraw_screen():
        screen_title="withdraw Screen"
        frm_tittle.configure(text=screen_title)

        ifrm=Frame(frm,highlightbackground="black",highlightthickness=2)
        ifrm.configure(bg="#6493D3")
        ifrm.place(relx=.25,rely=.15,relwidth=.7,relheight=.7)

        def withdraw():
            uamt=int(e_amt.get())
            conobj=sqlite3.connect(database="bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select users_bal from users where users_acnno=?",(user_acno,))
            ubal=curobj.fetchone()[0]
            conobj.close()

            if ubal>uamt:
                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                curobj.execute("update users set users_bal=users_bal-? where users_acnno=?",(uamt,user_acno))
                conobj.commit()
                conobj.close()

                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                curobj.execute("insert into txn(txn_acno,txn_type,txn_amt,txt_bal,txn_date)values(?,?,?,?,?)",(user_acno,"debit",uamt,ubal-uamt,date))
                conobj.commit()
                conobj.close()

                messagebox.showinfo("Withdraw",f"{uamt}Withdrawl,Updated Bal:{ubal-uamt}")
            else:
                messagebox.showerror("withdraw",f"Insufficient Bal:{ubal}")



        lbl_amt=Label(ifrm,text="Amount",font=("arial",20,"bold"),bg="#F5F5F5",fg="#333333")
        lbl_amt.place(relx=.25,rely=.25)

        e_amt=Entry(ifrm,font=("arial",20,"bold"),bd=5,bg="#FFFFFF",fg="#000000",highlightthickness=2,highlightbackground="#DCDCDC")
        e_amt.place(relx=.4,rely=.25)

        btn_submit=Button(ifrm,text="submit",font=("arial",20,"bold"),bd=5,bg="#90EE90",fg="#000000",command=withdraw)
        btn_submit.place(relx=.6,rely=.4 )

    def transfer_screen():
        screen_title="transfer Screen"
        frm_tittle.configure(text=screen_title)

        ifrm=Frame(frm,highlightbackground="black",highlightthickness=2)
        ifrm.configure(bg="#6493D3")
        ifrm.place(relx=.25,rely=.15,relwidth=.7,relheight=.7)

        def transfer():
            uamt=int(e_amt.get())
            utoacn=int(e_to.get())
            conobj=sqlite3.connect("bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("select * from users where users_acnno=?",(utoacn,)) 
            tup=curobj.fetchone()
            conobj.close()
            if tup==None:
                messagebox.showerror("Transfer","Invalid Acn number")
                return
            else:
                uamt=int(e_amt.get())
                conobj=sqlite3.connect(database="bank.sqlite")
                curobj=conobj.cursor()
                curobj.execute("select users_bal from users where users_acnno=?",(user_acno,))
                ubal=curobj.fetchone()[0]
                conobj.close()

                if ubal>uamt:
                    conobj=sqlite3.connect(database="bank.sqlite")
                    curobj=conobj.cursor()
                    curobj.execute("update users set users_bal=users_bal-? where users_acnno=?",(uamt,user_acno))
                    curobj.execute("update users set users_bal=users_bal+? where users_acnno=?",(uamt,utoacn))
                    conobj.commit()
                    conobj.close()

                    conobj=sqlite3.connect(database="bank.sqlite")
                    curobj=conobj.cursor()
                    curobj.execute("insert into txn(txn_acno,txn_type,txn_amt,txt_bal,txn_date)values(?,?,?,?,?)",(user_acno,"debit",uamt,ubal-uamt,date))
                    curobj.execute("insert into txn(txn_acno,txn_type,txn_amt,txt_bal,txn_date)values(?,?,?,?,?)",(utoacn,"crdeit",uamt,ubal+uamt,date))
                    conobj.commit()
                    conobj.close()

                    messagebox.showinfo("Transfer",f"{uamt}Transferred,Updated Bal:{ubal-uamt}")
                else:
                    messagebox.showerror("TRansfer",f"Insufficient Bal:{ubal}")




        lbl_to=Label(ifrm,text="To Acn No",font=("arial",20,"bold"),bg="#F5F5F5",fg="#333333")
        lbl_to.place(relx=.25,rely=.25)

        e_to=Entry(ifrm,font=("arial",20,"bold"),bd=5,bg="#FFFFFF",fg="#000000",highlightthickness=2,highlightbackground="#DCDCDC")
        e_to.place(relx=.4,rely=.25)

        lbl_amt=Label(ifrm,text="Amount",font=("arial",20,"bold"),bg="#F5F5F5",fg="#333333")
        lbl_amt.place(relx=.25,rely=.45)

        e_amt=Entry(ifrm,font=("arial",20,"bold"),bd=5,bg="#FFFFFF",fg="#000000",highlightthickness=2,highlightbackground="#DCDCDC")
        e_amt.place(relx=.4,rely=.45)

        btn_submit=Button(ifrm,text="submit",font=("arial",20,"bold"),bd=5,bg="#90EE90",fg="#000000",command=transfer)
        btn_submit.place(relx=.4,rely=.7)

    def update_screen():
        screen_title="Update Screen"
        frm_tittle.configure(text=screen_title)


        def update_db():
            upass=e_pass.get()
            umob=e_mob.get()
            uemail=e_email.get()
            conobj=sqlite3.connect("bank.sqlite")
            curobj=conobj.cursor()
            curobj.execute("update users set users_pass=?,users_mob=?,users_email=? where users_acnno=?",(upass,umob,uemail,user_acno))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("update Details","Updated")
        ifrm=Frame(frm,highlightbackground="black",highlightthickness=2)
        ifrm.configure(bg="#6493D3")
        ifrm.place(relx=.25,rely=.15,relwidth=.7,relheight=.7)

        lbl_pass=Label(ifrm,text="Pass",font=("arial",20,"bold"),bg="#F5F5F5",fg="#333333")
        lbl_pass.place(relx=.25,rely=.15)

        e_pass=Entry(ifrm,font=("arial",20,"bold"),bd=5,bg="#FFFFFF",fg="#000000",highlightthickness=2,highlightbackground="#DCDCDC")
        e_pass.place(relx=.35,rely=.15)

        lbl_mob=Label(ifrm,text="Mob",font=("arial",20,"bold"),bg="#F5F5F5",fg="#333333")
        lbl_mob.place(relx=.25,rely=.35)

        e_mob=Entry(ifrm,font=("arial",20,"bold"),bd=5,bg="#FFFFFF",fg="#000000",highlightthickness=2,highlightbackground="#DCDCDC")
        e_mob.place(relx=.35,rely=.35)

        lbl_email=Label(ifrm,text="Email",font=("arial",20,"bold"),bg="#F5F5F5",fg="#333333")
        lbl_email.place(relx=.25,rely=.55)

        e_email=Entry(ifrm,font=("arial",20,"bold"),bd=5,bg="#FFFFFF",fg="#000000",highlightthickness=2,highlightbackground="#DCDCDC")
        e_email.place(relx=.35,rely=.55)

        btn_submit=Button(ifrm,text="submit",font=("arial",20,"bold"),bd=5,bg="#90EE90",fg="#000000",command=update_db)
        btn_submit.place(relx=.4,rely=.75 )

        conobj=sqlite3.connect("bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select users_pass,users_mob,users_email from users where users_acnno=?",(user_acno,))
        tup=curobj.fetchone()
        conobj.close()

        e_pass.insert(0,tup[0])
        e_mob.insert(0,tup[1])
        e_email.insert(0,tup[2])

    def history_screen():
        screen_title="User transaction history Screen"
        frm_tittle.configure(text=screen_title)

        ifrm=Frame(frm,highlightbackground="black",highlightthickness=2)
        ifrm.configure(bg="#6493D3")
        ifrm.place(relx=.25,rely=.15,relwidth=.7,relheight=.7)

        data={}
        conobj=sqlite3.connect("bank.sqlite")
        curobj=conobj.cursor()
        curobj.execute("select * from txn where txn_acno=?",(user_acno,))
        tups=curobj.fetchall()
        i=1
        for tup in tups:
            data[str(i)]={"txn Amt":tup[3],"txn type":tup[2],"updated Bal":tup[4],"txn date":tup[5],"txn id":tup[0]}
            i+=1
        model=TableModel()
        model.importDict(data)
        table_frm=Frame(ifrm)
        table_frm.place(relx=.2,rely=.2)
        table=TableCanvas(table_frm, model=model,editable=False)
        table.show()

    def update_picture():
        img_path=filedialog.askopenfilename()
        shutil.copy(img_path,f"{user_acno}.png")
        

        pro_img=Image.open(f"{user_acno}.png").resize((220,160))
        pro_bitmap_img=ImageTk.PhotoImage(pro_img,master=frm)

        prolbl_img=Label(frm,image=pro_bitmap_img)
        prolbl_img.image=pro_bitmap_img
        prolbl_img.place(relx=.02,rely=.05) 
        
    btn_logout=Button(frm,text="logout",font=("arial",20,"bold"),bd=5,command=logout,bg="#007BFF",fg="#FFFFFF")
    btn_logout.place(relx=.92,rely=0)

    if os.path.exists(f"{user_acno}.png"):
        pro_img=Image.open(f"{user_acno}.png").resize((220,160))
    else:
        pro_img=Image.open("default.png").resize((220,160))
        
    pro_bitmap_img=ImageTk.PhotoImage(pro_img,master=frm)

    prolbl_img=Label(frm,image=pro_bitmap_img)
    prolbl_img.image=pro_bitmap_img
    prolbl_img.place(relx=.02,rely=.05) 

    btn_update_pro=Button(frm,text="Update pfp",font=("arial",15,),bd=5,bg="#007BFF",fg="#FFFFFF",width=15,command=update_picture)
    btn_update_pro.place(relx=.04,rely=.27)

    btn_details=Button(frm,text="Check details",font=("arial",20,"bold"),bd=5,command=details_screen,bg="#90EE90",fg="#000000")
    btn_details.place(relx=0,rely=.35,relwidth=.2)

    btn_deposit=Button(frm,text="Deposit",font=("arial",20,"bold"),bd=5,command=deposit_screen,bg="#F08080",fg="#000000")
    btn_deposit.place(relx=0,rely=.45,relwidth=.2)

    btn_withdrawl=Button(frm,text="withdrawl",font=("arial",20,"bold"),bd=5,command=withdraw_screen,bg="#F08080",fg="#000000")
    btn_withdrawl.place(relx=0,rely=.55,relwidth=.2)

    btn_update=Button(frm,text="update",font=("arial",20,"bold"),bd=5,command=update_screen,bg="#F08080",fg="#000000")
    btn_update.place(relx=0,rely=.65,relwidth=.2)

    btn_transfer=Button(frm,text="transfer",font=("arial",20,"bold"),bd=5,command=transfer_screen,bg="#F05680",fg="#000000")
    btn_transfer.place(relx=0,rely=.75,relwidth=.2)

    btn_history=Button(frm,text="Transaction history",font=("arial",20,"bold"),bd=5,command=history_screen,bg="#F05680",fg="#000000")
    btn_history.place(relx=0,rely=.85,relwidth=.2)

main_screen()
win.mainloop()  #window display
