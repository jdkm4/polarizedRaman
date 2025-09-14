from pylablib.devices import Thorlabs
import time
import tkinter as tk
import math

window = tk.Tk()
window.title("KIN Controller")
window.geometry("300x300")

def setKINStages():
    with Thorlabs.KinesisPiezoMotor("97251742") as stage:
        stage.set_default_channel(1)
        stage.setup_drive(velocity=1396)
        stage.move_to(int(float(stage1.get())*2*math.pi*10**6/(360*250)))
        stage.wait_move()
        stage.set_default_channel(2)
        stage.setup_drive(velocity=1396)
        stage.move_to(int(float(stage2.get())*2*math.pi*10**6/(360*250)))
        stage.wait_move()
        stage.set_default_channel(3)
        stage.setup_drive(velocity=1396)
        stage.move_to(int(float(stage3.get())*2*math.pi*10**6/(360*250)))
        stage.wait_move()
        stage.set_default_channel(4)
        stage.setup_drive(velocity=1396)
        stage.move_to(int(float(stage4.get())*2*math.pi*10**6/(360*250)))
        stage.wait_move()

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)


stage1Label = tk.Label(window, text="Stage 1 Angle:")
stage1Label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

stage1 = tk.Entry(window, width=10)
stage1.grid(row=0, column=1, padx=10, pady=10, sticky="w")

stage2Label = tk.Label(window, text="Stage 2 Angle:")
stage2Label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

stage2 = tk.Entry(window, width=10)
stage2.grid(row=1, column=1, padx=10, pady=10, sticky="w")

stage3Label = tk.Label(window, text="Stage 3 Angle:")
stage3Label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

stage3 = tk.Entry(window, width=10)
stage3.grid(row=2, column=1, padx=10, pady=10, sticky="w")

stage4Label = tk.Label(window, text="Stage 4 Angle:")
stage4Label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

stage4 = tk.Entry(window, width=10)
stage4.grid(row=3, column=1, padx=10, pady=10, sticky="w")

start_button = tk.Button(window, text="Start", command=setKINStages)
start_button.grid(row=4, column=0, columnspan=2, pady=20)

window.mainloop()
