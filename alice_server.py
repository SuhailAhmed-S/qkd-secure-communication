"""
Distributed Alice Server for QKD BB84 Protocol

This server runs Alice's part of the protocol:
1. Prepares qubits
2. Sends quantum data to Eve
3. Receives Bob's measurement bases
4. Performs sifting and QBER calculation
5. Derives shared key and encrypts message
"""

import socket
import json
import sys
import os

# Add project directory to path
sys.path.insert(0, os.path.dirname(__file__))

from alice import alice_prepare
from security import calculate_qber, derive_key, xor_encrypt

def main():
    # Configuration
    ALICE_PORT = 5004
    EVE_HOST = 'localhost'
    EVE_PORT = 5002
    BOB_HOST = 'localhost'
    BOB_PORT = 5003

    num_qubits = 100
    message = "Hello, Quantum World!"
    eve_enabled = True  # Set to False to skip Eve

    print("Alice: Preparing qubits...")
    alice_data = alice_prepare(num_qubits)

    # Send to Eve
    print("Alice: Sending qubits to Eve...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((EVE_HOST, EVE_PORT))
        s.sendall(json.dumps(alice_data).encode())

    # Wait for Bob's bases and bits from Eve (Eve forwards)
    print("Alice: Waiting for Bob's data...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(('localhost', ALICE_PORT))
        server.listen(1)
        conn, addr = server.accept()
        with conn:
            data = conn.recv(4096)
            bob_data = json.loads(data.decode())
            bob_bases = bob_data['bases']
            bob_bits = bob_data['bits']

    # Perform sifting
    print("Alice: Performing sifting...")
    sifted_bits = []
    sifted_bases = []
    sifted_bob_bits = []
    for i in range(num_qubits):
        if alice_data['bases'][i] == bob_bases[i]:
            sifted_bits.append(alice_data['bits'][i])
            sifted_bob_bits.append(bob_bits[i])
            sifted_bases.append(alice_data['bases'][i])

    sift_count = len(sifted_bits)
    print(f"Alice: Sifted {sift_count} bits")

    # Calculate QBER
    qber_result = calculate_qber(sifted_bits, sifted_bob_bits)
    qber = qber_result['qber']
    secure = qber_result['secure']
    errors = qber_result['errors']
    total = qber_result['total']

    print(f"Alice: QBER = {qber:.2%}, Errors = {errors}/{total}")

    if secure:
        # Derive key
        key = derive_key(sifted_bits)
        encrypted = xor_encrypt(message, key)
        print(f"Alice: Secure key established")
        print(f"Message: {message}")
        print(f"Encrypted: {encrypted}")
    else:
        print("Alice: Communication not secure")

if __name__ == '__main__':
    main()