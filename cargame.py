import pygame
from pygame.locals import *
import random
import time
# TO DO: Add sound effect, trees graphics, on-screen score

pygame.init()

# variables
size = width, height = (800, 660)
road_w = int(width / 1.6)
roadmark_w = int(width / 80)
right_lane = width / 2 + road_w / 4
left_lane = width / 2 - road_w / 4
speed = 1
car_lane = 'R'
car2_lane = 'L'

running = True
screen = pygame.display.set_mode(size, pygame.RESIZABLE)

pygame.display.set_caption("2D Car Game")

game_over_font = pygame.font.SysFont("Arial", 60)
score_font = pygame.font.SysFont("Arial", 30)
def message_display(text, font, text_col, x, y, center = True): #Added function comments
    """
    This is a function which displays text with the desired specifications

    param: text: This is the Text to display
    type: str

    param: font: The font that will be used
    type: Font

    param: text_col: The color that the text will be in (R, G, B) format
    type: tuple

    param: x: The x coordinate of the text
    type: int

    param: y: The y coordinate of the text
    type: int

    param: center: Determines if the text is centered 
    type: bool
    """
    img = font.render(text, True, text_col)
    img = img.convert_alpha()

    if center:
        # Adjust x and y to center the text
        x -= img.get_width() / 2
        y -= img.get_height() / 2

    screen.blit(img, (x, y))

def game_over():
    print("GAME OVER!")
    message_display("GAME OVER!", game_over_font, (128, 128, 128), width/2, 330)
    message_display("FINAL SCORE ", score_font, (100, 100, 100), width/2 - 100, 230)
    message_display(str(newScore), score_font, (100, 100, 100), width/2 + 100, 230)
    pygame.display.update()
    # Read high_scores from txt file, which are in the form of space separated numbers
    hs_file = open('high_scores.txt', 'r')
    high_scores = hs_file.read()
    hs_file.close()

    # Convert the high score string data into list of numbers and add new score to the data
    scores = [int(x) for x in high_scores.split()]
    scores.append(newScore)

    # Sort in descending order, then keep only the top 5 scores by deleting the extra score if present
    scores.sort()
    scores.reverse() 
    if (len(scores) > 5):
        scores.remove(scores[5])

    # Printing top 5 high scores 
    message_display("HIGH SCORES ", score_font, (100, 100, 100), width/2, 410)
    score_index = 1
    for score in scores:
        message_display(str(score_index) + '. ' + str(score), score_font, (100, 100, 100), width/2, 410 + (score_index * 30))
        score_index += 1

    # Rewrite the high_scores file with the updated high scores
    hs_file = open('high_scores.txt', 'w')
    for score in scores:
        hs_file.write(str(score) + ' ')
    #Updates Display
    pygame.display.update()
    #Timer to allow user to see the Game Over
    pygame.time.delay(2000)
    exit()

def score():
    message_display("SCORE ", score_font, (100, 100, 100), right_lane + road_w/4, 20)
    message_display(str(newScore), score_font, (100, 100, 100), right_lane + road_w/4, 55)


#apply changes
pygame.display.update()

# load player car
original_car = pygame.image.load("assets/car.png")
car = pygame.transform.scale(original_car, (int(original_car.get_width()*(width/800)), int(original_car.get_height()*(height/600))))
car_loc = car.get_rect()
car_loc.center = right_lane, height - car_loc.height*.5

# load enemy car
original_car2 = pygame.image.load("assets/otherCar.png")
car2 = pygame.transform.scale(original_car2, (int(original_car2.get_width()*(width/800)), int(original_car2.get_height()*(height/600))))
car2_loc = car2.get_rect()
car2_loc.center = left_lane, height * 0.2

scale = height - car2_loc.height
print(scale)
# tracking the score
newScore = 0
level = 0

def draw_graphics():
    """
    This is a function that draws the background of the game and is used to update the background when resized
    """
    size = width, height
    road_w = int(width / 1.6)
    roadmark_w = int(width / 80)
    right_lane = width / 2 + road_w / 4
    left_lane = width / 2 - road_w / 4


    # drawing the dark road on the center of green screen
    pygame.draw.rect(screen, (50, 50, 50), (width / 2 - road_w / 2, 0, road_w, height))
    # drawing a yellow line on the center side of road
    pygame.draw.rect(screen, (255, 240, 60), (width / 2 - roadmark_w / 2, 0, roadmark_w, height))
    # drawing a white line on the left side of road
    pygame.draw.rect(screen, (255, 255, 255), (width / 2 - road_w / 2 + roadmark_w * 2, 0, roadmark_w, height))
    # drawing a white line on the right side of road
    pygame.draw.rect(screen, (255, 255, 255), (width / 2 + road_w / 2 - roadmark_w * 3, 0, roadmark_w, height))


while running:
    screen.fill((60, 220, 0))
    # if score is greater than 5000 then move to a new level and increase the speed of enemy car
    newScore += 1
    if newScore % 5000 == 0:
        speed += .16
        level += 1
        print("Level Up!")
    # animate enemy vehicle
    speed_factor = height/660
    # adding speed to change y-axis of car2_loc
    car2_loc[1] += speed * speed_factor
    # if car2 move & disappear then, changing the loaction of new car2
    if car2_loc[1] > height:
        # using random integer from 0 to 1 to appear car in random order
        if random.randint(0, 1) == 0:
            car2_loc.center = right_lane, -200
            car2_lane = 'R'
        else:
            car2_loc.center = left_lane, -200
            car2_lane = 'L'


    # game ending logic
    # New Collision using the colliderect which checks if two rects are colliding
    # If Cars collide game ends    
    if car2_loc.colliderect(car_loc): game_over()
    # Changed this You can add it back if this was the intended game function
    # You are no longer allowed to leave the road  

    # event listener
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key in [K_a, K_LEFT] and car_lane == 'R':
                # Use this line to add game over
                # if car_lane == 'L': game_over()
                car_loc = car_loc.move([-int(road_w / 2), 0])
                car_lane = 'L'
            if event.key in [K_d, K_RIGHT] and car_lane == 'L':
                car_loc = car_loc.move([int(road_w / 2), 0])
                car_lane = 'R'
        if event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            
            # Update lane positions
            road_w = int(width / 1.6)
            right_lane = width / 2 + road_w / 4
            left_lane = width / 2 - road_w / 4

            # Rescale the car images using the original images
            car = pygame.transform.scale(original_car, (int(original_car.get_width()*(width/800)), int(original_car.get_height()*(height/600))))
            car2 = pygame.transform.scale(original_car2, (int(original_car2.get_width()*(width/800)), int(original_car2.get_height()*(height/600))))

            # Update car rectangle positions based on the updated lane positions
            if car_lane == 'R':
                car_loc = car.get_rect(center=(right_lane, height * 0.8))
            else:
                car_loc = car.get_rect(center=(left_lane, height * 0.8))

            if car2_lane == 'R':
                car2_loc = car2.get_rect(center=(right_lane, car2_loc.center[1]))
            else:
                car2_loc = car2.get_rect(center=(left_lane, car2_loc.center[1]))


            draw_graphics()



    
    draw_graphics()
    # load the car on road
    screen.blit(car, car_loc)
    screen.blit(car2, car2_loc)
    score()
    pygame.display.update()
    

    if not running: game_over()

