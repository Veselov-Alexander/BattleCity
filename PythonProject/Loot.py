from GameObject import *

class Loot(GameObject):
    def __init__(self, point):
        GameObject.__init__(self, point)
        self.textures.clear()
        self.direction = Direction.DEFAULT

    def draw(self):
        GameObject.draw(self, 0)

    def __str__(self):
        return "LOOT_CLASS"


class HealthBox(Loot):
    def __init__(self, point):
        Loot.__init__(self, point)
        self.type = "HP"
        self.add_texture(HP_BOX)

class ArmorBox(Loot):
    def __init__(self, point):
        Loot.__init__(self, point)
        self.type = "ARMOR"
        self.add_texture(ARMOR_BOX)

class BulletsBox(Loot):
    def __init__(self, point):
        Loot.__init__(self, point)
        self.type = "BULLETS"
        self.add_texture(BULLETS_BOX)