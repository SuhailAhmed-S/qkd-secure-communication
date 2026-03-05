"""
Distributed Bob Server for QKD BB84 Protocol

This server runs Bob's part:
1. Receives qubits from Eve
2. Measures them
3. Sends measurement data back to Eve
"""

import socket
import json
import sys
import os

# Add project directory to path
sys.path.insert(0, os.path.dirname(__file__))

from bob import bob_measure

def main():
    BOB_PORT = 5003
    EVE_HOST = 'localhost'
    EVE_PORT = 5002 + 1  # Eve's response port

    print("Bob: Listening for Eve...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(('localhost', BOB_PORT))
        server.listen(1)
        conn, addr = server.accept()
        with conn:
            data = conn.recv(4096)
            transmit_data = json.loads(data.decode())
            print("Bob: Received qubits from Eve")

    print("Bob: Measuring qubits...")
    bob_data = bob_measure(transmit_data['bits'], transmit_data['bases'])

    # Send bases and measured bits back to Eve
    print("Bob: Sending data to Eve...")
    response_data = {'bases': bob_data['bob_bases'], 'bits': bob_data['bob_bits']}
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((EVE_HOST, EVE_PORT))
        s.sendall(json.dumps(response_data).encode())

if __name__ == '__main__':
    main()