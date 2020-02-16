import pygame


def fade_out(window, window_size):
    fadeout = pygame.Surface(window_size)
    fadeout.fill((0, 0, 0))
    alpha = 0
    while alpha < 300:
        fadeout.set_alpha(alpha)
        alpha = alpha + 10
        window.blit(fadeout, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)


def dim(window, window_size):
    dim_surf = pygame.Surface(window_size)
    dim_surf.fill((0, 0, 0))
    dim_surf.set_alpha(120)
    window.blit(dim_surf, (0, 0))

