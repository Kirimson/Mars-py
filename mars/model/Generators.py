from typing import List
from mars.model.Constants import ModelConstants
from mars.model.Entities import Location


class RockGenerator:
    @staticmethod
    def generate_rocks(cluster_count, rock_count, width, depth, std):

        # Make falsy 2d array the size of the field
        has_rock = [[False for x in range(width)] for y in range(depth)]

        locations = [Location for x in range(rock_count)]
        clusters = [Location for x in range(rock_count)]  # type: List[Location]

        for i in range(cluster_count):
            col = ModelConstants.random.randint(0, width - 1)
            row = ModelConstants.random.randint(0, depth - 1)
            clusters[i] = Location(row, col)

        i = 0
        while i < rock_count:
            c = ModelConstants.random.randint(0, cluster_count - 1)
            row = clusters[c].row + int(std * ModelConstants.random.gauss(0.0, 1.0))
            col = clusters[c].col + int(std * ModelConstants.random.gauss(0.0, 1.0))
            row = (row + 10 * depth) % depth
            col = (col + 10 * width) % width
            if not has_rock[row][col]:
                locations[i] = Location(row, col)
                has_rock[row][col] = True
                i += 1

        return locations
