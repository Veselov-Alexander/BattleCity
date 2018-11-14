from GameObjects import *
from Score import *
from Loot import *

import time

class Timer:
    def start(self):
        self.time = time.clock()

    def elapsed(self):
        return (time.clock() - self.time) * 1000

class Scene:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.dynamic_objects = list()
        self.static_objects = list()

        self.objects = [self.static_objects, self.dynamic_objects]

        self.timer = Timer()
        self.timer.start()

    def add_static_object(self, object):
        if type(object) is list:
            for item in object:
                self.static_objects.append(item)
        else:
            self.static_objects.append(object)

    def add_dynamic_object(self, object):
        self.dynamic_objects.append(object)

    def draw_static(self):
        for game_object in self.static_objects:
            game_object.draw()

    def draw_dynamic(self, process=False):
        for game_object in self.dynamic_objects:
            game_object.draw()

    def draw(self):
        self.draw_dynamic()
        self.draw_static()

    def get_time(self):
        return self.timer.elapsed()
 

class GameScene(Scene):
    def __init__(self, width, height):
        Scene.__init__(self, width, height)
        self.walls = list()
        self.base = None
        self.boss = None
        self.init_borders()
        self.init_UI()
        self.lootbox_timer = 0

    def init_borders(self):
        border_width = BORDER.width
        border_height = BORDER.height

        for coordinate in range(0, self.width):
            wall = Wall(Point(LEFT_SHIFT + coordinate * border_width,
                              TOP_SHIFT), 1)
            self.walls.append(wall)

        for coordinate in range(0, self.height + 1):
            wall = Wall(Point(LEFT_SHIFT,
                              TOP_SHIFT + coordinate * border_height), 1)
            self.walls.append(wall)

        for coordinate in range(0, self.width):
            wall = Wall(Point(LEFT_SHIFT + coordinate * border_width, 
                              TOP_SHIFT + border_height * self.height), 1)
            self.walls.append(wall)

        for coordinate in range(0, self.height + 1):
            wall = Wall(Point(LEFT_SHIFT + border_width * self.width, 
                              TOP_SHIFT + coordinate * border_height), 1)
            self.walls.append(wall)

    def init_UI(self):
        self.ui_elements = list()
        self.ui_elements.append(Text(Point(LEFT_SHIFT, 2), "health:"))
        self.ui_elements.append(Text(Point(LEFT_SHIFT, 4 + SPACE.height), "armor:"))
        self.health_bar = Text(Point(50, 2), "")
        self.armor_bar = Text(Point(50, 4 + SPACE.height), "")
        self.upper_bullets_bar = Text(Point(LEFT_SHIFT + int(self.width * 2), 1), "")
        self.lower_bullets_bar = Text(Point(LEFT_SHIFT + int(self.width * 2), 3 + SPACE.height), "")
        self.boss_bar = Text(Point(LEFT_SHIFT + int(self.width * 4.2), 4), "boss:")
        self.boss_hp = Text(Point(LEFT_SHIFT + int(self.width * 5.2), 4), "1000")

    def update_bullets(self):

        bullets = self.hero.bullets_count
        left_shift = self.upper_bullets_bar.point.x
        for dy in range(BULLET_ICON.height):
            if bullets >= 10:
                setCursorXY(left_shift + (bullets - 10) * BULLET_ICON.width + (bullets - 10), 3 + SPACE.height + dy)
            else:
                setCursorXY(left_shift + bullets * BULLET_ICON.width + bullets, 1 + dy)
            print(' ' * (BULLET_ICON.width + 1))

    def draw(self):
        Scene.draw(self)

        for element in self.ui_elements:
            element.draw()

        for element in self.walls:
            element.draw()

    def add_hero(self, tank):
        self.hero = tank
        self.dynamic_objects.append(tank)
        self.last_info = 0

    def add_base(self, base):
        self.base = base
        self.add_static_object(base)

    def add_boss(self, boss):
        self.boss = boss
        self.boss_info = boss.health
        self.add_dynamic_object(boss)

    def update_ui_bar(self):       
        self.update_ui_stats()
        for y in range(BULLET_RELOADING.height):
            dy = BULLET_RELOADING.height - y
            setCursorXY(LEFT_SHIFT + int(self.width * 3.65), 1 + y)
            if dy < ((self.hero.reloading_stage * BULLET_RELOADING.height + 1)/ Tank.RELOADING_TICKS):
                print(BULLET_RELOADING.texture[y])
            else:
                print(' ' * BULLET_RELOADING.width)
        bullets = self.hero.bullets_count
        if bullets > 10:
            self.upper_bullets_bar.draw(10 * "@")
            self.lower_bullets_bar.draw((bullets - 10) * "@")
        elif bullets > 0:
            self.upper_bullets_bar.draw(bullets * "@")
        self.last_info = self.hero.armor + self.hero.health

        if self.boss:
            self.boss_bar.draw()
            self.boss_hp.draw()

    def update_ui_stats(self):
        if self.boss and self.boss_info != self.boss.health:
            for y in range(4):
                setCursorXY(self.boss_hp.point.x, self.boss_hp.point.y + y)
                print(' ' * 22)
            self.boss_hp.draw(str(self.boss.health))
            self.boss_info = self.boss.health

        if self.last_info == self.hero.armor + self.hero.health or self.hero.health <= 0:
            return
        for y in range(SPACE.height * 2 + 2):
            setCursorXY(50, 2 + y)
            print(' ' * 15)


        self.health_bar.draw(str(self.hero.health))
        self.armor_bar.draw(str(self.hero.armor))


    def update(self):
        game_is_over = True
        for game_object in self.dynamic_objects:
            if type(game_object) == Enemy or type(game_object) == Boss:
                game_is_over = False
            game_object.update(self)

        if game_is_over:
            return GameStatus.LEVEL_END

        self.lootbox_timer += 1
        if self.lootbox_timer == 200:
            self.lootbox_timer = 0
            self.add_static_object(self.create_lootbox())
            self.static_objects[-1].draw()

        self.update_ui_bar()
        if self.hero.health <= 0 or self.base is not None and self.base.is_destroyed:
            return GameStatus.DEAD

        return GameStatus.IN_GAME

    def object_is_free(self, obj):
        for type in self.objects:
            for object in type:
                if object.is_overlaping(obj):
                    return False
        return True

    def find_empty_point(self):    
        x = LEFT_SHIFT + random.randint(1, self.width - 2) * WALL.width
        y = TOP_SHIFT + random.randint(1, self.height - 2) * WALL.height
        point = Point(x, y)
        box = Tank(point)
        if not self.object_is_free(box):
            return self.find_empty_point()
        return point


    def create_lootbox(self):
        point = self.find_empty_point()
        return random.choice([ArmorBox(point),
                                HealthBox(point),
                                BulletsBox(point)])

    def input(self, direction):
        if direction == Direction.UP:    
            self.hero.move_up(self.objects)
        elif direction == Direction.DOWN:
            self.hero.move_down(self.objects)
        elif direction == Direction.LEFT:
            self.hero.move_left(self.objects)
        elif direction == Direction.RIGHT:
            self.hero.move_right(self.objects)
        elif direction == Direction.DEFAULT:
            bullet = self.hero.shoot()
            if bullet is not None:
                self.update_bullets()
                self.dynamic_objects.append(bullet)
        elif direction == Direction.ESCAPE:
            return GameStatus.PAUSED

class UIScene(Scene):
    def __init__(self, width, height, buttons):
        Scene.__init__(self, width, height)
        self.buttons = buttons

    def update(self):
        self.draw()
        self.buttons.draw()

    def get_scene_index(self):
        return self.buttons.get_selected_button().scene_index

    def input(self, direction):
        self.buttons.clear_border()
        if direction == Direction.UP:    
            self.buttons.select_prev()
        elif direction == Direction.DOWN:
            self.buttons.select_next()
        elif direction == Direction.LEFT:
            self.buttons.select_prev()
        elif direction == Direction.RIGHT:
            self.buttons.select_next()
        elif direction == Direction.DEFAULT:
            pass
        elif direction == Direction.ENTER:
            return GameStatus.SCENE_SELECTION
        self.buttons.draw_border()

class Button:
    def __init__(self, text, scene_index):
        self.text = text
        self.scene_index = scene_index
        self.text_length = text.calculate_length()

    def draw(self):
        self.text.draw()

class ButtonList:
    def __init__(self, buttons):
        self.buttons = buttons
        self.selected_index = 0

    def get_selected_button(self):
        return self.buttons[self.selected_index]

    def draw_border(self):
        button = self.buttons[self.selected_index]
        shift = int(button.text_length // 1.5)
        setCursorXY(button.text.point.x - shift,
                    button.text.point.y + SPACE.height + 1)
        print('█' *  (shift * 2))

    def clear_border(self):
        button = self.buttons[self.selected_index]
        shift = int(button.text_length // 1.5)
        setCursorXY(button.text.point.x - shift,
                    button.text.point.y + SPACE.height + 1)
        print(' ' *  (shift * 2))

    def draw(self):
        for button_index, button in enumerate(self.buttons):
            if self.selected_index == button_index:
                self.draw_border()
            button.draw()

    def select_next(self):
        self.selected_index = (self.selected_index + 1) % len(self.buttons)

    def select_prev(self):
        self.selected_index = (self.selected_index - 1) % len(self.buttons)


class Deathmatch(GameScene):
    def __init__(self, width, height):
        GameScene.__init__(self, width, height)
        self.add_hero(Tank(Point(10, 20)))
        self.generate()
        for _ in range(3):
            self.add_dynamic_object(Enemy(self.find_empty_point()))
        self.spawner = Timer()
        self.spawner.start()

    def generate(self):
        for _ in range(20):
            self.add_path(self.find_empty_point())
        self.draw_static()

    def add_path(self, start):
        hero = Wall(start)
        self.add_dynamic_object(hero)
        for i in range(20):           
            dir = random.randint(0, 3)

            count = 3
            if random.randint(0, 99) > 20:
                obj = Wall(hero.point)
            else:
                obj = Wall(hero.point, 1)

  
            if dir == 0:
                for _ in range(count):
                    hero.move_left(self.objects)
            elif dir == 1:
                for _ in range(count):
                    hero.move_right(self.objects)
            elif dir == 2:
                for _ in range(count):
                    hero.move_up(self.objects)
            elif dir == 3:
                for _ in range(count):
                    hero.move_down(self.objects)
            
            if self.object_is_free(obj):
                self.add_static_object(obj)
        del self.objects[1][-1]

    def update(self):
        if self.spawner.elapsed() > 10000:
            self.add_dynamic_object(Enemy(self.find_empty_point()))
            self.spawner.start()
        status = GameScene.update(self)
        if status == GameStatus.LEVEL_END:
            return None
        elif status == GameStatus.DEAD:
            return GameStatus.LEVEL_END
        else:
            return status