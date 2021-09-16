import pgzrun
import random


TITLE = "iwas mit space"
WIDTH = 1000
HEIGHT = 714

SPAWN_ITEM_INTERVAL = 0.5 # 0.5
ITEM_X_MIN = 250
ITEM_X_MAX = 750
FALL_SPEED = 5

PLAYER_Y = 690
PLAYER_SPEED = 10
CATCH_RANGE_X = 80
CATCH_RANGE_Y = 120
IMAGE_SIZE = 128

NUM_ITEM_TYPES = 5
item_images = ["alien",
               "meteroied_k",
               "trash",
               "black_hole",
               "spaceman"
               ] 

class GameData:
    pass

game = GameData()

def start_game():
    game.score = 0
    game.items = []
    game.player_items = []
    game.player = Actor("raumschiff3", (WIDTH/2, PLAYER_Y))
    clock.schedule(spawn_item, SPAWN_ITEM_INTERVAL)
    
def draw_sequence(sequence, pos_x, pos_y):
    screen.draw.text(" {0} points".format(),
      centerx = pos_x + IMAGE_SIZE/2,
      centery = pos_y + 80,
      color="orange")
    for item_type in sequence:
        screen.blit(item_images[item_type], (pos_x, pos_y))
        pos_y -= item_heights[item_type]

def draw():
    screen.blit("background_s",(0,0))
    for item in game.items:
        item.draw()
    game.player.draw()
    for item in game.player_items:
        item.draw()
        draw_pos = HEIGHT-150
    screen.draw.text("Score: {0}".format(game.score),
                 centerx = WIDTH/2,
                 bottom = HEIGHT,
                 fontsize=40)
        
def update():
    if (keyboard[keys.A] or keyboard[keys.LEFT]):
        game.player.x -= PLAYER_SPEED
    if (keyboard[keys.D] or keyboard[keys.RIGHT]):
        game.player.x += PLAYER_SPEED
    if (game.player.x < ITEM_X_MIN):
        game.player.x = ITEM_X_MIN
    if (game.player.x > ITEM_X_MAX):
        game.player.x = ITEM_X_MAX
    
    for item in list(game.items):
        item.y += FALL_SPEED
        if (item.y > HEIGHT):
            game.items.remove(item)
        elif (abs(item.y - (game.player.y - game.stack_height)) < CATCH_RANGE_Y and
              abs(item.x - game.player.x) < CATCH_RANGE_X and item.item_type == NUM_ITEM_TYPES - 1):
            game.items.remove(item)
            game.player_items.append(item)
            game.score = game.score + 1
    game.stack_height = 1
    for item in game.player_items:
        item.y = game.player.y - game.stack_height
        item.x = game.player.x
    for item in list(game.items):
        if item.colliderect(game.player):
            hit()
        
        
def spawn_item():
    item_type = random.randint(0, NUM_ITEM_TYPES-1)
    new_item = Actor(item_images[item_type], (random.randint(ITEM_X_MIN, ITEM_X_MAX),50)) #lässt random fallen
    new_item.item_type = item_type
    game.items.append(new_item)
    clock.schedule(spawn_item, SPAWN_ITEM_INTERVAL)

def hit():
    print ("GAME OVER")
    file = open("highscore.txt", "r")
    score = file.read()
    print("Highscore:", score)
    file.close()
    
    if (game.score > int(score)):
        file = open("highscore.txt", "w")
        score = str(game.score)
        print("New Highscore!!!:", score)
        file.write(score)
        file.close()
        
    print("Score:",game.score)
        
    quit()
    
    
start_game()
pgzrun.go()