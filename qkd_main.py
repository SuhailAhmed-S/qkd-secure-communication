"""
QKD Orchestrator — ties all 6 modules together.
Run this to simulate the complete BB84 QKD pipeline.

Pipeline:
    Alice → Quantum Channel (→ optional Eve) → Bob → Sift → QBER → Encrypt
"""

import json
from alice          import alice_prepare
from quantum_channel import quantum_channel_transmit
from bob            import bob_measure, sift_key
from security       import secure_communication, calculate_qber


def run_qkd(num_qubits: int = 100,
            message:     str  = "Hello, Quantum World!",
            eve_enabled: bool = False) -> dict:
    """
    Runs the complete BB84 QKD protocol and returns a full result dictionary.
    """
    print("=" * 60)
    print("  BB84 Quantum Key Distribution — Full Simulation")
    print("=" * 60)
    print(f"  Qubits     : {num_qubits}")
    print(f"  Message    : {message}")
    print(f"  Eve Active : {eve_enabled}")
    print()

    # ── Step 1: Alice prepares qubits ────────────────────────────────────────
    alice_data = alice_prepare(num_qubits)
    print(f"[Alice] Generated {num_qubits} random bits & bases.")
    print(f"        First 10 bits  : {alice_data['bits'][:10]}")
    print(f"        First 10 bases : {alice_data['bases'][:10]}")
    print(f"        First 10 states: {alice_data['states'][:10]}")
    print()

    # ── Step 2: Quantum channel (with optional Eve) ───────────────────────────
    channel = quantum_channel_transmit(
        alice_data['bits'], alice_data['bases'], eve_enabled=eve_enabled
    )
    if eve_enabled:
        print(f"[Eve]   Intercepted qubits! Resent with her own bases.")
        print(f"        Eve's first 10 bases: {channel['eve_bases'][:10]}")
    else:
        print("[Channel] No eavesdropping. Qubits transmitted cleanly.")
    print()

    # ── Step 3: Bob measures ─────────────────────────────────────────────────
    bob_data = bob_measure(channel['transmitted_bits'], channel['transmitted_bases'])
    print(f"[Bob]   Measured qubits in random bases.")
    print(f"        Bob's first 10 bases: {bob_data['bob_bases'][:10]}")
    print(f"        Bob's first 10 bits : {bob_data['bob_bits'][:10]}")
    print()

    # ── Step 4: Key sifting ───────────────────────────────────────────────────
    sift = sift_key(
        alice_data['bits'], alice_data['bases'],
        bob_data['bob_bits'], bob_data['bob_bases']
    )
    print(f"[Sift]  Matching bases: {sift['sift_count']}/{num_qubits} bits kept.")
    print(f"        Alice sifted (first 20): {sift['alice_sifted'][:20]}")
    print(f"        Bob   sifted (first 20): {sift['bob_sifted'][:20]}")
    print()

    # ── Step 5: QBER + Secure Communication ──────────────────────────────────
    result = secure_communication(
        sift['alice_sifted'], sift['bob_sifted'], message
    )
    print(f"[Security] QBER      : {result['qber']*100:.2f}%  "
          f"({result['errors']} errors / {result['total']} bits)")
    print(f"[Security] Status    : {result['status']}")
    if result['key_hex']:
        print(f"[Security] Key (hex) : {result['key_hex']}")
        print(f"[Encrypt]  Ciphertext: {result['encrypted'][:40]}...")
        print(f"[Decrypt]  Plaintext : {result['decrypted']}")
    print()
    print("=" * 60)

    return {
        'num_qubits':    num_qubits,
        'message':       message,
        'eve_enabled':   eve_enabled,
        'alice_bits':    alice_data['bits'],
        'alice_bases':   alice_data['bases'],
        'alice_states':  alice_data['states'],
        'eve_bases':     channel.get('eve_bases', []),
        'bob_bases':     bob_data['bob_bases'],
        'bob_bits':      bob_data['bob_bits'],
        'alice_sifted':  sift['alice_sifted'],
        'bob_sifted':    sift['bob_sifted'],
        'sift_count':    sift['sift_count'],
        'matching_idx':  sift['matching_idx'],
        **result
    }


if __name__ == '__main__':
    print("\n>>> TEST 1: Normal communication (no eavesdropping)\n")
    run_qkd(num_qubits=200, message="Secure message from Alice!", eve_enabled=False)

    print("\n>>> TEST 2: With Eve eavesdropping\n")
    run_qkd(num_qubits=200, message="Intercepted message test.", eve_enabled=True)
