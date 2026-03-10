"""
Improved Distributed Bob Server for QKD BB84 Protocol

This server implements Bob's role as the receiver:
- Receives quantum data from Eve (or Alice)
- Measures qubits in random bases
- Sends measurement results back to Eve (or Alice)

Communication Protocol:
1. Listen for qubits on port 5003
2. Measure them in random bases
3. Send bases and measured bits back to Eve/Alice
"""

import socket
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from bob import bob_measure

BOB_PORT = 5003
EVE_RESPONSE_HOST = 'localhost'
EVE_RESPONSE_PORT = 5004  # Port to send response to Eve

def main():
    print("=" * 70)
    print("  BOB SERVER — Quantum Receiver")
    print("=" * 70)
    print(f"Listening on port {BOB_PORT}...")
    print()

    while True:
        try:
            # Listen for qubits from Eve (or Alice)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.bind(('localhost', BOB_PORT))
                server.listen(5)
                print("Waiting for qubits...")
                conn, addr = server.accept()

                with conn:
                    conn.settimeout(10.0)
                    data = b''
                    try:
                        while True:
                            chunk = conn.recv(4096)
                            if not chunk:
                                break
                            data += chunk
                    except socket.timeout:
                        print("[BOB] Timeout receiving data")
                        continue
                    
                    data_str = data.decode().strip()
                    if not data_str:
                        print("[BOB] No data received, waiting for next connection...")
                        continue
                    
                    try:
                        transmit_data = json.loads(data_str)
                    except json.JSONDecodeError as e:
                        print(f"[BOB] Failed to parse JSON: {str(e)}")
                        continue
                    
                    print(f"[BOB] Received {len(transmit_data['bits'])} qubits")

            # Measure qubits
            print("[BOB] Measuring qubits in random bases...")
            bob_data = bob_measure(transmit_data['bits'], transmit_data['bases'])

            # Prepare response
            response = {
                'bases': bob_data['bob_bases'],
                'bits': bob_data['bob_bits']
            }

            # Send response back to Eve
            print(f"[BOB] Sending {len(response['bases'])} measurement bases to Eve...")
            try:
                # Retry connection to Eve (she might not be listening yet)
                max_retries = 5
                for attempt in range(max_retries):
                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            s.settimeout(2.0)
                            s.connect((EVE_RESPONSE_HOST, EVE_RESPONSE_PORT))
                            s.sendall(json.dumps(response).encode())
                            print("[BOB] ✓ Successfully sent response to Eve")
                            break
                    except (ConnectionRefusedError, socket.timeout) as retry_error:
                        if attempt < max_retries - 1:
                            print(f"[BOB] Connection attempt {attempt + 1}/{max_retries} failed, retrying...")
                            import time
                            time.sleep(0.5)
                        else:
                            raise retry_error
            except Exception as e:
                print(f"[BOB ERROR] Failed to send response to Eve: {str(e)}")
                raise

            print("[BOB] Measurement complete\n")

        except KeyboardInterrupt:
            print("\n[BOB] Keyboard interrupt received; continuing to listen...")
            continue
        except Exception as e:
            print(f"[BOB ERROR] {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    main()
