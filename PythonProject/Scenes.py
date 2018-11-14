from SceneManager import *


width, height = 38, 22

scenes = list()

#intro #0
ok_text =  Text(Point((width * WALL.width) // 2, 60), "", Text.Align.CENTER)
buttons = ButtonList([Button(ok_text, 1)])
scene = UIScene(width, height, buttons)
scene.add_static_object(Text(Point((width * WALL.width) // 2, 10), "battle city", Text.Align.CENTER))
scene.add_static_object(Text(Point((width * WALL.width) // 2, 20), "powered by: alexander", Text.Align.CENTER))
scene.add_dynamic_object(FlyingText(Point((width * WALL.width) // 2, 45), "press enter", Text.Align.CENTER))
scenes.append(scene)

#menu #1
levels_text =  Text(Point((width * WALL.width) // 2, 20), "levels", Text.Align.CENTER)
deathmatch_text = Text(Point((width * WALL.width) // 2, 30), "deathmatch", Text.Align.CENTER)
leaderboard_text = Text(Point((width * WALL.width) // 2, 40), "leaderboard", Text.Align.CENTER)
exit_text = Text(Point((width * WALL.width) // 2, 60), "exit", Text.Align.CENTER)
buttons = ButtonList([Button(levels_text, 2),
                      Button(deathmatch_text, 3),
                      Button(leaderboard_text, 4),
                      Button(exit_text, 0)])
scene = UIScene(width, height, buttons)
scenes.append(scene)

#levels #2
level_1 = Text(Point((width * WALL.width) // 2, 10), "level 1", Text.Align.CENTER)
level_2 = Text(Point((width * WALL.width) // 2, 20), "level 2", Text.Align.CENTER)
level_3 = Text(Point((width * WALL.width) // 2, 30), "level 3", Text.Align.CENTER)
boss = Text(Point((width * WALL.width) // 2, 40), "boss", Text.Align.CENTER)
back = Text(Point((width * WALL.width) // 2, 60), "back", Text.Align.CENTER)
buttons = ButtonList([Button(level_1, 5),
                      Button(level_2, 6),
                      Button(level_3, 7),
                      Button(boss, 8),
                      Button(back, 1)])
scene = UIScene(width, height, buttons)
scenes.append(scene)

#deathmatch #3
scene = GameScene(width, height)
scenes.append(scene)

#leaderboard #4
buttons = ButtonList([Button(back, 1)])
scene = UIScene(width, height, buttons)
level_1 = Text(Point((width * WALL.width) // 8, 10), "level 1:", Text.Align.LEFT)
level_2 = Text(Point((width * WALL.width) // 8, 20), "level 2:", Text.Align.LEFT)
level_3 = Text(Point((width * WALL.width) // 8, 30), "level 3:", Text.Align.LEFT)
boss_text = Text(Point((width * WALL.width) // 8, 40), "boss:", Text.Align.LEFT)
deathmatch_text = Text(Point((width * WALL.width) // 8, 50), "deathmatch:", Text.Align.LEFT)

level_1_score = Text(Point((width * WALL.width) // 8 * 6, 10), to_minutes(score_object.stats[0]), Text.Align.LEFT)
level_2_score = Text(Point((width * WALL.width) // 8 * 6, 20), to_minutes(score_object.stats[1]), Text.Align.LEFT)
level_3_score = Text(Point((width * WALL.width) // 8 * 6, 30), to_minutes(score_object.stats[2]), Text.Align.LEFT)
boss_score = Text(Point((width * WALL.width) // 8 * 6, 40), to_minutes(score_object.stats[3]), Text.Align.LEFT)
deathmatch_text_score = Text(Point((width * WALL.width) // 8 * 6, 50), to_minutes(score_object.stats[4]), Text.Align.LEFT)

scene.add_static_object(level_1)
scene.add_static_object(level_2)
scene.add_static_object(level_3)
scene.add_static_object(boss_text)
scene.add_static_object(deathmatch_text)
scene.add_static_object(level_1_score)
scene.add_static_object(level_2_score)
scene.add_static_object(level_3_score)
scene.add_static_object(boss_score)
scene.add_static_object(deathmatch_text_score)
scenes.append(scene)





#level1 #5
scene = GameScene(width, height)
scene.add_hero(Tank(Point(10, 20)))
for i in range(10): 
    scene.add_static_object(Wall(Point(LEFT_SHIFT + (i + width // 6) * WALL.width, 20)))
    scene.add_static_object(Wall(Point(LEFT_SHIFT + (i + width // 6) * WALL.width, 50)))
    scene.add_static_object(Wall(Point(LEFT_SHIFT + 125, (i + width // 6 + 1) * WALL.height)))
    scene.add_static_object(Wall(Point(LEFT_SHIFT + 110, (i + width // 6 + 1) * WALL.height)))
    scene.add_static_object(Wall(Point(LEFT_SHIFT + (i + width // 6 * 4) * WALL.width, 20)))
    scene.add_static_object(Wall(Point(LEFT_SHIFT + (i + width // 6 * 4) * WALL.width, 50)))
scene.add_dynamic_object(Enemy(Point(200, 30)))
scene.add_dynamic_object(Enemy(Point(220, 30)))
scene.add_dynamic_object(Enemy(Point(220, 50)))
scene.add_dynamic_object(Enemy(Point(70, 70)))
scenes.append(scene)

#level2 #6
scene = GameScene(width, height)

center_x = (width // 2 + 1) * BORDER.width
scene.add_dynamic_object(Enemy(Point(center_x - WALL.width * 10, 20), True))
scene.add_dynamic_object(Enemy(Point(center_x + WALL.width * 14, 35)))
scene.add_dynamic_object(Enemy(Point(center_x - WALL.width * 18, (height - 10) * BORDER.height)))
scene.add_dynamic_object(Enemy(Point(center_x + WALL.width * 10, (height - 3) * BORDER.height)))

scene.add_base(Base(Point(center_x - BASE.width // 2,
                          (height + 1) * BORDER.height + 2)))
for i in range(4):
    scene.add_static_object(Wall(Point(center_x - BASE.width, (height + i) * BORDER.height)))
    scene.add_static_object(Wall(Point(center_x + BASE.width - WALL.width, (height + i) * BORDER.height)))
    scene.add_static_object(Wall(Point(center_x + BASE.width - WALL.width - (i + 1) * WALL.width, height * BORDER.height)))
    scene.add_static_object(Wall(Point(center_x - BASE.width - WALL.width, (height + i) * BORDER.height)))
    scene.add_static_object(Wall(Point(center_x + BASE.width, (height + i) * BORDER.height)))
    scene.add_static_object(Wall(Point(center_x + BASE.width - WALL.width - (i + 1) * WALL.width, height * BORDER.height - WALL.height)))

for i in range(7):
    scene.add_static_object(Wall(Point(center_x - WALL.width * 10, (height + i - 5) * BORDER.height)))
    scene.add_static_object(Wall(Point(center_x + WALL.width * 9, (height + i - 5) * BORDER.height)))
    scene.add_static_object(Wall(Point(center_x + WALL.width * (11 + i), (height - 8) * BORDER.height)))
    scene.add_static_object(Wall(Point(center_x - WALL.width * (12 + i), (height - 8) * BORDER.height)))
    scene.add_static_object(Wall(Point(center_x + WALL.width * (8 + i), (height - 12) * BORDER.height)))
    scene.add_static_object(Wall(Point(center_x - WALL.width * (9 + i), (height - 12) * BORDER.height)))

for i in range(3):
    scene.add_static_object(Wall(Point(center_x - WALL.width * 6, (height + i - 7) * BORDER.height)))
    scene.add_static_object(Wall(Point(center_x + WALL.width * 5, (height + i - 7) * BORDER.height)))
    scene.add_static_object(Wall(Point(center_x + WALL.width * (4 - i), (height - 5) * BORDER.height)))
    scene.add_static_object(Wall(Point(center_x - WALL.width * (5 - i), (height - 5) * BORDER.height)))

scene.add_hero(Tank(Point(center_x - TANK_UP_FRAME.width // 2, (height - 3) * BORDER.height)))
scenes.append(scene)

#level3 #7
scene = GameScene(width, height)
center_x = (width // 2 + 1) * BORDER.width

for i in range(7):
    if i % 2 == 0:
        scene.add_dynamic_object(Enemy(Point(40 + (WALL.width * 4) * i, 20), False))

scene.add_dynamic_object(Enemy(Point(center_x - 15 * WALL.width, 50), False))
scene.add_dynamic_object(Enemy(Point(center_x + 15 * WALL.width, 50), True))


scene.add_base(Base(Point(center_x - BASE.width // 2,
                          (height + 1) * BORDER.height + 2)))
for i in range(4):
    scene.add_static_object(Wall(Point(center_x - BASE.width, (height + i) * BORDER.height)))
    scene.add_static_object(Wall(Point(center_x + BASE.width - WALL.width, (height + i) * BORDER.height)))
    scene.add_static_object(Wall(Point(center_x + BASE.width - WALL.width - (i + 1) * WALL.width, height * BORDER.height)))


for i in range(6):
    scene.add_static_object(Wall(Point(center_x + BASE.width - 8 * WALL.width, (height + i - 2) * BORDER.height)))
    scene.add_static_object(Wall(Point(center_x + BASE.width + WALL.width, (height + i - 2) * BORDER.height)))
    scene.add_static_object(Wall(Point(center_x + BASE.width - WALL.width - i * WALL.width, (height - 2) * BORDER.height)))


dx = center_x - WALL.width * width // 4 - 12
for i in range(width // 4 ):
    if i % 4 == 0:
        scene.add_static_object(Wall(Point(dx + (i + 1) * WALL.width, (height - 6) * BORDER.height)))
    else:
        scene.add_static_object(Wall(Point(dx + (i + 1) * WALL.width, (height - 7) * BORDER.height)))
        scene.add_static_object(Wall(Point(dx + (i + 1) * WALL.width, (height - 8) * BORDER.height)))

dx = center_x + LEFT_SHIFT
for i in range(width // 4):
    if i % 4 == 0:
        scene.add_static_object(Wall(Point(dx + (i + 1) * WALL.width, (height - 6) * BORDER.height)))
    else:
        scene.add_static_object(Wall(Point(dx + (i + 1) * WALL.width, (height - 7) * BORDER.height)))
        scene.add_static_object(Wall(Point(dx + (i + 1) * WALL.width, (height - 8) * BORDER.height)))

scene.add_hero(Tank(Point(center_x - TANK_UP_FRAME.width // 2, (height - 4) * BORDER.height)))
scenes.append(scene)

#boss #8
scene = GameScene(width, height)
scene.add_hero(Tank(Point((width * WALL.width) // 2, (height + 1) * WALL.height)))
scene.add_boss(Boss(Point((width * WALL.width) // 2 - BOSS.width // 3, 20)))
for i in range(3):
    scene.add_static_object(Wall(Point(LEFT_SHIFT + (i + 3) * WALL.width, TOP_SHIFT + (0 + 3) * WALL.height), 1))
    scene.add_static_object(Wall(Point(LEFT_SHIFT + (0 + 3) * WALL.width, TOP_SHIFT + (i + 3) * WALL.height), 1))

    scene.add_static_object(Wall(Point(LEFT_SHIFT + (width - i - 3) * WALL.width, TOP_SHIFT + (0 + 3) * WALL.height), 1))
    scene.add_static_object(Wall(Point(LEFT_SHIFT + (width - 3) * WALL.width, TOP_SHIFT + (i + 3) * WALL.height), 1))

    scene.add_static_object(Wall(Point(LEFT_SHIFT + (i + 3) * WALL.width, TOP_SHIFT + (height - 3) * WALL.height), 1))
    scene.add_static_object(Wall(Point(LEFT_SHIFT + (0 + 3) * WALL.width, TOP_SHIFT + (height - i - 3) * WALL.height), 1))

    scene.add_static_object(Wall(Point(LEFT_SHIFT + (width - i - 3) * WALL.width, TOP_SHIFT + (height - 3) * WALL.height), 1))
    scene.add_static_object(Wall(Point(LEFT_SHIFT + (width - 3) * WALL.width, TOP_SHIFT + (height - i - 3) * WALL.height), 1))

for i in range(5):
    scene.add_static_object(Wall(Point(LEFT_SHIFT + (width // 2 - 2 + i) * WALL.width, (height - 1) * WALL.height), 1))
    scene.add_static_object(Wall(Point(LEFT_SHIFT + (width // 3 - 2 - 2) * WALL.width, TOP_SHIFT + (i + 9) * WALL.height), 1))
    scene.add_static_object(Wall(Point(LEFT_SHIFT + (width // 4 * 3 + 1 + 2) * WALL.width, TOP_SHIFT + (i + 9) * WALL.height), 1))



scenes.append(scene)

#pause #9
continue_text = Text(Point((width * WALL.width) // 2, 30), "continue", Text.Align.CENTER)
exit_text = Text(Point((width * WALL.width) // 2, 40), "back to menu", Text.Align.CENTER)
buttons = ButtonList([Button(continue_text, 12),
                      Button(exit_text, 1)])
scene = UIScene(width, height, buttons)
scenes.append(scene)

#game over #10
game_over = Text(Point((width * WALL.width) // 2, 15), "game over", Text.Align.CENTER)
retry = Text(Point((width * WALL.width) // 2, 35), "retry", Text.Align.CENTER)
exit_text = Text(Point((width * WALL.width) // 2, 45), "back to menu", Text.Align.CENTER)
buttons = ButtonList([Button(retry, 13),
                      Button(exit_text, 1)])
scene = UIScene(width, height, buttons)
scene.add_static_object(game_over)
scenes.append(scene)

#level end #11
game_over = Text(Point((width * WALL.width) // 2, 15), "level complited", Text.Align.CENTER)
result_text = Text(Point((width * WALL.width) // 2, 30), "result: " + to_minutes(score_object.current_score), Text.Align.CENTER)
retry = Text(Point((width * WALL.width) // 2, 50), "retry", Text.Align.CENTER)
exit_text = Text(Point((width * WALL.width) // 2, 60), "back to menu", Text.Align.CENTER)
buttons = ButtonList([Button(retry, 13),
                      Button(exit_text, 1)])
scene = UIScene(width, height, buttons)
scene.add_static_object(game_over)
scene.add_static_object(result_text)
scenes.append(scene)

#continue #12

#retry #13