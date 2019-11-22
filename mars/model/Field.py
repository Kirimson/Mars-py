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

    def free_adjacent_location(self, location):
        locations = self.adjacent_locations(location, 1)
        for location in locations:
            if self.entity_at(location) is None:
                return location
        return None

    def adjacent_locations(self, location, w=1):
        row = location.row
        col = location.col
        locations = list()

        # Change the offset from -1 to 1, to get all spaces including diagonals
        for row_offset in range(-w, w+1):
            next_row = row + row_offset
            for col_offset in range(-w, w + 1):
                next_col = col + col_offset
                # If going out of the bounds, wrap around
                if next_col < 0:
                    next_col = next_col + self.width
                if next_col >= self.width:
                    next_col = next_col - self.width
                if next_row < 0:
                    next_row = next_row + self.depth
                if next_row >= self.depth:
                    next_row = next_row - self.depth

                # Dont add the same location as the checking entity, not adjacent
                adj_location = Location(next_row, next_col)
                if location != adj_location:
                    locations.append(adj_location)
        ModelConstants.random.shuffle(locations)
        return locations

    def neighbor_to(self, location, entity_type):
        adj_locations = self.adjacent_locations(location)
        for adj_location in adj_locations:
            entity = self.entity_at(adj_location)
            if entity:
                if entity.__class__.__name__ == entity_type:
                    return True
        return False

    def crumbs_at(self, location: Location) -> int:
        return self.crumbs[location.row][location.col]

    def signal_at(self, location: Location) -> int:
        return self.signal_strength[location.row][location.col]

    def entity_at(self, location: Location) -> Entity:
        return self.map[location.row][location.col]

    def location_free(self, location):
        return self.entity_at(location) is None

    def clear_location(self, location):
        self.map[location.row][location.col] = None

    def place_entity(self, entity, location):
        self.map[location.row][location.col] = entity
