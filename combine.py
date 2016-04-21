from random import choice
from collections import Counter

import conf


class Combine:
    def __init__(self, point, field, i=-1):
        self.x = point[0]
        self.y = point[1]
        self.field = field
        self.way = []
        self.extracted_cells = Counter()
        self.in_shaft = False
        if i != -1:
            self.capacity = conf.combine_capacity[i]
            self.move_cost = conf.combine_move_cost[i]
            self.speed = conf.combine_speed[i]
        self.moves = 0
        self.target_value = 0
        self.day_expanses = 0

    def easy_way(self, cell_values):
        nearest_cells = self.get_neighbor_cells()
        nearest_cells = list(filter(lambda x: self.field[x[1]][x[0]] in cell_values, nearest_cells))
        if len(nearest_cells):
            return choice(nearest_cells)

    def find_way_to_nearest(self, cell_values):
        near_cell = self.easy_way(cell_values)
        if near_cell:
            return [near_cell]
        d = {}
        p = {}
        targets = set()
        seen = set()
        not_seen = set()
        search_list = [0, conf.shaft_const] + list(cell_values)
        for cell in self.get_neighbor_cells():
            if self.field[cell[1]][cell[0]] in search_list:
                d[cell] = float('inf')
                not_seen.add(cell)
        d[(self.x, self.y)] = 0
        p[(self.x, self.y)] = []
        not_seen.add((self.x, self.y))
        while len(not_seen):
            v = min(not_seen, key=d.get)
            not_seen.remove(v)
            seen.add(v)
            v_neighbors = self.get_neighbor_cells(v)
            for cell in v_neighbors:
                if self.field[cell[1]][cell[0]] in search_list and cell not in seen:
                    if cell not in d:
                        d[cell] = float('inf')
                    not_seen.add(cell)
            for cell in filter(lambda x: x in not_seen, v_neighbors):
                if d[cell] > d[v] + self.move_cost:
                    d[cell] = d[v] + self.move_cost
                    p[cell] = p[v] + [cell]
                    if self.field[cell[1]][cell[0]] in cell_values:
                        targets.add(cell)
        # return [p[x] for x in targets]
        return p[min(targets, key=d.get)]

    def get_neighbor_cells(self, point=None):
        if point:
            return self._get_neighbors_for(point[0], point[1])
        else:
            return self._get_neighbors_for(self.x, self.y)

    def _get_neighbors_for(self, x, y):
        neighbors = []
        if x + 1 < len(self.field[0]):
            neighbors.append((x + 1, y))
        if y + 1 < len(self.field[0]):
            neighbors.append((x, y + 1))
        if x - 1 >= 0:
            neighbors.append((x - 1, y))
        if y - 1 >= 0:
            neighbors.append((x, y - 1))
        return neighbors

    def get_way(self):
        if self.current_cells < self.capacity:
            way = self.find_way_to_nearest([20, 50, 80])
            cell = way[-1]
            self.target_value = self.field[cell[1]][cell[0]]
            self.field[cell[1]][cell[0]] = conf.target_const
            return way
        else:
            return self.find_way_to_nearest([conf.shaft_const])

    def move(self):
        if self.in_shaft:
            return
        if self.moves >= self.speed:
            return

        if not self.way:
            self.way = self.get_way()

        cell = self.way[0]

        if self.field[self.y][self.x] == conf.busy_const:
            self.field[self.y][self.x] = 0

        self.x, self.y = cell
        self.moves += 1
        self.day_expanses += self.move_cost

        if self.field[self.y][self.x] == conf.target_const:
            self.extracted_cells[self.target_value] += 1
            self.field[self.y][self.x] = conf.busy_const
        elif self.field[self.y][self.x] == 0:
            self.field[self.y][self.x] = conf.busy_const
        self.way.pop(0)
        if self.field[self.y][self.x] == conf.shaft_const and self.current_cells == self.capacity:
            self.in_shaft = True

    @property
    def current_cells(self):
        return sum(self.extracted_cells.values())

    def remove(self, value, amt):
        assert amt <= self.extracted_cells[value]
        self.extracted_cells[value] -= amt

    @property
    def ore20(self):
        return self.extracted_cells[20]

    @property
    def ore50(self):
        return self.extracted_cells[50]

    @property
    def ore80(self):
        return self.extracted_cells[80]
