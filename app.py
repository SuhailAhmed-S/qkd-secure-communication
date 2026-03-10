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
import threading
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

def send_to_server(server_name: str, data: Dict, retries: int = 3) -> Optional[Dict]:
    """Send data to a distributed server and get response."""
    for attempt in range(retries):
        try:
            server = SERVERS[server_name]
            add_message('SYSTEM', f'Sending data to {server_name} on port {server["port"]} (attempt {attempt + 1}/{retries})', 'system')
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(10.0)
                print(f"[DEBUG] Connecting to {server_name} at {server['host']}:{server['port']}")
                s.connect((server['host'], server['port']))
                json_data = json.dumps(data).encode()
                print(f"[DEBUG] Sending {len(json_data)} bytes")
                add_message('SYSTEM', f'Sending {len(json_data)} bytes to {server_name}', 'system')
                s.sendall(json_data)
                print(f"[DEBUG] Shutting down write side")
                s.shutdown(socket.SHUT_WR)  # Signal end of data
                print(f"[DEBUG] Successfully sent data to {server_name}")
                add_message('SYSTEM', f'Successfully sent data to {server_name}', 'success')
                return {}  # Alice will send result back via result server
        except socket.timeout:
            print(f"[DEBUG] Timeout connecting to {server_name} (attempt {attempt + 1}/{retries})")
            add_message('SYSTEM', f'Timeout connecting to {server_name} (attempt {attempt + 1}/{retries})', 'warning')
            if attempt < retries - 1:
                continue
        except ConnectionRefusedError:
            print(f"[DEBUG] Connection refused by {server_name} (attempt {attempt + 1}/{retries})")
            add_message('SYSTEM', f'Connection refused by {server_name} - is it running?', 'error')
            if attempt < retries - 1:
                continue
        except Exception as e:
            print(f"[DEBUG] Error sending to {server_name}: {str(e)}")
            add_message('SYSTEM', f'Error sending to {server_name}: {str(e)}', 'error')
            if attempt < retries - 1:
                continue
    
    return None

def wait_for_result(timeout: int = 30) -> Optional[Dict]:
    """Wait for result from Alice server."""
    add_message('SYSTEM', f'Waiting for result from Alice on port 9999 (timeout: {timeout}s)...', 'system')
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('localhost', 9999))
            server.settimeout(timeout)
            server.listen(1)
            add_message('SYSTEM', 'Listening for Alice result...', 'system')

            conn, addr = server.accept()
            add_message('SYSTEM', f'Connection from {addr} for result', 'success')
            with conn:
                response_data = conn.recv(65536).decode()
                add_message('SYSTEM', f'Received {len(response_data)} bytes of result data', 'success')
                result = json.loads(response_data)
                add_message('SYSTEM', 'Result parsed successfully', 'success')
                return result
    except socket.timeout:
        add_message('SYSTEM', 'Timeout waiting for results from Alice', 'error')
        return None
    except Exception as e:
        add_message('SYSTEM', f'Error receiving results: {str(e)}', 'error')
        return None

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


# Global variable to store result from Alice
qkd_result = {'result': None, 'ready': False}
qkd_result_lock = threading.Lock()

def result_listener_thread(timeout: int = 40):
    """Listen for result from Alice in a separate thread."""
    try:
        add_message('SYSTEM', f'Starting result listener on port 9999 (timeout: {timeout}s)...', 'system')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('localhost', 9999))
            server.settimeout(timeout)
            server.listen(1)
            add_message('SYSTEM', 'Result listener ready, waiting for Alice...', 'system')

            conn, addr = server.accept()
            add_message('SYSTEM', f'Connection from {addr} for result', 'success')
            with conn:
                conn.settimeout(10.0)
                response_data = b''
                while True:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    response_data += chunk
                
                add_message('SYSTEM', f'Received {len(response_data)} bytes of result data', 'success')
                result = json.loads(response_data.decode())
                add_message('SYSTEM', 'Result parsed successfully', 'success')
                
                with qkd_result_lock:
                    qkd_result['result'] = result
                    qkd_result['ready'] = True
    except socket.timeout:
        add_message('SYSTEM', 'Result listener timeout - Alice did not respond', 'error')
    except Exception as e:
        add_message('SYSTEM', f'Result listener error: {str(e)}', 'error')

@app.route('/api/run_qkd', methods=['POST'])
def api_run_qkd() -> Tuple[Dict, int]:
    """
    Execute the BB84 QKD protocol using in-process execution.

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
        1. Validate input parameters
        2. Execute QKD protocol in-process
        3. Calculate QBER and security status
        4. Encrypt/decrypt message
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

        # Add message to log
        add_message('SYSTEM', f'Starting QKD protocol with {num_qubits} qubits', 'system')
        add_message('SYSTEM', f'Message: {message}', 'system')
        add_message('SYSTEM', f'Eve enabled: {eve_enabled}', 'system')

        # Execute QKD protocol in-process
        add_message('SYSTEM', 'Executing BB84 protocol...', 'system')
        result = run_qkd(num_qubits=num_qubits, message=message, eve_enabled=eve_enabled)
        
        # Add final results to message log
        add_message('SYSTEM', f'QKD Protocol completed: {result["status"]}', 'success' if result['secure'] else 'warning')
        add_message('SYSTEM', f'QBER: {result["qber"]*100:.2f}%', 'success' if result['secure'] else 'warning')
        add_message('SYSTEM', f'Sifted key length: {result["sift_count"]} bits', 'info')

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
        import traceback
        traceback.print_exc()
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
