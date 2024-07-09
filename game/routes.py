from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from game.game import game 

game_bp = Blueprint("game_bp", __name__, template_folder="templates/game", static_folder="static")

@game_bp.route('/')
@login_required
def game_index():
    cases = game.get_cases()
    return render_template('game.html', cases=cases)

@game_bp.route('/choose_case', methods=['POST'])
@login_required
def choose_case():
    num = int(request.form['case_num'])
    game.choose_case(num)
    return jsonify(success=True)

@game_bp.route('/reveal_cases', methods=['POST'])
@login_required
def reveal_cases():
    nums = request.json['case_nums']
    revealed = game.reveal_cases(nums)
    return jsonify(revealed=revealed)

@game_bp.route('/get_offer', methods=['GET'])
@login_required
def get_offer():
    offer = game.get_dealer_offer()
    game.add_offer(offer)
    return jsonify(offer=offer)

@game_bp.route('/final_choice', methods=['POST'])
@login_required
def final_choice():
    keep_original = request.json['keep_original']
    final_case = game.get_final_choice(keep_original)
    return jsonify(case_num=final_case.num, case_value=final_case.value, offers=game.get_offers())
