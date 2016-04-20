from collections import Counter

import conf
import combine


class Factory:
    def __init__(self):
        self.performance = conf.factory_performance
        self.complete_salt = 0
        self.salt_counter = Counter()

    def handle(self, comb: combine.Combine):
        while self.complete_salt < self.performance:
            self.salt_counter[comb.extracted_cells[0]] += 1
            del comb.extracted_cells[0]
            if len(comb.extracted_cells) == 0:
                comb.current_cells = 0
                break
            self.complete_salt += 1
        pass
