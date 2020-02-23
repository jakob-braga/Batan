from board import *


class Game:
    def __init__(self):
        self.players = []
        self.player_turn = 0
        self.first_rotate = True
        self.one_settlement_placed_for_all = False
        self.dice_rolled = False

        # monopoly
        self.monopoly_resource = None
        self.in_monopoly = False
        self.monopoly_id = -1

        # trading
        self.resources_to_give = None
        self.resources_to_get = None
        self.in_trade = False
        self.trade_id = -1
        self.accept_trade = False

        # vps
        self.record_army = 2
        self.record_road = 4
        self.largest_army = -1
        self.longest_road = -1

        # winning
        self.winning_player = -1
        self.game_over = False
        
        # stealing
        self.robbed_player_id = -1
        self.robbed_resource = None
        self.robbing = False

        self.timer = 0

        self.ready = False

        self.roll_sum = None

        self.board = Board()

        self.dev_cards = []

    # setup #############################

    def make_big_board(self):
        self.board.construct_big()

    def make_small_board(self):
        self.board.construct_small()

    def randomize_board(self):
        self.board.randomize_tiles()

    def randomize_board_vals(self):
        self.board.randomize_vals()

    def all_ready_check(self):
        for player in self.players:
            if not player.ready:
                return False
        return True

    def start(self):
        self.ready = True
        self.board.finalize_board()
        self.dev_cards = (['soldier'] * 14) + (['victory_point'] * 5) + (['build_roads'] * 2) + (['plenty'] * 2) + (['monopoly'] * 2)
        if self.board.big:
            self.dev_cards.extend((['soldier'] * 6) + ['build_roads', 'monopoly', 'plenty'])

    def rotate_initial_settlement_place(self):
        if self.player_turn < len(self.players) - 1 and not self.one_settlement_placed_for_all:
            self.player_turn += 1
        elif self.player_turn == len(self.players) - 1 and not self.one_settlement_placed_for_all:
            self.one_settlement_placed_for_all = True
        elif self.player_turn > 0:
            self.player_turn -= 1
        else:
            self.first_rotate = False

    # checks ###############################

    def nearby_settlements_check(self, pos):
        for player in self.players:
            for settlement in player.settlements:
                if settlement.is_inside(pos):
                    return False
        return True

    def settlement_check(self, pos):
        if self.board.count_intersections(pos) == 3 and self.nearby_settlements_check(pos):
            return True
        else:
            return False

    def settlement_upgrade_check(self, pos, playerId):
        for settlement in self.players[playerId].settlements:
            if settlement.is_inside_local(pos) and settlement.level == 1:
                return True
        return False

    def count_structs(self, pos):
        i = 0
        for player in self.players:
            for settlement in player.settlements:
                if settlement.is_inside_local(pos):
                    i += 1
            for road in player.roads:
                if road.is_inside_local(1, pos):
                    i += 1
                elif road.is_inside_local(2, pos):
                    i += 1

        return i

    def road_pos1_check(self, pos):
        if self.board.count_intersections(pos) == 3 and self.count_structs(pos) < 4:
            return True
        else:
            return False

    def road_pos2_check(self, road, pos):
        if self.board.count_intersections(pos) == 3 and self.count_structs(pos) < 4:
            if road.radius < dist(road.pos1[0], road.pos1[1], pos[0], pos[1]) < 60:
                for player in self.players:
                    for r in player.roads:
                        if r.is_inside_local(1, road.pos1) and r.is_inside_local(2, pos):
                            return False
                        if r.is_inside_local(2, road.pos1) and r.is_inside_local(1, pos):
                            return False
                return True

    def thief_check(self, pos):
        if self.board.count_intersections(pos) == 1:
            for tile in self.board.lot:
                if tile.is_inside(pos) and not tile.thief:
                    return True
        return False

    def port_check(self, player, port):
        for tile in self.board.lot:
            if tile.val == -1:
                for settlement in player.settlements:
                    if tile.is_inside(settlement.pos) and tile.type == port:
                        return True
        return False

    # Update ################################

    def update_player(self, player):
        self.players[player.playerId] = player

    def roll_dice(self):
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        self.roll_sum = dice1 + dice2
        self.dice_rolled = True

    def next_turn(self):
        print('player ', self.player_turn, '\'s turn has ended')
        self.player_turn += 1
        if self.player_turn == len(self.players):
            self.first_rotate = False
            self.player_turn = 0
        print('player ', self.player_turn, '\'s turn has begun')
        self.dice_rolled = False

    # Dev Cards ################################

    def monopoly_rotate(self):
        if self.monopoly_id == len(self.players) - 1:
            self.monopoly_id = 0
        else:
            self.monopoly_id += 1
        if self.monopoly_id == self.player_turn:
            self.in_monopoly = False

    def monopoly(self, data):
        self.in_monopoly = True
        self.monopoly_resource = data
        if self.player_turn == len(self.players) - 1:
            self.monopoly_id = 0
        else:
            self.monopoly_id = self.player_turn + 1

    def move_thief(self, index_of_new_thief):
        i = 0
        while i < len(self.board.lot):
            if i == index_of_new_thief:
                self.board.lot[i].thief = True
            else:
                self.board.lot[i].thief = False
            i += 1

    def dev_card_bought(self, index):
        self.dev_cards.pop(index)
            
    # Stealing ################################
    
    def steal_resource_setup(self, info):
        self.robbed_resource = info[0]
        self.robbed_player_id = info[1]
        self.robbing = True
        
    def stop_robbing(self):
        self.robbing = False

    # Trade ###############################

    def send_trade_offer(self, data):
        give = data[0]
        get = data[1]
        self.in_trade = True
        self.resources_to_give = give
        self.resources_to_get = get
        if self.player_turn == len(self.players) - 1:
            self.trade_id = 0
        else:
            self.trade_id = self.player_turn + 1

    def rotate_trade_offer(self):
        if self.trade_id == len(self.players) - 1:
            self.trade_id = 0
        else:
            self.trade_id += 1
        if self.trade_id == self.player_turn:
            self.in_trade = False
            self.resources_to_give = []
            self.resources_to_get = []

    def trade_accepted(self):
        self.in_trade = False
        self.accept_trade = True

    def trade_collected(self):
        self.accept_trade = False

    def vp_updates(self):
        for player in self.players:
            if len(player.roads) > self.record_road:
                self.longest_road = player.playerId
                self.record_road = len(player.roads)
            if player.army > self.record_army:
                self.largest_army = player.playerId
                self.record_army = player.army
            if player.count_vps() >= 10:
                self.game_over = True
                self.winning_player = player.playerId
