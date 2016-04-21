from collections import Counter

import conf
import combine


class Factory:
    def __init__(self):
        self.warehouse1 = 0
        self.warehouse2 = 0
        self.performance = conf.factory_performance
        self.complete_salt = 0
        self.day_buffer = Counter()
        self.money = 0

    @property
    def available_wh2(self):
        return conf.warehouse2_capacity - self.warehouse2

    @property
    def available_wh1(self):
        return conf.warehouse1_capacity - self.warehouse1

    @property
    def available_salt(self):
        return self.performance - self.complete_salt

    def handle(self, comb: combine.Combine):
        if comb.ore50:
            if comb.ore50 % 2:
                self.day_buffer[50] += 1
                comb.remove(50, 1)
            if self.day_buffer[50] == 2:
                self.day_buffer[50] = 0
                self.money += conf.salt_cost
                self.complete_salt += 2

            if comb.ore50 > self.available_salt:
                comb.remove(50, self.available_salt)
                self.money += (self.available_salt // 2) * conf.salt_cost
                self.complete_salt += self.available_salt
            else:
                self.money += (comb.ore50 // 2) * conf.salt_cost
                self.complete_salt += comb.ore50
                comb.remove(50, comb.ore50)

        s = min(comb.ore20, comb.ore80, self.available_salt)
        self.money += s * conf.salt_cost
        self.complete_salt += s * 2
        comb.remove(20, s)
        comb.remove(80, s)
        if not self.available_salt:
            return
        else:
            if comb.ore20 > comb.ore80:
                s = comb.ore20 - comb.ore80
                if self.available_wh1 > s:
                    self.add_to_wh1(s, comb)
                else:
                    s -= self.available_wh1
                    self.add_to_wh1(self.available_wh1, comb)
                    if 0 < s < self.available_wh2:
                        self.add_to_wh2(s, comb)
                    else:
                        comb.remove(20, comb.ore20)
            elif comb.ore80 > comb.ore20:
                s = comb.ore80 - comb.ore20
                if self.warehouse2 >= s:
                    while self.available_salt and s:
                        self.warehouse2 -= 1
                        comb.remove(80, 1)
                        self.money += conf.salt_cost
                        self.complete_salt += 2
                        s -= 1
                elif self.warehouse2 > 0:
                    while self.available_salt and s and self.warehouse2:
                        comb.remove(80, 1)
                        s -= 1
                        self.warehouse2 -= 1
                        self.complete_salt += 2
                if s:
                    if self.warehouse1 >= s:
                        while self.available_salt and s:
                            self.warehouse1 -= 1
                            comb.remove(80, 1)
                            self.money += conf.salt_cost
                            self.complete_salt += 2
                            s -= 1
                    elif self.warehouse1 > 0:
                        while self.available_salt and s and self.warehouse1:
                            comb.remove(80, 1)
                            s -= 1
                            self.warehouse1 -= 1
                            self.complete_salt += 2

        if comb.current_cells == 0:
            comb.in_shaft = False

    def add_to_wh1(self, amt, comb: combine.Combine):
        assert amt <= self.available_wh1
        self.warehouse1 += amt
        comb.remove(20, amt)

    def add_to_wh2(self, amt, comb: combine.Combine):
        assert amt <= self.available_wh2
        self.warehouse2 += amt
        comb.remove(20, amt)

    def day_ending(self):
        self.money -= (self.warehouse1 + self.warehouse2) * conf.storing_cost
