from mars.model.Constants import ModelConstants
from mars.model.Entities import Entity
from mars.model.Field import Field


class Simulator:
    def __init__(self):
        self.field = None

    def set_up(self):
        rnd_model = ModelConstants()
        rnd_model.set_random()
        self.field = Field()

    def simulate(self):
        for row in self.field.map:
            for entity in row:
                if isinstance(entity, Entity):
                    entity.act(self.field)
