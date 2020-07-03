from tkinter import *
from sqlite3 import *
import requests as r
from tkinter.ttk import Progressbar
from tkinter import messagebox
import bs4
import re
import webbrowser
class Mygui():
    
    def __init__(self):
        #database
        self.con=connect("user.db")
        self.c=self.con.cursor()
        try:
            self.c.execute("create table data(name varchar(500),price varchar(50),ptag float,site varchar(50))")
            self.c.execute("create table users(name varchar(20) UNIQUE,password varchar(20),email varchar(50))")
        except:
            pass
        #main screen
        scr=Tk(className="Scrapper")
        p=PhotoImage(file="minion.png")
        l=Label(scr,image=p)
        l.grid(row=0,column=0)
        p2=PhotoImage(file="pjimage2.png")
        l2=Label(scr,image=p2)
        l2.place(x=800,y=100)
        lab=Label(scr,text="LOGIN Page",font=("Script MT",30,"bold"))
        lab.place(x=250,y=40)
        u=Label(scr,text="User Name",font=("times",20,"underline"))
        u.place(x=100,y=250)
        pa=Label(scr,text="Password",font=("times",20,"underline"))
        pa.place(x=100,y=300)
        user=Entry(scr,font=("times",20,"bold"))
        user.place(x=300,y=250)
        pas=Entry(scr,font=("times",20,"bold"),show="*")
        pas.place(x=300,y=300)
        b=Button(scr,text="Login",font=("times",20,"italic"),command=lambda :self.login(scr,user.get(),pas.get()))
        b.place(x=100,y=350)
        b1=Button(scr,text="Register",font=("times",20,"italic"),command=lambda :self.registerpage(scr))
        b1.place(x=300,y=350)
        scr.mainloop()
    def login(self,ui,username,password):
        if len(username) and len(password):
            x=self.c.execute("select count(*) from users where name=%r and password=%r"%(username,password))
            if list(x)[0][0]!=0:
                ui.destroy()
                self.screen()
            else:
                messagebox.showinfo("Scrapper login","incorrect credentials")
        else:
            messagebox.showinfo("Scrapper login","please enter user name and password")
    def logout(self,scr):
        scr.destroy()
        Mygui()
            
    def registerpage(self,ui):
        ui.destroy()
        scr=Tk(className="Scrapper")
        p=PhotoImage(file="minion.png")
        l=Label(scr,image=p)
        l.grid(row=0,column=0)
        lab=Label(scr,text="Register Page",font=("times",30,"underline"))
        lab.place(x=250,y=40)
        u=Label(scr,text="User Name",font=("times",20,"underline"))
        u.place(x=100,y=200)
        pa=Label(scr,text="Password",font=("times",20,"underline"))
        pa.place(x=100,y=250)
        pa1=Label(scr,text="Retype Password",font=("times",20,"underline"))
        pa1.place(x=100,y=300)
        el=Label(scr,text="email",font=("times",20,"underline"))
        el.place(x=100,y=350)
        user=Entry(scr,font=("times",20,"bold"))
        user.place(x=300,y=200)
        pas=Entry(scr,font=("times",20,"bold"),show="*")
        pas.place(x=300,y=250)
        pas1=Entry(scr,font=("times",20,"bold"),show="*")
        pas1.place(x=300,y=300)
        email=Entry(scr,font=("times",20,"bold"))
        email.place(x=300,y=350)
        b1=Button(scr,text="Register",font=("times",20,"italic"),command=lambda :self.register(scr,user.get(),pas.get(),pas1.get(),email.get()))
        b1.place(x=300,y=400)
        scr.mainloop()
    def register(self,ui,n,pass1,pass2,email):
        if len(n) and len(pass1) and len(pass2) and len(email):
            if pass1==pass2:
                if re.search(r"\w+@+\w+.+\w",email):
                    try:
                        self.c.execute("insert into users values(%r,%r,%r)"%(n,pass1,email))
                        self.con.commit()
                    except:
                        messagebox.showinfo("Scrapper login","username all ready exists")
                    else:
                        ui.destroy()
                        self.__init__()
                else:
                    messagebox.showinfo("Scrapper login","invalid email")
            else:
                messagebox.showinfo("Scrapper login","incorrect password")
        else:
            messagebox.showinfo("Scrapper login","please all field")

    def Amazon(sf,sc1,sc2,sc3):
    
        headers={'User-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
        dt=r.request("get","https://www.amazon.in/s/field-keywords=%s %s"%(sc1,sc3),headers=headers)
        s=bs4.BeautifulSoup(dt.text,"html.parser")
        for i in s.findAll("div",{"class":'s-item-container'}):
            a=''
            b=''
            c=''
            d=''
            try:
                a1=i.find('h2').text
                if (sc3.casefold() not in a1) and (sc3.upper() not in a1):
                 continue
            except:
                pass
            try:
                b=i.find('span',{'class':'a-size-small a-color-secondary a-text-strike'}).text
            except:
                pass
            try:
                 c=i.find('span',{'class':'a-size-base a-color-price s-price a-text-bold'}).text
            except:
                 pass
            try:
                 d=i.find('span',{'class':'a-size-small a-color-price'}).text
            except:
                 pass
            if a1!='' and c!='' and d!='' :
                sf.c.execute("insert into data values(%r,%r,%f,%r)"%(a1,c,float(c.replace(',','')),"AMAZON"))
        sf.v.set(30)
    def flipkart(sf,sc1,sc2,sc3):
            headers={'User-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
            data=r.request('get',"https://www.flipkart.com/search?q=%s %s %s"%(sc1,sc2,sc3))
            s=bs4.BeautifulSoup(data.text,"html.parser")
            for i in s.findAll("div",{"class":"bhgxx2 col-12-12"}):
                a=i.find('div',{"class":"_3wU53n"})
                if a:
                    a=a.text
                    if (sc3.casefold() not in a) and (sc3.upper() not in a):
                     continue
                else:
                    a=i.find('a',{"class":"_2cLu-l"})
                    if a:
                     a=a.text
                     if ('j5' not in a) and ('J5' not in a):
                      continue
                b=i.find('div',{"class":"hGSR34 _2beYZw"})
                if b:
                    b=b.text
                c=""
                for j in i.findAll('li',{'class':'tVe95H'}):
                    m=j.text
                    if m:
                        c+=m+'\n'
                d=i.find('div',{"class":"_1vC4OE _2rQ-NK"})
                if d:
                    d=d.text.split('₹')[1]
                else:
                    d=i.find('a',{"class":"_1Vfi6u"})
                    if d:
                     d=d.text.split('₹')[1]   
                f=i.find('div',{"class":"VGWI6T"})
                if f:
                    f=f.text
                if a!=None and d !=None and f!=None :
                    sf.c.execute("insert into data values(%r,%r,%f,%r)"%(a,d,int(d.replace(',','')),"FLIPKART"))
            sf.v.set(70)       
    def snapdeal(sf,sc1,sc2,sc3):
           headers={'User-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
           dt1=r.request("get","https://www.snapdeal.com/search?keyword=%s %s %s"%(sc1,sc2,sc3))
           s1=bs4.BeautifulSoup(dt1.text,"html.parser")
           k=s1.find('div',{'class','product-row js-product-list centerCardAfterLoadWidgets dp-click-widgets'})
           for i in k.findAll("section",{"class":'js-section clearfix dp-widget '}):
               for j in i.findAll("div",{"class":'col-xs-6 favDp product-tuple-listing js-tuple '}):
                 m=""
                 price=""
                 disc=""
                 b1=j.find('div',{'class','product-tuple-description '})
                 b2=b1.find('div',{'class','product-desc-rating '})
                 b3=b2.find('a')
                 m=b3.find('p').text
                 if (sc3.casefold() not in m) and (sc3.upper() not in m) :
                  break
                 b4=b3.find('div',{'class':'product-price-row clearfix'})
                 b5=b4.find('div',{'class':'lfloat marR10'})
                 price=b5.find('span',{'class':'lfloat product-price'})
                 price=price.text
                 try:
                   b6=b4.find('div',{'class':'product-discount'})
                   disc=b6.find('span').text
                 except:
                     pass
                 if m!='' and price!='' and disc!='' and "Cover" not in m:
                     p=price.split()[1]
                     sf.c.execute("insert into data values(%r,%r,%f,%r)"%(m,p,int(p.replace(',','')),"SNAPDEAL"))
           sf.con.commit()
           sf.v.set(100)
    def screen(sf):
        scr=Tk(className="USER SCREEN")
        sf.v=IntVar()
        pk=PhotoImage(file="image4.png")
        l0=Label(scr,image=pk)
        l0.pack()
        l=Label(scr,font=("times",30,"bold italic"),text="Enter your product details")
        l.place(x=200,y=25)
        l1=Label(scr,font=("times",15,"italic"),text="Enter name")
        l1.place(x=200,y=80)
        e1=Entry(scr,bg='white',font=("times",20,"bold"))
        e1.place(x=350,y=80)
        l2=Label(scr,font=("times",15,"italic"),text="Enter category")
        l2.place(x=200,y=120)
        e2=Entry(scr,bg='white',font=("times",20,"bold"))
        e2.place(x=350,y=120)
        l3=Label(scr,font=("times",15,"italic"),text="Enter brand")
        l3.place(x=200,y=160)
        e3=Entry(scr,bg='white',font=("times",20,"bold"))
        e3.place(x=350,y=160)
        bt=Button(scr,activebackground="yellow",activeforeground="green",bd=10,bg="blue",fg="white",relief='sunken',state="active",underline=0,text="submit",command=lambda :sf.check(scr,e3.get(),e2.get(),e1.get()))
        bt.place(x=200,y=230)
        bt2=Button(scr,activebackground="yellow",activeforeground="green",bd=10,bg="blue",fg="white",relief='sunken',state="active",underline=0,text="logout",command=lambda :sf.logout(scr))
        bt2.place(x=300,y=230)
        sf.pr=Progressbar(scr,length=400,variable=sf.v,mode='determinate')
        sf.pr.place(x=200,y=300)
        sf.v.set(10)
        scr.mainloop()
    def check(sf,scr,x,y,z):
        if len(x)>0 and len(y)>0 and len(z)>0:
            sf.result(x,y,z,scr)            
        else:
            messagebox.showerror("SCRAPPER","enter all the fields")

    def result(sf,c,b,a,scr):
        sf.c.execute("delete from data")
        sf.con.commit()
        sf.Amazon(a,b,c)
        sf.flipkart(a,b,c)
        sf.snapdeal(a,b,c)
        sf.output(scr)

    def redirect(sf,name,site):
        if(site=='FLIPKART'):
            webbrowser.open_new(r"https://www.flipkart.com/search?q=%s"%(name))
        elif(site=='AMAZON'):
            webbrowser.open_new(r"https://www.amazon.in/s/field-keywords=%s"%(name))
        else:
            webbrowser.open_new(r"https://www.snapdeal.com/search?keyword=%s"%(name))
            
        
    def output(sf,scr):
        sf.v.set(100)
        sf.pr.destroy()
        l=Label(scr,text="BEST SEVEN OFFERS ARE",bg="blue",fg="white",font=('default',20,"underline"))
        l.pack(side=BOTTOM,fill=X)
        data=sf.c.execute('select * from data order by ptag')
        data=list(data)
        if(len(data)>7):
            data=data[:7]
            ty=300
            for i in range(7):
                tx=0
                l=Message(scr,text=data[i][0],bg='white',width=300,font=("times",15,"underline"))
                l.place(x=tx,y=ty)
                tx+=400
                l1=Label(scr,text=data[i][2],bg='white',font=("times",15,"italic"))
                l1.place(x=tx,y=ty)
                tx+=200
                l2=Label(scr,text=data[i][3],bg='white',fg='blue',font=("times",15,"bold"))
                l2.place(x=tx,y=ty)
                bt=Button(scr,text='click',command=lambda:sf.redirect(data[i][0],data[i][3]))
                bt.place(x=tx,y=ty)
                ty+=50
        else:
           ty=300
           for i in range(len(data)):
                tx=0
                l=Message(scr,text=data[i][0],bg='white',width=400,font=("times",15,"underline"))
                l.place(x=tx,y=ty)
                tx+=400
                l1=Label(scr,text=data[i][2],bg='white',font=("times",15,"italic"))
                l1.place(x=tx,y=ty)
                tx+=200
                l2=Label(scr,text=data[i][3],bg='white',fg='blue',font=("times",15,"bold"),cursor='hand2')
                l2.config(fg="blue")
                l2.place(x=tx,y=ty)
                tx+=300
                bt=Button(scr,text='click',command=lambda:sf.redirect(data[i][0],data[i][3]))
                bt.place(x=tx,y=ty)
                ty+=50
        
            
            
        

            
Mygui()

