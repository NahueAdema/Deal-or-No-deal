import random
CASE_VALS = [1,5,10,15,25,50,75,100,200,300,400,500,750,1000,5000,10000,25000,50000,75000,100000,200000,300000,400000,500000,750000,1000000]

class Case:
    def __init__(self, value, num):
        self.value = value
        self.available = True
        self.num = num

    def __str__(self):
        return "[" + str(self.num) + "]"


class DealOrNoDeal:
    def __init__(self, case_vals=CASE_VALS):
        self.case_vals = sorted(case_vals)
        self.vals_left = case_vals
        random.shuffle(case_vals)
        self.cases = [Case(value, num) for num, value in enumerate(case_vals, 1)]
        self.__choice_case = None
        self.rounds = [5, 5, 5, 5, 3, 1]
        self.offers = []
        self.playing = True

    def get_cases(self):
        return [str(case) for case in self.cases]

    def get_values_left(self):
        return self.vals_left

    def choose_case(self, num):
        self.__choice_case = self.cases[num - 1]
        self.cases[num - 1].available = False

    def reveal_cases(self, nums):
        revealed = []
        for num in nums:
            case = self.cases[num - 1]
            case.available = False
            self.vals_left.remove(case.value)
            revealed.append((case.num, case.value))
        return revealed

    def get_dealer_offer(self):
        return round((sum(self.vals_left) / len(self.vals_left)) * (random.randrange(75, 86) / 100), 2)

    def get_final_choice(self, keep_original):
        if keep_original:
            return self.__choice_case
        else:
            return [case for case in self.cases if case.available][0]

    def add_offer(self, offer):
        self.offers.append(offer)

    def get_offers(self):
        return self.offers


game = DealOrNoDeal()