from GameObject import *
import random
import SceneManager
import math

class Bullet(GameObject):
    def __init__(self, point : Point, direction):
        GameObject.__init__(self, point)
        self.direction = direction
        self.add_texture(BULLET)

    def draw(self):
        GameObject.draw(self, 0)

    def update(self, scene):
        if self.move(scene.objects):
            self.draw()

    def move(self, game_objects):
        self.clear()
        object = GameObject.try_move(self, game_objects)
        if object is None:
            GameObject.move(self)  
            object = GameObject.try_move(self, game_objects)
            if object is None:
                GameObject.move(self)  
                return True
            return True
        elif object is True:
            game_objects[1].remove(self)
            self.clear()
        else:
            game_objects[1].remove(self)
            self.clear()
            object_type = type(object)
            if object_type is SceneManager.Wall and object.type == 1:
                return False
            elif object_type is Enemy:
                object.take_damage(game_objects[1])
            elif object_type is Tank:
                object.take_damage(game_objects[1])
            elif object_type is Boss:
                object.take_damage(game_objects[1])
            elif object_type is Bullet:
                game_objects[1].remove(object)
                object.clear()
            else:
                game_objects[0].remove(object)
                object.clear()
            return False

class Tank(GameObject):
    MAX_BULLETS_COUNT = 20
    MAX_HEALTH = 100
    RELOADING_TICKS = 20

    def __init__(self, point : Point):
        GameObject.__init__(self, point)
        self.direction = Direction.UP
        self.add_texture(TANK_UP_FRAME)
        self.add_texture(TANK_DOWN_FRAME)
        self.add_texture(TANK_LEFT_FRAME)
        self.add_texture(TANK_RIGHT_FRAME)
        self.health = Tank.MAX_HEALTH
        self.armor = 50
        self.bullets_count = Tank.MAX_BULLETS_COUNT
        self.reloading_stage = Tank.RELOADING_TICKS

    def take_damage(self, tanks):
        damage = random.randint(25, 60)
        #damage = 1000
        self.armor -= damage
        if self.armor <= 0:
            self.health += self.armor
            self.armor = 0
        if self.health <= 0:
            self.clear()
            tanks.remove(self)

    def draw(self):
        GameObject.draw(self, self.direction - 1)

    def update(self, scene):
        self.draw()
        if self.reloading_stage != Tank.RELOADING_TICKS and self.bullets_count != 0:
            self.reloading_stage += 1

    def move(self):
        self.clear()
        GameObject.move(self)
        self.draw()

    def use_loot(self, loot):
        if loot.type == "BULLETS":
            self.bullets_count = Tank.MAX_BULLETS_COUNT
        elif loot.type == "ARMOR":
            self.armor = min(self.armor + 70, 100)
        elif loot.type == "HP":
            self.health = min(self.health + 70, 100)

    def shoot(self):
        if self.reloading_stage != Tank.RELOADING_TICKS or self.bullets_count == 0:
            return None
         
        if self.direction == Direction.UP:
            point = self.point.right(2)
        elif self.direction == Direction.DOWN:
            point = self.point.right(2).lower(4)
        elif self.direction == Direction.LEFT:
            point = self.point.lower(2)
        elif self.direction == Direction.RIGHT:
            point = self.point.right(4).lower(2)

        self.bullets_count -= 1
        self.reloading_stage = 0

        return Bullet(point, self.direction)

class Base(GameObject):
    def __init__(self, point : Point):
        GameObject.__init__(self, point)
        self.direction = Direction.DEFAULT
        self.add_texture(BASE)
        self.is_destroyed = False

    def clear(self):
        self.is_destroyed = True
        GameObject.clear(self)

    def draw(self):
        GameObject.draw(self, self.direction)

class Enemy(Tank):
    def __init__(self, point, is_hunter=False):
        Tank.__init__(self, point)
        self.textures.clear()
        self.add_texture(ENEMY_UP_FRAME)
        self.add_texture(ENEMY_DOWN_FRAME)
        self.add_texture(ENEMY_LEFT_FRAME)
        self.add_texture(ENEMY_RIGHT_FRAME)
        self.moves = 0
        self.dir = 0
        self.move_counter = 0
        self.range = 1
        self.is_stuck = False
        self.is_hunter = is_hunter


    def update_direction(self, hero):
        move_stack = []
        if self.point.y < hero.point.y:
            move_stack.append(Direction.DOWN)
        if self.point.y > hero.point.y:
            move_stack.append(Direction.UP)
        if self.point.x < hero.point.x:
            move_stack.append(Direction.RIGHT)
        if self.point.x > hero.point.x:
            move_stack.append(Direction.LEFT)

        for move in move_stack:
            if move == Direction.opposite(self.direction):
                move_stack.remove(move)
                break
        if len(move_stack) == 0:
            move_stack.append(Direction.LEFT)
            move_stack.append(Direction.RIGHT) 
            move_stack.append(Direction.UP) 
            move_stack.append(Direction.DOWN)

        self.direction = random.choice(move_stack)

    def AI(self, scene):
        if self.is_hunter:
            hero = scene.base
        else:
            hero = scene.hero
        game_objects = scene.objects

        self.move_counter += 1
        if self.move_counter == self.range:
            self.update_direction(hero)
            self.range = random.randint(20, 50)
            self.move_counter = 0


        if self.is_stuck:
            self.direction = random.choice([Direction.LEFT, Direction.RIGHT,
                    Direction.DOWN, Direction.UP])
            self.range = random.randint(3, 5)
            self.is_stuck = False
            bullet = self.shoot()
            if bullet:
                scene.dynamic_objects.append(bullet)
            self.move_counter = 0


        object = self.try_move(game_objects)
        if not object:
            x = self.point.x
            y = self.point.y
            self.move()
            if self.point.x == x and self.point.y == y:
                self.is_stuck = True
        else:
             self.is_stuck = True

    def is_same_level(self, hero):
        if self.direction == Direction.UP and self.is_on_same_x(hero):
            return self.point.y > hero.point.y
        elif self.direction == Direction.DOWN and self.is_on_same_x(hero):
            return self.point.y < hero.point.y
        elif self.direction == Direction.LEFT and self.is_on_same_y(hero):
            return self.point.x > hero.point.x
        elif self.direction == Direction.RIGHT and self.is_on_same_y(hero):
            return self.point.x < hero.point.x

    def is_on_same_y(self, hero):
        return math.fabs(self.point.y - hero.point.y) <= TANK_UP_FRAME.height

    def is_on_same_x(self, hero):
        return math.fabs(self.point.x - hero.point.x) <= TANK_UP_FRAME.width

    def update(self, scene):        
        Tank.update(self, scene) 
        self.AI(scene)
        if self.is_hunter:
            hero = scene.base
        else:
            hero = scene.hero
        if self.is_same_level(hero):
            bullet = self.shoot()
            if bullet:
                scene.dynamic_objects.append(bullet)


class Boss(Enemy):
    def __init__(self, point):
        Enemy.__init__(self, point)
        self.textures.clear()
        self.add_texture(BOSS)
        self.health = 1000
        self.armor = 0
        self.regen = 0

    def draw(self):
        GameObject.draw(self, 0)
     
    def shoot(self):
        if self.reloading_stage != Tank.RELOADING_TICKS or self.bullets_count == 0:
            return None
        points = list()
        points.append(Bullet(self.point.right(4), Direction.UP))
        points.append(Bullet(self.point.right(6.5), Direction.UP))
        points.append(Bullet(self.point.right(9), Direction.UP))

        points.append(Bullet(self.point.lower(4), Direction.LEFT))
        points.append(Bullet(self.point.lower(7), Direction.LEFT))
        points.append(Bullet(self.point.lower(10), Direction.LEFT))

        points.append(Bullet(self.point.right(13).lower(4), Direction.RIGHT))
        points.append(Bullet(self.point.right(13).lower(7), Direction.RIGHT))
        points.append(Bullet(self.point.right(13).lower(10), Direction.RIGHT))

        points.append(Bullet(self.point.right(4).lower(14), Direction.DOWN))
        points.append(Bullet(self.point.right(6.5).lower(14), Direction.DOWN))
        points.append(Bullet(self.point.right(9).lower(14), Direction.DOWN))

        self.reloading_stage = 0

        return points

    def update(self, scene):        
        Tank.update(self, scene) 
        self.regen += 1
        if self.regen == 20:
            self.health = min(self.health + 1, 1000)
            self.regen = 0
        self.AI(scene)
        bullets = self.shoot()
        if bullets:
            for bullet in bullets:
                scene.dynamic_objects.append(bullet)