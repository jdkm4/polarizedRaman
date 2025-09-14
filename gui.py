import customtkinter as ctk
import matplotlib.pylab as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class PolarizationApp(ctk.CTk):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("GUI")
        self.geometry("1920x1080")

        self.customMode = False
        self.theta = np.linspace(0, 2 * np.pi, 1000)

        self._create_widgets()
        self._setup_plot_and_canvas()
        self.update_plot_and_gui()

    def goButton(self):
        print("button pressed")

    def _create_widgets(self):

        button = ctk.CTkButton(self, text="Run", command=self.goButton)
        button.grid(row=0, column=0, padx=20, pady=20, columnspan=4, sticky='ew')

        tab_view = ctk.CTkTabview(master=self)
        tab_view.grid(row=1, column=0, columnspan=4, sticky='ew')

        simpleTab = tab_view.add("Simple Mode")
        advancedTab = tab_view.add("Advanced Mode")

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        presets = ["Vertical", "Horizontal", "Left-hand Circular", "Right-hand Circular"]
        incomingLabel = ctk.CTkLabel(master=simpleTab, text="Incoming Polarization:")
        incomingLabel.grid(row=0, column=0)
        incomingDropdown = ctk.CTkComboBox(master=simpleTab, values=presets)
        incomingDropdown.grid(row=0, column=1, padx=10, pady=20, sticky='ew')
        receivingLabel = ctk.CTkLabel(master=simpleTab, text="Incoming Polarization:")
        receivingLabel.grid(row=0, column=2)
        receivingDropdown = ctk.CTkComboBox(master=simpleTab, values=presets)
        receivingDropdown.grid(row=0, column=3, padx=10, pady=20, sticky='ew')

        advancedTab.grid_columnconfigure(tuple(range(8)), weight=1)
        advancedInfo = ctk.CTkLabel(master=advancedTab, text="Configure rotation of the waveplates in degrees from vertical. \n Recieving waveplates will by default return the light back to linear vertical.")
        advancedInfo.grid(row=0, column=0, columnspan=4)

        customReceiving = ctk.CTkSwitch(master=advancedTab, text="Custom receiving mode", command=self.customModeFunction)
        customReceiving.grid(row=0, column=4, sticky="e", columnspan=2)

        self.incomingHWPValue = ctk.StringVar()
        self.incomingHWPValue.trace_add("write", self.update_plot_and_gui)
        self.incomingQWPValue = ctk.StringVar()
        self.incomingQWPValue.trace_add("write", self.update_plot_and_gui)

        ctk.CTkLabel(master=advancedTab, text="Incoming HWP:", padx=10).grid(row=1, column=0, sticky="e")
        ctk.CTkEntry(master=advancedTab, placeholder_text="° from vertical", textvariable=self.incomingHWPValue).grid(row=1, column=1, padx=10, pady=20, sticky="ew")

        ctk.CTkLabel(master=advancedTab, text="Incoming QWP:", padx=10).grid(row=1, column=2, sticky="e")
        ctk.CTkEntry(master=advancedTab, placeholder_text="° from vertical", textvariable=self.incomingQWPValue).grid(row=1, column=3, padx=10, pady=20, sticky="ew")

        ctk.CTkLabel(master=advancedTab, text="Receiving QWP:", padx=10).grid(row=1, column=4, sticky="e")
        self.receivingQWP = ctk.CTkEntry(master=advancedTab, placeholder_text="° from vertical")
        self.receivingQWP.grid(row=1, column=5, padx=10, pady=20)
        self.receivingQWP.insert(0, "0.0")
        self.receivingQWP.configure(state="disabled")

        ctk.CTkLabel(master=advancedTab, text="Receiving HWP:", padx=10).grid(row=1, column=6, sticky="e")
        self.receivingHWP = ctk.CTkEntry(master=advancedTab, placeholder_text="° from vertical")
        self.receivingHWP.grid(row=1, column=7, padx=10, pady=20)
        self.receivingHWP.insert(0, "0.0")
        self.receivingHWP.configure(state="disabled")

        graph = ctk.CTkFrame(advancedTab)
        graph.grid(row=2, column=0, columnspan=4)
        
        self.fig, self.ax = plt.subplots(subplot_kw={'projection': 'polar'})
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph)
        self.canvas.get_tk_widget().pack(side=ctk.TOP, fill=ctk.BOTH, expand=1)

    def _setup_plot_and_canvas(self):
        """This function sets up the basic look of the plot one time."""
        angles = np.array([0, 45, 90, 135, 180, 225, 270, 315])
        new_labels_numeric = (angles - 90) % 360
        new_labels_str = [f'{angle}°' for angle in new_labels_numeric]
        self.ax.set_thetagrids(angles, new_labels_str)
        self.ax.set_rlim(0, 1.0)
        self.ax.set_rticks([])
        self.ax.grid(False)

    def update_plot_and_gui(self, *args):

        try:
            hwp_str = self.incomingHWPValue.get()
            incomingHWPFloat = float(hwp_str) if hwp_str else 0.0
            
            qwp_str = self.incomingQWPValue.get()
            incomingQWPFloat = float(qwp_str) if qwp_str else 0.0
        except ValueError:
            return

        if not self.customMode:
            self.receivingQWP.configure(state="normal")
            self.receivingQWP.delete(0, "end")
            self.receivingQWP.insert(0, str(incomingQWPFloat))
            self.receivingQWP.configure(state="disabled")

            self.receivingHWP.configure(state="normal")
            self.receivingHWP.delete(0, "end")
            self.receivingHWP.insert(0, str(incomingQWPFloat - incomingHWPFloat))
            self.receivingHWP.configure(state="disabled")

        self.ax.clear()
        self._setup_plot_and_canvas()

        a = (incomingHWPFloat * 2 * np.pi / 360) + np.pi / 2
        b = (incomingQWPFloat * 2 * np.pi / 360) + np.pi / 2

        if (np.abs(np.sin(a - b) * np.cos(a - b))) < 0.006:
            self.ax.plot([a, a + np.pi], [1, 1], color='red', label='Polarization')
        else:
            r = np.abs((np.sin(a - b) * np.cos(a - b))) / np.sqrt(
                (np.sin(self.theta - b) ** 2) * (np.cos(a - b) ** 2) +
                (np.cos(self.theta - b) ** 2) * (np.sin(a - b) ** 2)
            )
            self.ax.plot(self.theta, r, color='red', label='Polarization')

        self.ax.plot([a, a + np.pi], [1, 1], color='black', linestyle='--', label='HWP')
        self.ax.plot([b, b + np.pi], [1, 1], color='black', linestyle=':', label='QWP')

        self.ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.15))
        self.canvas.draw()

    def customModeFunction(self):
        self.customMode = not self.customMode

        if self.customMode:
            self.receivingQWP.configure(state="normal")
            self.receivingHWP.configure(state="normal")
        else:
            self.receivingQWP.configure(state="disabled")
            self.receivingHWP.configure(state="disabled")
            self.update_plot_and_gui()

if __name__ == "__main__":
    app = PolarizationApp()
    app.mainloop()