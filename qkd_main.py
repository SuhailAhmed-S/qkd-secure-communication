"""
QKD Orchestrator Module

This module coordinates the complete BB84 Quantum Key Distribution protocol,
tying together all 6 components into a single, cohesive simulation.

Protocol Pipeline:
    1. Alice → Generates random qubits and bases
    2. Quantum Channel → Transmits qubits (optionally through Eve)
    3. Eve (optional) → Intercepts and re-sends, introducing detectable errors
    4. Bob → Measures qubits in random bases
    5. Sift → Both compare bases publicly, keep matching bits
    6. QBER → Calculate error rate, detect eavesdropping
    7. Encrypt → Use shared key to encrypt/decrypt message

BB84 Security Properties:
    - Information-theoretic security: Proven secure against quantum computers
    - Eavesdropping detection: Eve's presence raises QBER from 0% to ~25%
    - Key generation rate: ~50% of transmitted qubits become usable key
    - No pre-shared secrets: Key is generated from scratch each session

Expected Results:
    - Clean channel (no Eve): QBER ≈ 0%, ~N/2 bits in sifted key
    - With Eve: QBER ≈ 25%, elevated error rate easily detected
"""

import json
from typing import Dict, Optional

from alice import alice_prepare
from quantum_channel import quantum_channel_transmit
from bob import bob_measure, sift_key
from security import secure_communication, calculate_qber


def run_qkd(num_qubits: int = 100,
            message: str = "Hello, Quantum World!",
            eve_enabled: bool = False) -> Dict[str, object]:
    """
    Runs the complete BB84 QKD protocol and returns comprehensive results.
    
    This is the main entry point for the QKD simulation. It orchestrates all
    protocol steps and returns detailed metrics about the key distribution
    and encryption.
    
    Args:
        num_qubits (int): Number of qubits to transmit.
                         Must be between 10 and 10,000.
                         Typical: 100-1000 for simulation
                         Default: 100
                         
        message (str): Message to encrypt and transmit.
                      Must be non-empty.
                      Default: "Hello, Quantum World!"
                      
        eve_enabled (bool): Whether to simulate eavesdropping.
                           True: Eve intercepts and re-sends (detectable)
                           False: Clean quantum channel
                           Default: False
                           
    Returns:
        Dict[str, object]: Comprehensive results containing:
            - Protocol metrics: num_qubits, message, eve_enabled
            - Alice's data: alice_bits, alice_bases, alice_states
            - Eve's data: eve_bases (empty if eve_enabled=False)
            - Bob's data: bob_bases, bob_bits
            - Sifting results: alice_sifted, bob_sifted, sift_count, matching_idx
            - Security metrics: qber, errors, total, secure, status
            - Encryption results: key_hex, encrypted, decrypted
            
    Raises:
        ValueError: If num_qubits is out of valid range
        ValueError: If message is empty
        
    Security Considerations:
        1. The sifted keys should be identical (alice_sifted == bob_sifted)
           unless eavesdropping occurred
        2. QBER < 11% indicates secure channel
        3. QBER ≈ 25% indicates eavesdropping
        4. In practice, additional privacy amplification would be applied
        
    Performance Notes:
        - Linear time complexity: O(num_qubits)
        - Memory: O(num_qubits) for storing all intermediate results
        - Typical execution: < 100ms for 1000 qubits
        
    Example:
        >>> result = run_qkd(num_qubits=100, 
        ...                   message="Secret", 
        ...                   eve_enabled=False)
        >>> result['secure']
        True
        >>> result['sift_count'] > 0
        True
    """
    # Input validation
    if not isinstance(num_qubits, int) or num_qubits < 10 or num_qubits > 10000:
        raise ValueError(f"num_qubits must be between 10 and 10,000, got {num_qubits}")
    if not message or not isinstance(message, str):
        raise ValueError("message must be a non-empty string")
    
    print("=" * 70)
    print("  BB84 Quantum Key Distribution — Full Simulation")
    print("=" * 70)
    print(f"  Qubits     : {num_qubits}")
    print(f"  Message    : {message}")
    print(f"  Eve Active : {eve_enabled}")
    print()

    # ── Step 1: Alice prepares qubits ────────────────────────────────────────
    print("[1] ALICE — Qubit Preparation")
    print("-" * 70)
    alice_data = alice_prepare(num_qubits)
    print(f"    Generated {num_qubits} random bits & bases.")
    print(f"    First 10 bits  : {alice_data['bits'][:10]}")
    print(f"    First 10 bases : {alice_data['bases'][:10]}")
    print(f"    First 10 states: {alice_data['states'][:10]}")
    print()

    # ── Step 2: Quantum channel (with optional Eve) ───────────────────────────
    print("[2] QUANTUM CHANNEL — Transmission")
    print("-" * 70)
    channel = quantum_channel_transmit(
        alice_data['bits'], alice_data['bases'], eve_enabled=eve_enabled
    )
    if eve_enabled:
        print(f"    ⚠  EVE ACTIVE: Intercepted qubits! Resent with her own bases.")
        print(f"    Eve's first 10 bases: {channel['eve_bases'][:10]}")
    else:
        print("    ✓  Clean transmission: No eavesdropping detected.")
    print()

    # ── Step 3: Bob measures ─────────────────────────────────────────────────
    print("[3] BOB — Qubit Measurement")
    print("-" * 70)
    bob_data = bob_measure(channel['transmitted_bits'], channel['transmitted_bases'])
    print(f"    Measured qubits in random bases.")
    print(f"    Bob's first 10 bases: {bob_data['bob_bases'][:10]}")
    print(f"    Bob's first 10 bits : {bob_data['bob_bits'][:10]}")
    print()

    # ── Step 4: Key sifting ───────────────────────────────────────────────────
    print("[4] SIFTING — Basis Reconciliation")
    print("-" * 70)
    sift = sift_key(
        alice_data['bits'], alice_data['bases'],
        bob_data['bob_bits'], bob_data['bob_bases']
    )
    print(f"    Matching bases: {sift['sift_count']}/{num_qubits} bits kept")
    print(f"    Sift efficiency: {(sift['sift_count']/num_qubits)*100:.1f}%")
    print(f"    Alice sifted (first 20): {sift['alice_sifted'][:20]}")
    print(f"    Bob   sifted (first 20): {sift['bob_sifted'][:20]}")
    print()

    # ── Step 5: QBER + Secure Communication ──────────────────────────────────
    print("[5] SECURITY ANALYSIS — QBER & Encryption")
    print("-" * 70)
    result = secure_communication(
        sift['alice_sifted'], sift['bob_sifted'], message
    )
    
    print(f"    QBER: {result['qber']*100:.2f}% ({result['errors']} errors / {result['total']} bits)")
    print(f"    Threshold: < 11% for secure channel")
    print(f"    Status: {result['status']}")
    
    if result['key_hex']:
        print(f"    Key (hex): {result['key_hex']}")
        print(f"    Ciphertext: {result['encrypted'][:40]}...")
        print(f"    Plaintext: {result['decrypted']}")
    print()
    print("=" * 70)
    print()

    # Compile complete results dictionary
    return {
        # Protocol parameters
        'num_qubits': num_qubits,
        'message': message,
        'eve_enabled': eve_enabled,
        
        # Alice's transmission
        'alice_bits': alice_data['bits'],
        'alice_bases': alice_data['bases'],
        'alice_states': alice_data['states'],
        
        # Eve's interception (empty if no eavesdropping)
        'eve_bases': channel.get('eve_bases', []),
        
        # Bob's measurement
        'bob_bases': bob_data['bob_bases'],
        'bob_bits': bob_data['bob_bits'],
        
        # Sifting results
        'alice_sifted': sift['alice_sifted'],
        'bob_sifted': sift['bob_sifted'],
        'sift_count': sift['sift_count'],
        'matching_idx': sift['matching_idx'],
        
        # Security and encryption results
        **result
    }


if __name__ == '__main__':
    print("\n" + "█" * 70)
    print("█  TEST 1: Normal communication (no eavesdropping)")
    print("█" * 70 + "\n")
    run_qkd(num_qubits=200, message="Secure message from Alice!", eve_enabled=False)

    print("\n" + "█" * 70)
    print("█  TEST 2: With Eve eavesdropping")
    print("█" * 70 + "\n")
    run_qkd(num_qubits=200, message="Intercepted message test.", eve_enabled=True)
