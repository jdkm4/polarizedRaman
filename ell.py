from pylablib.devices import Thorlabs
import time
import tkinter as tk

window = tk.Tk()
window.title("ELL Controller")
window.geometry("300x300")

def setELLStages():
    with Thorlabs.ElliptecMotor("COM3") as stage:
        stage.set_default_addr(1)
        stage.move_to(int(stage1.get()))
        stage.set_default_addr(2)
        stage.move_to(int(stage2.get()))
        stage.set_default_addr(3)
        stage.move_to(int(stage3.get()))
        stage.set_default_addr(4)
        stage.move_to(int(stage4.get()))

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

start_button = tk.Button(window, text="Start", command=setELLStages)
start_button.grid(row=4, column=0, columnspan=2, pady=20)

window.mainloop()
