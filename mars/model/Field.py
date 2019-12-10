from mars.model.Constants import ModelConstants
from mars.model.Entities import Entity, Location


class Field:
    def __init__(self):
        self.width = ModelConstants.width
        self.depth = ModelConstants.depth
        # Set map up, including crumbs and signal
        self.crumbs = [[0 for x in range(self.width)] for y in range(self.depth)]
        self.signal_strength = [[0 for x in range(self.width)] for y in range(self.depth)]
        self.map = [[None for x in range(self.width)] for y in range(self.depth)]

    def to_string(self):
        field_string = ""
        for row in self.map:
            for entity in row:
                if isinstance(entity, Entity):
                    field_string += F"{entity.__class__.__name__[0]} "
                else:
                    field_string += "B "
            field_string += "\n"
        return field_string

    def all_free_adjacent_locations(self, location):
        free_locations = list()
        for adj_location in self.adjacent_locations(location):
            if self.location_free(adj_location):
                free_locations.append(adj_location)
        return free_locations

    def free_adjacent_location(self, location):
        locations = self.adjacent_locations(location, 1)
        for location in locations:
            if self.entity_at(location) is None:
                return location
        return None

    def adjacent_locations(self, location, w=1):
        if location:
            row = location.row
            col = location.col
            locations = list()

            # Change the offset from -1 to 1, to get all spaces including diagonals
            for row_offset in range(-w, w + 1):
                next_row = row + row_offset
                for col_offset in range(-w, w + 1):
                    next_col = col + col_offset
                    # If going out of the bounds, wrap around
                    if next_row < 0:
                        next_row = next_row + self.depth
                    if next_row >= self.depth:
                        next_row = next_row - self.depth
                    if next_col < 0:
                        next_col = next_col + self.width
                    if next_col >= self.width:
                        next_col = next_col - self.width

                    adj_location = Location(next_row, next_col)
                    locations.append(adj_location)
            ModelConstants.random.shuffle(locations)
            return locations
        return None

    def neighbor_to(self, location, entity_type):
        adj_locations = self.adjacent_locations(location)
        for adj_location in adj_locations:
            entity = self.entity_at(adj_location)
            if entity and isinstance(entity, entity_type):
                return True
        return False

    def get_neighbor(self, location, entity_type):
        adj_locations = self.adjacent_locations(location, 1)
        for adj_location in adj_locations:
            entity = self.entity_at(adj_location)
            if entity and isinstance(entity, entity_type):
                return adj_location
        return None

    def reduce_crumbs(self):
        for row in range(len(self.crumbs)):
            for col in range(len(self.crumbs[0])):
                if self.crumbs[row][col] > 0:
                    self.crumbs[row][col] -= 1

    def place_crumbs(self, location, quantity):
        if self.crumbs_at(location) < 10 - quantity:
            self.crumbs[location.row][location.col] += quantity

    def crumbs_at(self, location: Location) -> int:
        return self.crumbs[location.row][location.col]

    def crumbs_at_rc(self, row, col) -> int:
        return self.crumbs[row][col]

    def pick_up_crumb(self, location):
        if self.crumbs_at(location) > 0:
            self.crumbs[location.row][location.col] -= 1

    def signal_at(self, location: Location) -> int:
        return self.signal_strength[location.row][location.col]

    def set_signal_rc(self, row, col, value):
        self.signal_strength[row][col] = value

    def entity_at_rc(self, row, col):
        return self.map[row][col]

    def entity_at(self, location: Location):
        return self.map[location.row][location.col]

    def location_free(self, location):
        return self.map[location.row][location.col] is None

    def clear_location(self, location):
        self.map[location.row][location.col] = None

    def place_entity(self, entity, location):
        self.map[location.row][location.col] = entity
