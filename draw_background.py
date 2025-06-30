import pygame

class DrawBackground:
    def __init__(self, game):
        self.game = game

    def draw(self, event_updater_counter):
        """
        This is a function that draws the background of the game and is
        used to update the background when resized
        For moving the yellow dashed line on the road, several rect are drawn
        and then moved with the event_updater_counter variable.
        Once the event_update_counter reaches 30, the rects are reset to their
        original positions and the process is repeated.
        """
        g = self.game
        # drawing the dark road on the center of green screen
        g.SCREEN.fill(g.GRASS_COLOR)

        pygame.draw.rect(
            g.SCREEN,
            g.DARK_ROAD_COLOR,
            (
                g.SCREEN_WIDTH / 2 - g.road_w / 2,
                0,
                g.road_w,
                g.SCREEN_HEIGHT,
            ),
        )

        # drawing the yellow dashed line on the center of dark road
        num_yellow_lines = 11  # 10 + 1 moving in the borders of the screen
        # event_updater_counter is used to move the yellow dashed line
        line_positions = [
            (
                g.SCREEN_WIDTH / 2 - g.roadmark_w / 2,
                # be careful changing this values, it may cause the lines
                # to not be drawn correctly
                # line speed is 75% of car2 speed
                int(
                    (g.SCREEN_HEIGHT / 20
                     + 2 * g.SCREEN_HEIGHT / 20 * num_line
                     + g.speed * g.speed_factor * event_updater_counter * 0.75)
                    % g.SCREEN_HEIGHT / 10 * 11
                    - g.SCREEN_HEIGHT / 20
                ),
                g.roadmark_w,
                g.SCREEN_HEIGHT / 20,
            )
            for num_line in range(num_yellow_lines)
        ]

        for line_position in line_positions:
            pygame.draw.rect(
                g.SCREEN,
                g.YELLOW_LINE_COLOR,
                line_position,
            )

        # drawing a white line on the left side of road
        pygame.draw.rect(
            g.SCREEN,
            g.WHITE_LINE_COLOR,
            (
                g.SCREEN_WIDTH / 2 - g.road_w / 2 + g.roadmark_w * 2,
                0,
                g.roadmark_w,
                g.SCREEN_HEIGHT,
            ),
        )
        # drawing a white line on the right side of road
        pygame.draw.rect(
            g.SCREEN,
            (255, 255, 255),
            (
                g.SCREEN_WIDTH / 2 + g.road_w / 2 - g.roadmark_w * 3,
                0,
                g.roadmark_w,
                g.SCREEN_HEIGHT,
            ),
        )

        # load the car on road
        g.SCREEN.blit(g.car, g.car_loc)
        g.SCREEN.blit(g.car2, g.car2_loc)