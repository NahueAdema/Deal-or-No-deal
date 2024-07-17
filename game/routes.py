from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from .game import DealOrNoDeal as GameInstance

game_bp = Blueprint("game_bp", __name__, template_folder="templates/game", static_folder="static")

game_instance = GameInstance()

@game_bp.route('/')
@login_required
def game_index():
    cases = game_instance.get_cases()
    return render_template('game.html', cases=cases)

@game_bp.route('/choose_case', methods=['POST'])
@login_required
def choose_case():
    num = int(request.form['case_num'])
    game_instance.choose_case(num)
    return redirect(url_for('game_bp.reveal_cases'))

@game_bp.route('/reveal_cases', methods=['GET', 'POST'])
@login_required
def reveal_cases():
    if request.method == 'POST':
        nums = [int(n) for n in request.form.getlist('case_nums')]
        revealed = game_instance.reveal_cases(nums)
        return render_template('reveal.html', revealed=revealed)
    else:
        num_to_reveal = game_instance.get_num_cases_to_reveal()
        cases = game_instance.get_cases()
        return render_template('reveal.html', num_to_reveal=num_to_reveal, cases=cases)

@game_bp.route('/get_offer', methods=['GET'])
@login_required
def get_offer():
    offer = game_instance.get_dealer_offer()
    game_instance.add_offer(offer)
    return render_template('offer.html', offer=offer)

@game_bp.route('/accept_offer', methods=['POST'])
@login_required
def accept_offer():
    case_num = game_instance.chosen_case.num
    case_value = game_instance.chosen_case.value
    offers = game_instance.get_offers()
    return redirect(url_for('game_bp.final', case_num=case_num, case_value=case_value, offers=offers))

@game_bp.route('/reject_offer', methods=['POST'])
@login_required
def reject_offer():
    return redirect(url_for('game_bp.next_round'))

@game_bp.route('/next_round', methods=['GET', 'POST'])
@login_required
def next_round():
    game_instance.current_round += 1
    return redirect(url_for('game_bp.reveal_cases'))


@game_bp.route('/final', methods=['GET'])
@login_required
def final():
    case_num = request.args.get('case_num')
    case_value = request.args.get('case_value')
    offers = game_instance.get_offers()
    return render_template('final.html', case_num=case_num, case_value=case_value, offers=offers)
