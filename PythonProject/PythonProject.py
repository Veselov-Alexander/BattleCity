import msvcrt
import sys

from Scenes import *

class Game:
    def __init__(self, scenes):
        hide_cursor()
        self.scenes = scenes      
        self.select_scene(0)
        self.scene_before_pause = None

    def select_scene(self, scene_index):
        os.system('cls') 
        if scene_index == 12:
            self.scene = self.scene_before_pause
        elif scene_index == 13:
            self.scene = deepcopy(self.scenes[self.last_scene_index])
        elif scene_index == 3:
            self.scene = Deathmatch(width, height)
        else:
            self.scene = deepcopy(self.scenes[scene_index])
        self.scene.timer.start()
        self.scene.draw()

    def process_input(self):
        if msvcrt.kbhit():
            pressedKey = msvcrt.getch().decode('utf-8', "ignore")

            if pressedKey == 'w':    
                scene = self.scene.input(Direction.UP)
            elif pressedKey == 's':
                scene = self.scene.input(Direction.DOWN)
            elif pressedKey == 'a':
                scene = self.scene.input(Direction.LEFT)
            elif pressedKey == 'd':
                scene = self.scene.input(Direction.RIGHT)
            elif pressedKey == ' ':
                scene = self.scene.input(Direction.DEFAULT)
            elif pressedKey == chr(13):
                scene = self.scene.input(Direction.ENTER)
            elif pressedKey == chr(27):
                scene = self.scene.input(Direction.ESCAPE)
            else:
                scene = self.scene.input(Direction.ANY)

            if scene == GameStatus.LEVEL_END:
                self.scene_before_pause = self.scene
                self.select_scene(11)
            elif scene == GameStatus.PAUSED:
                self.scene_before_pause = self.scene
                self.select_scene(9)
            elif scene == GameStatus.SCENE_SELECTION:
                scene_index = self.scene.get_scene_index()
                if scene_index < len(self.scenes) and (type(self.scenes[scene_index]) is GameScene or type(self.scenes[scene_index]) is Deathmatch):
                    self.last_scene_index = scene_index
                self.select_scene(scene_index)


    def run(self):
        timer = Timer()
        timer.start()

        while True:
            self.process_input()
            if timer.elapsed() >= 50:
                timer.start()
                status = self.scene.update()
                if status == GameStatus.DEAD:
                    self.select_scene(10)
                elif status == GameStatus.LEVEL_END:          
                    score_object.update(self.last_scene_index - 5,
                                        round(self.scene.get_time() / 1000),
                                        self.scenes[11],
                                        self.scenes[4])
                    self.select_scene(11)
            self.process_input()






cols = LEFT_SHIFT * 2 + (width + 1) * BORDER.width
lines = TOP_SHIFT + (height + 1) * BORDER.height + 1


os.system("mode con cols=" + str(cols) + " lines=" + str(lines))

game = Game(scenes)
game.select_scene(0)
game.run()

