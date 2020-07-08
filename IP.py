#! python3
#-*-coding: utf-8 -*-
import sys
import os
import tkinter as tk
import socket
from ConfigParser import SafeConfigParser
import codecs
import tkMessageBox as messagebox  # Python 2
from tkinter.font import Font

root = tk.Tk()

ip = tk.StringVar()
pcname = tk.StringVar()


def mouseHover(win):
    width = 200
    height = 70
    w_top_right = (win.winfo_screenwidth()) - (width)
    win.geometry('{}x{}+{}+{}'.format(width, height, w_top_right, 0))
    win.attributes('-alpha',0.8)
    win.overrideredirect(1)
    ip.set(get_ip_address())

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
    #return socket.gethostname()
    return unicode(socket.gethostname(),'tis-620')

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(10)
        s.connect((readConf(), 80))
        return s.getsockname()[0]
    except socket.error:
        return "เรียก IP ใหม่"
        

def center(win):
    width = 200 #win.winfo_width()
    height = 70 #win.winfo_height()
    win.update_idletasks()
    w_top_right = (win.winfo_screenwidth()) - (width)    
    win.geometry('{}x{}+{}+{}'.format(width, height, w_top_right, 0))
    win.attributes('-alpha',0.8)
    win.overrideredirect(1)
    tk.Label(win,textvariable=pcname,font=12, fg="deepskyblue").pack()
    tk.Label(win,textvariable=ip,font=16, fg="red",cursor="hand2").pack()
    tk.Label(win,text="Copyright © จตุรภัทร ศิริบูรณ์",fg="dimgray").pack()


if __name__ == "__main__":
    center(root)
    ip.set(get_ip_address())
    pcname.set(getHost())
    root.bind("<Enter>", mouseHover(root))
    root.bind('<Button-1>', mouseHover(root))
    root.bind('<Double-1>', mouseHover(root))

    root.mainloop()
