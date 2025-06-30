import unittest
import pygame
from game_logic import Game

class TestApp(unittest.TestCase):
    """
    Unit tests for Pygame Racing Car app functionalities including event loop and game over functions are behaving as expected.
    """
    def setUp(self):
        """
        Initialize pygame
        """
        pygame.init()
        self.game = Game()

    def tearDown(self):
        """
        Clean up the test environment by quit the pygame
        """
        pygame.quit()

    def test_event_loop_speed_changing(self):
        initial_speed = self.game.speed

        # check if pressing down the W key increases car's speed
        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_w))
        self.game.event_loop()
        self.assertEqual(self.game.speed, initial_speed + 5)

        # check the speed returns when release the key
        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_w))
        self.game.event_loop()
        self.assertEqual(self.game.speed, initial_speed)

    def test_game_over(self):
        self.assertEqual(self.game.game_state, "MAIN GAME")

        # make both cars(player's car and enemy car) have same location
        self.game.car2_loc.center = self.game.car_loc.center

        # check they are crashed
        if self.game.car2_loc.colliderect(self.game.car_loc):
            self.game.game_state = "GAME OVER"

        self.assertEqual(self.game.game_state, "GAME OVER")

if __name__ == '__main__':
    unittest.main()
