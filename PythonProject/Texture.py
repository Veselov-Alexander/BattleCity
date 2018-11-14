from Transform import *
from WinAPI import *

class Texture:
    def __init__(self, path):
        self.texture = list()
        path = "Textures/" + path
        with open(path, encoding='utf-8') as file:
            for line in file:
                self.texture.append(line)
        self.texture.pop(0)
        self.width = len(self.texture[0]) - 1
        self.height = len(self.texture)

    def draw(self, point : Point):
        for y, line in enumerate(self.texture):
            setCursorXY(point.x, point.y + y)
            print(line)

TANK_LEFT_FRAME = Texture("Tank/tank_left")
TANK_RIGHT_FRAME = Texture("Tank/tank_right")
TANK_UP_FRAME = Texture("Tank/tank_up")
TANK_DOWN_FRAME = Texture("Tank/tank_down")

ENEMY_LEFT_FRAME = Texture("Enemy/enemy_left")
ENEMY_RIGHT_FRAME = Texture("Enemy/enemy_right")
ENEMY_UP_FRAME = Texture("Enemy/enemy_up")
ENEMY_DOWN_FRAME = Texture("Enemy/enemy_down")

BOSS = Texture("Boss/boss")

WALL = Texture("wall")
BASE = Texture("base")
BULLET = Texture("bullet")
BORDER = Texture("border")

BULLET_ICON = Texture("bullet_icon")
BULLET_RELOADING = Texture("bullet_reloading")

ALPHABET = list()
NUMBERS = list()
SPACE = Texture("Font/SPACE")
COLON = Texture("Font/COLON")

HP_BOX = Texture("Loot/hp")
ARMOR_BOX = Texture("Loot/armor")
BULLETS_BOX = Texture("Loot/bullets")

alphabet_letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
numbers_letters = "0123456789"

for symbol in alphabet_letters:
    ALPHABET.append(Texture("Font/" + symbol))

for number in numbers_letters:
    NUMBERS.append(Texture("Font/" + number))
