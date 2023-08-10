# Waddill Platt kqr2pp and Benjamin Cassett rcx7vy
"""
The general plan for our game is to make a game where the user is controlling a character. The user will attempt
to collect multiple coins on each level. Once they have collected all the coins they will progress to the next level.
Each Level may have a different background, different enemies/different number of enemies and potentially more coins.
Enemies will move after the character, but the character will always be faster than the enemies. It is possible that
the enemies will get faster as the levels get higher. There will be a health bar and the character has 3 lives, if
they hit 3 enemies than their game ends. The health bar will not reset with each level, it will carry over.

Basic Features:
User input: to move the character
Will Set xspeed and yspeed based on the arrow keys being pressed then user.move(). Might just add and subtract to x and
y coordinates though, unsure as of now
Game Over: Once 3 enemies are hit and the health bar hits 0 the game ends
if the health variable hits 0 game over screen will ensue
Graphics/Images: the character and the enemies will have custom sprites as well as the coins
uvage.from_image(), Sprites have yet to be chosen

Additional Features:
Enemies: Multiple enemies will be moving towards the character trying to make it lose health. Enemies will be held in a
list that will get added to as each level increases, there will be an if statement checking if coins have been collected
and once that has been fufilled another enemy will be appeneded to the list and spawned on the next level
Collectibles: Coins will be the main collectible and will be what is necessary to continue to higher levels. They will
be held in a list that will be refilled after all have been collected. Once one is collected that coin will be deleted
from the list, this will make it so end of level if statement will be when the len of the coins list is 0, and then it
will call a function that will refill it and add an enemy, and potentially change the background.
Collectibles: Power Ups/Health Boosts might be implemented, but we are unsure if they will be (NOT SURE HOW IT WILL BE
IMPLEMENTED OR IF IT WILL BE INCLUDED)
Health Bar: A health bar will be visible to indicate how many times an enemy can hit the user until they die. Will be
using a health function that will have an if statement using a integer variable called health that will decrease when
contact with an enemy is made. Depending on what the integer is the image of the health bar/ text will change
Multiple Levels: Once all the coins are collected on a level a new level will be made and there will be more coins to
get and more enemies --> the levels will progressively get more and more difficult. Inside of if statement where the
level ends everything will get reset and more coins and enemies will be spawned in
Sprite Animation: We may attempt to make our characters turn and face the way they are moving, as well as have the
coins flipping back and forth to make it less stationary and boring.
Using Sprite sheet and a function that will alternate them based on direction moving using xspeed. For coins might be
alternating using a hidden timer variable that will get added to every run of the tick function, alternations will happen
every half second or when timer variable % 15 == 0.
"""

import uvage, random

gamelive = True
camera = uvage.Camera(800, 600)
character = uvage.from_image(100, 300, "UFO1S.png")
health = 3
healthB = uvage.from_image(700, 550, "HealthBarFullS.png")
level = 1
enemy = {1:[uvage.from_image(400,300,"RedEnemySF.png")],
         2:[uvage.from_image(400,300,"RedEnemySF.png"),uvage.from_image(400,200,"BlueEnemySF.png")],
         3:[uvage.from_image(400,300,"RedEnemySF.png"),uvage.from_image(700,100,"BlueEnemySF.png"),
            uvage.from_image(700,500,"OrangeEnemySF.png")],
         4:[uvage.from_image(400,300,"RedEnemySF.png"),uvage.from_image(700,100,"BlueEnemySF.png"),
            uvage.from_image(700,500,"OrangeEnemySF.png"),uvage.from_image(100,500,"DPurpleEnemySF.png")],
         5:[uvage.from_image(400,300,"RedEnemySF.png"),uvage.from_image(700,100,"BlueEnemySF.png"),
            uvage.from_image(700,500,"OrangeEnemySF.png"),uvage.from_image(100,500,"DPurpleEnemySF.png"),
            uvage.from_image(100,100,"GreenEnemySF.png")]}
timer = 0
coins = {1: [uvage.from_image(700,300,"MARIOCOINS.png")],
         2: [uvage.from_image(700,200,"MARIOCOINS.png"), uvage.from_image(700,400,"MARIOCOINS.png")],
         3: [uvage.from_image(700,200,"MARIOCOINS.png"), uvage.from_image(700,400,"MARIOCOINS.png"),
             uvage.from_image(500,100,"MARIOCOINS.png")],
         4: [uvage.from_image(700,200,"MARIOCOINS.png"), uvage.from_image(700,400,"MARIOCOINS.png"),
             uvage.from_image(500,100,"MARIOCOINS.png"), uvage.from_image(500,500,"MARIOCOINS.png")],
         5: [uvage.from_image(100,100,"MARIOCOINS.png"), uvage.from_image(700,500,"MARIOCOINS.png"),
             uvage.from_image(100,500,"MARIOCOINS.png"), uvage.from_image(700,100,"MARIOCOINS.png"),
             uvage.from_image(400,300,"MARIOCOINS.png")]}
walls = [uvage.from_color(180,-10,"green",370,24),uvage.from_color(620,-10,"green",370,24),
         uvage.from_color(180,610,"green",370,24),uvage.from_color(620,610,"green",370,24),
         uvage.from_color(-25,130,"green",54,270),uvage.from_color(-25,470,"green",54,270),
         uvage.from_color(825,130,"green",54,270),uvage.from_color(825,470,"green",54,270)]
leveltext = uvage.from_text(725,25, "Level: "+str(level), 50, "white")
countdown = 60
countdowntext = uvage.from_text(25,585,str(countdown),50,"white")
score = 0
gameovertext = uvage.from_text(400,300, "GAMEOVER!", 100, "white")
gameovertextreason = 1

def usermove():
    global character
    if uvage.is_pressing("right arrow"):
        character.x += 6
    if uvage.is_pressing("left arrow"):
        character.x += -6
    if uvage.is_pressing("up arrow"):
        character.y += -6
    if uvage.is_pressing("down arrow"):
        character.y += 6

def teleport():
    global character
    if character.x <= -26:
        character.x = 825
    if character.x >= 826:
        character.x = -25
    if character.y <= -14:
        character.y = 613
    if character.y >= 614:
        character.y = -13

def enemymove():
    global enemy
    global character
    for z in enemy[level]:
        if level == 1 or level == 2:
            if character.x > z.x:
                z.x += 2
            elif character.x < z.x:
                z.x -= 2
            if character.y > z.y:
                z.y += 2
            elif character.y < z.y:
                z.y -= 2
        if level == 3 or level == 4:
            if character.x > z.x:
                z.x += 2
            elif character.x < z.x:
                z.x -= 2
            if character.y > z.y:
                z.y += 2
            elif character.y < z.y:
                z.y -= 2
        if level == 5:
            if character.x > z.x:
                z.x += 3
            elif character.x < z.x:
                z.x -= 3
            if character.y > z.y:
                z.y += 3
            elif character.y < z.y:
                z.y -= 3

def healthbar():
    global healthB, health, gamelive
    if health == 2:
        healthB = uvage.from_image(700, 550, "HealthBarMediumS.png")
    if health == 1:
        healthB = uvage.from_image(700, 550, "HealthBarLowS.png")
    if health == 0:
        healthB = uvage.from_image(700, 550, "HealthBarEmptyS.png")
        gamelive = False

def enemycontact():
    global character, enemy, health, level
    for z in enemy[level]:
        if character.touches(z):
            health -= 1
            c = random.randint(1,4)
            if c == 1:
                z.x = 750
                z.y = 550
            if c == 2:
                z.x = 50
                z.y = 50
            if c == 3:
                z.x = 750
                z.y = 50
            if c == 4:
                z.x = 50
                z.y = 550
            break

def timers():
    global timer, countdown, countdowntext, gamelive
    if timer%30 == 0:
        countdown-=1
    countdowntext = uvage.from_text(25, 585, str(countdown), 50, "white")
    if countdown == 0:
        gamelive = False

def coincontact():
    global score, coins, character, level
    for z in coins[level]:
        if z.touches(character):
            score+=1
            z.y = -200

def levelup():
    global score, level, character, countdown, leveltext, gamelive
    if score == level:
        score = 0
        level += 1
        countdown = 60
        leveltext = uvage.from_text(725, 25, "Level: " + str(level), 50, "white")
        character.x = 100
        character.y = 300
    if level == 6:
        gamelive = False

def enemyoverlapping():
    global level, enemy
    for z in enemy[level]:
        for b in enemy[level]:
            if z != b and z.touches(b):
                z.move_both_to_stop_overlapping(b)

def gameover():
    global level, countdown, gameovertext, health, gameovertextreason
    if level == 6:
        gameovertext = uvage.from_text(400, 250, "GAME OVER! YOU WIN!", 50, "blue")
        gameovertextreason = uvage.from_text(400, 350, "You Completed Every Level!", 50, "blue")
    if health == 0:
        gameovertext = uvage.from_text(400, 250, "GAME OVER! YOU LOST!", 50, "red")
        gameovertextreason = uvage.from_text(400, 350, "You Lost All Of Your Health!", 50, "red")
    if countdown == 0:
        gameovertext = uvage.from_text(400, 250, "GAME OVER! YOU LOST!", 50, "red")
        gameovertextreason = uvage.from_text(400, 350, "You Ran Out Of Time!", 50, "red")

def walloverlapping():
    global character, enemy, walls, level
    for z in walls:
        if character.touches(z):
            character.move_to_stop_overlapping(z)
        for e in enemy[level]:
            if e.touches(z):
                e.move_to_stop_overlapping(z)

def drawing():
    global character, enemy, healthB, coins, leveltext, gameovertext, gameovertextreason, walls
    if gamelive:
        camera.draw(character)
        for z in enemy[level]:
            camera.draw(z)
        camera.draw(healthB)
        for z in coins[level]:
            camera.draw(z)
        camera.draw(leveltext)
        camera.draw(countdowntext)
        for z in walls:
            camera.draw(z)
    if not gamelive:
        camera.clear("white")
        camera.draw(gameovertext)
        camera.draw(gameovertextreason)

def tick():
    global gamelive, timer
    camera.clear("black")
    if gamelive:
        usermove()
        teleport()
        enemymove()
        enemyoverlapping()
        walloverlapping()
        healthbar()
        enemycontact()
        timers()
        coincontact()
        levelup()
    if not gamelive:
        gameover()
    drawing()
    camera.display()
    timer += 1


uvage.timer_loop(30, tick)