"""
Module 1 (Backend): Flask Web Application for QKD BB84 Protocol

This module provides a complete web interface for the Distributed QKD BB84 protocol simulator
with real-time communication monitoring between Alice, Bob, and Eve servers.

Features:
    - Distributed server communication (Alice, Bob, Eve on separate systems)
    - Real-time message feed showing protocol communication
    - Server status monitoring and control
    - Live QKD protocol execution with distributed components
    - Interactive controls for each participant

Environment:
    - Framework: Flask (Python micro web framework)
    - Port: 8000 (default)
    - Distributed: Alice (port 5004), Eve (port 5002), Bob (port 5003)
"""

import sys
import os
import json
import socket
import time
from typing import Dict, Tuple, List, Optional

# Add project directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, request, jsonify, render_template
from qkd_main import run_qkd

# Initialize Flask application
app = Flask(__name__, template_folder='templates')
app.config['JSON_SORT_KEYS'] = False

# Distributed server configuration
SERVERS = {
    'alice': {'host': 'localhost', 'port': 5004, 'status': 'unknown'},
    'eve': {'host': 'localhost', 'port': 5002, 'status': 'unknown'},
    'bob': {'host': 'localhost', 'port': 5003, 'status': 'unknown'}
}

# Global message log for real-time communication display
message_log: List[Dict] = []

def add_message(sender: str, message: str, message_type: str = 'info'):
    """Add a message to the global log for real-time display."""
    timestamp = time.strftime('%H:%M:%S')
    message_log.append({
        'timestamp': timestamp,
        'sender': sender,
        'message': message,
        'type': message_type
    })
    # Keep only last 50 messages
    if len(message_log) > 50:
        message_log.pop(0)

def check_server_status(server_name: str) -> bool:
    """Check if a distributed server is running."""
    try:
        server = SERVERS[server_name]
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)
            result = s.connect_ex((server['host'], server['port']))
            status = result == 0
            server['status'] = 'online' if status else 'offline'
            return status
    except:
        server['status'] = 'offline'
        return False

def send_to_server(server_name: str, data: Dict) -> Optional[Dict]:
    """Send data to a distributed server and get response."""
    try:
        server = SERVERS[server_name]
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5.0)
            s.connect((server['host'], server['port']))
            s.sendall(json.dumps(data).encode())

            # For servers that respond
            if server_name in ['alice']:
                response = s.recv(8192)
                return json.loads(response.decode())
    except Exception as e:
        add_message('SYSTEM', f'Error communicating with {server_name}: {str(e)}', 'error')
        return None
    return {}

# Configuration constants
MIN_QUBITS = 10
MAX_QUBITS = 1000
PREVIEW_LENGTH = 20


@app.route('/')
def home() -> str:
    """Render the home page with protocol overview."""
    return render_template('home.html')


@app.route('/simulator')
def simulator() -> str:
    """Render the interactive QKD simulator."""
    return render_template('simulator.html')


@app.route('/documentation')
def documentation() -> str:
    """Render the documentation page."""
    return render_template('documentation.html')


@app.route('/api/server_status', methods=['GET'])
def api_server_status() -> Tuple[Dict, int]:
    """Get the status of all distributed servers."""
    status = {}
    for server_name, server_info in SERVERS.items():
        is_online = check_server_status(server_name)
        status[server_name] = {
            'host': server_info['host'],
            'port': server_info['port'],
            'status': 'online' if is_online else 'offline'
        }

    return jsonify(status), 200


@app.route('/api/messages', methods=['GET'])
def api_messages() -> Tuple[Dict, int]:
    """Get the current message log for real-time communication display."""
    return jsonify({'messages': message_log}), 200


@app.route('/api/clear_messages', methods=['POST'])
def api_clear_messages() -> Tuple[Dict, int]:
    """Clear the message log."""
    global message_log
    message_log.clear()
    add_message('SYSTEM', 'Message log cleared', 'system')
    return jsonify({'status': 'cleared'}), 200
def api_run_qkd() -> Tuple[Dict, int]:
    """
    Execute the BB84 QKD protocol using distributed servers.

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

    Processing:
        1. Check server connectivity
        2. Send configuration to Alice server
        3. Monitor protocol execution through message log
        4. Receive final results from Alice server
        5. Return formatted response
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

        # Check server connectivity
        add_message('SYSTEM', 'Checking server connectivity...', 'system')

        servers_online = True
        for server_name in ['alice', 'eve', 'bob']:
            if not check_server_status(server_name):
                add_message('SYSTEM', f'{server_name.upper()} server is offline', 'error')
                servers_online = False
            else:
                add_message('SYSTEM', f'{server_name.upper()} server is online', 'success')

        if not servers_online:
            return jsonify({
                'error': 'One or more servers are offline. Please start Alice, Bob, and Eve servers.'
            }), 400

        # Send configuration to Alice server
        add_message('SYSTEM', f'Starting QKD protocol with {num_qubits} qubits', 'system')

        config_data = {
            'command': 'run_qkd',
            'num_qubits': num_qubits,
            'message': message,
            'eve_enabled': eve_enabled
        }

        result = send_to_server('alice', config_data)

        if result is None:
            return jsonify({'error': 'Failed to communicate with Alice server'}), 500

        # Add final results to message log
        add_message('SYSTEM', f'QKD Protocol completed: {result["status"]}', 'success' if result['secure'] else 'warning')

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
        add_message('SYSTEM', f'Unexpected error: {str(e)}', 'error')
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
    app.run(debug=True, port=8000, host='0.0.0.0')
