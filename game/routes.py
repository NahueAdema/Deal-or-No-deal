from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from db import session
from models.models import GameState
from .game import DealOrNoDeal as GameInstance

game_bp = Blueprint("game_bp", __name__, template_folder="templates/game", static_folder="static")

@game_bp.route('/')
@login_required
def game_index():
    try:
        game_instance = GameInstance()
        cases = game_instance.get_cases()
        return render_template('game.html', cases=cases)
    except SQLAlchemyError:
        session.rollback()
        flash("Error al cargar el juego. Inténtalo de nuevo.")
        return redirect(url_for('game_bp.game_index'))
    finally:
        session.close()

@game_bp.route('/choose_case', methods=['POST'])
@login_required
def choose_case():
    try:
        game_instance = GameInstance()
        num = int(request.form['case_num'])
        game_instance.choose_case(num)
        return redirect(url_for('game_bp.reveal_cases'))
    except SQLAlchemyError:
        session.rollback()
        flash("Error al elegir el caso. Inténtalo de nuevo.")
        return redirect(url_for('game_bp.game_index'))
    finally:
        session.close()

@game_bp.route('/reveal_cases', methods=['GET', 'POST'])
@login_required
def reveal_cases():
    try:
        game_instance = GameInstance()

        if request.method == 'POST':
            selected_cases = [int(n) for n in request.form.getlist('case_nums')]
            num_to_reveal = game_instance.get_num_cases_to_reveal()
            if len(selected_cases) != num_to_reveal:
                flash(f"Please select exactly {num_to_reveal} cases.")
                return redirect(url_for('game_bp.reveal_cases'))
            
            revealed = game_instance.reveal_cases(selected_cases)
            if not game_instance.playing:
                return redirect(url_for('game_bp.final'))
            
            return render_template('reveal.html', revealed=revealed, num_to_reveal=num_to_reveal, cases=game_instance.get_cases())
        
        else:
            num_to_reveal = game_instance.get_num_cases_to_reveal()
            cases = game_instance.get_cases()
            return render_template('reveal.html', num_to_reveal=num_to_reveal, cases=cases)
    except SQLAlchemyError:
        session.rollback()
        flash("Error al revelar los casos. Inténtalo de nuevo.")
        return redirect(url_for('game_bp.game_index'))
    finally:
        session.close()

@game_bp.route('/get_offer', methods=['GET'])
@login_required
def get_offer():
    try:
        game_instance = GameInstance()
        offer = game_instance.get_dealer_offer()
        return render_template('offer.html', offer=offer)
    except SQLAlchemyError:
        session.rollback()
        flash("Error al obtener la oferta. Inténtalo de nuevo.")
        return redirect(url_for('game_bp.game_index'))
    finally:
        session.close()

@game_bp.route('/accept_offer', methods=['POST'])
@login_required
def accept_offer():
    try:
        game_instance = GameInstance()
        offer = game_instance.get_dealer_offer()
        game_instance.playing = False  
        game_instance.save_state()
        return redirect(url_for('game_bp.final', offer=offer))
    except SQLAlchemyError:
        session.rollback()
        flash("Error al aceptar la oferta. Inténtalo de nuevo.")
        return redirect(url_for('game_bp.game_index'))
    finally:
        session.close()

@game_bp.route('/reject_offer', methods=['POST'])
@login_required
def reject_offer():
    try:
        game_instance = GameInstance()
        if game_instance.check_game_end():
            return redirect(url_for('game_bp.final'))
        if game_instance.current_round >= len(game_instance.rounds):
            return redirect(url_for('game_bp.final'))
        return redirect(url_for('game_bp.reveal_cases'))
    except SQLAlchemyError:
        session.rollback()
        flash("Error al rechazar la oferta. Inténtalo de nuevo.")
        return redirect(url_for('game_bp.game_index'))
    finally:
        session.close()

@game_bp.route('/final', methods=['GET', 'POST'])
@login_required
def final():
    try:
        game_instance = GameInstance()
        case_num = game_instance.chosen_case.num if game_instance.chosen_case else None
        offers = game_instance.get_offers()
        offer = request.args.get('offer')

        if offer: 
            case_value = game_instance.chosen_case.value if game_instance.chosen_case else None
            return render_template('final.html', case_num=case_num, case_value=case_value, offers=offers, offer=offer)

        if request.method == 'POST':
            keep_original = request.form['keep_original'] == 'True'
            final_case = game_instance.get_final_choice(keep_original)
            return render_template('final.html', case_num=final_case.num, case_value=final_case.value, offers=offers, offer=offer)

        available_cases = [case for case in game_instance.cases if case.available]
        if available_cases:
            last_case_num = available_cases[0].num
        else:
            last_case_num = None

        return render_template('final_choice.html', game_instance=game_instance, last_case_num=last_case_num, case_num=case_num, offer=offer)
    except SQLAlchemyError:
        session.rollback()
        flash("Error al cargar el estado final. Inténtalo de nuevo.")
        return redirect(url_for('game_bp.game_index'))
    finally:
        session.close()

@game_bp.route('/reset_game', methods=['POST'])
@login_required
def reset_game():
    try:
        session.query(GameState).filter_by(user_id=current_user.id).delete()
        session.commit()
        return redirect(url_for('game_bp.game_index'))
    except SQLAlchemyError:
        session.rollback()
        flash("Error al reiniciar el juego. Inténtalo de nuevo.")
        return redirect(url_for('game_bp.game_index'))
    finally:
        session.close()

@game_bp.route('/history')
@login_required
def game_history():
    try:
        games = session.query(GameState).filter_by(user_id=current_user.id).order_by(GameState.saved_at.desc()).all()
        return render_template('game_history.html', games=games)
    except SQLAlchemyError:
        session.rollback()
        flash("Error al cargar el historial de partidas. Inténtalo de nuevo.")
        return redirect(url_for('game_bp.game_index'))
    finally:
        session.close()

@game_bp.route('/resume/<int:game_id>', methods=['POST'])
@login_required
def resume_game(game_id):
    try:
        game_instance = GameInstance()
        game_state = session.query(GameState).filter_by(id=game_id, user_id=current_user.id).first()
        if game_state:
            game_instance.load_state()
            return redirect(url_for('game_bp.reveal_cases')) 
        else:
            flash("No se encontró la partida.")
            return redirect(url_for('game_bp.game_history'))
    except SQLAlchemyError:
        session.rollback()
        flash("Error al retomar la partida. Inténtalo de nuevo.")
        return redirect(url_for('game_bp.game_history'))
    finally:
        session.close()