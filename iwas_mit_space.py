import pgzrun
import random
from time import sleep

TITLE = "iwas mit space"
WIDTH = 1000
HEIGHT = 714

SPAWN_ITEM_INTERVAL = 0.5 # 0.5
ITEM_X_MIN = 250 #250
ITEM_X_MAX = 750 #750
FALL_SPEED = 5 #5

PLAYER_Y = 690 #690
PLAYER_SPEED = 10 #10
CATCH_RANGE_X = 80 #80
CATCH_RANGE_Y = 120 #120
IMAGE_SIZE = 128 #128

NUM_ITEM_TYPES = 5
item_images = ["alien",    #item bilder
               "meteroied_k",
               "trash",
               "black_hole",
               "spaceman"
               ] 

class GameData:
    pass

game = GameData()


    
def start_game():
    game.score = 0 #score am start 0
    game.items = [] #item liste
    game.player_items = [] #eingesamelte item liste
    game.player = Actor("raumschiff3", (WIDTH/2, PLAYER_Y))
    clock.schedule(spawn_item, SPAWN_ITEM_INTERVAL)
    sounds.dnb.play()
    
def draw():
    screen.blit("background_s",(0,0)) #hintergrundbild
    for item in game.items: #items werden angezeigt
        item.draw()
    game.player.draw() #raumschiff wird angezeigt
    for item in game.player_items: #spaceman wird nach catch angezeigt
        item.draw()
        draw_pos = HEIGHT-150
    screen.draw.text("Score: {0}".format(game.score), #score steht unten
                 centerx = WIDTH/2,
                 bottom = HEIGHT,
                 fontsize=40)
        
def update():
    if (keyboard[keys.A] or keyboard[keys.LEFT]): #bewegungen
        game.player.x -= PLAYER_SPEED
    if (keyboard[keys.D] or keyboard[keys.RIGHT]):
        game.player.x += PLAYER_SPEED
    if (game.player.x < ITEM_X_MIN):
        game.player.x = ITEM_X_MIN
    if (game.player.x > ITEM_X_MAX):
        game.player.x = ITEM_X_MAX
        
    
    for item in list(game.items): #items fallen
        item.y += FALL_SPEED
        if (item.y > HEIGHT):
            game.items.remove(item) #items werden unter dem bildschirm entfernt
        elif (abs(item.y - (game.player.y - game.stack_height)) < CATCH_RANGE_Y and
              abs(item.x - game.player.x) < CATCH_RANGE_X and item.item_type == NUM_ITEM_TYPES - 1): #spaceman kann gefangen werden
            game.items.remove(item) #spaceman wird nach catch entfernt
            game.player_items.append(item) #spaceman wird angehängt
            sounds.point.play()
            game.score = game.score + 1 #score um 1 erhöht
    game.stack_height = 1
    for item in game.player_items: #spaceman haftet am raumschiff
        item.y = game.player.y - game.stack_height
        item.x = game.player.x
    for item in list(game.items):
        if item.colliderect(game.player): #items kollidieren 
            hit() #hit wird ausgeführt
        
        
def spawn_item(): #spawnt items und lässt sie random fallen
    item_type = random.randint(0, NUM_ITEM_TYPES-1) 
    new_item = Actor(item_images[item_type], (random.randint(ITEM_X_MIN, ITEM_X_MAX),50))
    new_item.item_type = item_type
    game.items.append(new_item)
    clock.schedule(spawn_item, SPAWN_ITEM_INTERVAL)

def hit(): #wenn Raumschiff getroffen wird
    sounds.explosion.play()
    print ("GAME OVER")
    sleep(1)
    file = open("highscore.txt", "r") #öffnet highscore.txt zum lesen
    score = file.read() #liest highscore
    print("Highscore:", score) 
    file.close()
    
    if (game.score > int(score)): #wenn neuer highscore
        file = open("highscore.txt", "w") #öffnet highscore.txt zum schreiben
        score = str(game.score) #schreibt neuen highscore in txt
        print("New Highscore!!!:", score)
        file.write(score)
        file.close() 
        
    print("Score:",game.score)
    
    quit()
    
    
start_game()
pgzrun.go()