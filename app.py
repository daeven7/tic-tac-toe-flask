from flask import Flask, request, jsonify
import os
import numpy as np
from engine import Environment, AgentEval
from utils.board_converter import board_to_array, array_to_board

app = Flask(__name__)

sv_path = ''  

def get_next_action(env, symbol='x', sv_path=''):
    try:
        vx_val = np.load(os.path.join(sv_path, 'vx.npy'))
        vo_val = np.load(os.path.join(sv_path, 'vo.npy'))
        x_agent = AgentEval(env.x, vx_val)
        o_agent = AgentEval(env.o, vo_val)
        if symbol.lower() == 'x':
            return x_agent.take_action(env)
        else:
            return o_agent.take_action(env)
    except Exception as e:
        raise Exception(f"error in get_next_action: {str(e)}")

def validate_board_data(data):
    if not data:
        return None, "No data provided"
    
    board = data.get('board')
    if not board:
        return None, "Board state is required"
    
    if not isinstance(board, list) or len(board) != 3:
        return None, "Board must be a 3x3 array"
    
    for row in board:
        if not isinstance(row, list) or len(row) != 3:
            return None, "Each row must be a list of 3 elements"
    
    return board, None

def validate_player_data(data):
    player = data.get('player')
    if not player:
        return None, "Player turn is required"
    
    if player.upper() not in ['X', 'O']:
        return None, "Player must be 'X' or 'O'"
    
    return player, None

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"})

@app.route('/move', methods=['POST'])
def make_move():
    try:
        data = request.get_json()
        board, error = validate_board_data(data)
        if error:
            return jsonify({"error": error}), 400
        
        player, error = validate_player_data(data)
        if error:
            return jsonify({"error": error}), 400
        
        try:
            board_array = board_to_array(board)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        
        env = Environment()
        env.set_state(board_array)
        
        if env.game_over():
            winner = None
            if env.winner == env.x:
                winner = 'X'
            elif env.winner == env.o:
                winner = 'O'
            
            return jsonify({
                "error": "Game is already over",
                "game_state": {
                    "is_over": True,
                    "winner": winner,
                    "is_draw": env.is_draw()
                }
            }), 400
        
        valid_moves = []
        for i in range(3):
            for j in range(3):
                if env.is_empty(i, j):
                    valid_moves.append([i, j])
        
        if not valid_moves:
            return jsonify({
                "error": "No valid moves available",
                "game_state": {
                    "is_over": True,
                    "winner": None,
                    "is_draw": True
                }
            }), 400
        
        try:
            best_move = get_next_action(env, symbol=player.lower(), sv_path=sv_path)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
        game_over = env.game_over()
        winner = None
        if env.winner == env.x:
            winner = 'X'
        elif env.winner == env.o:
            winner = 'O'
        
        updated_board = array_to_board(env.board)
        
        return jsonify({
            "move": {
                "row": best_move[0],
                "col": best_move[1]
            },
            "board": updated_board,
            "game_state": {
                "is_over": game_over,
                "winner": winner,
                "is_draw": env.is_draw()
            }
        })
        
    except Exception as e:
        return jsonify({"error": f"make_move error: {str(e)}"}), 500

@app.route('/game-state', methods=['POST'])
def check_game_state():
    try:
        data = request.get_json()        
        board, error = validate_board_data(data)
        if error:
            return jsonify({"error": error}), 400
        
        try:
            board_array = board_to_array(board)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        
        env = Environment()
        env.set_state(board_array)
        
        game_over = env.game_over()
        winner = None
        if env.winner == env.x:
            winner = 'X'
        elif env.winner == env.o:
            winner = 'O'
        
        return jsonify({
            "game_state": {
                "is_over": game_over,
                "winner": winner,
                "is_draw": env.is_draw()
            },
            "board": board
        })
        
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


if __name__ == '__main__':
    print("Tic-Tac-Toe engine running...")
  
    
    app.run(debug=True, host='0.0.0.0', port=5000) 