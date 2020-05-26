import tkinter as tk
import matplotlib as plt
import numpy as np
import serial
import random
import threading
import queue
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

myDPI = 100
xVals = range(0,1000)
yVals = [0] * 1000
listening = 1
count = 0
news = queue.Queue()

window = tk.Tk()
fig = Figure(figsize=(800/myDPI, 300/myDPI), dpi=myDPI)
t = np.arange(0, 3, .01)
fig.add_subplot(111).plot(xVals, yVals)
axes = fig.gca()
axes.set_ylim(0,4095)

canvas = FigureCanvasTkAgg(fig, master=window)
ser = serial.Serial('COM3', 115200)  # open serial port

def updateChart():
    if news.empty(): return
    newVal = news.get()
    fig.clear()
    yVals.pop(0)
    yVals.append(newVal)
    fig.add_subplot(111).plot(xVals, yVals)
    axes = fig.gca()
    axes.set_ylim(0,4095)
    canvas.draw()

def listen():
    while listening:
        global count
        b = ser.read(2)
        count += 1
        i = int.from_bytes(b, "little")
        news.put(i)

def on_closing():
    global listening
    listening = 0
    print(count)
    window.destroy()

def main():
    window.geometry("800x600")
    window.title('ES ECG')
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)
    window.protocol("WM_DELETE_WINDOW", on_closing)
    listenThread = threading.Thread(target=listen).start()
    #window.mainloop()
    while listening:
        updateChart()
        window.update_idletasks()
        window.update()
    ser.close()

if __name__ == '__main__':
    main()

