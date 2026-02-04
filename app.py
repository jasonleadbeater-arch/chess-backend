from flask import Flask, request, jsonify
from flask_cors import CORS
import chess
import chess.engine
import os

app = Flask(__name__)
CORS(app)  # This allows your Pygame website to talk to this API

# This points to the Stockfish file you downloaded
STOCKFISH_PATH = os.path.join(os.path.dirname(__file__), "stockfish")

@app.route('/get-move', methods=['POST'])
def get_move():
    try:
        data = request.json
        fen = data.get('fen')
        skill_level = data.get('level', 5) # Default to 5 if not sent

        board = chess.Board(fen)
        
        # Open the engine
        engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        engine.configure({"Skill Level": skill_level})
        
        # Think for 0.5 seconds
        result = engine.play(board, chess.engine.Limit(time=0.5))
        engine.quit()

        return jsonify({'move': result.move.uci()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
