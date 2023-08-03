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

running = True
screen = pygame.display.set_mode(size)

pygame.display.set_caption("2D Car Game")

game_over_font = pygame.font.SysFont("Arial", 60)
score_font = pygame.font.SysFont("Arial", 30)
def message_display(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    img = img.convert_alpha()
    screen.blit(img, (x, y))

def game_over():
    message_display("GAME OVER!", game_over_font, (128, 128, 128), 225, 330)
    message_display("FINAL SCORE ", score_font, (100, 100, 100), 270, 230)
    message_display(str(newScore), score_font, (100, 100, 100), 450, 230)

def score():
    message_display("SCORE ", score_font, (100, 100, 100),680, 20)
    message_display(str(newScore), score_font, (100, 100, 100),690, 55)


#apply changes
pygame.display.update()

# load player car
car = pygame.image.load("assets/car.png")
car_loc = car.get_rect()
car_loc.center = right_lane, height * 0.8

# load enemy car
car2 = pygame.image.load("assets/otherCar.png")
car2_loc = car2.get_rect()
car2_loc.center = left_lane, height * 0.2

# tracking the score
newScore = 0
level = 0

while running:
    screen.fill((60, 220, 0))
    # if score is greater than 5000 then move to a new level and increase the speed of enemy car
    newScore += 1
    if newScore % 5000 == 0:
        speed += .16
        level += 1
        print("Level Up!")
    # animate enemy vehicle
    # adding speed to change y-axis of car2_loc
    car2_loc[1] += speed
    # if car2 move & disappear then, changing the loaction of new car2
    if car2_loc[1] > height:
        # using random integer from 0 to 1 to appear car in random order
        if random.randint(0, 1) == 0:
            car2_loc.center = right_lane, -200
        else:
            car2_loc.center = left_lane, -200

    # game ending logic
    # if both car in same location in x-axis and y-axis then the will collide
    # we subtracting 250 from y because even if the front of car touches another car they actually collide
    if car_loc[0] == car2_loc[0] and car2_loc[1] > car_loc[1] - 250:
        print("GAME OVER!")
        game_over()
        pygame.display.update()
        break

    # if the car get out of the road the game will be over
    if car_loc[0] == width / 2 + road_w / 2 or car_loc[0] == width / 2 - road_w:
        print("GAME OVER!")
        game_over()
        pygame.display.update()
        break       
        

    # event listener
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key in [K_a, K_LEFT]:
                car_loc = car_loc.move([-int(road_w / 2), 0])
            if event.key in [K_d, K_RIGHT]:
                car_loc = car_loc.move([int(road_w / 2), 0])

    # darw graphics
    # drawing the dark road on the center of green screen
    pygame.draw.rect(screen, (50, 50, 50), (width / 2 - road_w / 2, 0, road_w, height))
    # drawing a yellow line on the center side of road
    pygame.draw.rect(screen, (255, 240, 60), (width / 2 - roadmark_w / 2, 0, roadmark_w, height))
    # drawing a white line on the left side of road
    pygame.draw.rect(screen, (255, 255, 255), (width / 2 - road_w / 2 + roadmark_w * 2, 0, roadmark_w, height))
    # drawing a white line on the right side of road
    pygame.draw.rect(screen, (255, 255, 255), (width / 2 + road_w / 2 - roadmark_w * 3, 0, roadmark_w, height))

    # load the car on road
    screen.blit(car, car_loc)
    screen.blit(car2, car2_loc)
    score()
    pygame.display.update()
    

    if not running:
        game_over()
        pygame.display.update()
        break




time.sleep(2)
pygame.quit()
