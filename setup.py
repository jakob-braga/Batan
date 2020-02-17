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


def split_text(text):
    i = 0
    last_space = 0
    low = []
    for char in text:
        if last_space == 0 and char == " ":
            low.append(text[last_space:i + 1])
            last_space = i
        elif char == " ":
            low.append(text[last_space + 1:i + 1])
            last_space = i
        elif i == len(text) - 1:
            low.append(text[last_space + 1:])
        i += 1
    return low


def back_to_text(low):
    text = ""
    for word in low:
        text = text + word
    return text
