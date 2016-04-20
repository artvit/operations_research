from random import choice

import conf


class Combine:
    def __init__(self, point, field, i=-1):
        self.x = point[0]
        self.y = point[1]
        self.field = field
        self.way = []
        self.extracted_cells = []
        self.current_cells = 0
        self.in_shaft = False
        if i != -1:
            self.capacity = conf.combine_capacity[i]
            self.move_cost = conf.combine_move_cost[i]

    def find_nearest_available(self):
        rx, ry = -1, -1
        k = 1
        not_found = True
        while not_found:
            for i in range(2 * k + 1):
                if self.field[self.y - k][self.x - k + i] in [20, 50, 80]:
                    rx, ry = self.y - k, self.x - k + i
                    not_found = False
                if self.field[self.y + k][self.x - k + i] in [20, 50, 80]:
                    rx, ry = self.y + k, self.x - k + i
                    not_found = False
            for i in range(2 * k - 1):
                if self.field[self.y - k + 1 + i][self.x - k] in [20, 50, 80]:
                    rx, ry = self.y - k + 1 + i, self.x - k
                    not_found = False
                if self.field[self.y - k + 1 + i][self.x + k] in [20, 50, 80]:
                    rx, ry = self.y - k + 1 + i, self.x + k
                    not_found = False
            k += 1
        return rx, ry

    def find_way_to_nearest(self, cell_values):
        nearest_cells = self.get_neighbor_cells()
        nearest_cells = list(filter(lambda x: self.field[x[1]][x[0]] in cell_values, nearest_cells))
        if len(nearest_cells):
            return [choice(nearest_cells)]
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
            for cell in self.get_neighbor_cells(v):
                if self.field[cell[1]][cell[0]] in search_list and cell not in seen:
                    if cell not in d:
                        d[cell] = float('inf')
                    not_seen.add(cell)
            for cell in filter(lambda x: x in not_seen, self.get_neighbor_cells(v)):
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
            self.field[cell[1]][cell[0]] = conf.target_const
            return way
        else:
            return self.find_way_to_nearest([conf.shaft_const])

    def move(self):
        if self.field[self.y][self.x] == conf.shaft_const and self.current_cells == self.capacity:
            self.in_shaft = True
            return
        if not self.way:
            self.way = self.get_way()
        cell = self.way[0]
        if self.field[cell[1]][cell[0]] == conf.busy_const:
            # TODO if deadlock
            return
        if self.field[self.y][self.x] == conf.busy_const:
            self.field[self.y][self.x] = 0

        self.x, self.y = cell

        if self.field[self.y][self.x] == conf.target_const:
            self.extracted_cells.append(self.field[self.y][self.x])
            self.current_cells += 1
            self.field[self.y][self.x] = conf.busy_const
        elif self.field[self.y][self.x] == 0:
            self.field[self.y][self.x] = conf.busy_const
        self.way.pop(0)
