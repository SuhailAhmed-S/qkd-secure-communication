"""
Module 1 (Backend): Flask API Server
Handles requests from the frontend, orchestrates the QKD pipeline,
and returns results as JSON.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, request, jsonify, render_template
from qkd_main import run_qkd

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/run_qkd', methods=['POST'])
def api_run_qkd():
    data        = request.get_json()
    num_qubits  = int(data.get('num_qubits', 100))
    message     = data.get('message', 'Hello QKD!')
    eve_enabled = bool(data.get('eve_enabled', False))

    # Validate input
    if num_qubits < 10 or num_qubits > 1000:
        return jsonify({'error': 'num_qubits must be between 10 and 1000'}), 400
    if not message:
        return jsonify({'error': 'Message cannot be empty'}), 400

    result = run_qkd(num_qubits=num_qubits, message=message, eve_enabled=eve_enabled)

    # Trim large arrays for JSON response to keep it readable
    summary = {
        'num_qubits':   result['num_qubits'],
        'eve_enabled':  result['eve_enabled'],
        'message':      result['message'],
        'sift_count':   result['sift_count'],
        'qber':         result['qber'],
        'qber_pct':     f"{result['qber']*100:.2f}%",
        'errors':       result['errors'],
        'total':        result['total'],
        'secure':       result['secure'],
        'status':       result['status'],
        'key_hex':      result['key_hex'],
        'encrypted':    result['encrypted'],
        'decrypted':    result['decrypted'],
        # First 20 for visualization
        'alice_bits_preview':   result['alice_bits'][:20],
        'alice_bases_preview':  result['alice_bases'][:20],
        'alice_states_preview': result['alice_states'][:20],
        'bob_bases_preview':    result['bob_bases'][:20],
        'bob_bits_preview':     result['bob_bits'][:20],
        'alice_sifted_preview': result['alice_sifted'][:20],
        'bob_sifted_preview':   result['bob_sifted'][:20],
        'eve_bases_preview':    result['eve_bases'][:20] if result['eve_bases'] else []
    }
    return jsonify(summary)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
