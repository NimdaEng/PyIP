#! python3
#-*-coding: utf-8 -*-
import sys, os, socket
import tkinter as tk
from configparser import SafeConfigParser
import codecs
from tkinter import messagebox
from tkinter.font import Font

root = tk.Tk()

ip = tk.StringVar()
pcname = tk.StringVar()


def readConf():

    parser = SafeConfigParser()
    try:
        with codecs.open('config.ini', 'r', encoding='utf-8') as f:
            parser.readfp(f)
            return parser.get('gateway', 'ip')
    except IOError:
        parser.write(open('config.ini', 'w'))
        parser.add_section('gateway')
        parser.set('gateway','ip','192.168.1.1')
        with codecs.open('config.ini','w') as f:
            parser.write(f)
        messagebox.showinfo("เกิดข้อผิดพลาด", "หา config.ini ไม่พบ. ลองใหม่")
        return False

def getHost():
    return socket.gethostname()
    #return unicode(socket.gethostname(),'tis-620')

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        result = s.connect_ex((readConf(), 80))
        if result:
            return "เรียก IP ใหม่"
        else:
            return s.getsockname()[0] 
    except:
        return "เรียก IP ใหม่"
    finally:
        s.close()         
        

def center(win):
    width = 200 #win.winfo_width()
    height = 70 #win.winfo_height()
    win.update_idletasks()
    w_top_right = (win.winfo_screenwidth()) - (width)    
    win.geometry('{}x{}+{}+{}'.format(width, height, w_top_right, 0))
    win.attributes('-alpha',0.8)
    win.overrideredirect(1)
    win.bind("<Button-1>", set_ip)
    tk.Label(win,textvariable=pcname,font=12, fg="deepskyblue").pack()
    tk.Label(win,textvariable=ip,font=16, fg="red",cursor="hand2").pack()
    tk.Label(win,text="Copyright © จตุรภัทร ศิริบูรณ์",fg="dimgray").pack()
    

def set_ip(event):
    #ip.set(get_ip_address())
    #messagebox.showinfo("เกิดข้อผิดพลาด", get_ip_address())
    ip.set(get_ip_address())
    print(get_ip_address());

def callback():
    if messagebox.askokcancel("ห้ามปิดโปรแกรมนี้", get_ip_address(), default="cancel"): 
        ip.set(get_ip_address())
    else :        
        ip.set(get_ip_address())


if __name__ == "__main__":
    center(root)
    ip.set(get_ip_address())
    pcname.set(getHost())
    root.protocol("WM_DELETE_WINDOW", callback) # ป้องกันการ close windows
    root.bind("<Enter>", set_ip)
    root.update()
    root.mainloop()
