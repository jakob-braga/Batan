import pygame


class Button:
    def __init__(self, text, x, y, call):
        self.text = text
        self.x = x
        self.y = y
        self.active = False
        self.width = 120
        self.height = 50
        self.data = call
        self.clicked = False
        self.click_timer = 0

    def draw(self, win):
        font = pygame.font.SysFont("calibri", 20)
        text = font.render(self.text, 1, (255, 255, 255))
        text_x = self.x + round((self.width - text.get_width()) / 2)
        text_y = self.y + round((self.height - text.get_height()) / 2)
        win.blit(text, (text_x, text_y))

    def click_check(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height and self.active:
            return True
        else:
            return False

    def click(self):
        self.clicked = True
        self.active = False

    def click_timer_update(self):
        if self.click_timer == 5:
            self.click_timer = 0
            self.clicked = False
            self.active = True
        else:
            self.click_timer += 1
