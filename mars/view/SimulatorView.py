from tkinter import Canvas, Frame, Label, StringVar, Toplevel

from mars.model.Constants import ViewConstants, ModelConstants


class View:

    def __init__(self, master, field_model, simulator):

        self.field = field_model

        self.field_window = Toplevel(master)
        self.field_window.protocol("WM_DELETE_WINDOW", simulator.stop_simulation)
        self.field_window.title("Mars Field")

        self.step_text = StringVar(value=F"Step: 0")
        self.step_label = Label(self.field_window, textvariable=self.step_text).grid(pady=1)

        self.canvas = Canvas(self.field_window,
                             height=self.field.depth * ViewConstants.scale + (self.field.depth - 1),
                             width=self.field.width * ViewConstants.scale + (self.field.width - 1),
                             bg=ViewConstants.bg_color)
        self.canvas.grid()

        self.config_frame = Frame(master)
        self.config_frame.grid()

        self.draw_village()

    def draw(self, step):
        self.canvas.delete("all")
        self.draw_village()
        self.canvas.grid()
        self.step_text.set(F"Step: {step}")

    def draw_village(self):
        for row in self.field.map:
            for entity in row:
                if entity:
                    self.draw_entity(entity)

    def draw_entity(self, entity):
        row = entity.location.row
        col = entity.location.col
        color = entity.color
        y = row + (ViewConstants.scale * row) + ViewConstants.scale/2
        x = col + (ViewConstants.scale * col)

        y1 = row + (ViewConstants.scale * row) + ViewConstants.scale + ViewConstants.scale/2
        x1 = col + (ViewConstants.scale * col) + ViewConstants.scale
        self.canvas.create_rectangle(x, y, x1, y1, outline="", fill=color)
