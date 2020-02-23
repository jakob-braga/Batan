class Player:
    def __init__(self, playerId):
        self.playerId = playerId

        self.lumber = 1
        self.wheat = 1
        self.sheep = 1
        self.ore = 0
        self.brick = 1

        self.army = 0

        self.largest_army = False
        self.longest_road = False

        self.settlements = []
        self.roads = []
        self.dev_cards = []

        self.ready = False

    # checks #########################

    def can_buy_settlement(self):
        if self.lumber >= 1 and self.brick >= 1 and self.sheep >= 1 and self.wheat >= 1 and len(self.settlements) < 5:
            return True
        elif len(self.settlements) < 2:
            return True
        else:
            return False

    def can_upgrade_settlement(self):
        if self.wheat >= 2 and self.ore >= 3 and self.count_cities() < 4:
            return True
        else:
            return False

    def can_buy_road(self):
        if (self.brick >= 1 and self.lumber >= 1 and len(self.roads) < 15) or len(self.roads) < 2:
            return True
        else:
            return False

    def can_buy_dev_card(self, lodc):
        if self.sheep >= 1 and self.wheat >= 1 and self.ore >= 1 and lodc:
            return True
        else:
            return False

    def road_at_pos(self, pos):
        for road in self.roads:
            if road.is_inside_local(1, pos) or road.is_inside_local(2, pos):
                return True
        return False

    def settlement_at_pos(self, pos):
        for settlement in self.settlements:
            if settlement.is_inside_local(pos):
                return True
        return False

    # purchase #########################

    def buy_settlement(self):
        if len(self.settlements) >= 2:
            self.lumber -= 1
            self.brick -= 1
            self.sheep -= 1
            self.wheat -= 1

    def upgrade_settlement(self):
        self.wheat -= 2
        self.ore -= 3

    def buy_road(self):
        if len(self.roads) >= 2:
            self.brick -= 1
            self.lumber -= 1

    def buy_dev_card(self):
        self.sheep -= 1
        self.wheat -= 1
        self.ore -= 1

    # misc ####################

    def count_resources(self):
        sum_of_resources = self.brick + self.lumber + self.sheep + self.wheat + self.ore
        return sum_of_resources
    
    def get_list_of_resources(self):
        resource_list = []
        resource_list = resource_list + (['lumber'] * self.lumber) + (['wheat'] * self.wheat) + (['ore'] * self.ore)
        resource_list = resource_list + (['brick'] * self.brick) + (['sheep'] * self.sheep)
        return resource_list

    def count_cities(self):
        i = 0
        for settlement in self.settlements:
            if settlement.level == 2:
                i += 1
        return i

    # dev cards ###############

    def count_dev_card(self, card_type):
        i = 0
        for card in self.dev_cards:
            if card == card_type:
                i += 1

        return i

    def pop_dev_card(self, card_type):
        i = 0
        while i < len(self.dev_cards):
            if self.dev_cards[i] == card_type:
                self.dev_cards.pop(i)
                return
            i += 1
            
    # Trade #################
    
    def can_4_for_1(self):
        t1 = self.wheat >= 4 or self.lumber >= 4 or self.ore >= 4 or self.brick >= 4 or self.sheep >= 4
        return t1
    
    def can_3_for_1(self):
        can = self.wheat >= 3 or self.lumber >= 3 or self.ore >= 3 or self.brick >= 3 or self.sheep >= 3
        return can

    def add_amount_of(self, resource, num):
        if resource == 'lumber':
            self.lumber += num
        elif resource == 'sheep':
            self.sheep += num
        elif resource == 'wheat':
            self.wheat += num
        elif resource == 'ore':
            self.ore += num
        elif resource == 'brick':
            self.brick += num

    def has_resources(self):
        can = self.wheat or self.lumber or self.ore or self.brick or self.sheep
        return can

    # victory_points

    def count_vps(self):
        vps = 0
        for settlement in self.settlements:
            vps += settlement.level
        vps += self.dev_cards.count('victory_point')
        if self.longest_road:
            vps += 2
        if self.largest_army:
            vps += 2
        return vps

