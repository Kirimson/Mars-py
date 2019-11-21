from mars.controller.Simulator import Simulator
from mars.view.SimulatorView import View
from mars.model.Constants import ModelConstants
from tkinter import Tk, Button, Entry, Label


def int_parse(value):
    try:
        val = int(value)
    except ValueError as e:
        val = None
    return val


def set_width(value):
    value = int_parse(value)
    if value:
        ModelConstants.width = value


def set_depth(value):
    value = int_parse(value)
    if value:
        ModelConstants.depth = value


class GUIMain:
    master = Tk()
    view = None
    simulator = None
    step = 0

    def __init__(self):
        self.simulator = Simulator()

        self.setup_size_buttons()

        step_button = Button(self.master, text="Step Once", command=lambda: self.run_simulation(1))
        step_button.grid(row=2)

        view_button = Button(self.master, text="Start Simulation", command=self.setup_view)
        view_button.grid(row=3)

        self.master.grid_rowconfigure(2, weight=1)

        self.master.title("Mars")
        self.master.mainloop()

    def setup_view(self):
        if not ModelConstants.running:
            ModelConstants.running = True
            self.simulator.set_up()
            self.view = View(self.master, self.simulator.field)

    def run_simulation(self, step_amount, i=0):
        i += 1
        self.step += 1

        self.simulator.simulate()

        self.view.redraw_village()

        if i < step_amount:
            self.master.after(20, self.run_simulation, step_amount, i)

    def setup_size_buttons(self):
        width_label = Label(self.master, text="Width: ")
        width_label.grid(row=0, column=2)
        width_entry = Entry(self.master)
        width_entry.bind("<KeyRelease>", lambda event: set_width(width_entry.get()))
        width_entry.grid(row=0, column=3)

        height_label = Label(self.master, text="Height: ")
        height_label.grid(row=1, column=2)
        height_entry = Entry(self.master)
        height_entry.bind("<KeyRelease>", lambda event: set_depth(height_entry.get()))
        height_entry.grid(row=1, column=3)


if __name__ == '__main__':
    gui = GUIMain()
