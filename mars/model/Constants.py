from random import Random


class ViewConstants:
    scale = 5
    vehicle_color = "Cyan"
    vehicle_sample_color = "Blue"
    rock_color = "Yellow"
    obstacle_color = "Black"
    mothership_color = "Purple"
    bg_color = "White"
    quiet = False
    show_crumbs = True


class ModelConstants:
    random = Random()
    depth = 50
    width = 50
    seed = 133
    simulation_length = 1000
    rock_count = 300
    cluster_count = 7
    std = 2.0
    obstacle_chance = 0.002
    vehicle_chance = 0.002
    running = False

    def set_random(self):
        self.random.seed(self.seed)
