class Direction(enumerate):
    DEFAULT = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    ENTER = 5
    ANY = 6
    ESCAPE = 7

    def opposite(dir):
        if dir == Direction.UP:
            return Direction.DOWN
        if dir == Direction.DOWN:
            return Direction.UP
        if dir == Direction.LEFT:
            return Direction.RIGHT
        if dir == Direction.RIGHT:
            return Direction.LEFT

class GameStatus(enumerate):
    DEAD = 0
    IN_GAME = 1
    PAUSED = 2
    SCENE_SELECTION = 3
    LEVEL_END = 4

class Point:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def higher(self, distance = 1):
        return Point(self.x, int(self.y - distance))

    def lower(self, distance = 1):
        return Point(self.x, int(self.y + distance))

    def left(self, distance = 1):
        return Point(self.x - int(2 * distance), self.y)

    def right(self, distance = 1):
        return Point(self.x + int(2 * distance), self.y)

    def __eq__(self, point):
        return self.x == point.x and self.y == point.y


LEFT_SHIFT = 2
TOP_SHIFT = 12