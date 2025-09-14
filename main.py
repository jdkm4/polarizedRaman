from pylablib.devices import Thorlabs
import time
import tkinter as tk
import math

window = tk.Tk()
window.title("Piezo Motor Controller")
window.geometry("300x600")

def setStages():
    with Thorlabs.KinesisPiezoMotor("97251742") as stage:
        stage.set_default_channel(1)
        stage.setup_drive(velocity=1396)
        stage.move_to(int(float(stage1PDR.get())*2*math.pi*10**6/(360*250)))
        stage.wait_move()
        stage.set_default_channel(2)
        stage.setup_drive(velocity=1396)
        stage.move_to(int(float(stage2PDR.get())*2*math.pi*10**6/(360*250)))
        stage.wait_move()
        stage.set_default_channel(3)
        stage.setup_drive(velocity=1396)
        stage.move_to(int(float(stage3PDR.get())*2*math.pi*10**6/(360*250)))
        stage.wait_move()
        stage.set_default_channel(4)
        stage.setup_drive(velocity=1396)
        stage.move_to(int(float(stage4PDR.get())*2*math.pi*10**6/(360*250)))
        stage.wait_move()

    with Thorlabs.ElliptecMotor("COM3") as stage:
        stage.set_default_addr(1)
        stage.move_to(int(stage1ELL.get()))
        stage.set_default_addr(2)
        stage.move_to(int(stage2ELL.get()))
        stage.set_default_addr(3)
        stage.move_to(int(stage3ELL.get()))

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)

PDRLabel = tk.Label(window, text="PDR Devices:")
PDRLabel.grid(row=0, column=0, columnspan=2, pady=20)

stage1PDRLabel = tk.Label(window, text="Stage 1 Angle:")
stage1PDRLabel.grid(row=1, column=0, padx=10, pady=10, sticky="w")

stage1PDR = tk.Entry(window, width=10)
stage1PDR.grid(row=1, column=1, padx=10, pady=10, sticky="w")

stage2PDRLabel = tk.Label(window, text="Stage 2 Angle:")
stage2PDRLabel.grid(row=2, column=0, padx=10, pady=10, sticky="w")

stage2PDR = tk.Entry(window, width=10)
stage2PDR.grid(row=2, column=1, padx=10, pady=10, sticky="w")

stage3PDRLabel = tk.Label(window, text="Stage 3 Angle:")
stage3PDRLabel.grid(row=3, column=0, padx=10, pady=10, sticky="w")

stage3PDR = tk.Entry(window, width=10)
stage3PDR.grid(row=3, column=1, padx=10, pady=10, sticky="w")

stage4PDRLabel = tk.Label(window, text="Stage 4 Angle:")
stage4PDRLabel.grid(row=4, column=0, padx=10, pady=10, sticky="w")

stage4PDR = tk.Entry(window, width=10)
stage4PDR.grid(row=4, column=1, padx=10, pady=10, sticky="w")

ELLLabel = tk.Label(window, text="ELL14 Devices:")
ELLLabel.grid(row=5, column=0, columnspan=2, pady=20)

stage1ELLLabel = tk.Label(window, text="Stage 1 Angle:")
stage1ELLLabel.grid(row=6, column=0, padx=10, pady=10, sticky="w")

stage1ELL = tk.Entry(window, width=10)
stage1ELL.grid(row=6, column=1, padx=10, pady=10, sticky="w")

stage2ELLLabel = tk.Label(window, text="Stage 2 Angle:")
stage2ELLLabel.grid(row=7, column=0, padx=10, pady=10, sticky="w")

stage2ELL = tk.Entry(window, width=10)
stage2ELL.grid(row=7, column=1, padx=10, pady=10, sticky="w")

stage3ELLLabel = tk.Label(window, text="Stage 3 Angle:")
stage3ELLLabel.grid(row=8, column=0, padx=10, pady=10, sticky="w")

stage3ELL = tk.Entry(window, width=10)
stage3ELL.grid(row=8, column=1, padx=10, pady=10, sticky="w")

stage4ELLLabel = tk.Label(window, text="Stage 4 Angle:")
stage4ELLLabel.grid(row=9, column=0, padx=10, pady=10, sticky="w")

stage4ELL = tk.Entry(window, width=10)
stage4ELL.grid(row=9, column=1, padx=10, pady=10, sticky="w")

start_button = tk.Button(window, text="Start", command=setStages)
start_button.grid(row=10, column=0, columnspan=2, pady=20)

window.mainloop()