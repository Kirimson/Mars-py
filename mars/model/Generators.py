import random

from mars.model import Entities
from mars.model.Constants import ModelConstants
from mars.model.Entities import Location


class VillageGenerator:
    @staticmethod
    def populate_village():
        depth = ModelConstants.depth
        width = ModelConstants.width

        village_map = [[Entities.Entity for x in range(width)] for y in range(depth)]
        for row in range(0, depth):
            for col in range(0, width):
                village_map[row][col] = None
        village_map[0][0] = Entities.Rock(Location(0, 0))
        village_map[0][3] = Entities.Vehicle(Location(0, 3))
        village_map[1][0] = Entities.Mothership(Location(1, 0))
        return village_map
