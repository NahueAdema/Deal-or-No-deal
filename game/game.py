import random
from sqlalchemy.orm import Session
import db
from flask_login import current_user
from models.models import GameState

CASE_VALS = [0.01, 1, 5, 10, 25, 50, 75, 100, 200, 300, 400, 500, 750, 1000, 5000, 10000, 25000, 50000, 75000, 100000, 200000, 300000, 400000, 500000, 750000, 1000000]

class Case:
    def __init__(self, value, num):
        self.value = value
        self.available = True
        self.num = num

    def __str__(self):
        return "[" + str(self.num) + "]"

class DealOrNoDeal:
    def __init__(self, case_vals=CASE_VALS):
        self.initialize_game(case_vals)
        self.load_state()

    def initialize_game(self, case_vals):
        self.case_vals = random.sample(case_vals, len(case_vals))
        self.vals_left = self.case_vals.copy()
        self.cases = [Case(value, num) for num, value in enumerate(self.case_vals, 1)]
        self.chosen_case = None
        self.rounds = [5, 5, 5, 5, 3, 1, 1]
        self.current_round = 0
        self.offers = []
        self.playing = True
        self.revealed_cases = set()

    def load_state(self):
        if current_user.is_authenticated:
            game_state = db.session.query(GameState).filter_by(user_id=current_user.id).first()
            if game_state:
                self.chosen_case = self.cases[game_state.chosen_case - 1] if game_state.chosen_case else None
                self.current_round = game_state.current_round
                self.playing = game_state.playing
                self.vals_left = list(map(float, game_state.vals_left.split(','))) if game_state.vals_left else []
                self.revealed_cases = set(map(int, game_state.revealed_cases.split(','))) if game_state.revealed_cases else set()
                self.offers = list(map(float, game_state.offers.split(','))) if game_state.offers else []
                for case in self.cases:
                    if case.num == (self.chosen_case.num if self.chosen_case else None) or case.num in self.revealed_cases:
                        case.available = False

    def save_state(self):
        if current_user.is_authenticated:
            game_state = db.session.query(GameState).filter_by(user_id=current_user.id).first()
            if not game_state:
                game_state = GameState(user_id=current_user.id)
            game_state.chosen_case = self.chosen_case.num if self.chosen_case else None
            game_state.current_round = self.current_round
            game_state.playing = self.playing
            game_state.vals_left = ','.join(map(str, self.vals_left))
            game_state.revealed_cases = ','.join(map(str, self.revealed_cases))
            game_state.offers = ','.join(map(str, self.offers))
            db.session.add(game_state)
            db.session.commit()

    def get_cases(self):
        return [{"num": case.num, "disabled": not case.available, "selected": case == self.chosen_case, "revealed": case.num in self.revealed_cases} for case in self.cases]

    def get_values_left(self):
        return self.vals_left

    def choose_case(self, num):
        self.chosen_case = self.cases[num - 1]
        self.cases[num - 1].available = False
        self.save_state()

    def reveal_cases(self, nums):
        num_to_reveal = self.get_num_cases_to_reveal()
        if len(nums) != num_to_reveal:
            raise ValueError("Número incorrecto de casos seleccionados para revelar")

        revealed = []
        # print(f"Valores restantes antes de revelar: {self.vals_left}")
        # print(f"Maletines a revelar: {nums}")

        for num in nums:
            case = self.cases[num - 1]
            if case.available and case.num not in self.revealed_cases:
                case.available = False
                if case.value in self.vals_left:
                    self.vals_left.remove(case.value)
                revealed.append((case.num, case.value))
                self.revealed_cases.add(num)

        # Prints usados para debug JJAJAJAJAJA
        print(f"Maletines revelados en esta ronda: {revealed}")
        # print(f"Maletines revelados acumulados: {self.revealed_cases}")
        print(f"Valores restantes después de revelar: {self.vals_left}")

        if len(self.vals_left) <= 1:
            self.playing = False

        if revealed:
            self.current_round += 1

        self.save_state()
        self.check_game_end()
        return revealed

    def get_dealer_offer(self):
        average = sum(self.vals_left) / len(self.vals_left)
        multiplier = random.uniform(0.5, 0.75)
        offer = round(average * multiplier, 2)
        self.add_offer(offer)
        return offer

    def get_final_choice(self, keep_original):
        if keep_original:
            return self.chosen_case
        else:
            return [case for case in self.cases if case.available][0]

    def add_offer(self, offer):
        self.offers.append(offer)
        self.save_state()

    def get_offers(self):
        return self.offers

    def get_num_cases_to_reveal(self):
        if not self.playing:
            return 0
        if self.current_round < len(self.rounds):
            return self.rounds[self.current_round]
        return 1

    def check_game_end(self):
        if len(self.vals_left) <= 1:
            self.playing = False
            self.save_state()
            return True
        return False

    def get_final_case_value(self):
        if self.chosen_case:
            return self.chosen_case.value
        return None
