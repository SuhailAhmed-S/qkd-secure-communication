"""
Improved Distributed Eve Server for QKD BB84 Protocol

This server implements Eve's role as a potential eavesdropper:
- Receives qubits from Alice
- Optionally intercepts and measures them
- Forwards qubits to Bob
- Receives Bob's measurement bases and forwards them back to Alice

Communication Protocol:
1. Receive qubits from Alice on port 5002
2. Optionally intercept (measure in random bases)
3. Forward to Bob on port 5003
4. Receive Bob's response on port 5004
5. Forward Bob's data back to Alice on port 5005
"""

import socket
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from eve import eve_intercept

EVE_PORT = 5002
EVE_RESPONSE_PORT = 5003 + 1  # Port to send intercepted data to Bob
BOB_PORT = 5003
ALICE_RESPONSE_PORT = 5004 + 1  # Port to receive from Bob and send to Alice

def main():
    print("=" * 70)
    print("  EVE SERVER — Quantum Channel Eavesdropper")
    print("=" * 70)
    print(f"Listening on port {EVE_PORT}...")
    print()

    while True:
        try:
            # Receive Alice's qubits
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.bind(('localhost', EVE_PORT))
                server.listen(5)
                print("Waiting for Alice's qubits...")
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
                        print("[EVE] Timeout receiving data from Alice")
                        continue
                    
                    data_str = data.decode().strip()
                    if not data_str:
                        print("[EVE] No data received, waiting for next connection...")
                        continue
                    
                    try:
                        alice_data = json.loads(data_str)
                    except json.JSONDecodeError as e:
                        print(f"[EVE] Failed to parse JSON from Alice: {str(e)}")
                        continue
                    
                    print(f"[EVE] Received {len(alice_data['bits'])} qubits from Alice")

            eve_enabled = True  # Set based on config if needed
            eve_bases = []
            eve_intercepted_bits = []

            if eve_enabled:
                print("[EVE] Intercepting qubits...")
                eve_data = eve_intercept(alice_data['bits'], alice_data['bases'])
                eve_bases = eve_data['bases']
                eve_intercepted_bits = eve_data['resent_bits']
                transmit_data = {
                    'bits': eve_data['resent_bits'],
                    'bases': eve_data['resent_bases'],
                    'states': alice_data['states']
                }
            else:
                print("[EVE] Forwarding qubits without interception...")
                transmit_data = alice_data
                eve_bases = []

            # Forward to Bob
            print("[EVE] Forwarding to Bob...")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', BOB_PORT))
                s.sendall(json.dumps(transmit_data).encode())

            # Wait for Bob's response
            print("[EVE] Waiting for Bob's measurement data...")
            bob_response = None
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
                    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    server.bind(('localhost', EVE_RESPONSE_PORT))
                    server.settimeout(10.0)
                    server.listen(5)
                    print(f"[EVE] Listening on port {EVE_RESPONSE_PORT} for Bob's response...")
                    conn, addr = server.accept()
                    print(f"[EVE] Received connection from {addr}")
                    with conn:
                        conn.settimeout(5.0)
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
                        if data_str:
                            bob_response = json.loads(data_str)
                            print("[EVE] ✓ Successfully received Bob's data")
                        else:
                            print("[EVE ERROR] No data received from Bob")
                            raise Exception("No data from Bob")
            except Exception as e:
                print(f"[EVE ERROR] Failed to receive Bob's response: {str(e)}")
                raise

            print(f"[EVE] Received Bob's {len(bob_response.get('bases', []))} measurement bases")

            # Add Eve's bases to the response
            if eve_enabled:
                bob_response['eve_bases'] = eve_bases

            # Forward Bob's data to Alice
            print("[EVE] Forwarding Bob's data to Alice...")
            try:
                # Retry connection to Alice (she might not be listening yet)
                max_retries = 5
                for attempt in range(max_retries):
                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            s.settimeout(2.0)
                            s.connect(('localhost', ALICE_RESPONSE_PORT))
                            s.sendall(json.dumps(bob_response).encode())
                            print("[EVE] ✓ Successfully forwarded Bob's data to Alice")
                            break
                    except (ConnectionRefusedError, socket.timeout) as retry_error:
                        if attempt < max_retries - 1:
                            print(f"[EVE] Connection attempt {attempt + 1}/{max_retries} failed, retrying...")
                            import time
                            time.sleep(0.5)
                        else:
                            raise retry_error
            except Exception as e:
                print(f"[EVE ERROR] Failed to forward to Alice: {str(e)}")
                raise

            print("[EVE] Transaction complete\n")

        except KeyboardInterrupt:
            print("\n[EVE] Keyboard interrupt received; continuing to listen...")
            continue
        except Exception as e:
            print(f"[EVE ERROR] {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    main()
