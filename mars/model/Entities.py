from mars.model.Constants import ViewConstants


class Location:
    def __init__(self, col, row):
        self.row = col
        self.col = row

    def __eq__(self, other):
        return self.row == other.row and self.col == self.col

    def __ne__(self, other):
        return not self == other

    def to_string(self):
        return F"Row: {self.row} Col: {self.col}"


class Entity:
    def __init__(self, location, color):
        self.location = location
        self.color = color

    def act(self, f):
        """
        Base act method to be overridden
        """
        pass


class Vehicle(Entity):
    def __init__(self, location):
        super().__init__(location, "Cyan")
        self.old_location = location

    def act(self, f):
        self.towards_ship(f)
        # self.random_move(f)

    def towards_ship(self, field):
        best_location = self.location
        best_score = field.signal_at(self.location)
        for location in field.adjacent_locations(self.location):
            if field.location_free(location) and field.signal_at(location) > best_score:
                best_score = field.signal_at(location)
                best_location = location
        self.move_to(best_location, field)

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

    def emit_signal(self, signal_strength, depth, width):
        for row in range(depth):
            for col in range(width):
                d1 = abs(row-self.location.row)
                d2 = depth - d1
                x = min(d1*d1, d2*d2)

                d3 = abs(col-self.location.col)
                d4 = width - d3
                y = min(d3*d3, d4*d4)

                signal = depth * depth + width * width - (x+y)
                signal_strength[row][col] = signal

        return signal_strength
