#!/usr/bin/env python3
from mars.controller.Simulator import Simulator
from mars.view.SimulatorView import View
from mars.model.Constants import ModelConstants, ViewConstants
from tkinter import Tk, Button, Entry, Label, constants, Frame, Checkbutton
import argparse
import json


def int_parse(value):
    try:
        val = int(value)
    except ValueError as e:
        val = None
    return val


def float_parse(value):
    try:
        val = float(value)
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


def set_length(value):
    value = int_parse(value)
    if value:
        ModelConstants.simulation_length = value


def set_seed(value):
    value = int_parse(value)
    if value:
        ModelConstants.seed = value


def set_rock_num(value):
    value = int_parse(value)
    if value:
        ModelConstants.rock_count = value


def set_cluster(value):
    value = int_parse(value)
    if value:
        ModelConstants.cluster_count = value


def set_std(value):
    value = float_parse(value)
    if value:
        ModelConstants.std = value


def set_obs_chance(value):
    value = float_parse(value)
    if value:
        ModelConstants.obstacle_chance = value


def set_vehicle_chance(value):
    value = float_parse(value)
    if value:
        ModelConstants.vehicle_chance = value


def set_quiet(value):
    if value:
        ViewConstants.quiet = value


class GUIMain:
    master = Tk()
    view = None
    simulator = None
    step = 0

    def __init__(self):
        self.simulator = Simulator()

        if not ViewConstants.quiet:
            self.reset_button = Button()
            self.view_button = Button()
            self.run_button = Button()

            sim_frame = Frame(self.master, highlightbackground="gray",
                              highlightcolor="gray", highlightthickness=1)
            sim_frame.grid(row=0, sticky='we', columnspan=4)
            self.setup_simulation_parameters(sim_frame)

            rock_frame = Frame(self.master, highlightbackground="gray",
                               highlightcolor="gray", highlightthickness=1)
            rock_frame.grid(row=1, sticky='we', columnspan=2)
            self.setup_rocks(rock_frame)

            other_frame = Frame(self.master, highlightbackground="gray",
                                highlightcolor="gray", highlightthickness=1)
            other_frame.grid(row=1, column=2, sticky='we', columnspan=2)
            self.setup_other(other_frame)

            self.setup_buttons()

            self.master.title("Mars")
            self.master.mainloop()
        else:
            self.run_headless()

    def run_headless(self):
        self.simulator.set_up()
        while not self.simulator.is_finished():
            self.step += 1
            self.simulator.simulate(self.step)
        return self.step

    def setup_view(self):
        self.simulator.set_up()
        ModelConstants.running = True
        self.view = View(self.master, self.simulator.field, self,
                         self.simulator.get_stats())
        self.reset_button['state'] = 'normal'
        self.view_button['state'] = 'disabled'

    def stop_simulation(self):
        self.view.field_window.destroy()
        ModelConstants.running = False
        self.step = 0
        self.reset_button['state'] = 'disabled'
        self.view_button['state'] = 'normal'

    def run_simulation(self, step_amount, i=0):
        if ModelConstants.running:
            i += 1
            if not self.simulator.is_finished():
                self.step += 1
                self.simulator.simulate(self.step)
                self.view.draw(self.step, self.simulator.get_stats())
            if i < step_amount:
                self.master.after(1, self.run_simulation, step_amount, i)
        else:
            return

    def quit(self):
        if ModelConstants.running:
            self.stop_simulation()
            self.master.after(10, self.quit)
        else:
            self.master.destroy()

    def setup_simulation_parameters(self, frame):
        Label(frame, text="Simulation Parameters").grid(row=0, column=0)
        Label(frame, text="Simulation Length: ").grid(row=1, column=0)
        length_entry = Entry(frame, width=5)
        length_entry.bind("<KeyRelease>",
                          lambda event: set_length(length_entry.get()))
        length_entry.insert(constants.END,
                            str(ModelConstants.simulation_length))
        length_entry.grid(row=1, column=1)

        Label(frame, text="Simulation Seed: ").grid(row=2, column=0)
        seed_entry = Entry(frame, width=5, validate='all',
                           validatecommand=lambda: not ModelConstants.running)
        seed_entry.bind("<KeyRelease>",
                        lambda event: set_seed(seed_entry.get()))
        seed_entry.insert(constants.END, str(ModelConstants.seed))
        seed_entry.grid(row=2, column=1)

        Label(frame, text="Mars Width: ").grid(row=1, column=2)
        width_entry = Entry(frame, width=5)
        width_entry.bind("<KeyRelease>",
                         lambda event: set_width(width_entry.get()))
        width_entry.insert(constants.END, str(ModelConstants.width))
        width_entry.grid(row=1, column=3)

        Label(frame, text="Mars Height: ").grid(row=2, column=2)
        height_entry = Entry(frame, width=5)
        height_entry.bind("<KeyRelease>",
                          lambda event: set_depth(height_entry.get()))
        height_entry.insert(constants.END, str(ModelConstants.depth))
        height_entry.grid(row=2, column=3)

    def setup_rocks(self, frame):
        Label(frame, text="Rock Placement").grid(row=0, column=0)
        Label(frame, text="Number of Rocks: ").grid(row=1, column=0)
        rock_num_entry = Entry(frame, width=5)
        rock_num_entry.bind("<KeyRelease>",
                            lambda event: set_rock_num(rock_num_entry.get()))
        rock_num_entry.insert(constants.END, str(ModelConstants.rock_count))
        rock_num_entry.grid(row=1, column=1)

        Label(frame, text="Number of Clusters: ").grid(row=2, column=0)
        cluster_entry = Entry(frame, width=5)
        cluster_entry.bind("<KeyRelease>",
                           lambda event: set_cluster(cluster_entry.get()))
        cluster_entry.insert(constants.END, str(ModelConstants.cluster_count))
        cluster_entry.grid(row=2, column=1)

        Label(frame, text="Rock Clusters Std: ").grid(row=3, column=0)
        std_entry = Entry(frame, width=5)
        std_entry.bind("<KeyRelease>", lambda event: set_std(std_entry.get()))
        std_entry.insert(constants.END, str(ModelConstants.std))
        std_entry.grid(row=3, column=1)

    def setup_other(self, frame):
        Label(frame, text="Obstacles & Vehicles").grid(row=0, column=0)
        Label(frame, text="Obstacle: ").grid(row=1, column=0)
        obs_entry = Entry(frame, width=5)
        obs_entry.bind("<KeyRelease>",
                       lambda event: set_obs_chance(obs_entry.get()))
        obs_entry.insert(constants.END, str(ModelConstants.obstacle_chance))
        obs_entry.grid(row=1, column=1)

        Label(frame, text="Vehicle: ").grid(row=2, column=0)
        vehicle_entry = Entry(frame, width=5)
        vehicle_entry.bind("<KeyRelease>", lambda event: set_vehicle_chance(
            vehicle_entry.get()))
        vehicle_entry.insert(constants.END, str(ModelConstants.vehicle_chance))
        vehicle_entry.grid(row=2, column=1)

        Label(frame, text="Show Crumb Trails: ").grid(row=3, column=0)
        crumb_box = Checkbutton(frame, variable=ViewConstants.show_crumbs,
                                fg="black")
        crumb_box.select()
        crumb_box.grid(row=3, column=1)

    def setup_buttons(self):
        self.view_button = Button(self.master, text="Set Up Simulation",
                                  command=lambda: self.setup_view())
        self.view_button.grid(row=2, sticky="we", columnspan=2)
        step_button = Button(self.master, text="Step Once",
                             command=lambda: self.run_simulation(1))
        step_button.grid(row=3, sticky="we", columnspan=2)
        self.reset_button = Button(self.master, text="Reset", state="disabled",
                                   command=lambda: self.stop_simulation())
        self.reset_button.grid(row=2, column=2, sticky="we", columnspan=2)
        self.run_button = Button(self.master, text="Run",
                                 command=lambda: self.run_simulation(
                                     ModelConstants.simulation_length))
        self.run_button.grid(row=3, column=2, sticky="we", columnspan=2)
        quit_button = Button(self.master, text="Quit", command=self.quit)
        quit_button.grid(row=4, sticky="we", columnspan=4)


def parse_args():
    parser = argparse.ArgumentParser(description='Run Mars Simulation.')
    parser.add_argument("--quiet", "-q", action="store_true")
    parser.add_argument("--seed", "-s", type=int)
    parser.add_argument("--width", "-w", type=int)
    parser.add_argument("--depth", "-d", type=int)
    parser.add_argument("--rocks", "-r", type=int)
    parser.add_argument("--clusters", "-c", type=int)
    parser.add_argument("--std", type=float)
    parser.add_argument("--obstacle", "-o", type=float)
    parser.add_argument("--vehicle", "-v", type=float)
    parser.add_argument("--file", "-f", type=str, default="config.json")
    return parser.parse_args()


def set_args(user_args):
    if user_args.get('seed'):
        set_seed(user_args['seed'])
    if user_args.get('width'):
        set_width(user_args['width'])
    if user_args.get('depth'):
        set_depth(user_args['depth'])
    if user_args.get('rocks'):
        set_rock_num(user_args['rocks'])
    if user_args.get('clusters'):
        set_cluster(user_args['clusters'])
    if user_args.get('std'):
        set_std(user_args['std'])
    if user_args.get('obstacle'):
        set_obs_chance(user_args['obstacle'])
    if user_args.get('vehicle'):
        set_vehicle_chance(user_args['vehicle'])
    if user_args.get('quiet'):
        set_quiet(user_args['quiet'])


def read_args(user_args):
    if args.file:
        try:
            with open(user_args.file, 'r') as arg_file:
                arg_json = json.loads(arg_file.read())
                set_args(arg_json)
        except FileNotFoundError:
            print('Config file not found, using default values')
    set_args(user_args.__dict__)


if __name__ == '__main__':
    args = parse_args()
    read_args(args)
    gui = GUIMain()
