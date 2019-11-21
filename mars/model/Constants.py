from random import Random


class ViewConstants:
    scale = 12


class ModelConstants:
    random = Random()
    depth = 50
    width = 50
    seed = 133
    running = False

    def set_random(self):
        self.random.seed(self.seed)
