from mars.model.Constants import ModelConstants
from mars.model.Entities import Rock, Location, Obstacle, Vehicle, Mothership
from mars.model.Field import Field
from mars.model.Generators import RockGenerator


class Simulator:
    def __init__(self):
        self.field = None
        self.rocks = list()
        self.vehicles = list()

    def set_up(self):
        # Set the random seed
        rnd_model = ModelConstants()
        rnd_model.set_random()
        # Initialise the field, clearing the old on if it exists
        self.field = Field()
        # Populate field with rocks, obstacles and vehicles
        self.populate()
        self.set_mothership()

    def populate(self):
        # Empty old lists
        self.rocks = list()
        self.vehicles = list()
        # Generate rock clusters and add to the field
        rock_locations = RockGenerator.generate_rocks(ModelConstants.cluster_count, ModelConstants.rock_count,
                                                      ModelConstants.width, ModelConstants.depth, ModelConstants.std)
        for rock_location in rock_locations:
            rock = Rock(rock_location)
            self.field.place_entity(rock, rock_location)
            self.rocks.append(rock)

        # Generate obstacles and vehicles based on given chance args
        obs_chance = ModelConstants.obstacle_chance
        vehicle_chance = ModelConstants.obstacle_chance + ModelConstants.vehicle_chance

        for row in range(self.field.depth):
            for col in range(self.field.width):
                location = Location(row, col)
                if self.field.entity_at(location) is None:
                    rand = ModelConstants.random.random()
                    if rand <= obs_chance:
                        obstacle = Obstacle(location)
                        self.field.place_entity(obstacle, location)
                    elif obs_chance < rand <= vehicle_chance:
                        vehicle = Vehicle(location)
                        # Add vehicles to a list, ensures we only go over them once
                        # If we iterate over the field, a vehicle may move into a non processed location, giving it
                        # multiple turns
                        self.vehicles.append(vehicle)
                        self.field.place_entity(vehicle, location)

    def simulate(self, step):
        # Python does not copy by reference for stuff like this!
        collected_rocks = list()

        for vehicle in self.vehicles:
            vehicle.act(self.field, collected_rocks)

        for rock in collected_rocks:
            self.rocks.remove(rock)

        if step % (self.field.depth * 2 + self.field.width * 2) == 0:
            self.field.reduce_crumbs()

    def set_mothership(self):
        row = ModelConstants.random.randint(0, self.field.depth - 1)
        col = ModelConstants.random.randint(0, self.field.width - 1)
        location = Location(row, col)
        while self.field.entity_at(location) is not None:
            row = ModelConstants.random.randint(0, self.field.depth - 1)
            col = ModelConstants.random.randint(0, self.field.width - 1)
            location = Location(row, col)
        mothership = Mothership(location)
        self.field.place_entity(mothership, location)
        mothership.emit_signal(self.field, self.field.depth, self.field.width)

    def get_stats(self):
        return {
            "rocks": len(self.rocks),
            "vehicles": len(self.vehicles)
        }

    def is_finished(self):
        carrying = False
        for vehicle in self.vehicles:
            if vehicle.carrying_sample:
                carrying = True
        if len(self.rocks) == 0 and carrying == False:
            return True
        else:
            return False
