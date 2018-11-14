from Texture import *
from copy import deepcopy

class GameObject:
    def __init__(self, point : Point):
        self.point = point
        self.textures = list()
        self.width = 0
        self.height = 0
        self.direction = Direction.DEFAULT

    def add_texture(self, texture : Texture):
        self.width = max(self.width, texture.width)
        self.height = max(self.height, texture.height)
        self.textures.append(texture)

    def draw(self, texture_index):
        self.textures[texture_index].draw(self.point)

    def update(self, *args):
        pass

    def change_direction(self, direction : Direction):
        self.direction = direction  

    def is_overlaping(self, game_object):
        l1 = self.point
        r1 = l1.right(self.width // 2).higher(game_object.height)
        l2 = game_object.point
        r2 = l2.right(game_object.width // 2).higher(self.height)

        if (l1.x >= r2.x) or (l2.x >= r1.x):
            return False

        if (l1.y <= r2.y) or (l2.y <= r1.y):
            return False

        return True

    def clear(self):
        for line in range(self.height):
            setCursorXY(self.point.x, self.point.y + line)
            print(' ' *  self.width)

    def move(self):
        if self.direction == Direction.UP:    
            self.point = self.point.higher()
        elif self.direction == Direction.DOWN:
            self.point = self.point.lower()
        elif self.direction == Direction.LEFT:
            self.point = self.point.left()
        elif self.direction == Direction.RIGHT:
            self.point = self.point.right()

    def try_move(self, game_objects):
        replaced_object = deepcopy(self)
        GameObject.move(replaced_object)

        if not (LEFT_SHIFT + WALL.width <= replaced_object.point.x <= LEFT_SHIFT + WALL.width * 38 -  self.width):
            del replaced_object
            return True

        if not (TOP_SHIFT + WALL.height <= replaced_object.point.y <= TOP_SHIFT + WALL.height * 22 -  self.height):
            del replaced_object
            return True

        for game_object_type in game_objects:
            for game_object in game_object_type:
                if game_object is not self and game_object.is_overlaping(replaced_object):
                    if str(game_object) == "LOOT_CLASS" and str(type(self)) != "<class 'Tank.Bullet'>":
                        game_objects[0].remove(game_object)
                        game_object.clear()
                        self.use_loot(game_object)
                        continue
                    del replaced_object
                    return game_object
        del replaced_object
        return None

    def move_up(self, game_objects):
        self.change_direction(Direction.UP)
        object = self.try_move(game_objects)
        if object is True:
            return None
        if object:
            return object
        self.move()
        return None

    def move_down(self, game_objects):
        self.change_direction(Direction.DOWN)
        object = self.try_move(game_objects)
        if object is True:
            return None
        if object:
            return object
        self.move()
        return None

    def move_left(self, game_objects):
        self.change_direction(Direction.LEFT)
        object = self.try_move(game_objects)
        if object is True:
            return None
        if object:
            return object
        self.move()
        return None

    def move_right(self, game_objects):
        self.change_direction(Direction.RIGHT)
        object = self.try_move(game_objects)
        if object is True:
            return None
        if object:
            return object
        self.move()
        return None