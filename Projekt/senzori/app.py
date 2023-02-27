from tkinter import *
from  tkinter import ttk
from tkinter import font
import tkinter as tk
import serial
import time
import threading
from time import sleep
import numpy as np
import random
from itertools import count
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import collections

port = "/dev/ttyACM0"
data  = []
buffer = [20,1010,500,100.00]
isAuto = True
counter10 = 0
temp_buffer = collections.deque(maxlen=10)
temp_buffer.append(0)
hum_buffer = collections.deque(maxlen=10)
hum_buffer.append(0)
press_buffer = collections.deque(maxlen=10)
press_buffer.append(0)
lux_buffer = collections.deque(maxlen=10)
lux_buffer.append(0)
last_temp = 0
last_hum = 0
pocetak = True



target_temperature = 22
target_pressure = 1013
heating_threshold = 15
cooling_threshold = 30
high_pressure_threshold = 1007
low_pressure_threshold = 1000

def conn():
    global data
    global buffer
    ser = serial.Serial(port=port, baudrate=115200, timeout=.1)
    time.sleep(1)
    b = ser.readline()        # read a byte string
    string_n = b.decode()  # decode byte string into Unicode  
    string = string_n.rstrip() # remove \n and \r
    data = string.split("x")          
    ser.close()
    x = len(data)
    #print(data)
    if x != 4:
        conn() 
    temp_buffer.append(data[0])
    hum_buffer.append(data[3])
    press_buffer.append(data[1])
    lux_buffer.append(data[2])
    
def values():
    global counter10
    global last_temp
    global pocetak
    global last_hum
    
    conn()

    if pocetak == True:
        last_temp = temp_buffer[-1]
        last_hum = hum_buffer[-1]
        pocetak = False   
    sec.delete(0, 'end')
    sec.insert(END, "Temperatura: ") 
    if counter10 == 10:
        sec.insert(END, temp_buffer[-1] )
        sec.insert(END, u" \N{DEGREE SIGN}C") 
        last_temp = temp_buffer[-1]  
    else:
        sec.insert(END, last_temp)
        sec.insert(END, u" \N{DEGREE SIGN}C")
    sec.insert(END, "\n")
    sec.insert(END, "Tlak: ") 
    sec.insert(END, press_buffer[-1] ) 
    sec.insert(END, " hPa") 
    sec.insert(END, "\n")
    sec.insert(END, "Svjetlost: ") 
    sec.insert(END, lux_buffer[-1]) 
    sec.insert(END, " lux") 
    sec.insert(END, "\n")
    sec.insert(END, "Vlažnost: ") 
    if counter10 == 10:
        sec.insert(END,hum_buffer[-1] ) 
        sec.insert(END, " %") 
        last_hum = hum_buffer[-1]
        counter10 = 0
    else:
        sec.insert(END, last_hum) 
        sec.insert(END, " %") 
    sec.insert(END, "\n")
    
    counter10 = counter10 + 1
    root.after(100, values)
    
def animate(i):
    yar.append(int(float(lux_buffer[-1])))
    xar.append(i)
    line.set_data(xar, yar)
    ax1.set_xlim(0, i+1)

def animate_temp(i):
    yar_temp.append(int(float(temp_buffer[-1])))
    xar_temp.append(i*10)
    line_temp.set_data(xar_temp, yar_temp)
    ax1_temp.set_xlim(0, i+1)

def animate_pre(i):
    yar_pre.append(int(float(press_buffer[-1])))
    xar_pre.append(i)
    line_pre.set_data(xar_pre, yar_pre)
    ax1_pre.set_xlim(0, i+1)

def animate_hum(i):
    yar_hum.append(int(float(hum_buffer[-1])))
    xar_hum.append(i*10)
    line_hum.set_data(xar_hum, yar_hum)
    ax1_hum.set_xlim(0, i+1)

def lights():
    if(float(lux_buffer[-1]) > 50):
        return "upaljeno"
    else:
        return "ugašeno"
def pressure():
    if(float(press_buffer[-1]) >= int(minTlak_spinbox.get())):
        return "loše"
    elif(float(press_buffer[-1]) >= int(maxTlak_spinbox.get())):
        return "dobro"
    elif(float(press_buffer[-1]) > 1010 and float(press_buffer[-1]) < 1019):
        return "neodređeno"
def humid():
    if(float(hum_buffer[-1]) < 40):
        return "uključeno"
    else:
        return "isključeno"
def dehumid():
    if(float(hum_buffer[-1]) > 60):
        return "uključeno"
    else:
        return "isključeno"
def rucno_auto(i):
    global isAuto
    if isAuto == True:
        return automatski(i)
    else:
        return rucno(i)
def prozorf():
    if(float(press_buffer[-1]) < 1010):
        return "zatvoreno"
    else:
        return "otvoreno"

def automatski(i):
    if i == 0:
        if(float(temp_buffer[-1]) <= int(zeljenaTmp_spinbox.get())):
            return "uključeno"
        else:
            return "isključeno"
    else :
        if(float(temp_buffer[-1]) >= int(zeljenaTmp_spinbox.get())):
            return "uključeno"
        else:
            return "isključeno"

def rucno(i):
    if i == 0:
        if(float(temp_buffer[-1]) <= int(grijanjeTmp_spinbox.get())):
            return "uključeno"
        else:
            return "isključeno"
    else:
        if(float(temp_buffer[-1]) >= int(hladenjeTmp_spinbox.get())):
            return "uključeno"
        else:
            return "isključeno"
def tablica():
    grijanje = Label(tbl_frame,text=rucno_auto(0), font=("Tahoma", 16), relief=SUNKEN)
    grijanje.grid(row=0, column=1)
    hladjenje = Label(tbl_frame, text=rucno_auto(1), font=("Tahoma", 16), relief=SUNKEN )
    hladjenje.grid(row=1, column=1)
    osvjetljenje = Label(tbl_frame, text=lights(), font=("Tahoma", 16), relief=SUNKEN )
    osvjetljenje.grid(row=2, column=1)
    ovlazivanje = Label(tbl_frame, text=humid(), font=("Tahoma", 16), relief=SUNKEN )
    ovlazivanje.grid(row=3, column=1)
    odvlazivanje = Label(tbl_frame, text=dehumid(), font=("Tahoma", 16), relief=SUNKEN )
    odvlazivanje.grid(row=4, column=1)
    prozor = Label(tbl_frame, text=prozorf(), font=("Tahoma", 16), relief=SUNKEN )
    prozor.grid(row=5, column = 1) 
    vrijeme = Label(tbl_frame, text=pressure(), font=("Tahoma", 16), relief=SUNKEN )
    vrijeme.grid(row=6, column=1) 
    root.after(10, tablica)

def setRucno():
    global isAuto
    if toggle_rucno.cget('bg') == 'red':
        toggle_rucno.config(bg='#90ee90')
        toggle_auto.config(bg='red')
        isAuto = False
    

def setAutomatski():
    global isAuto
    if toggle_auto.cget('bg') == 'red':
        toggle_auto.config(bg='#90ee90')
        toggle_rucno.config(bg='red')
        isAuto = True
    

root = Tk()
root.title('Pametni stan')
root.geometry('400x750+50+50')
root['bg'] = '#eeeee4'
xar = []
yar = []
xar_temp = []
yar_temp = []
xar_pre = []
yar_pre = []
xar_hum = []
yar_hum = []
var = StringVar(root)

newwindow = tk.Toplevel(root)
newwindow.geometry("1500x500+500+300")
newwindow['bg'] = 'black'


style.use('ggplot')
#plot_svjetlost
fig = plt.figure(figsize=(14, 4.5), dpi=50)
ax1 = fig.add_subplot(1, 1, 1)
ax1.set_ylim(0, 10000)
ax1.set_xlabel('Vrijeme, s')
ax1.set_ylabel('Svjetlost, lux')
line, = ax1.plot(xar, yar, 'r', marker='o')

#plot_temp

fig_temp = plt.figure(figsize=(14, 4.5), dpi=50)
ax1_temp = fig_temp.add_subplot(1, 1, 1)
ax1_temp.set_ylim(0, 50)
ax1_temp.set_xlabel('Vrijeme, s')
ax1_temp.set_ylabel('Temperatura, \N{DEGREE SIGN}C')
line_temp, = ax1_temp.plot(xar_temp, yar_temp, 'r', marker='o')

#plot_pre
fig_pre = plt.figure(figsize=(14, 4.5), dpi=50)
ax1_pre = fig_pre.add_subplot(1, 1, 1)
ax1_pre.set_ylim(900, 1200)
line_pre, = ax1_pre.plot(xar_pre, yar_pre, 'r', marker='o')
ax1_pre.set_xlabel('Vrijeme, s')
ax1_pre.set_ylabel('Tlak, pHa')

#plot_hum
fig_hum = plt.figure(figsize=(14, 4.5), dpi=50)
ax1_hum = fig_hum.add_subplot(1, 1, 1)
ax1_hum.set_ylim(0, 100)
line_hum, = ax1_hum.plot(xar_hum, yar_hum, 'r', marker='o')
ax1_hum.set_ylabel('Vlaga, %')
ax1_hum.set_xlabel('Vrijeme, s')


#Naslov
l = Label(root, text = "Vrijednosti parametara")
l.config(font = ("Courier", 17))
l.pack(pady=10)

#Izmjereni podaci
glavni = ttk.Label(
    root,
    text='',
    font=("Arial", 18),
    textvariable=var)
glavni.pack(ipadx=10, ipady=10, pady=10)
sec = Entry(root, textvariable = var)


l = Label(root, text = "Podešavanje")
l.config(font = ("Courier", 17))
l.pack(pady=10)

#definiranje frame-a za odabire
odabir = Frame(root)
odabir.pack()

# spinbox za odabir zeljene temp
var = IntVar()
var.set(target_temperature)
zeljenaTmp_label = Label(odabir, text="Odabir temperature(\N{DEGREE SIGN}C): ", font=("Arial", 10))
zeljenaTmp_label.grid(column = 0, row = 0)
zeljenaTmp_spinbox = \
            Spinbox(odabir, from_=0, to=40, textvariable=var, font=('Arial', 10))
zeljenaTmp_spinbox.grid(column = 1, row = 0)

# spinbox za zeljeni tlak
var = IntVar()
var.set(target_pressure)
zeljeniTlak_label = Label(odabir, text="Odabir tlaka(hPa): ", font=("Arial", 10))
zeljeniTlak_label.grid(column = 0, row = 1)
zeljeniTlak_spinbox = \
            Spinbox(odabir, from_=900, to=1100, textvariable=var, font=('Arial', 10))
zeljeniTlak_spinbox.grid(column = 1, row = 1)

# spinbox za temperaturu ukljucivanja grijanja
var = IntVar()
var.set(heating_threshold)
grijanjeTmp_label = Label(odabir, text="Uključi grijanje: ", font=("Arial", 10))
grijanjeTmp_label.grid(column = 0, row = 2)
grijanjeTmp_spinbox = \
            Spinbox(odabir, from_=-20, to=25, textvariable=var, font=('Arial', 10))
grijanjeTmp_spinbox.grid(column = 1, row = 2)

# spinbox za temperaturu iskljucivanja grijanja
var = IntVar()
var.set(cooling_threshold)
hladenjeTmp_label = Label(odabir, text="Uključi hlađenje: ", font=("Arial", 10))
hladenjeTmp_label.grid(column = 0, row = 3)
hladenjeTmp_spinbox = \
            Spinbox(odabir, from_=20, to=40, textvariable=var, font=('Arial', 10))
hladenjeTmp_spinbox.grid(column = 1, row = 3)

# spinbox za minimalni tlak
var = IntVar()
var.set(low_pressure_threshold)
minTlak_label = Label(odabir, text="Min. tlak: ", font=("Arial", 10))
minTlak_label.grid(column = 0, row = 4)
minTlak_spinbox = \
            Spinbox(odabir, from_=1000, to=1007, textvariable=var, font=('Arial', 10))
minTlak_spinbox.grid(column = 1, row = 4)

# spinbox za maksimalni tlak
var = IntVar()
var.set(high_pressure_threshold)
maxTlak_label = Label(odabir, text="Max. tlak: ", font=("Arial", 10))
maxTlak_label.grid(column = 0, row = 5)
maxTlak_spinbox = \
            Spinbox(odabir, from_=1007, to=1020, textvariable=var, font=('Arial', 10))
maxTlak_spinbox.grid(column = 1, row = 5)

#gumb
toggle_rucno = Button(odabir, bg='red',text="RUČNO", width=10, command=setRucno, font='Arial 10 bold')
toggle_rucno.grid(column = 0, row = 6)

toggle_auto = Button(odabir, bg='#90ee90', text="AUTOMATSKI",width=10, command = setAutomatski,font='Arial 10 bold')
toggle_auto.grid(column=1, row=6)

#tablica
tbl_frame = Frame(root)
tbl_frame.pack(ipadx=10, ipady=10, pady=15)

grijanje = Label(tbl_frame,text="GRIJANJE", font=("Tahoma", 17))
grijanje.grid(row=0, column=0)
hladjenje = Label(tbl_frame, text="HLAĐENJE", font=("Tahoma", 17))
hladjenje.grid(row=1, column=0)
osvjetljenje = Label(tbl_frame, text="RASVJETA", font=("Tahoma", 17))
osvjetljenje.grid(row=2, column=0)
ovlazivanje = Label(tbl_frame, text="OVLAŽIVANJE", font=("Tahoma", 17))
ovlazivanje.grid(row=3, column=0)
odvlazivanje = Label(tbl_frame, text="ODVLAŽIVANJE", font=("Tahoma", 17))
odvlazivanje.grid(row=4, column=0)
prozor = Label(tbl_frame, text="PROZOR/VRATA", font=("Tahoma", 17))
prozor.grid(row=5, column=0)
vrijeme = Label(tbl_frame, text="VRIJEME", font=("Tahoma", 17))
vrijeme.grid(row=6, column=0)
tablica()
values()

#svjetlost
l = Label(newwindow, text = "Jačina svjetlosti:", font=("Tahoma", 10, 'bold'), bg = "white")
l.grid(column=1, row=0)
plotcanvas = FigureCanvasTkAgg(fig, newwindow)
plotcanvas.get_tk_widget().grid(column=1, row=1)
ani = animation.FuncAnimation(fig, animate, interval=1000, blit=False)

#temp
l = Label(newwindow, text = "Prikaz temperature u vremenu:", font=("Tahoma", 10, 'bold'), bg = "white")
l.grid(column=1, row=2)
plotcanvas_temp = FigureCanvasTkAgg(fig_temp, newwindow)
plotcanvas_temp.get_tk_widget().grid(column=1, row=3)
ani_temp = animation.FuncAnimation(fig_temp, animate_temp, interval=1000, blit=False)

#pressure
l = Label(newwindow, text = "Prikaz tlaka u vremenu:", font=("Tahoma", 10, 'bold'), bg = "white")
l.grid(column=2, row=0)
plotcanvas_pre = FigureCanvasTkAgg(fig_pre, newwindow)
plotcanvas_pre.get_tk_widget().grid(column=2, row=1)
ani_pre = animation.FuncAnimation(fig_pre, animate_pre, interval=1000, blit=False)

#humidity
l = Label(newwindow, text = "Prikaz vlažnosti u vremenu:", font=("Tahoma", 10, 'bold'), bg = "white")
l.grid(column=2, row=2)
plotcanvas_hum = FigureCanvasTkAgg(fig_hum, newwindow)
plotcanvas_hum.get_tk_widget().grid(column=2, row=3)
ani_hum = animation.FuncAnimation(fig_hum, animate_hum, interval=1000, blit=False)


root.mainloop()
