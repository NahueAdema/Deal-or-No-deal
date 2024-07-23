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
        if not game_instance.playing:
            return redirect(url_for('game_bp.final')) 
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
    offer = game_instance.get_dealer_offer()
    game_instance.playing = False  # Termina el juego
    return redirect(url_for('game_bp.final', offer=offer))

@game_bp.route('/reject_offer', methods=['POST'])
@login_required
def reject_offer():
    if game_instance.check_game_end():
        return redirect(url_for('game_bp.final'))
    if game_instance.current_round >= len(game_instance.rounds):
        return redirect(url_for('game_bp.final'))
    game_instance.current_round += 1
    return redirect(url_for('game_bp.reveal_cases'))

@game_bp.route('/final', methods=['GET'])
@login_required
def final():
    case_num = game_instance.chosen_case.num if game_instance.chosen_case else None
    case_value = game_instance.get_final_case_value() if game_instance.chosen_case else None
    offers = game_instance.get_offers()
    offer = request.args.get('offer')  # Obtiene la oferta de la cadena de consulta
    return render_template('final.html', case_num=case_num, case_value=case_value, offers=offers, offer=offer)

@game_bp.route('/reset_game', methods=['POST'])
@login_required
def reset_game():
    global game_instance
    game_instance = GameInstance()  # Reinicia la instancia del juego
    return redirect(url_for('game_bp.game_index'))