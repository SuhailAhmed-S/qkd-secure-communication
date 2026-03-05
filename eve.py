"""
Module 4: Eve Module (Attack Simulation — Intercept-Resend Attack)

Simulates an eavesdropper (Eve) who intercepts quantum bits, measures them,
and resends them to Bob.

Description:
    Eve performs an "intercept-resend" attack:
    1. Eve randomly selects measurement bases for each qubit
    2. Eve measures and records results
    3. Eve re-encodes her measured bits and resends them to Bob
    4. This introduces approximately 25% errors in the final sifted key
    
    The errors arise because:
    - When Eve uses the wrong basis (~50% of the time), she gets random results
    - Bob then measures the corrupted qubit with either correct or wrong basis
    - If both Eve and Bob used wrong bases but different from Alice's,
      it introduces errors into the sifted key

BB84 Measurement Rules (for Eve):
    - If Eve's basis matches Alice's basis → Eve measures the correct bit
    - If Eve's basis differs from Alice's → Eve gets a random bit (50% error)
    - Eve then resends the bit she measured (not the original)
    
    The key insight: Eve cannot measure without disturbing the state.
    This disturbance is detectable by Alice and Bob via increased QBER.

Security Implications:
    - Expected QBER with Eve: ~25% (error_rate * measurement_mismatch_rate)
    - Threshold for detection: QBER < 11% normally, ~25% with eavesdropping
    - Alice and Bob can detect Eve's presence with high confidence
"""

import random
from typing import Dict, List


def eve_intercept(alice_bits: List[int], alice_bases: List[str]) -> Dict[str, List]:
    """
    Simulates Eve's intercept-resend attack on the quantum channel.
    
    Eve intercepts each qubit traveling from Alice to Bob, measures it
    with a randomly chosen basis, and then re-encodes and resends her
    measurement result. This introduces detectable errors.
    
    Args:
        alice_bits (List[int]): Alice's original bits
        alice_bases (List[str]): Alice's measurement bases
        
    Returns:
        Dict[str, List]: Dictionary containing:
            - 'eve_bases': List[str] - Eve's measurement bases
            - 'resent_bits': List[int] - Eve's measurement results (what she resends)
            - 'resent_bases': List[str] - Eve's encoding bases for resending
            
    Note:
        The key security feature is that Eve resends in HER bases (her measurement
        bases), not Alice's. This is different from transparent transmission where
        the encoding basis would be preserved.
        
    Attack Details:
        - Eve uses 50/50 basis choice, matching Alice's ~50% of the time
        - When bases match: Eve measures correctly (0 error)
        - When bases differ: Eve gets random result (50% chance of error)
        - Overall error rate from Eve: 50% × 50% = 25%
        
    Security Detection:
        The QBER will be elevated from ~0% (clean channel) to ~25% (with Eve),
        allowing Alice and Bob to detect the eavesdropping attempt.
    """
    num_qubits = len(alice_bits)
    # Eve makes random basis choices (same as Alice and Bob)
    eve_bases: List[str] = [random.choice(['+', '×']) for _ in range(num_qubits)]
    resent_bits: List[int] = []
    resent_bases: List[str] = []

    # Eve intercepts and re-encodes each qubit
    for i in range(num_qubits):
        if eve_bases[i] == alice_bases[i]:
            # Eve's basis matches Alice's → Eve measures the correct bit
            measured_bit = alice_bits[i]
        else:
            # Eve's basis differs from Alice's → quantum measurement disturbance
            # Eve measures a random result (50/50 probability)
            measured_bit = random.randint(0, 1)

        # Eve resends the bit she measured in her basis
        # This is different from a transparent transmission where encoding
        # basis would be preserved
        resent_bits.append(measured_bit)
        resent_bases.append(eve_bases[i])

    return {
        'eve_bases': eve_bases,
        'resent_bits': resent_bits,
        'resent_bases': resent_bases
    }
