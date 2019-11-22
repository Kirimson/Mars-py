from mars.model.Constants import ModelConstants
from mars.model.Entities import Entity, Rock
from mars.model.Field import Field
from mars.model.Generators import RockGenerator


class Simulator:
    def __init__(self):
        self.field = None
        self.rocks = list()

    def set_up(self):
        rnd_model = ModelConstants()
        rnd_model.set_random()
        self.field = Field()
        self.populate()

    def populate(self):
        rock_locations = RockGenerator.generate_rocks(ModelConstants.cluster_count, ModelConstants.rock_count,
                                                      ModelConstants.width, ModelConstants.depth, ModelConstants.std)
        for rock_location in rock_locations:
            rock = Rock(rock_location)
            self.field.place_entity(rock, rock_location)
            self.rocks.append(rock)

        vehicle_chance = ModelConstants.vehicle_chance
        obs_chance = ModelConstants.obstacle_chance

        for row in range(self.field.depth):


    def simulate(self):
        for row in self.field.map:
            for entity in row:
                if isinstance(entity, Entity):
                    entity.act(self.field)
