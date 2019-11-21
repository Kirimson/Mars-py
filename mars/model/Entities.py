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
        self.random_move(f)

    def random_move(self, field):
        new_location = field.free_adjacent_location(self.location)
        field.clear_location(self.location)
        self.location = new_location
        field.place_entity(self, new_location)


class Shadow(Entity):
    def __init__(self, location):
        super().__init__(location, "Gray")


class Rock(Entity):
    def __init__(self, location):
        super().__init__(location, "Yellow")


class Mothership(Entity):
    def __init__(self, location):
        super().__init__(location, "Purple")
