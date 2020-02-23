from network import Network
from button import Button
from structs import *
import random

pygame.init()

width = 1200
height = 650

clock = pygame.time.Clock()


class Client:
    def __init__(self):
        self.network = None
        self.player = None
        self.game = None
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("[B]atan")
        self.turn_change = -1
        self.placing_road_pos1 = False
        self.placing_road_pos2 = False
        self.placing_settlement = False
        self.upgrading_settlement = False
        self.temp_road = None
        self.displayed_roll = False
        self.on_first_rotate = True
        self.road_card = False
        self.moving_thief = False

        # selecting resources
        self.resources_selected = []

        # colours
        self.player_colours = {
            0: (255, 251, 50),
            1: (255, 0, 4),
            2: (0, 8, 255),
            3: (5, 181, 13),
            4: (178, 0, 142),
            5: (63, 204, 185)
        }

        # buttons
        self.buttons = []
        self.button_font = pygame.font.SysFont('times, new roman', 14)
        self.button_font_colour = (255, 255, 255)
        self.dev_card_buttons = []
        self.resource_buttons = []
        self.trade_buttons = []
        self.trade_offer_buttons = []

        # board
        self.board_val_font = pygame.font.SysFont('times, new roman', 14, True)

        # images
        self.side_bar = pygame.image.load('images/side_bar.png').convert_alpha()

        self.menu = pygame.transform.scale(self.side_bar, (800, 500))
        self.menu_x = self.side_bar.get_width() + ((width - self.side_bar.get_width() - self.menu.get_width()) // 2)
        self.menu_y = (height - self.menu.get_height()) // 2
        self.menu_center = self.menu_x + (self.menu.get_width() // 2)

        self.side_bar_width = self.side_bar.get_width()
        self.tile_dict = {
            'brick': pygame.image.load('images/tiles/brick_tile.png').convert_alpha(),
            'ore': pygame.image.load('images/tiles/ore_tile.png').convert_alpha(),
            'wheat': pygame.image.load('images/tiles/wheat_tile.png').convert_alpha(),
            'sheep': pygame.image.load('images/tiles/sheep_tile.png').convert_alpha(),
            'lumber': pygame.image.load('images/tiles/lumber_tile.png').convert_alpha(),
            'desert': pygame.image.load('images/tiles/desert_tile.png').convert_alpha(),
            'water': pygame.image.load('images/tiles/water_tile.png').convert_alpha()
        }

        # sub titles
        self.big_font = pygame.font.SysFont('times, new roman', 20, True)
        self.title_font = pygame.font.SysFont('times, new roman', 18, True)
        title_font_colour = (220, 220, 220)
        self.resource_title = self.title_font.render('Resources', True, title_font_colour)
        self.resource_title_x = (self.side_bar_width - self.resource_title.get_width()) // 2
        self.resource_title_y = 95
        self.option_title = self.title_font.render('Buy Options', True, title_font_colour)
        self.option_title_x = (self.side_bar_width - self.option_title.get_width()) // 2
        self.option_title_y = 210
        self.resource_font = pygame.font.SysFont('times, new roman', 16, True)

    def title_screen(self):
        run = True
        font = pygame.font.SysFont("times, new roman", 20)
        text = font.render("Click to Play!", 1, (225, 167, 25))
        text_x = (width - text.get_width()) // 2
        text_y = height - 75

        title_img = pygame.image.load('images/title_screen.png').convert()

        while run:
            clock.tick(60)
            self.window.blit(title_img, (0, 0))
            self.window.blit(text, (text_x, text_y))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    run = False

        fade_out(self.window, (width, height))
        self.setup_loop()

    # setup #######################################################

    def setup_loop(self):
        s_f = open('server_ip.txt', 'r')
        s_ip = s_f.read()
        self.network = Network(s_ip, 5555)
        s_f.close()
        self.player = self.network.get_player()
        print('You are player:', self.player.playerId)
        self.buttons = [Button('3-4 Players', 25, 50, 'make_small_board'),
                        Button('5-6 Players', 155, 50, 'make_big_board'),
                        Button('Randomize Board', 25, 200, 'randomize_board'),
                        Button('Randomize Values', 155, 200, 'randomize_board_vals'),
                        Button('Ready', 75, 500, self.player),
                        Button('Start', 75, 400, 'start')]
        if self.player.playerId == 0:
            self.buttons[0].active = True
            self.buttons[1].active = True
            self.buttons[2].active = True
            self.buttons[3].active = True

        run = True
        while run:
            clock.tick(60)

            try:
                self.game = self.network.send('get')
            except:
                print('failed to get game info')
                exit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    for button in self.buttons:
                        if button.click_check(pygame.mouse.get_pos()) and button.active:
                            button.click()
                            if button.text == 'Ready':
                                self.player.ready = True
                            elif button.text == 'Unready':
                                self.player.ready = False
                            try:
                                self.game = self.network.send(button.data)
                            except:
                                print('failed call:', button.data)

            self.setup_buttons_update()
            self.redraw_setup()

            if self.game.ready:
                run = False

        self.main_loop()

    def setup_buttons_update(self):
        if self.player.ready:
            self.buttons[4] = Button('Unready', 75, 500, self.player)
            self.buttons[4].click()
        else:
            self.buttons[4].click()
            self.buttons[4] = Button('Ready', 75, 500, self.player)

        self.buttons[4].active = True

        if self.game.all_ready_check() and self.player.playerId == 0:
            self.buttons[5].active = True
        else:
            self.buttons[5].active = False

    def redraw_setup(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.side_bar, (0, 0))
        self.draw_buttons(self.buttons)
        self.draw_board()
        pygame.display.update()

    # main #######################################################

    def main_loop(self):
        fade_out(self.window, (width, height))
        self.buttons = [Button('Settlement', 25, 240, self.player),
                        Button('Road', 155, 240, self.player),
                        Button('Upgrade Settlement', 25, 300, self.player),
                        Button('Development Card', 155, 300, None),
                        Button('Trade', 25, 400, self.player),
                        Button('Next Turn', 90, 550, 'next_turn'),
                        Button('Your Dev Cards', 155, 400, self.player)]

        run = True

        while run:

            clock.tick(60)

            try:
                self.game = self.network.send(self.player)
            except Exception as e:
                print(e)

            if self.game.first_rotate:
                self.starting_rotation()
            elif self.game.first_rotate != self.on_first_rotate:
                self.game_beginning_indicator()
                self.on_first_rotate = False
            elif not self.game.dice_rolled and self.player.playerId == self.game.player_turn:
                self.player_roll_dice()
            elif self.game.in_monopoly and self.game.monopoly_id == self.player.playerId:
                self.in_monopoly()
            elif self.game.robbing and self.game.robbed_player_id == self.player.playerId:
                self.robbed()
            elif self.game.in_trade and self.game.trade_id == self.player.playerId:
                self.trade_offer_loop()
            elif self.game.accept_trade and self.game.player_turn == self.player.playerId:
                self.collect_trade()
                self.notify('Trade Accepted By Player ' + str(self.game.players[self.game.trade_id].playerId))
            elif self.game.game_over:
                self.game_over_loop()

            if self.game.longest_road == self.player.playerId:
                self.player.longest_road = True
            else:
                self.player.longest_road = False

            if self.game.largest_army == self.player.playerId:
                self.player.largest_army = True
            else:
                self.player.largest_army = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    for button in self.buttons:
                        if button.click_check(pygame.mouse.get_pos()) and button.active:
                            button.click()
                            self.draw_main()
                            if button.text == 'Settlement':
                                self.placing_settlement = True
                                self.place_loop()
                                self.placing_settlement = False
                            elif button.text == 'Road':
                                self.placing_road_pos1 = True
                                self.place_loop()
                                self.temp_road = None
                                self.placing_road_pos2 = False
                            elif button.text == 'Upgrade Settlement':
                                self.upgrading_settlement = True
                                self.place_loop()
                                self.upgrading_settlement = False
                            elif button.text == 'Development Card':
                                self.buying_dev_card()
                            elif button.text == 'Your Dev Cards':
                                self.view_dev_cards_loop()
                            elif button.text == 'Trade':
                                self.trade_choose_loop()
                            try:
                                self.game = self.network.send(button.data)
                            except:
                                print('failed call:', button.data)

            self.manage_dice_roll()

            self.main_buttons_update()

            self.draw_main()

        pygame.quit()
        exit()

    def starting_rotation(self):
        self.draw_main()
        if self.game.first_rotate and self.player.playerId == self.game.player_turn:
            self.placing_settlement = True
            self.place_loop()
            try:
                self.game = self.network.send(self.player)
            except:
                print('failed to send player')
            self.draw_main()
            self.placing_settlement = False
            self.placing_road_pos1 = True
            self.place_loop()
            self.temp_road = None
            self.placing_road_pos2 = False
            try:
                self.game = self.network.send(self.player)
                self.game = self.network.send('rotate_initial_settlement_place')
            except:
                print('failed to send player info')

    def main_buttons_update(self):
        if self.game.first_rotate:
            for button in self.buttons:
                button.active = False
        elif self.game.dice_rolled:
            on_turn = (self.player.playerId == self.game.player_turn)
            self.buttons[5].active = (self.player.playerId == self.game.player_turn)
            self.buttons[0].active = self.player.can_buy_settlement() and on_turn
            self.buttons[1].active = self.player.can_buy_road() and on_turn
            self.buttons[2].active = self.player.can_upgrade_settlement() and on_turn
            self.buttons[3].active = self.player.can_buy_dev_card(self.game.dev_cards) and on_turn
            self.buttons[6].active = on_turn
            self.buttons[4].active = on_turn

        if self.player.playerId != self.game.player_turn:
            for button in self.buttons:
                button.active = False
        elif self.game.in_trade:
            for button in self.buttons:
                button.active = False

    def draw_main(self):
        # clear and side bar
        pygame.draw.rect(self.window, (0, 0, 0), (0, 0, width, height))
        self.window.blit(self.side_bar, (0, 0))

        # setting colours
        player_turn_colour = self.player_colours[self.game.player_turn]
        player_colour = self.player_colours[self.player.playerId]

        # indication of whose turn it is (side bar)
        if self.player.playerId == self.game.player_turn:
            turn_text = self.title_font.render('Your Turn', True, player_turn_colour)
        else:
            turn_text = self.title_font.render('Player ' + str(self.game.player_turn) + '\'s Turn', True, player_turn_colour)
        turn_text_x = (self.side_bar_width - turn_text.get_width()) // 2
        self.window.blit(turn_text, (turn_text_x, 500))

        # who you are (side bar)
        player_indicator = self.title_font.render('Player ' + str(self.player.playerId), True, player_colour)
        player_indicator_x = (self.side_bar_width - player_indicator.get_width()) // 2
        self.window.blit(player_indicator, (player_indicator_x, 30))

        # sub titles (side bar)
        self.window.blit(self.resource_title, (self.resource_title_x, self.resource_title_y))
        self.window.blit(self.option_title, (self.option_title_x, self.option_title_y))

        # longest road/largest army/devcards
        if self.game.longest_road != -1:
            self.print_text((width - 220, 10, 240, 200), 'Longest Road: Player ' + str(self.game.longest_road))
        if self.game.largest_army != -1:
            self.print_text((width - 220, 35, 240, 200), 'Largest Army: Player ' + str(self.game.largest_army))
        if self.game.players[self.game.player_turn].dev_cards:
            dev_card_count_text = 'Player ' + str(self.game.player_turn) + ' has '
            dev_card_count_text = dev_card_count_text + str(len(self.game.players[self.game.player_turn].dev_cards))
            dev_card_count_text = dev_card_count_text + ' unplayed dev card(s)'
            self.print_text((self.side_bar_width + 10, height - 25, width, 40), dev_card_count_text)

        self.draw_buttons(self.buttons)
        self.draw_board()
        self.draw_resources()

        # displaying a turn change
        if self.turn_change != self.game.player_turn:
            self.turn_indicator()
            self.turn_change = self.game.player_turn

        if self.game.in_trade and self.player.playerId == self.game.player_turn:
            dim(self.window, (width, height))
            self.print_text((309, 9, 250, 500), 'Trade Pending...')
            self.draw_board()

        pygame.display.update()

    def draw_resources(self):
        lumber_text = self.resource_font.render('Lumber: ' + str(self.player.lumber), True, (114, 82, 29))
        brick_text = self.resource_font.render('Brick: ' + str(self.player.brick), True, (155, 72, 63))
        wheat_text = self.resource_font.render('Wheat: ' + str(self.player.wheat), True, (193, 184, 83))
        sheep_text = self.resource_font.render('Sheep: ' + str(self.player.sheep), True, (240, 240, 240))
        ore_text = self.resource_font.render('Ore: ' + str(self.player.ore), True, (150, 150, 150))
        self.window.blit(lumber_text, (50, 130))
        self.window.blit(sheep_text, (50, 150))
        self.window.blit(wheat_text, (50, 170))
        self.window.blit(brick_text, (180, 140))
        self.window.blit(ore_text, (180, 160))

    # placing ###########################################################

    def place_loop(self):
        dim(self.window, (width, height))
        self.draw_board()
        placing = True

        while placing:

            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    if self.placing_settlement and self.game.settlement_check(pos):
                        if len(self.player.settlements) < 2 or self.player.road_at_pos(pos):
                            self.player.settlements.append(Settlement(pos))
                            if len(self.player.settlements) > 2:
                                self.player.buy_settlement()
                            placing = False

                    elif self.upgrading_settlement and self.game.settlement_upgrade_check(pos, self.player.playerId):
                        i = 0
                        while i < len(self.player.settlements):
                            if self.player.settlements[i].is_inside_local(pos):
                                self.player.settlements[i].level = 2
                                self.player.upgrade_settlement()
                            i += 1
                        placing = False

                    elif self.placing_road_pos1 and self.game.road_pos1_check(pos):
                        if self.player.settlement_at_pos(pos) or self.player.road_at_pos(pos):
                            self.temp_road = Road(pos)
                            self.placing_road_pos1 = False
                            self.placing_road_pos2 = True

                    elif self.placing_road_pos2 and self.game.road_pos2_check(self.temp_road, pos):
                        self.temp_road.set_pos2(pos)
                        self.player.roads.append(self.temp_road)
                        if len(self.player.roads) > 2 and not self.road_card:
                            self.player.buy_road()
                        placing = False

                    elif self.moving_thief and self.game.thief_check(pos):
                        index_of_thief = 0
                        i = 0
                        while i < len(self.game.board.lot):
                            if self.game.board.lot[i].is_inside(pos):
                                index_of_thief = i
                            i += 1
                        data = {
                            'call': 'move_thief',
                            'data': index_of_thief
                        }
                        try:
                            self.game = self.network.send(data)
                        except:
                            print('failed to move thief')
                        placing = False

            if pygame.key.get_pressed()[pygame.K_ESCAPE] and not self.moving_thief:
                placing = False

            self.draw_place_loop()

    def draw_place_loop(self):
        text = ''
        if self.placing_settlement:
            text = 'Click to place settlement'
        elif self.upgrading_settlement:
            text = 'Click to upgrade settlement'
        elif self.placing_road_pos1:
            text = 'Click to set road starting position'
        elif self.placing_road_pos2:
            text = 'Click to set road ending position'
        elif self.moving_thief:
            text = 'Click to move the thief'
        if not self.game.first_rotate and not self.moving_thief:
            text = text + ', or [ESC] to return to options.'
        self.print_text((310, 10, 250, 500), text)

        self.draw_board()

        if self.temp_road:
            pygame.draw.circle(self.window, (0, 0, 0), self.temp_road.pos1, 10)
            pygame.draw.circle(self.window, self.player_colours[self.player.playerId], self.temp_road.pos1, 7)

        pygame.display.update()

    # dice ##############################################################

    def player_roll_dice(self):
        roll_button = Button('Roll Dice', 310, 10, 'roll_dice')
        roll_button.active = True
        self.buttons.append(roll_button)
        roll_button.height = 100
        roll_button.width = 200

        roll_loop = True

        while roll_loop:

            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if roll_button.click_check(pos):
                        roll_button.click()
                        self.draw_main()
                        self.buttons.pop(len(self.buttons) - 1)
                        try:
                            self.game = self.network.send(roll_button.data)
                        except:
                            print('failed call:', roll_button.data)
                        self.draw_dice_outcome()
                        self.collect(self.game.roll_sum)
                        self.displayed_roll = True
                        roll_loop = False

                        if self.game.roll_sum == 7:
                            self.moving_thief = True
                            self.place_loop()
                            self.moving_thief = False
                            self.steal_resource()

            self.draw_main()

    def manage_dice_roll(self):
        if self.displayed_roll != self.game.dice_rolled and self.game.dice_rolled:
            self.draw_dice_outcome()
            self.collect(self.game.roll_sum)
            self.displayed_roll = True

        elif self.displayed_roll != self.game.dice_rolled:
            self.displayed_roll = False

    def draw_dice_outcome(self):
        self.print_text((309, 9, 250, 500), 'Dice Rolled! $%^ Outcome: ' + str(self.game.roll_sum))
        self.draw_board()
        pygame.display.update()
        pygame.time.delay(2500)
        pygame.draw.rect(self.window, (0, 0, 0), (310, 10, 400, 400))
        self.draw_board()
        pygame.display.update()

    # general ###########################################################

    def turn_indicator(self):
        pygame.draw.rect(self.window, (0, 0, 0), (309, 9, 400, 400))
        self.draw_board()
        if self.player.playerId == self.game.player_turn:
            text = self.big_font.render('Your Turn', True, (240, 240, 240))
        else:
            text = self.big_font.render('Player ' + str(self.game.player_turn) + '\'s Turn', True, (240, 240, 240))
        text_x = 310
        text_y = 10
        self.window.blit(text, (text_x, text_y))
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.draw.rect(self.window, (0, 0, 0), (310, 10, 400, 400))
        self.draw_board()
        pygame.display.update()

    def game_beginning_indicator(self):
        text = self.big_font.render('First Round Over', True, (240, 240, 240))
        text_x = 310
        text_y = 10
        self.window.blit(text, (text_x, text_y))
        pygame.display.update()
        pygame.time.delay(2000)
        pygame.draw.rect(self.window, (0, 0, 0), (310, 10, 400, 400))
        self.draw_board()
        pygame.display.update()
        self.first_collect()

    def print_text(self, rect, full_text, clear=True, center=False):
        if clear:
            pygame.draw.rect(self.window, (0, 0, 0), rect)
        low = split_text(full_text)
        font = self.big_font
        text = None
        text_colour = (240, 240, 240)
        lot = []
        i = 0
        j = 0
        while i <= len(low):
            text = back_to_text(low[:i])
            text_surf = font.render(text, False, (25, 25, 25), True).convert_alpha()
            if back_to_text(low[i - 1]) == '$%^ ':
                text = back_to_text(low[:i - 1])
                lot.append(text)
                low = low[i:]
                i = 0
            if text_surf.get_width() < rect[2]:
                i += 1
            else:
                text = back_to_text(low[:i - 1])
                lot.append(text)
                low = low[i - 1:]
                i = 0
        lot.append(text)

        while j < len(lot):
            text_surf = font.render(lot[j], True, text_colour, True).convert_alpha()
            if center:
                text_x = rect[0] + ((rect[2] - text_surf.get_width()) // 2)
            else:
                text_x = rect[0]
            self.window.blit(text_surf, (text_x, rect[1] + (j * text_surf.get_height())))
            j += 1

    def draw_buttons(self, lob):
        i = 0
        while i < len(lob):
            if lob[i].active or lob[i].clicked:
                button_colour = (0, 100, 0)
                button_colour2 = (0, 50, 0)
                text_colour = (255, 255, 255)
            else:
                button_colour = (150, 150, 150)
                button_colour2 = (100, 100, 100)
                text_colour = (200, 200, 200)
            button_dimensions = (lob[i].x, lob[i].y, lob[i].width, lob[i].height)
            pygame.draw.rect(self.window, button_colour, button_dimensions)
            pygame.draw.rect(self.window, button_colour2, button_dimensions, 4)
            text = self.button_font.render(lob[i].text, 1, text_colour)
            text_x = (lob[i].x + lob[i].width // 2) - (text.get_width() // 2)
            text_y = (lob[i].y + lob[i].height // 2) - (text.get_height() // 2)
            self.window.blit(text, (text_x, text_y))
            if lob[i].clicked:
                dim_surf = pygame.Surface((lob[i].width, lob[i].height))
                dim_surf.fill((0, 0, 0))
                dim_surf.set_alpha(100)
                self.window.blit(dim_surf, (lob[i].x, lob[i].y))
                lob[i].click_timer_update()
            i += 1

    def draw_board(self):
        # drawing tiles
        for tile in self.game.board.lot:
            if tile.val != -1:
                self.window.blit(self.tile_dict[tile.type], (tile.x - 123, tile.y - 124))
            else:
                self.window.blit(self.tile_dict['water'], (tile.x - 123, tile.y - 124))
            if tile.val > 0:
                if tile.val == 6 or tile.val == 8:
                    text = self.board_val_font.render(str(tile.val), 1, (200, 0, 0))
                else:
                    text = self.board_val_font.render(str(tile.val), 1, (0, 0, 0))
                circle_y = tile.y + 16
                pygame.draw.circle(self.window, (150, 150, 150), (tile.x, circle_y), 17)
                pygame.draw.circle(self.window, (200, 200, 200), (tile.x, circle_y), 15)
                self.window.blit(text, (tile.x - (text.get_width() // 2), circle_y - (text.get_height() // 2)))
            elif tile.val == -1:
                pygame.draw.circle(self.window, (220, 220, 220), (tile.x, tile.y), 25)
                text = self.board_val_font.render(tile.type, 1, (0, 0, 0))
                self.window.blit(text, (tile.x - (text.get_width() // 2), tile.y - (text.get_height() // 2)))
            if tile.thief:
                point_list = [(tile.x - 25, tile.y - 20), (tile.x + 25, tile.y - 20), (tile.x, tile.y + 23)]
                pygame.draw.polygon(self.window, (0, 0, 0), point_list)
                point_list = [(tile.x - 20, tile.y - 17), (tile.x + 20, tile.y - 17), (tile.x, tile.y + 17)]
                pygame.draw.polygon(self.window, (70, 70, 70), point_list)

        # drawing structures
        for player in self.game.players:
            player_colour = self.player_colours[player.playerId]

            for road in player.roads:
                pygame.draw.line(self.window, (0, 0, 0), road.pos1, road.pos2, 12)
                pygame.draw.line(self.window, player_colour, road.pos1, road.pos2, 6)

            for settlement in player.settlements:
                pygame.draw.rect(self.window, player_colour, (settlement.x - 10, settlement.y - 10, 20, 20))
                pygame.draw.rect(self.window, (0, 0, 0), (settlement.x - 10, settlement.y - 10, 20, 20), 4)
                if settlement.level == 2:
                    pygame.draw.circle(self.window, (0, 0, 0), (settlement.x, settlement.y), 4)

    def notify(self, text):
        self.print_text((309, 9, 250, 500), text)
        self.draw_board()
        pygame.display.update()
        pygame.time.delay(1500)

    # Collect ########################################################

    def collect(self, val):
        for tile in self.game.board.lot:
            if tile.val == val and not tile.thief:
                for settlement in self.player.settlements:
                    if tile.is_inside(settlement.pos) and tile.val > 0:
                        if tile.type == 'lumber':
                            self.player.lumber += settlement.level
                        elif tile.type == 'ore':
                            self.player.ore += settlement.level
                        elif tile.type == 'sheep':
                            self.player.sheep += settlement.level
                        elif tile.type == 'wheat':
                            self.player.wheat += settlement.level
                        elif tile.type == 'brick':
                            self.player.brick += settlement.level

    def first_collect(self):
        for tile in self.game.board.lot:
            settlement = self.player.settlements[0]
            if tile.is_inside(settlement.pos):
                if tile.type == 'lumber' and tile.val > 0:
                    self.player.lumber += settlement.level
                elif tile.type == 'ore':
                    self.player.ore += settlement.level
                elif tile.type == 'sheep':
                    self.player.sheep += settlement.level
                elif tile.type == 'wheat':
                    self.player.wheat += settlement.level
                elif tile.type == 'brick':
                    self.player.brick += settlement.level

    # Dev Cards ######################################################

    def buying_dev_card(self):
        i = random.randint(0, len(self.game.dev_cards) - 1)
        self.player.buy_dev_card()
        self.player.dev_cards.append(self.game.dev_cards[i])

        data = {
            'call': 'dev_card_bought',
            'data': i
        }

        self.buttons[3].data = data

    def view_dev_cards_loop(self):
        dim(self.window, (width, height))
        mon_amount = '(x' + str(self.player.dev_cards.count('monopoly')) + ')'
        yop_amount = '(x' + str(self.player.dev_cards.count('plenty')) + ')'
        vp_amount = '(x' + str(self.player.dev_cards.count('victory_point')) + ')'
        br_amount = '(x' + str(self.player.dev_cards.count('build_roads')) + ')'
        sol_amount = '(x' + str(self.player.dev_cards.count('soldier')) + ')'
        self.dev_card_buttons = [Button('Monopoly ' + mon_amount, self.menu_x + 170, 300, None),
                                 Button('Year of Plenty ' + yop_amount, self.menu_x + 330, 300, None),
                                 Button('Victory Point ' + vp_amount, self.menu_x + 490, 300, None),
                                 Button('Build Roads ' + br_amount, self.menu_x + 250, 450, None),
                                 Button('Soldier ' + sol_amount, self.menu_x + 410, 450, None)]

        dev_card_loop = True

        while dev_card_loop:

            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    for button in self.dev_card_buttons:
                        if button.click_check(pos) and button.active:
                            button.click()
                            if 'Monopoly' in button.text:
                                self.choose_resource_loop('monopoly')
                                data = {
                                    'call': 'monopoly',
                                    'data': self.resources_selected[0]
                                }
                                try:
                                    self.game = self.network.send(data)
                                except:
                                    print('failed to monopoly')
                                reduced_player_list = self.game.players.copy()
                                reduced_player_list.pop(self.player.playerId)
                                for player in reduced_player_list:
                                    if self.game.monopoly_resource == 'lumber':
                                        self.player.lumber += player.lumber
                                    elif self.game.monopoly_resource == 'ore':
                                        self.player.ore += player.ore
                                    elif self.game.monopoly_resource == 'sheep':
                                        self.player.sheep += player.sheep
                                    elif self.game.monopoly_resource == 'brick':
                                        self.player.brick += player.brick
                                    elif self.game.monopoly_resource == 'wheat':
                                        self.player.wheat += player.wheat
                                del reduced_player_list
                                self.player.pop_dev_card('monopoly')
                                dev_card_loop = False

                            elif 'Year of Plenty' in button.text:
                                self.choose_resource_loop('year_of_plenty')
                                for resource in self.resources_selected:
                                    if resource == 'lumber':
                                        self.player.lumber += 1
                                    elif resource == 'ore':
                                        self.player.ore += 1
                                    elif resource == 'sheep':
                                        self.player.sheep += 1
                                    elif resource == 'brick':
                                        self.player.brick += 1
                                    elif resource == 'wheat':
                                        self.player.wheat += 1
                                self.player.pop_dev_card('plenty')
                                dev_card_loop = False

                            elif 'Build Roads' in button.text:
                                self.road_card = True
                                self.draw_main()
                                self.placing_road_pos1 = True
                                self.place_loop()
                                self.temp_road = None
                                self.placing_road_pos2 = False
                                try:
                                    self.game = self.network.send(self.player)
                                except:
                                    print('failed to send player while using build roads dev card')
                                self.draw_main()
                                self.placing_road_pos1 = True
                                self.place_loop()
                                self.temp_road = None
                                self.placing_road_pos2 = False
                                self.road_card = False
                                dev_card_loop = False
                                self.player.pop_dev_card('build_roads')

                            elif 'Soldier' in button.text:
                                self.draw_main()
                                self.moving_thief = True
                                self.place_loop()
                                self.moving_thief = False
                                self.steal_resource()
                                self.player.pop_dev_card('soldier')
                                self.player.army += 1
                                dev_card_loop = False

            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                dev_card_loop = False

            self.dev_card_button_update()

            self.draw_dev_card_loop()

    def dev_card_button_update(self):
        self.dev_card_buttons[0].active = self.player.count_dev_card('monopoly') > 0
        self.dev_card_buttons[1].active = self.player.count_dev_card('plenty') > 0
        self.dev_card_buttons[2].active = self.player.count_dev_card('victory_point') > 0
        self.dev_card_buttons[3].active = self.player.count_dev_card('build_roads') > 0
        self.dev_card_buttons[4].active = self.player.count_dev_card('soldier') > 0

    def in_monopoly(self):
        if self.game.monopoly_resource == 'lumber':
            self.player.lumber = 0
        elif self.game.monopoly_resource == 'ore':
            self.player.ore = 0
        elif self.game.monopoly_resource == 'sheep':
            self.player.sheep = 0
        elif self.game.monopoly_resource == 'brick':
            self.player.brick = 0
        elif self.game.monopoly_resource == 'wheat':
            self.player.wheat = 0

        try:
            self.game = self.network.send('monopoly_rotate')
        except:
            print('failed to rotate_monopoly')

    def draw_dev_card_loop(self):
        self.window.blit(self.menu, (self.menu_x, self.menu_y))
        self.draw_buttons(self.dev_card_buttons)
        text_rect = (self.menu_x, self.menu_y + 40, self.menu.get_width(), self.menu.get_height())
        self.print_text(text_rect, 'Your Development Cards', clear=False, center=True)
        pygame.display.update()

    # Steal #####################################################

    def steal_resource(self):
        index_thief = 0
        for tile in self.game.board.lot:
            if tile.thief:
                index_thief = self.game.board.lot.index(tile)

        reduced_list = self.game.players.copy()
        reduced_list.pop(self.player.playerId)

        steal_player_list = []

        for player in reduced_list:
            for settlement in player.settlements:
                if self.game.board.lot[index_thief].is_inside(settlement.pos):
                    steal_player_list.append(player)

        if steal_player_list:
            rand_player = random.randint(0, len(steal_player_list) - 1)
            robbed_player = steal_player_list[rand_player]
            resource_list = robbed_player.get_list_of_resources()
            if resource_list:
                rand_resource = random.randint(0, len(resource_list) - 1)
                robbed_resource = resource_list[rand_resource]
                data = {
                    'call': 'steal_resource_setup',
                    'data': (robbed_resource, robbed_player.playerId)
                }

                if robbed_resource == 'lumber':
                    self.player.lumber += 1
                elif robbed_resource == 'sheep':
                    self.player.sheep += 1
                elif robbed_resource == 'wheat':
                    self.player.wheat += 1
                elif robbed_resource == 'brick':
                    self.player.brick += 1
                elif robbed_resource == 'ore':
                    self.player.ore += 1

                text = 'You stole a ' + robbed_resource + ' from player ' + str(robbed_player.playerId) + '!'

                try:
                    self.game = self.network.send(data)
                except:
                    print('failed to send call to steal resource')

            else:
                text = 'Tried to steal from player ' + str(robbed_player.playerId) + ', they had no resources to steal...'
        else:
            text = 'No nearby players to steal from.'

        self.notify(text)

    def robbed(self):
        robbed_resource = self.game.robbed_resource
        if robbed_resource == 'lumber':
            self.player.lumber -= 1
        elif robbed_resource == 'sheep':
            self.player.sheep -= 1
        elif robbed_resource == 'wheat':
            self.player.wheat -= 1
        elif robbed_resource == 'brick':
            self.player.brick -= 1
        elif robbed_resource == 'ore':
            self.player.ore -= 1
        try:
            self.game = self.network.send('stop_robbing')
        except:
            print('failed to stop robbing')
        text = 'A ' + robbed_resource + ' has been stolen!'
        self.notify(text)

    # trade ######################################################

    def trade_choose_loop(self):
        self.trade_buttons = [Button('4:1 Any', self.menu_x + 40, self.menu_y + 30, None),
                              Button('Player Trade', self.menu_x + 40, self.menu_y + 300, None),
                              Button('3:1 Any', self.menu_x + 300, self.menu_y + 30, None),
                              Button('2:1 Sheep', self.menu_x + 300, self.menu_y + 90, None),
                              Button('2:1 Lumber', self.menu_x + 300, self.menu_y + 150, None),
                              Button('2:1 Ore', self.menu_x + 300, self.menu_y + 210, None),
                              Button('2:1 Brick', self.menu_x + 300, self.menu_y + 270, None),
                              Button('2:1 Wheat', self.menu_x + 300, self.menu_y + 330, None)]

        trade_choose = True

        while trade_choose:

            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    for button in self.trade_buttons:
                        if button.click_check(pos):
                            if button.text == '4:1 Any' and self.player.can_4_for_1():
                                self.choose_resource_loop('4:1')
                                self.player.add_amount_of(self.resources_selected[0], -4)
                                self.choose_resource_loop('choose_one')
                                self.player.add_amount_of(self.resources_selected[0], 1)
                                trade_choose = False

                            elif button.text == '3:1 Any':
                                self.choose_resource_loop('3:1')
                                self.player.add_amount_of(self.resources_selected[0], -3)
                                self.choose_resource_loop('choose_one')
                                self.player.add_amount_of(self.resources_selected[0], 1)
                                trade_choose = False

                            elif button.text[:3] == '2:1':
                                self.player.add_amount_of(button.text[4:].lower(), -2)
                                self.choose_resource_loop('choose_one')
                                self.player.add_amount_of(self.resources_selected[0], 1)
                                trade_choose = False

                            elif button.text == 'Player Trade':
                                self.choose_resource_loop('trade_to_give')
                                give = self.resources_selected.copy()
                                self.choose_resource_loop('trade_to_take')
                                get = self.resources_selected.copy()
                                data = {
                                    'call': 'send_trade_offer',
                                    'data': (give, get)
                                }
                                try:
                                    self.game = self.network.send(data)
                                except:
                                    print('couldn\'t send trade offer')
                                trade_choose = False

                elif event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    trade_choose = False

            self.update_trade_loop()
            self.draw_trade_loop()

    def update_trade_loop(self):
        self.trade_buttons[0].active = self.player.can_4_for_1()
        self.trade_buttons[1].active = self.player.has_resources()
        self.trade_buttons[2].active = self.player.can_3_for_1() and self.game.port_check(self.player, 'any')
        self.trade_buttons[3].active = self.player.sheep >= 2 and self.game.port_check(self.player, 'sheep')
        self.trade_buttons[4].active = self.player.lumber >= 2 and self.game.port_check(self.player, 'lumber')
        self.trade_buttons[5].active = self.player.ore >= 2 and self.game.port_check(self.player, 'ore')
        self.trade_buttons[6].active = self.player.brick >= 2 and self.game.port_check(self.player, 'brick')
        self.trade_buttons[7].active = self.player.wheat >= 2 and self.game.port_check(self.player, 'wheat')

    def draw_trade_loop(self):
        self.window.blit(self.menu, (self.menu_x, self.menu_y))
        self.draw_buttons(self.trade_buttons)
        text_rect = (self.menu_x, self.menu_y + 20, self.menu.get_width(), self.menu_y)
        self.print_text(text_rect, 'Select Trade', clear=False, center=True)
        pygame.display.update()

    def trade_offer_loop(self):
        self.trade_offer_buttons = [
            Button('Accept', self.menu_x + 220, self.menu_y + 400, 'trade_accepted'),
            Button('Decline', self.menu_x + 470, self.menu_y + 400, 'rotate_trade_offer')
        ]

        trade_offer = True

        while trade_offer:

            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    for button in self.trade_offer_buttons:
                        if button.click_check(pos):
                            button.click()
                            if button.text == 'Accept':
                                self.player.wheat -= self.game.resources_to_get.count('wheat')
                                self.player.wheat += self.game.resources_to_give.count('wheat')
                                self.player.ore -= self.game.resources_to_get.count('ore')
                                self.player.ore += self.game.resources_to_give.count('ore')
                                self.player.brick -= self.game.resources_to_get.count('brick')
                                self.player.brick += self.game.resources_to_give.count('brick')
                                self.player.lumber -= self.game.resources_to_get.count('lumber')
                                self.player.lumber += self.game.resources_to_give.count('lumber')
                                self.player.sheep -= self.game.resources_to_get.count('sheep')
                                self.player.sheep += self.game.resources_to_give.count('sheep')
                            try:
                                self.game = self.network.send(button.data)
                            except:
                                print('failed call: ' + button.data)
                            trade_offer = False

            self.trade_offer_buttons_update()
            self.draw_trade_offer()

    def draw_trade_offer(self):
        self.window.blit(self.menu, (self.menu_x, self.menu_y))
        wanted = list_of_str_to_str('Wanted: ', self.game.resources_to_get)
        offered = list_of_str_to_str('Offered: ', self.game.resources_to_give)
        self.draw_buttons(self.trade_offer_buttons)
        wanted_rect = (self.menu_x, self.menu_y + 130, self.menu.get_width(), self.menu.get_height())
        self.print_text(wanted_rect, wanted, clear=False, center=True)
        offered_rect = (self.menu_x, self.menu_y + 250, self.menu.get_width(), self.menu.get_height())
        self.print_text(offered_rect, offered, clear=False, center=True)
        title_rect = (self.menu_x, self.menu_y + 30, self.menu.get_width(), self.menu.get_height())
        self.print_text(title_rect, 'Incoming Trade Offer', clear=False, center=True)
        pygame.display.update()

    def trade_offer_buttons_update(self):
        self.trade_offer_buttons[1].active = True
        lumber = 0
        sheep = 0
        ore = 0
        wheat = 0
        brick = 0
        for item in self.game.resources_to_get:
            if item == 'lumber':
                lumber += 1
            elif item == 'sheep':
                sheep += 1
            elif item == 'ore':
                ore += 1
            elif item == 'wheat':
                wheat += 1
            elif item == 'brick':
                brick += 1

        if self.player.lumber >= lumber and self.player.sheep >= sheep and self.player.ore >= ore:
            if self.player.wheat >= wheat and self.player.brick >= brick:
                self.trade_offer_buttons[0].active = True
            else:
                self.trade_offer_buttons[0].active = False
        else:
            self.trade_offer_buttons[0].active = False

    def collect_trade(self):
        self.player.wheat += self.game.resources_to_get.count('wheat')
        self.player.wheat -= self.game.resources_to_give.count('wheat')
        self.player.ore += self.game.resources_to_get.count('ore')
        self.player.ore -= self.game.resources_to_give.count('ore')
        self.player.brick += self.game.resources_to_get.count('brick')
        self.player.brick -= self.game.resources_to_give.count('brick')
        self.player.lumber += self.game.resources_to_get.count('lumber')
        self.player.lumber -= self.game.resources_to_give.count('lumber')
        self.player.sheep += self.game.resources_to_get.count('sheep')
        self.player.sheep -= self.game.resources_to_give.count('sheep')
        try:
            self.game = self.network.send('trade_collected')
        except:
            print('failed call: trade_collected')

    # choosing resources loop ####################################

    def choose_resource_loop(self, reason):
        self.resource_buttons = [Button('Lumber', self.menu_x + 150, self.menu_y + 100, 'lumber'),
                                 Button('Wheat', self.menu_x + 320, self.menu_y + 100, 'wheat'),
                                 Button('Brick', self.menu_x + 490, self.menu_y + 100, 'brick'),
                                 Button('Ore', self.menu_x + 235, self.menu_y + 220, 'ore'),
                                 Button('Sheep', self.menu_x + 405, self.menu_y + 220, 'sheep')]

        if reason == 'trade_to_give' or reason == 'trade_to_take':
            self.resource_buttons.append(Button('Submit', self.menu_center - 75, self.menu_y + 400, 'submit_trade'))

        self.resources_selected = []

        choose_loop = True

        while choose_loop:

            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    for button in self.resource_buttons:
                        if button.click_check(pos) and button.active:
                            button.click()
                            if button.text != 'Submit':
                                self.resources_selected.append(button.data)
                            else:
                                choose_loop = False

                elif event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    choose_loop = False

            if reason == 'monopoly' or reason == '4:1' or reason == '3:1' or reason == 'choose_one':
                if len(self.resources_selected) == 1:
                    choose_loop = False
            elif reason == 'year_of_plenty' and len(self.resources_selected) == 2:
                choose_loop = False

            self.update_resource_buttons(reason)
            self.draw_resource_loop(reason)

    def update_resource_buttons(self, reason):
        if reason == 'monopoly' or reason == 'year_of_plenty' or reason == 'choose_one':
            i = 0
            while i < len(self.resource_buttons):
                self.resource_buttons[i].active = True
                i += 1

        elif reason == '4:1':
            self.resource_buttons[0].active = self.player.lumber >= 4
            self.resource_buttons[1].active = self.player.wheat >= 4
            self.resource_buttons[2].active = self.player.brick >= 4
            self.resource_buttons[3].active = self.player.ore >= 4
            self.resource_buttons[4].active = self.player.sheep >= 4

        elif reason == '3:1':
            self.resource_buttons[0].active = self.player.lumber >= 3
            self.resource_buttons[1].active = self.player.wheat >= 3
            self.resource_buttons[2].active = self.player.brick >= 3
            self.resource_buttons[3].active = self.player.ore >= 3
            self.resource_buttons[4].active = self.player.sheep >= 3

        elif reason == 'trade_to_give':
            self.resource_buttons[0].active = self.player.lumber - self.resources_selected.count('lumber') > 0
            self.resource_buttons[1].active = self.player.wheat - self.resources_selected.count('wheat') > 0
            self.resource_buttons[2].active = self.player.brick - self.resources_selected.count('brick') > 0
            self.resource_buttons[3].active = self.player.ore - self.resources_selected.count('ore') > 0
            self.resource_buttons[4].active = self.player.sheep - self.resources_selected.count('sheep') > 0
            self.resource_buttons[5].active = True

        elif reason == 'trade_to_take':
            self.resource_buttons[0].active = True
            self.resource_buttons[1].active = True
            self.resource_buttons[2].active = True
            self.resource_buttons[3].active = True
            self.resource_buttons[4].active = True
            self.resource_buttons[5].active = True

    def draw_resource_loop(self, reason):
        title = 'there was an error'
        if reason == 'monopoly':
            title = 'Choose a resource'
        elif reason == 'choose_one':
            title = 'Choose a resource to receive'
        elif reason == '3:1' or reason == '4:1':
            title = 'Choose the resource you would like to trade'
        elif reason == 'year_of_plenty':
            title = 'Choose 2 resources'
        elif reason == 'trade_to_give':
            title = 'Choose the resource(s) you would like to trade'
        elif reason == 'trade_to_take':
            title = 'Choose the resource(s) you would like to receive'
        text = list_of_str_to_str('Selected: ', self.resources_selected)

        self.window.blit(self.menu, (self.menu_x, self.menu_y))
        self.print_text((self.menu_x, self.menu_y + 20, self.menu.get_width(), 100), title, clear=False, center=True)
        self.print_text((self.menu_x, self.menu_y + 330, self.menu.get_width(), 100), text, clear=False, center=True)
        self.draw_buttons(self.resource_buttons)

        pygame.display.update()

    # game_over ##################################################

    def game_over_loop(self):
        show_loop = True

        if self.player.playerId == self.game.winning_player:
            text = 'YOU WON!'
        else:
            text = 'Player ' + str(self.game.winning_player) + ' WON! $%^ LOSER!'

        dim(self.window, (width, height))
        self.window.blit(self.menu, (self.menu_x, self.menu_y))
        self.print_text((self.menu_x, self.menu_y + 100, self.menu.get_width(), 200), text, clear=False, center=True)

        while show_loop:

            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            pygame.display.update()


client = Client()

while True:
    client.title_screen()
