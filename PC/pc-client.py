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


samplingRateOptions = ["25", "50", "100", "200"] 

myDPI = 100
xVals = range(0,500)
yVals = [0] * 500
listening = 1
news = queue.Queue()

window = tk.Tk()
fig = Figure(figsize=(800/myDPI, 300/myDPI), dpi=myDPI)
t = np.arange(0, 3, .01)
fig.add_subplot(111).plot(xVals, yVals)
axes = fig.gca()
axes.set_ylim(0,4095)

variable = tk.StringVar(window)
variable.set(samplingRateOptions[0])
bpmVar = tk.StringVar(window)
bpmVar.set("N/A")

canvas = FigureCanvasTkAgg(fig, master=window)
ser = serial.Serial('COM3', 115200)  # open serial port

count = 0

#for bpm
higher = 0
bSum = 0

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
    global bSum, higher, count
    while listening:
        b = ser.read(2)
        count += 1
        i = int.from_bytes(b, "little")
        if(i > 2500 and higher == 0):
            higher = 1
            bSum += 1
        if(i < 2500):
            higher = 0
        news.put(i)

def on_closing():
    global listening, count
    print(count)
    listening = 0
    window.destroy()

def startReceiving():
    global bSum
    bSum = 0
    samplingRate = str(int(int(variable.get()) / 25))
    ser.write(bytes(samplingRate, 'ascii'))
    ser.write(bytes('0', 'ascii'))

def displayBPM():
    bpmVar.set(str(bSum))
    


def main():
    window.geometry("800x600")
    window.title('ES ECG')
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=0)
    window.protocol("WM_DELETE_WINDOW", on_closing)

    startB = tk.Button(window, text ="Collect Data", command = startReceiving, pady=5)
    bpmB = tk.Button(window, text ="Get BPM", command = displayBPM, pady=5)
    samplingRateL = tk.Label(window, text="Sampling Rate:")
    bpmL = tk.Label(window, text="BPM:")
    bpmVal = tk.Label(window, textvariable=bpmVar)
    samplingList = tk.OptionMenu(window, variable, *samplingRateOptions)

    startB.pack()
    bpmB.pack()
    samplingRateL.pack()
    samplingList.pack()
    bpmL.pack()
    bpmVal.pack()

    startB.place(relx=0.8, rely=0.6)
    bpmB.place(relx=0.8, rely=0.7)
    samplingRateL.place(relx=0.05, rely=0.6)
    samplingList.place(relx=0.2, rely=0.6)
    bpmL.place(relx=0.4, rely=0.55)
    bpmVal.place(relx=0.5, rely=0.55)

    listenThread = threading.Thread(target=listen).start()
    while listening:
        updateChart()
        window.update_idletasks()
        window.update()
    ser.close()

if __name__ == '__main__':
    main()

