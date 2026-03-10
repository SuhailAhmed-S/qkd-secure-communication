"""
Improved Distributed Alice Server for QKD BB84 Protocol

This server implements Alice's role in a networked QKD system:
- Prepares quantum bits
- Sends qubits through Eve to Bob
- Receives Bob's measurement data from Eve
- Calculates QBER and derives the final key
- Sends results back to the orchestrator

Communication Protocol:
1. Receive config from Flask (via localhost)
2. Send qubits to Eve
3. Receive Bob's measurements from Eve
4. Perform sifting and QBER calculation
5. Return results to Flask
"""

import socket
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from alice import alice_prepare
from security import calculate_qber, derive_key, xor_encrypt

ALICE_PORT = 5004
EVE_HOST = 'localhost'
EVE_PORT = 5002
BOB_PORT = 5003

def main():
    print("=" * 70)
    print("  ALICE SERVER — Quantum Key Distribution Transmitter")
    print("=" * 70)
    print(f"Listening on port {ALICE_PORT}...")
    print()

    # create main listening socket once so port remains bound
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', ALICE_PORT))
    server.listen(5)

    while True:
        try:
            print("Waiting for configuration from Flask...")
            conn, addr = server.accept()

            with conn:
                print(f"Connected by {addr}")
                conn.settimeout(10.0)
                data = b''
                try:
                    while True:
                        chunk = conn.recv(4096)
                        if not chunk:
                            break
                        data += chunk
                except socket.timeout:
                    pass
                
                data_str = data.decode().strip()
                print(f"[ALICE] Received {len(data_str)} characters: '{data_str[:100]}...'")
                if not data_str:
                    print("[ALICE] No data received, waiting for next connection...")
                    continue
                
                config = json.loads(data_str)
                print(f"[ALICE] Parsed config: {config}")

                num_qubits = config['num_qubits']
                message = config['message']
                eve_enabled = config['eve_enabled']

                print(f"\n[ALICE] Preparing {num_qubits} qubits...")
                alice_data = alice_prepare(num_qubits)

                print("[ALICE] Sending qubits to Eve...")
                eve_send_data = {
                    'bits': alice_data['bits'],
                    'bases': alice_data['bases'],
                    'states': alice_data['states']
                }

                try:
                    # Retry connection to Eve (she might not be listening yet)
                    max_retries = 5
                    for attempt in range(max_retries):
                        try:
                            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                                s.settimeout(2.0)
                                s.connect((EVE_HOST, EVE_PORT))
                                s.sendall(json.dumps(eve_send_data).encode())
                                print("[ALICE] ✓ Successfully sent qubits to Eve")
                                break
                        except (ConnectionRefusedError, socket.timeout) as retry_error:
                            if attempt < max_retries - 1:
                                print(f"[ALICE] Connection attempt {attempt + 1}/{max_retries} failed, retrying...")
                                import time
                                time.sleep(0.5)
                            else:
                                raise retry_error
                except Exception as e:
                    print(f"[ALICE ERROR] Failed to connect to Eve: {str(e)}")
                    raise

                print("[ALICE] Waiting for Bob's measurement data from Eve...")
                bob_data = None
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server2:
                        server2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        server2.bind(('localhost', ALICE_PORT + 1))
                        server2.settimeout(10.0)
                        server2.listen(5)
                        print(f"[ALICE] Listening on port {ALICE_PORT + 1} for Bob's response...")
                        conn2, addr2 = server2.accept()
                        print(f"[ALICE] Received connection from {addr2}")
                        with conn2:
                            conn2.settimeout(5.0)
                            bob_response = conn2.recv(8192).decode()
                            bob_data = json.loads(bob_response)
                            print("[ALICE] ✓ Successfully received Bob's data")
                except socket.timeout:
                    print("[ALICE ERROR] Timeout waiting for Bob's response")
                    raise
                except Exception as e:
                    print(f"[ALICE ERROR] Failed to receive Bob's data: {str(e)}")
                    raise

                print(f"[ALICE] Received Bob's {len(bob_data['bases'])} measurement bases")

                # Sifting
                print("[ALICE] Performing basis reconciliation (sifting)...")
                alice_sifted = []
                bob_sifted = []

                for i in range(num_qubits):
                    if alice_data['bases'][i] == bob_data['bases'][i]:
                        alice_sifted.append(alice_data['bits'][i])
                        bob_sifted.append(bob_data['bits'][i])

                sift_count = len(alice_sifted)
                print(f"[ALICE] Sifted key length: {sift_count} bits")

                # QBER Calculation
                qber_result = calculate_qber(alice_sifted, bob_sifted)
                qber = qber_result['qber']
                errors = qber_result['errors']
                print(f"[ALICE] QBER: {qber*100:.2f}% ({errors} errors / {sift_count} bits)")

                # Determine security
                QBER_THRESHOLD = 0.11
                secure = qber < QBER_THRESHOLD

                if secure:
                    print(f"[ALICE] ✓ Channel is SECURE (QBER < {QBER_THRESHOLD*100:.1f}%)")
                    # Derive key and encrypt message
                    key_hex = derive_key(alice_sifted)
                    encrypted = xor_encrypt(message, key_hex)
                    decrypted = xor_encrypt(encrypted, key_hex)
                    status = "SECURE — Communication Successful"
                else:
                    print(f"[ALICE] ✗ Channel is COMPROMISED (QBER >= {QBER_THRESHOLD*100:.1f}%)")
                    key_hex = None
                    encrypted = None
                    decrypted = None
                    status = "COMPROMISED — Eavesdropping Detected"

                # Prepare result (moved outside if/else to always send results)
                result = {
                    'num_qubits': num_qubits,
                    'eve_enabled': eve_enabled,
                    'message': message,
                    'sift_count': sift_count,
                    'qber': qber,
                    'errors': errors,
                    'total': sift_count,
                    'secure': secure,
                    'status': status,
                    'key_hex': key_hex,
                    'encrypted': encrypted,
                    'decrypted': decrypted,
                    'alice_bits': alice_data['bits'],
                    'alice_bases': alice_data['bases'],
                    'alice_states': alice_data['states'],
                    'bob_bases': bob_data['bases'],
                    'bob_bits': bob_data['bits'],
                    'alice_sifted': alice_sifted,
                    'bob_sifted': bob_sifted,
                    'eve_bases': bob_data.get('eve_bases', [])
                }

                # Send results back to Flask
                print("[ALICE] Sending results to Flask...")
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(5.0)
                        s.connect(('localhost', 9999))  # Flask listens on this port for results
                        json_result = json.dumps(result).encode()
                        print(f"[ALICE] Sending {len(json_result)} bytes to Flask...")
                        s.sendall(json_result)
                        print("[ALICE] ✓ Successfully sent results to Flask")
                except Exception as e:
                    print(f"[ALICE ERROR] Failed to send results to Flask: {str(e)}")
                    raise

                print("[ALICE] Protocol complete\n")

        except KeyboardInterrupt:
            print("\n[ALICE] Keyboard interrupt received; continuing to listen...")
            continue
        except Exception as e:
            print(f"[ALICE ERROR] {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Try to send error result back to Flask
            try:
                error_result = {
                    'num_qubits': 0,
                    'eve_enabled': False,
                    'message': '',
                    'sift_count': 0,
                    'qber': 1.0,
                    'errors': 0,
                    'total': 0,
                    'secure': False,
                    'status': f'ERROR: {str(e)}',
                    'key_hex': None,
                    'encrypted': None,
                    'decrypted': None,
                    'alice_bits': [],
                    'alice_bases': [],
                    'alice_states': [],
                    'bob_bases': [],
                    'bob_bits': [],
                    'alice_sifted': [],
                    'bob_sifted': [],
                    'eve_bases': []
                }
                print("[ALICE] Attempting to send error result to Flask...")
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(5.0)
                    s.connect(('localhost', 9999))
                    s.sendall(json.dumps(error_result).encode())
                    print("[ALICE] Error result sent to Flask")
            except Exception as send_error:
                print(f"[ALICE ERROR] Could not send error result: {str(send_error)}")

if __name__ == '__main__':
    main()
