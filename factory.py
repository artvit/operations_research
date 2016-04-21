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
        c20 = comb.extracted_cells[20]
        c50 = comb.extracted_cells[50]
        c80 = comb.extracted_cells[80]
        if c50 % 2:
            self.day_buffer[50] += 1
            c50 -= 1
        if self.day_buffer[50] == 2:
            self.day_buffer[50] = 0
            self.money += conf.salt_cost
            self.complete_salt += 2
        if c50 > self.available_salt:
            c50 -= self.available_salt
            comb.current_cells -= self.available_salt
            comb.extracted_cells[50] -= self.available_salt
            self.money += (self.available_salt // 2) * conf.salt_cost
            self.complete_salt += self.available_salt
        else:
            comb.current_cells -= c50
            self.money += (c50 // 2) * conf.salt_cost
            self.complete_salt += c50
            comb.extracted_cells[50] -= c50

        s = min(c20, c80, self.available_salt)
        comb.current_cells -= s
        self.money += s * conf.salt_cost
        self.complete_salt += s
        comb.extracted_cells[20] -= s
        comb.extracted_cells[80] -= s
        c20, c80 = c20 - s, c80 - s
        if not self.available_salt:
            return
        else:
            if c20 > c80:
                s = c20 - c80
                if self.available_wh1 > s:
                    self.add_to_wh1(s, comb)
                else:
                    s -= self.available_wh1
                    self.add_to_wh1(self.available_wh1, comb)
                    if 0 < s < self.available_wh2:
                        self.add_to_wh2(s, comb)
                    else:
                        comb.current_cells -= comb.extracted_cells[20]
                        comb.extracted_cells[20] = 0
        comb.in_shaft = False

    def add_to_wh1(self, amt, comb: combine.Combine):
        assert amt < self.available_wh1
        self.warehouse1 += amt
        comb.extracted_cells[20] -= amt
        comb.current_cells -= amt

    def add_to_wh2(self, amt, comb: combine.Combine):
        assert amt < self.available_wh2
        self.warehouse2 += amt
        comb.extracted_cells[20] -= amt
        comb.current_cells -= amt

    def day_ending(self):
        pass
