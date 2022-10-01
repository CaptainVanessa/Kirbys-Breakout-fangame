import pgzrun

from random import randint

import pygame
from ctypes import windll

WIDTH = 800
HEIGHT = 600
center = [400, 300]
bricks_animation = []

def reset():
    global brick, all_bricks
    global player, playerbig, playersmall
    global ball1, ball2, ball3, ball4
    global balls, inactive_balls
    global all_powerups
    global bg
    global youWinScreen, youLoseScreen
    global timer
    global firstclic, isTitle, screenTitle
    global isPowerups, screenPowerups
    global game_lost, game_won
    
    bg = Actor("bg1")
    bg.pos = [400, 300]

    all_bricks = []
    for y in range(15, 6*30, 30):
        for x in range(0, WIDTH, 100):
            brick = Actor("kirby_brick", anchor=["left", "top"])
            brick.pos = [x, -30]
            animate(brick, tween="out_elastic", duration= 1.5 + 0.05, pos=[x, y])
            all_bricks.append(brick)

    screenTitle = Actor("kytitle", anchor=["center", "top"])
    screenTitle.pos = [400, 0]
    animate(screenTitle, tween="out_elastic", duration= 1.5, pos=[400, 200])

    screenPowerups = Actor("powerups", anchor=["center", "top"])
    screenPowerups.pos = [400, -214]
    animate(screenPowerups, tween="out_elastic", duration= 1.5, pos=[400, 0])

    youWinScreen = Actor("you_win1")
    youWinScreen.pos = [400, 300]
    youLoseScreen = Actor("you_lose1")
    youLoseScreen.pos = [400, 300]

    player = Actor("kirby_player")
    player.pos = [400, 550]

    playersmall = Actor("kirby_player")
    playersmall.pos = [400, 635]
    animate(playersmall, tween="out_elastic", duration= 1.5, pos=[400, 550])

    playerbig = Actor("kirby_big_player")
    playerbig.pos = [400, 550]

    player = playersmall

    balls = []
    ball1 = Actor("kirby_ball1")
    ball1.pos = [400, 490]
    ball1.speed = [0, 0]
    balls.append(ball1)

    inactive_balls = []
    ball2 = Actor("kirby_ball2")
    ball2.pos = [400, 500]
    ball2.speed = [3, -3]
    inactive_balls.append(ball2)
    ball3 = Actor("kirby_ball3")
    ball3.pos = [400, 500]
    ball3.speed = [3, -3]
    inactive_balls.append(ball3)
    ball4 = Actor("kirby_ball4")
    ball4.pos = [400, 500]
    ball4.speed = [3, -3]
    inactive_balls.append(ball4)

    all_powerups = []

    music.play("main_theme")

    timer = 0

    firstclic = True

    isTitle = True
    isPowerups = True

    game_lost = False
    game_won = False

def draw():
    global screenTitle, screenPowerups
    global game_lost, game_won
    
    screen.clear()

    bg.draw()

    if timer > 0 :
        screen.draw.text(f"Big cloud for {timer:.2f} seconds", [10, 560], fontname="kirbys", color="#9977f5", fontsize=37)

    for brick in all_bricks:
        brick.draw()

    for ball in balls:
        ball.draw()
    player.draw()

    for powerup in all_powerups:
        powerup.draw()

    if isTitle:
        screenTitle.draw()

    if isPowerups:
        screenPowerups.draw()

    for brick in all_bricks:
        if brick.colliderect(player) or brick.pos[1] >= 570 or balls == []:
            screen.clear()
            if not game_lost:
                sounds.lose.play()
                game_lost = True
            youLoseScreen.draw()
            for ball in balls:
                balls.remove(ball)
            for powerup in all_powerups:
                all_powerups.remove(powerup)
    if all_bricks == []:
        screen.clear()
        if not game_won:
            sounds.win.play()
            game_won = True
        youWinScreen.draw()
        for ball in balls:
            balls.remove(ball)
        for powerup in all_powerups:
            all_powerups.remove(powerup)

def invert_horizontal_speed(ball):
    ball.speed[0] = ball.speed[0] * -1

def invert_vertical_speed(ball):
    ball.speed[1] = ball.speed[1] * -1

def update(dt):
    global timer
    global player

    for ball in balls:
        new_x = ball.pos[0] + ball.speed[0]
        new_y = ball.pos[1] + ball.speed[1]
        ball.pos = [new_x, new_y]
        if ball.right >= WIDTH or ball.left <= 0:
            invert_horizontal_speed(ball)
        if ball.top <= 0:
            invert_vertical_speed(ball)
        if ball.colliderect(player):
            sounds.jump.play()
            invert_vertical_speed(ball)

    bricks_to_remove = []
    for brick in all_bricks:
        for ball in balls:
            if ball.colliderect(brick):
                sounds.hit.play()
                invert_vertical_speed(ball)
                number = randint(1, 100)
                if number <= 20:
                    powerup = Actor("kirby_powerup_fall+1")
                    powerup.type = "powerupball"
                    powerup.pos = [brick.pos[0] + brick.size[0]/2, brick.pos[1] + brick.size[1]/2]
                    all_powerups.append(powerup)
                if number > 20 and number <= 30:
                    powerup = Actor("kirby_starx2")
                    powerup.type = "powerupspeed"
                    powerup.pos = [brick.pos[0] + brick.size[0]/2, brick.pos[1] + brick.size[1]/2]
                    all_powerups.append(powerup)
                if number > 30 and number <= 35:
                    powerup = Actor("kirby_powerup_slow")
                    powerup.type = "powerupslow"
                    powerup.pos = [brick.pos[0] + brick.size[0]/2, brick.pos[1] + brick.size[1]/2]
                    all_powerups.append(powerup)
                if number > 35 and number <= 50:
                    powerup = Actor("kirby_powerup_big")
                    powerup.type = "powerupbig"
                    powerup.pos = [brick.pos[0] + brick.size[0]/2, brick.pos[1] + brick.size[1]/2]
                    all_powerups.append(powerup)
                if brick not in bricks_to_remove:
                    bricks_to_remove.append(brick)
                    global bricks_animation
                    index = 0
                    while index < len(bricks_animation):
                        if not bricks_animation[index].running:
                            bricks_animation.pop(index)
                        else:
                            index += 1
                    
                    if not bricks_animation:
                        for brick in all_bricks:
                            animation = animate(brick, tween="in_elastic", duration= 1.5, pos=[brick.pos[0], brick.pos[1]+30])
                            bricks_animation.append(animation)
    for element in bricks_to_remove:
        all_bricks.remove(element)

    if timer > 0 :
        timer -= dt
        if timer <= 0:
            playersmall.pos = player.pos
            player = playersmall

    update_powerups()

def update_powerups():
    global timer
    global player, playerbig
    powerups_to_remove = []
    for powerup in all_powerups:
        powerup.pos = [powerup.pos[0], powerup.pos[1] + 3]
        if powerup.colliderect(player):
            powerups_to_remove.append(powerup)
            if powerup.type == "powerupball":
                if inactive_balls != []:
                    new_ball = inactive_balls[0]
                    inactive_balls.remove(new_ball)
                    sounds.wave.play()
                    balls.append(new_ball)
            elif powerup.type == "powerupspeed":
                sounds.fast.play()
                for ball in balls:
                    ball.speed[0] *= 1.5
                    ball.speed[1] *= 1.5
            elif powerup.type == "powerupslow":
                sounds.slow.play()
                for ball in balls:
                    ball.speed[0] /= 1.5
                    ball.speed[1] /= 1.5
            elif powerup.type == "powerupbig":
                timer = 5
                playerbig.pos = player.pos
                sounds.longer.play()
                player = playerbig
        if powerup.top > HEIGHT:
            powerups_to_remove.append(powerup)
    for ball in balls:
        if ball.top > HEIGHT:
            balls.remove(ball)
            inactive_balls.append(ball)
            ball.pos = [400, 500]
            ball.speed = [3, -3]

    for element in powerups_to_remove:
        all_powerups.remove(element)

def on_mouse_down():
    global firstclic
    global ball1
    global isTitle
    global isPowerups
    if firstclic == True:
        ball1.pos = [400, 490]
        ball1.speed = [3, -3]
        firstclic = False
    if isTitle:
        isTitle = False
    if isPowerups:
        isPowerups = False

def on_mouse_move(pos):
    player.pos = [pos[0], player.pos[1]]

def on_key_down(key):
    if key == keys.R:
        reset()

reset()

hwnd = pygame.display.get_wm_info()["window"]
windll.user32.MoveWindow(hwnd, 100, 100, WIDTH, HEIGHT, False)

pgzrun.go()