from tkinter import Canvas, Frame, Label, StringVar, Toplevel

from mars.model.Constants import ViewConstants


def from_rgb(rgb):
    """translates an rgb tuple of int to hex
    """
    return "#%02x%02x%02x" % rgb


class View:

    def __init__(self, master, field_model, simulator, stats):

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

        self.stats_text = StringVar(value=F"Rocks: {stats['rocks']} "
                                    F"Vehicles: {stats['vehicles']}")
        self.stats = Label(self.field_window, textvariable=self.stats_text).grid()

        self.draw_village()

    def draw(self, step, stats):
        self.canvas.delete("all")
        self.draw_village()
        self.canvas.grid()
        self.step_text.set(F"Step: {step}")
        self.stats_text.set(F"Rocks: {stats['rocks']} "
                            F"Vehicles: {stats['vehicles']}")

    def draw_village(self):
        for row in range(self.field.depth):
            for col in range(self.field.width):
                entity = self.field.entity_at_rc(row, col)
                if entity:
                    self.draw_entity(entity)
                else:
                    quantity = self.field.crumbs_at_rc(row, col)
                    if quantity > 0 and ViewConstants.show_crumbs:
                        self.draw_crumb(row, col, quantity)

    def draw_crumb(self, row, col, quantity):
        crumb_col = 255 - 20 * quantity
        if crumb_col >= 255:
            crumb_col = 255
        if crumb_col <= 0:
            crumb_col = 0
        self.draw_square(row, col, from_rgb((255, crumb_col, crumb_col)))

    def draw_entity(self, entity):
        row = entity.location.row
        col = entity.location.col
        color = entity.color
        self.draw_square(row, col, color)

    def draw_square(self, row, col, color):
        y = row + (ViewConstants.scale * row) + ViewConstants.scale/2
        x = col + (ViewConstants.scale * col)

        y1 = row + (ViewConstants.scale * row) + ViewConstants.scale + ViewConstants.scale/2
        x1 = col + (ViewConstants.scale * col) + ViewConstants.scale
        self.canvas.create_rectangle(x, y, x1, y1, outline="", fill=color)
