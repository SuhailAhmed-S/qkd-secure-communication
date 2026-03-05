"""
Module 1 (Backend): Flask API Server

This module provides a REST API for the QKD simulator. It handles requests
from the web frontend, orchestrates the BB84 QKD pipeline, and returns
results as JSON.

API Endpoints:
    GET  / — Returns the main HTML interface
    POST /api/run_qkd — Executes QKD protocol with specified parameters
    
Environment:
    - Framework: Flask (Python micro web framework)
    - Port: 5000 (default)
    - Debug: True (set to False in production)
    
Security Notes:
    - CSRF protection should be enabled in production
    - Input validation is performed on num_qubits and message
    - Response data is trimmed to keep JSON payload manageable
    - Consider adding rate limiting for production deployment
"""

import sys
import os
import json
from typing import Dict, Tuple

# Add project directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, request, jsonify, render_template
from qkd_main import run_qkd

# Initialize Flask application
app = Flask(__name__, template_folder='templates')

# Configuration constants
MIN_QUBITS = 10
MAX_QUBITS = 1000
PREVIEW_LENGTH = 20  # Number of items to include in response preview


@app.route('/')
def index() -> str:
    """
    Serve the main HTML interface.
    
    Returns:
        str: Rendered HTML template (index.html)
    """
    return render_template('index.html')


@app.route('/api/run_qkd', methods=['POST'])
def api_run_qkd() -> Tuple[Dict, int]:
    """
    Execute the BB84 QKD protocol with provided parameters.
    
    HTTP Method: POST
    Content-Type: application/json
    
    Request Body:
        {
            "num_qubits": int (10-1000, required),
            "message": str (non-empty, required),
            "eve_enabled": bool (optional, default: false)
        }
        
    Response (Success - 200):
        {
            "num_qubits": int,
            "eve_enabled": bool,
            "message": str,
            "sift_count": int,
            "qber": float,
            "qber_pct": str,
            "errors": int,
            "total": int,
            "secure": bool,
            "status": str,
            "key_hex": str or null,
            "encrypted": str or null,
            "decrypted": str or null,
            "alice_bits_preview": list (first 20),
            "alice_bases_preview": list (first 20),
            "alice_states_preview": list (first 20),
            "bob_bases_preview": list (first 20),
            "bob_bits_preview": list (first 20),
            "alice_sifted_preview": list (first 20),
            "bob_sifted_preview": list (first 20),
            "eve_bases_preview": list (empty if no Eve)
        }
        
    Response (Error - 400):
        {
            "error": str
        }
        
    Validation Rules:
        - num_qubits must be 10-1000 (inclusive)
        - message cannot be empty
        - eve_enabled must be boolean
        
    Error Handling:
        - Invalid num_qubits: Returns 400 with error message
        - Empty message: Returns 400 with error message
        - Any other error: Returns 500 with error message
        
    Data Optimization:
        - Large arrays are trimmed to first 20 items for JSON response
        - This reduces bandwidth and improves frontend responsiveness
        - Full data is available for analysis if needed
        
    Processing:
        1. Parse and validate input
        2. Execute run_qkd() with provided parameters
        3. Extract summary from full result
        4. Return JSON with preview data
    """
    try:
        # Parse JSON request
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body must be valid JSON'}), 400
        
        # Extract and validate parameters
        try:
            num_qubits = int(data.get('num_qubits', 100))
        except (ValueError, TypeError):
            return jsonify({'error': 'num_qubits must be an integer'}), 400
            
        message = data.get('message', 'Hello QKD!')
        eve_enabled = bool(data.get('eve_enabled', False))

        # Validate input parameters
        if num_qubits < MIN_QUBITS or num_qubits > MAX_QUBITS:
            return jsonify({
                'error': f'num_qubits must be between {MIN_QUBITS} and {MAX_QUBITS}'
            }), 400
            
        if not message or not isinstance(message, str):
            return jsonify({'error': 'Message cannot be empty'}), 400

        # Execute QKD protocol
        result = run_qkd(num_qubits=num_qubits, message=message, eve_enabled=eve_enabled)

        # Prepare response summary (trim large arrays for JSON)
        summary = {
            'num_qubits': result['num_qubits'],
            'eve_enabled': result['eve_enabled'],
            'message': result['message'],
            'sift_count': result['sift_count'],
            'qber': result['qber'],
            'qber_pct': f"{result['qber']*100:.2f}%",
            'errors': result['errors'],
            'total': result['total'],
            'secure': result['secure'],
            'status': result['status'],
            'key_hex': result['key_hex'],
            'encrypted': result['encrypted'],
            'decrypted': result['decrypted'],
            # Include first N items for visualization
            'alice_bits_preview': result['alice_bits'][:PREVIEW_LENGTH],
            'alice_bases_preview': result['alice_bases'][:PREVIEW_LENGTH],
            'alice_states_preview': result['alice_states'][:PREVIEW_LENGTH],
            'bob_bases_preview': result['bob_bases'][:PREVIEW_LENGTH],
            'bob_bits_preview': result['bob_bits'][:PREVIEW_LENGTH],
            'alice_sifted_preview': result['alice_sifted'][:PREVIEW_LENGTH],
            'bob_sifted_preview': result['bob_sifted'][:PREVIEW_LENGTH],
            'eve_bases_preview': result['eve_bases'][:PREVIEW_LENGTH] if result['eve_bases'] else []
        }
        
        return jsonify(summary), 200
        
    except Exception as e:
        # Log unexpected errors and return generic message
        print(f"[ERROR] Unexpected error in /api/run_qkd: {str(e)}", file=sys.stderr)
        return jsonify({
            'error': f'Server error: {str(e)}'
        }), 500


# Error handlers
@app.errorhandler(404)
def not_found(error: Exception) -> Tuple[Dict, int]:
    """Handle 404 errors (endpoint not found)."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(405)
def method_not_allowed(error: Exception) -> Tuple[Dict, int]:
    """Handle 405 errors (HTTP method not allowed)."""
    return jsonify({'error': 'Method not allowed'}), 405


@app.errorhandler(500)
def internal_error(error: Exception) -> Tuple[Dict, int]:
    """Handle 500 errors (internal server error)."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Development server
    # In production, use a WSGI server like Gunicorn
    app.run(debug=True, port=5000, host='0.0.0.0')
