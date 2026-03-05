"""
Distributed Eve Server for QKD BB84 Protocol

This server runs Eve's part:
1. Receives qubits from Alice
2. Optionally intercepts (measures and resends)
3. Forwards to Bob
4. Forwards Bob's data back to Alice
"""

import socket
import json
import sys
import os

# Add project directory to path
sys.path.insert(0, os.path.dirname(__file__))

from eve import eve_intercept

def main():
    EVE_PORT = 5002
    BOB_HOST = 'localhost'
    BOB_PORT = 5003
    ALICE_HOST = 'localhost'
    ALICE_PORT = 5004

    eve_enabled = True  # Set to False to just forward

    print("Eve: Listening for Alice...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(('localhost', EVE_PORT))
        server.listen(1)
        conn, addr = server.accept()
        with conn:
            data = conn.recv(4096)
            alice_data = json.loads(data.decode())
            print("Eve: Received qubits from Alice")

    if eve_enabled:
        print("Eve: Intercepting qubits...")
        eve_data = eve_intercept(alice_data['bits'], alice_data['bases'])
        transmit_data = {
            'bits': eve_data['resent_bits'],
            'bases': eve_data['resent_bases'],
            'states': alice_data['states']
        }
    else:
        print("Eve: Forwarding qubits...")
        transmit_data = alice_data

    # Send to Bob
    print("Eve: Sending to Bob...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((BOB_HOST, BOB_PORT))
        s.sendall(json.dumps(transmit_data).encode())

    # Receive Bob's data from Bob
    print("Eve: Waiting for Bob's data...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(('localhost', EVE_PORT + 1))
        server.listen(1)
        conn, addr = server.accept()
        with conn:
            data = conn.recv(4096)
            bob_data = json.loads(data.decode())
            print("Eve: Received Bob's data")

    # Forward Bob's data to Alice
    print("Eve: Forwarding Bob's data to Alice...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ALICE_HOST, ALICE_PORT))
        s.sendall(json.dumps(bob_data).encode())

if __name__ == '__main__':
    main()