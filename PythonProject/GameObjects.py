from Tank import *

class Text:
    class Align(enumerate):
        LEFT = 0,
        CENTER = 1,
        RIGHT = 2

    def __init__(self, point, text, align=Align.LEFT):
        self.point = point
        self.text = text
        self.align = align
        self.text_length = self.calculate_length()

    def calculate_length(self):
        current_length = 0
        for letter in self.text:
            texture = self.texture_by_letter(letter)
            current_length += texture.width + 1
        return current_length

    def texture_by_letter(self, letter):
        if letter.isalpha():
            texture = ALPHABET[ord(letter) - ord("a")]
        elif letter.isdigit():
            texture = NUMBERS[ord(letter) - ord("0")]
        elif letter == " ":
            texture = SPACE
        elif letter == ":":
            texture = COLON
        elif letter == "@":
            texture = BULLET_ICON
        return texture

    def draw(self, text = None):
        if text:
            self.text = text
            self.text_length = self.calculate_length()

        current_length = 0
        for letter in self.text:
            texture = self.texture_by_letter(letter)
            half_length = current_length // 2
            if self.align == Text.Align.LEFT:
                texture.draw(self.point.right(half_length))
            elif self.align == Text.Align.CENTER:
                texture.draw(self.point.right(half_length).left(self.text_length // 4))
            elif self.align == Text.Align.RIGHT:
                texture.draw(self.point.left(self.text_length // 2 - half_length))

            current_length += texture.width + 1

class FlyingText(GameObject, Text):
    update_frequancy = 2
    shift_count = 5

    def __init__(self, point, text, align=Text.Align.LEFT):
        Text.__init__(self, point, text, align)
        GameObject.__init__(self, point)
        self.text_length = self.calculate_length()
        self.tick = 0
        self.frame = 0
        self.change_direction(Direction.DOWN)

    def clear(self):
        for y in range(SPACE.height):
            setCursorXY(self.point.x - self.text_length // 2,
                        self.point.y + y)
            print(' ' * self.text_length * 2)

    def draw(self):
        if self.tick % FlyingText.update_frequancy == 0:
            if self.frame == FlyingText.shift_count:
                self.change_direction(Direction.UP)
            elif self.frame == FlyingText.shift_count * 2:
                self.tick = 0
                self.frame = 0
                self.change_direction(Direction.DOWN)
            self.clear()
            self.move()
            Text.draw(self)
            self.frame+=1
        self.tick+=1

class Wall(GameObject):
    def __init__(self, point : Point, type=0):
        GameObject.__init__(self, point)
        self.add_texture(WALL)
        self.add_texture(BORDER)
        self.type = type

    def draw(self):
        GameObject.draw(self, self.type)

def add_wall(x, y):
    return Wall(Point(LEFT_SHIFT + (x + 0) * WALL.width, (y + 0) * WALL.height))

def add_block(x, y):
    return [Wall(Point(LEFT_SHIFT + (x + 0) * WALL.width, (y + 0) * WALL.height)), \
            Wall(Point(LEFT_SHIFT + (x + 1) * WALL.width, (y + 0) * WALL.height)), \
            Wall(Point(LEFT_SHIFT + (x + 0) * WALL.width, (y + 1) * WALL.height)), \
            Wall(Point(LEFT_SHIFT + (x + 1) * WALL.width, (y + 1) * WALL.height))]
