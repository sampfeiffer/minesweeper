import pygame

class Display():
    margin_side = 20
    margin_top = 40
    margin_bottom = 65
    spot_size = 19
    rect_size = spot_size + 1
    min_screen_width = 250

    frame_rate = 50

    pygame.font.init()
    basic_font = pygame.font.SysFont(None, 24)
    counter_font = pygame.font.SysFont(None, 48)
