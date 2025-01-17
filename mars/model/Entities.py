from mars.model.Constants import ViewConstants


class Location:
    def __init__(self, col, row):
        self.row = col
        self.col = row

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __ne__(self, other):
        return not self == other

    def to_string(self):
        return F"Row: {self.row} Col: {self.col}"


class Entity:
    def __init__(self, location, color):
        self.location = location
        self.color = color


class Vehicle(Entity):
    def __init__(self, location):
        super().__init__(location, ViewConstants.vehicle_color)
        self.carrying_sample = False

    def act(self, field, rocks_collected):
        # self.act_simple(field, rocks_collected)
        self.act_collaborative(field, rocks_collected)

    def act_collaborative(self, field, rocks_collected):
        if self.sample_at_base(field):
            self.carrying_sample = False
            self.color = ViewConstants.vehicle_color
            return

        if self.carrying_sample:
            field.place_crumbs(self.location, 2)
            self.travel_gradient(field)
            return

        if self.sample_detected(field):
            self.pick_sample(field, rocks_collected)
            return

        if self.sense_crumbs(field):
            field.pick_up_crumb(self.location)
            self.travel_gradient(field, False)
            return

        self.random_move(field)

    def act_simple(self, field, rocks_collected):
        if self.sample_at_base(field):
            self.carrying_sample = False
            self.color = ViewConstants.vehicle_color
            return

        if self.carrying_sample:
            self.travel_gradient(field)
            return

        if self.sample_detected(field):
            self.pick_sample(field, rocks_collected)
            return

        self.random_move(field)

    def sample_at_base(self, field):
        return field.neighbor_to(self.location, Mothership)\
            and self.carrying_sample

    def sample_detected(self, field):
        return field.neighbor_to(self.location, Rock)

    def pick_sample(self, field, rocks_collected):
        rock_location = field.get_neighbor(self.location, Rock)
        rock = field.entity_at(rock_location)
        self.carrying_sample = True
        self.color = ViewConstants.vehicle_sample_color
        rocks_collected.append(rock)
        field.clear_location(rock_location)

    def travel_gradient(self, field, up_gradient=True):
        best_location = self.location
        best_signal = field.signal_at(self.location)
        for adj_location in field.all_free_adjacent_locations(self.location):
            signal = field.signal_at(adj_location)
            if up_gradient:
                if best_signal:
                    if signal >= best_signal:
                        best_location = adj_location
                        best_signal = signal
                else:
                    best_location = adj_location
                    best_signal = field.signal_at(adj_location)
            else:
                signal -= field.crumbs_at(adj_location)
                if best_signal:
                    if signal <= best_signal:
                        best_location = adj_location
                        best_signal = signal
                else:
                    best_location = adj_location
                    best_signal = field.signal_at(adj_location)

        if self.location == best_location:
            self.random_move(field)
        else:
            self.move_to(best_location, field)

    def sense_crumbs(self, field):
        return field.crumbs_at(self.location) > 0

    def random_move(self, field):
        new_location = field.free_adjacent_location(self.location)
        self.move_to(new_location, field)

    def move_to(self, new_location, field):
        field.clear_location(self.location)
        self.location = new_location
        field.place_entity(self, self.location)


class Obstacle(Entity):
    def __init__(self, location):
        super().__init__(location, ViewConstants.obstacle_color)


class Rock(Entity):
    def __init__(self, location):
        super().__init__(location, ViewConstants.rock_color)


class Mothership(Entity):
    def __init__(self, location):
        super().__init__(location, ViewConstants.mothership_color)

    def emit_signal(self, field, depth, width):
        for row in range(depth):
            for col in range(width):
                d1 = abs(row-self.location.row)
                d2 = depth - d1
                x = min(d1*d1, d2*d2)

                d3 = abs(col-self.location.col)
                d4 = width - d3
                y = min(d3*d3, d4*d4)

                signal = depth * depth + width * width - (x+y)
                field.set_signal_rc(row, col, signal)
