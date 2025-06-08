import pygame

def draw(game, event_updater_counter):
    """
    This is a function that draws the background of the game and is
    used to update the background when resized
    For moving the yellow dashed line on the road, several rect are drawn
    and then moved with the event_updater_counter variable.
    Once the event_update_counter reaches 30, the rects are reset to their
    original positions and the process is repeated.
    """

    # drawing the dark road on the center of green screen
    game.SCREEN.fill(game.GRASS_COLOR)

    pygame.draw.rect(
        game.SCREEN,
        game.DARK_ROAD_COLOR,
        (
            game.SCREEN_WIDTH / 2 - game.road_w / 2,
            0,
            game.road_w,
            game.SCREEN_HEIGHT,
        ),
    )

    # drawing the yellow dashed line on the center of dark road
    num_yellow_lines = 11  # 10 + 1 moving in the borders of the screen
    # event_updater_counter is used to move the yellow dashed line
    line_positions = [
        (
            game.SCREEN_WIDTH / 2 - game.roadmark_w / 2,
            # be careful changing this values, it may cause the lines
            # to not be drawn correctly
            # line speed is 75% of car2 speed
            int(
                (game.SCREEN_HEIGHT / 20
                 + 2 * game.SCREEN_HEIGHT / 20 * num_line
                 + game.speed * game.speed_factor * event_updater_counter * 0.75)
                % game.SCREEN_HEIGHT / 10 * 11
                - game.SCREEN_HEIGHT / 20
            ),
            game.roadmark_w,
            game.SCREEN_HEIGHT / 20,
        )
        for num_line in range(num_yellow_lines)
    ]

    for line_position in line_positions:
        pygame.draw.rect(
            game.SCREEN,
            game.YELLOW_LINE_COLOR,
            line_position,
        )

    # drawing a white line on the left side of road
    pygame.draw.rect(
        game.SCREEN,
        game.WHITE_LINE_COLOR,
        (
            game.SCREEN_WIDTH / 2 - game.road_w / 2 + game.roadmark_w * 2,
            0,
            game.roadmark_w,
            game.SCREEN_HEIGHT,
        ),
    )
    # drawing a white line on the right side of road
    pygame.draw.rect(
        game.SCREEN,
        (255, 255, 255),
        (
            game.SCREEN_WIDTH / 2 + game.road_w / 2 - game.roadmark_w * 3,
            0,
            game.roadmark_w,
            game.SCREEN_HEIGHT,
        ),
    )

    # load the car on road
    game.SCREEN.blit(game.car, game.car_loc)
    game.SCREEN.blit(game.car2, game.car2_loc)