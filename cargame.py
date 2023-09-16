import pygame
import random
from sys import exit as sys_exit
# TO DO: Add sound effect, trees graphics

pygame.init()

pygame.mixer.init()

class Game:
    FPS = 60

    def __init__(self):
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 800, 660
        self.road_w = self.SCREEN_WIDTH // 1.6
        self.roadmark_w = self.SCREEN_WIDTH // 80
        self.right_lane = self.SCREEN_WIDTH / 2 + self.road_w / 4
        self.left_lane = self.SCREEN_WIDTH / 2 - self.road_w / 4
        self.speed = 3
        self.car_lane = "R"
        self.car2_lane = "L"

        self.score = 0
        self.level = 0

        self.CLOCK = pygame.time.Clock()

        self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)

        pygame.display.set_caption("2D Car Game")

        self.game_over_font = pygame.font.SysFont("Arial", 60)
        self.score_font = pygame.font.SysFont("Arial", 30)

        # load sound effects
        self.car_crash_sound = pygame.mixer.Sound("assets/carCrash.wav")

        # load player car
        self.original_car = pygame.image.load("assets/car.png")
        self.car = pygame.transform.scale(self.original_car, (int(self.original_car.get_width() * (self.SCREEN_WIDTH / 800)),
                                                              int(self.original_car.get_height() * (self.SCREEN_HEIGHT / 600))))
        self.car_loc = self.car.get_rect()
        self.car_loc.center = self.right_lane, self.SCREEN_HEIGHT - self.car_loc.height * .5

        # load enemy car
        self.original_car2 = pygame.image.load("assets/otherCar.png")
        self.car2 = pygame.transform.scale(self.original_car2, (int(self.original_car2.get_width() * (self.SCREEN_WIDTH / 800)),
                                                                int(self.original_car2.get_height() * (self.SCREEN_HEIGHT / 600))))
        self.car2_loc = self.car2.get_rect()
        self.car2_loc.center = self.left_lane, self.SCREEN_HEIGHT * 0.2

        self.scale = self.SCREEN_HEIGHT - self.car2_loc.height

        self.game_state = "MAIN GAME"

        self.has_update_scores = False
        self.scores = []

    def main_loop(self):
        while True:
            self.event_loop()

            if self.game_state == "GAME OVER":
                self.game_over_draw()

                self.CLOCK.tick(self.FPS)
                pygame.display.update()
                continue

            # if score is greater than 5000 then move to a new level and increase the speed of enemy car
            if self.score % 5000 == 0:
                self.speed += .16
                self.level += 1
                print("Level Up!")

            speed_factor = self.SCREEN_HEIGHT / 660  # animate enemy vehicle
            self.car2_loc[1] += self.speed * speed_factor  # adding speed to change y-axis of car2_loc

            # if car2 move & disappear then, changing the loaction of new car2
            if self.car2_loc[1] > self.SCREEN_HEIGHT:
                # using random integer from 0 to 1 to appear car in random order
                if random.randint(0, 1) == 0:
                    self.car2_loc.center = self.right_lane, -200
                    self.car2_lane = 'R'
                else:
                    self.car2_loc.center = self.left_lane, -200
                    self.car2_lane = 'L'

            # If Cars collide game ends
            if self.car2_loc.colliderect(self.car_loc):
                self.car_crash_sound.play()
                self.game_state = "GAME OVER"

            self.draw()
            self.display_score()

            self.score += 1

            self.CLOCK.tick(self.FPS)
            pygame.display.update()

    def event_loop(self):
        for event in pygame.event.get():  # Event Loop
            if event.type == pygame.QUIT:
                self.quit_game()

            if event.type == pygame.KEYDOWN:
                print(True)
                if event.key in [pygame.K_a, pygame.K_LEFT] and self.car_lane == 'R':
                    # Use this line to add game over
                    # if car_lane == 'L': game_over()
                    self.car_loc = self.car_loc.move([-int(self.road_w / 2), 0])
                    self.car_lane = 'L'
                if event.key in [pygame.K_d, pygame.K_RIGHT] and self.car_lane == 'L':
                    self.car_loc = self.car_loc.move([int(self.road_w / 2), 0])
                    self.car_lane = 'R'
            if event.type == pygame.VIDEORESIZE:
                self.SCREEN_WIDTH, self.SCREEN_HEIGHT = event.w, event.h
                self.SCREEN = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)

                # Update lane positions
                self.road_w = int(self.SCREEN_WIDTH / 1.6)
                self.right_lane = self.SCREEN_WIDTH / 2 + self.road_w / 4
                self.left_lane = self.SCREEN_WIDTH / 2 - self.road_w / 4

                # Rescale the car images using the original images
                self.car = pygame.transform.scale(self.original_car, (
                    int(self.original_car.get_width() * (self.SCREEN_WIDTH / 800)), int(self.original_car.get_height() * (self.SCREEN_HEIGHT / 600))))
                self.car2 = pygame.transform.scale(self.original_car2, (
                    int(self.original_car2.get_width() * (self.SCREEN_WIDTH / 800)), int(self.original_car2.get_height() * (self.SCREEN_HEIGHT / 600))))

                # Update car rectangle positions based on the updated lane positions
                if self.car_lane == 'R':
                    self.car_loc = self.car.get_rect(center=(self.right_lane, self.SCREEN_HEIGHT * 0.8))
                else:
                    self.car_loc = self.car.get_rect(center=(self.left_lane, self.SCREEN_HEIGHT * 0.8))

                if self.car2_lane == 'R':
                    self.car2_loc = self.car2.get_rect(center=(self.right_lane, self.car2_loc.center[1]))
                else:
                    self.car2_loc = self.car2.get_rect(center=(self.left_lane, self.car2_loc.center[1]))

    def draw(self):
        """
        This is a function that draws the background of the game and is used to update the background when resized
        """

        # drawing the dark road on the center of green screen
        self.SCREEN.fill((60, 220, 0))

        pygame.draw.rect(self.SCREEN, (50, 50, 50), (self.SCREEN_WIDTH / 2 - self.road_w / 2, 0, self.road_w, self.SCREEN_HEIGHT))
        # drawing a yellow line on the center side of road
        pygame.draw.rect(self.SCREEN, (255, 240, 60), (self.SCREEN_WIDTH / 2 - self.roadmark_w / 2, 0, self.roadmark_w, self.SCREEN_HEIGHT))
        # drawing a white line on the left side of road
        pygame.draw.rect(self.SCREEN, (255, 255, 255), (self.SCREEN_WIDTH / 2 - self.road_w / 2 + self.roadmark_w * 2, 0, self.roadmark_w, self.SCREEN_HEIGHT))
        # drawing a white line on the right side of road
        pygame.draw.rect(self.SCREEN, (255, 255, 255), (self.SCREEN_WIDTH / 2 + self.road_w / 2 - self.roadmark_w * 3, 0, self.roadmark_w, self.SCREEN_HEIGHT))

        # load the car on road
        self.SCREEN.blit(self.car, self.car_loc)
        self.SCREEN.blit(self.car2, self.car2_loc)

    def display_score(self):
        self.message_display("SCORE ", self.score_font, (255, 50, 50), self.right_lane + self.road_w / 4, 20)
        self.message_display(self.score, self.score_font, (255, 50, 50), self.right_lane + self.road_w / 4, 55)

    def game_over_draw(self):
        self.SCREEN.fill((200, 200, 200))
        self.message_display("GAME OVER!", self.game_over_font, (40, 40, 40), self.SCREEN_WIDTH / 2, 330)
        self.message_display("FINAL SCORE ", self.score_font, (80, 80, 80), self.SCREEN_WIDTH / 2 - 100, 230)
        self.message_display(self.score, self.score_font, (80, 80, 80), self.SCREEN_WIDTH / 2 + 100, 230)

        if not self.has_update_scores:
            # Read high_scores from txt file, which are in the form of space separated numbers
            with open("high_scores.txt", "r") as hs_file:
                high_scores = hs_file.read()
                hs_file.close()

            # Convert the high score string data into list of numbers and add new score to the data
            self.scores = [int(i) for i in high_scores.split()]
            self.scores.append(self.score)

            # Sort in descending order, then keep only the top 5 scores by deleting the extra score if present
            self.scores.sort()
            self.scores.reverse()

            if len(self.scores) > 5:
                self.scores = self.scores[:5]

            # Rewrites the high_scores file with the updated high scores
            with open("high_scores.txt", "w") as hs_file:
                hs_file.write(" ".join([str(i) for i in self.scores]))

            self.has_update_scores = True

            # Printing top 5 high scores
        self.message_display("HIGH SCORES", self.score_font, (100, 100, 100), self.SCREEN_WIDTH / 2, 410)

        for idx, score in enumerate(self.scores):
            self.message_display(f"{idx + 1}. {score}", self.score_font, (100, 100, 100), self.SCREEN_WIDTH / 2, 410 + ((idx+1) * 30))
    
    @staticmethod
    def quit_game():
        sys_exit()
        quit()
    
    def message_display(self, text, font, text_col, x, y, center=True):
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
        img = font.render(str(text), True, text_col)
        img = img.convert_alpha()
    
        if center:
            # Adjust x and y to center the text
            x -= img.get_width() / 2
            y -= img.get_height() / 2
    
        self.SCREEN.blit(img, (x, y))


if __name__ == "__main__":
    game = Game()

    game.main_loop()
