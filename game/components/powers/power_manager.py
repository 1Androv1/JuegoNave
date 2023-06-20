import random
from game.components.powers.powers import Power
from game.utils.constants import FIREBALL_TYPE, SHIELD_TYPE,SHIELD,FIREBALL


class PowerManager:
    def __init__(self):
        self.powers = []

    def update(self, game):
        self.add_power()
        for power in self.powers:
            power.update(self.powers, game)

    def add_power(self):
        if len(self.powers) < 1:
            self.type = random.choice(["shield", "shot"])

            if self.type == "shield":
                #print("sale escudo")
                power = Power(SHIELD, "shield")
            elif self.type == "shot":
                #print("sale multidisparo")
                power = Power(FIREBALL, "fireball")

            self.powers.append(power)

    def draw(self, screen):
        for power in self.powers:
            power.draw(screen)

    def reset(self):
        self.powers = []
