from tile import *
import random


class Board:
    def __init__(self):
        self.x = 600
        self.y = 250
        self.lot = []
        self.water_tile_list = []
        self.type_list = (['sheep'] * 4) + (['lumber'] * 4) + (['wheat'] * 4) + (['brick'] * 3) + (['ore'] * 3) + ['desert']
        self.type_list_ext = (['lumber'] * 2) + (['wheat'] * 2) + (['sheep'] * 2) + (['brick'] * 2) + (['ore'] * 2) + ['desert']
        self.val_list = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
        self.val_list_ext = [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
        self.port_list = ['sheep', 'lumber', 'wheat', 'brick', 'ore'] + (['any'] * 4)
        self.port_list_ext = ['any', 'sheep']
        self.big = False
        self.construct_small()

    # make small board

    def construct_small(self):
        self.big = False
        self.lot = []
        self.water_tile_list = []
        self.x = 600
        self.y = 250
        tlc = self.type_list.copy()
        vlc = self.val_list.copy()
        column = 0
        c_spacing = 73
        r_spacing = 45
        offset = round(24 * math.sqrt(3)) - 3
        row = 0
        while row < 3:
            i = random.randint(0, len(tlc) - 1)
            if tlc[i] == 'desert':
                vlc.insert(0, 0)
                j = 0
            else:
                j = random.randint(0, len(vlc) - 1)
            self.lot.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), tlc[i], vlc[j]))
            vlc.pop(j)
            tlc.pop(i)
            row += 1
        row = 0

        column = 1
        self.y -= offset
        while row < 4:
            i = random.randint(0, len(tlc) - 1)
            if tlc[i] == 'desert':
                vlc.insert(0, 0)
                j = 0
            else:
                j = random.randint(0, len(vlc) - 1)
            self.lot.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), tlc[i], vlc[j]))
            tlc.pop(i)
            vlc.pop(j)
            row += 1
        row = 0
        column = 2
        self.y -= offset
        while row < 5:
            i = random.randint(0, len(tlc) - 1)
            if tlc[i] == 'desert':
                vlc.insert(0, 0)
                j = 0
            else:
                j = random.randint(0, len(vlc) - 1)
            self.lot.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), tlc[i], vlc[j]))
            tlc.pop(i)
            vlc.pop(j)
            row += 1
        row = 0
        column = 3
        self.y += offset
        while row < 4:
            i = random.randint(0, len(tlc) - 1)
            if tlc[i] == 'desert':
                vlc.insert(0, 0)
                j = 0
            else:
                j = random.randint(0, len(vlc) - 1)
            self.lot.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), tlc[i], vlc[j]))
            tlc.pop(i)
            vlc.pop(j)
            row += 1
        row = 0
        column = 4
        self.y += offset
        while row < 3:
            i = random.randint(0, len(tlc) - 1)
            if tlc[i] == 'desert':
                vlc.insert(0, 0)
                j = 0
            else:
                j = random.randint(0, len(vlc) - 1)
            self.lot.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), tlc[i], vlc[j]))
            tlc.pop(i)
            vlc.pop(j)
            row += 1
        del tlc
        del vlc
        self.randomize_vals()
        self.construct_water_small()
        self.lot.extend(self.water_tile_list)

    def construct_water_small(self):
        self.water_tile_list = []
        wtl = self.water_tile_list
        c_spacing = 73
        r_spacing = 45
        offset = round(24 * math.sqrt(3)) - 3
        row = 0

        column = -1
        self.y -= offset
        while row < 4:
            wtl.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), 'water', 0))
            row += 1
        row = 0

        column = 0
        self.y -= offset
        while row < 5:
            wtl.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), 'water', 0))
            row += 1
        row = 0

        column = 1
        self.y -= offset
        while row < 6:
            wtl.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), 'water', 0))
            row += 1
        row = 0

        column = 2
        self.y -= offset
        while row < 7:
            wtl.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), 'water', 0))
            row += 1
        row = 0

        column = 3
        self.y += offset
        while row < 6:
            wtl.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), 'water', 0))
            row += 1
        row = 0

        column = 4
        self.y += offset
        while row < 5:
            wtl.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), 'water', 0))
            row += 1
        row = 0

        column = 5
        self.y += offset
        while row < 4:
            wtl.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), 'water', 0))
            row += 1

        # cut out land

        j = 0
        adjust = 0
        lor = [range(5, 8), range(10, 14), range(16, 21), range(23, 27), range(29, 32)]
        while j < 37:
            for rng in lor:
                if j in rng:
                    wtl.pop(j - adjust)
                    adjust += 1
            j += 1
        del lor

        self.randomize_ports_small()

    def randomize_ports_small(self):
        wtl = self.water_tile_list
        list_of_magic_numbers = [0, 2, 5, 6, 9, 10, 13, 14, 16]
        plc = self.port_list.copy()
        # this whole thing is disgusting, but really, REALLY. You should be ashamed of yourself
        j = 0
        while j < len(wtl):
            if j in list_of_magic_numbers:
                i = random.randint(0, len(plc) - 1)
                wtl[j].val = -1
                wtl[j].type = plc[i]
                plc.pop(i)
            j += 1
        del j, list_of_magic_numbers, plc

    # make large board

    def construct_big(self):
        self.big = True
        self.lot = []
        self.water_tile_list = []
        self.x = 520
        self.y = 250
        tlc = self.type_list.copy()
        tlc.extend(self.type_list_ext)
        vlc = self.val_list.copy()
        vlc.extend(self.val_list_ext)
        column = 0
        c_spacing = 73
        r_spacing = 45
        offset = round(24 * math.sqrt(3)) - 3
        row = 0
        while row < 3:
            i = random.randint(0, len(tlc) - 1)
            if tlc[i] == 'desert':
                vlc.insert(0, 0)
                j = 0
            else:
                j = random.randint(0, len(vlc) - 1)
            self.lot.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), tlc[i], vlc[j]))
            vlc.pop(j)
            tlc.pop(i)
            row += 1
        row = 0

        column = 1
        self.y -= offset
        while row < 4:
            i = random.randint(0, len(tlc) - 1)
            if tlc[i] == 'desert':
                vlc.insert(0, 0)
                j = 0
            else:
                j = random.randint(0, len(vlc) - 1)
            self.lot.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), tlc[i], vlc[j]))
            tlc.pop(i)
            vlc.pop(j)
            row += 1
        row = 0

        column = 2
        self.y -= offset
        while row < 5:
            i = random.randint(0, len(tlc) - 1)
            if tlc[i] == 'desert':
                vlc.insert(0, 0)
                j = 0
            else:
                j = random.randint(0, len(vlc) - 1)
            self.lot.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), tlc[i], vlc[j]))
            tlc.pop(i)
            vlc.pop(j)
            row += 1
        row = 0

        column = 3
        self.y -= offset
        while row < 6:
            i = random.randint(0, len(tlc) - 1)
            if tlc[i] == 'desert':
                vlc.insert(0, 0)
                j = 0
            else:
                j = random.randint(0, len(vlc) - 1)
            self.lot.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), tlc[i], vlc[j]))
            tlc.pop(i)
            vlc.pop(j)
            row += 1
        row = 0

        column = 4
        self.y += offset
        while row < 5:
            i = random.randint(0, len(tlc) - 1)
            if tlc[i] == 'desert':
                vlc.insert(0, 0)
                j = 0
            else:
                j = random.randint(0, len(vlc) - 1)
            self.lot.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), tlc[i], vlc[j]))
            tlc.pop(i)
            vlc.pop(j)
            row += 1
        row = 0

        column = 5
        self.y += offset
        while row < 4:
            i = random.randint(0, len(tlc) - 1)
            if tlc[i] == 'desert':
                vlc.insert(0, 0)
                j = 0
            else:
                j = random.randint(0, len(vlc) - 1)
            self.lot.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), tlc[i], vlc[j]))
            tlc.pop(i)
            vlc.pop(j)
            row += 1
        row = 0

        column = 6
        self.y += offset
        while row < 3:
            i = random.randint(0, len(tlc) - 1)
            if tlc[i] == 'desert':
                vlc.insert(0, 0)
                j = 0
            else:
                j = random.randint(0, len(vlc) - 1)
            self.lot.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), tlc[i], vlc[j]))
            tlc.pop(i)
            vlc.pop(j)
            row += 1
        del tlc
        del vlc
        self.randomize_vals()
        self.construct_water_big()
        self.lot.extend(self.water_tile_list)

    def construct_water_big(self):
        self.water_tile_list = []
        wtl = self.water_tile_list
        c_spacing = 73
        r_spacing = 45
        offset = round(24 * math.sqrt(3)) - 3
        row = 0

        column = -1
        self.y -= offset
        while row < 4:
            wtl.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), 'water', 0))
            row += 1
        row = 0

        column = 0
        self.y -= offset
        while row < 5:
            wtl.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), 'water', 0))
            row += 1
        row = 0

        column = 1
        self.y -= offset
        while row < 6:
            wtl.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), 'water', 0))
            row += 1
        row = 0

        column = 2
        self.y -= offset
        while row < 7:
            wtl.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), 'water', 0))
            row += 1
        row = 0

        column = 3
        self.y -= offset
        while row < 8:
            wtl.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), 'water', 0))
            row += 1
        row = 0

        column = 4
        self.y += offset
        while row < 7:
            wtl.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), 'water', 0))
            row += 1
        row = 0

        column = 5
        self.y += offset
        while row < 6:
            wtl.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), 'water', 0))
            row += 1
        row = 0

        column = 6
        self.y += offset
        while row < 5:
            wtl.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), 'water', 0))
            row += 1
        row = 0

        column = 7
        self.y += offset
        while row < 4:
            wtl.append(Tile((self.x + (column * c_spacing)), (self.y + (round(row * (r_spacing * math.sqrt(3))))), 'water', 0))
            row += 1

        # cut out land

        j = 0
        adjust = 0
        lor = [range(5, 8), range(10, 14), range(16, 21), range(23, 29), range(31, 36), range(38, 42), range(44, 47)]
        while j < 52:
            for rng in lor:
                if j in rng:
                    wtl.pop(j - adjust)
                    adjust += 1
            j += 1
        del lor

        self.randomize_ports_big()

    def randomize_ports_big(self):
        wtl = self.water_tile_list
        list_of_magic_numbers = [0, 2, 5, 6, 9, 10, 13, 14, 17, 18, 20]
        plc = self.port_list.copy()
        plc.extend(self.port_list_ext)
        # this whole thing is disgusting, but really, REALLY. You should be ashamed of yourself
        j = 0
        while j < len(wtl):
            if j in list_of_magic_numbers:
                i = random.randint(0, len(plc) - 1)
                wtl[j].val = -1
                wtl[j].type = plc[i]
                plc.pop(i)
            j += 1
        del j, list_of_magic_numbers, plc

    # randomize

    def randomize_tiles(self):
        tlc = self.type_list.copy()
        vlc = self.val_list.copy()
        if self.big:
            tlc.extend(self.type_list_ext)
            vlc.extend(self.val_list_ext)
        for tile in self.lot:
            if tile.val >= 0 and tile.type != 'water':
                i = random.randint(0, len(tlc) - 1)
                tile.type = tlc[i]
                if tile.type == 'desert':
                    vlc.insert(0, 0)
                    j = 0
                else:
                    j = random.randint(0, len(vlc) - 1)
                tile.val = vlc[j]
                vlc.pop(j)
                tlc.pop(i)
        del vlc, tlc, i, j
        if self.big:
            self.randomize_ports_big()
        else:
            self.randomize_ports_small()
        self.randomize_vals()

    def randomize_vals(self):
        vlc = self.val_list.copy()
        if self.big:
            vlc.extend(self.val_list_ext)
        for tile in self.lot:
            if tile.type != 'water' and tile.type != 'desert' and tile.val > 0:
                i = random.randint(0, len(vlc) - 1)
                tile.val = vlc[i]
                vlc.pop(i)
        del vlc
        if not self.tile_val_check():
            self.randomize_vals()

    def tile_val_check(self):
        i = 0
        while i < len(self.lot):
            j = i + 1
            while j < len(self.lot):
                if (self.lot[i].val in range(6, 9)) and (self.lot[j].val in range(6, 9)):
                    dist = math.sqrt((self.lot[i].x - self.lot[j].x) ** 2 + (self.lot[i]. y - self.lot[j].y) ** 2)
                    if dist < self.lot[i].radius * 2:
                        return False
                j += 1
            i += 1
        return True

    # misc

    def count_intersections(self, pos):
        i = 0
        for tile in self.lot:
            if tile.is_inside(pos):
                i += 1
        return i

    # finish

    def finalize_board(self):
        del self.water_tile_list, self.type_list, self.val_list, self.port_list, self.type_list_ext, self.val_list_ext, self.port_list_ext
