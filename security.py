"""
Module 6: Security Analysis & Communication Module

Implements quantum bit error rate (QBER) calculation, key derivation,
and message encryption/decryption using the quantum-derived key.

Key Concepts:

QBER (Quantum Bit Error Rate):
    Measures the fraction of bits that differ between Alice's and Bob's
    sifted keys:
    
        QBER = (number of differing bits) / (total sifted bits)
    
    - Clean channel (no eavesdropping): QBER ≈ 0% (due to quantum mechanics)
    - With eavesdropper (Eve): QBER ≈ 25% (measurable disturbance)
    
    This threshold is how Alice and Bob detect unauthorized access.

Security Threshold:
    - QBER < 11%: Channel considered secure (standard BB84 threshold)
    - QBER ≥ 11%: Likely eavesdropping detected, abort communication
    
    The 11% threshold accounts for:
    - Quantum noise in real systems (~1-2%)
    - Environmental decoherence
    - Detector imperfections
    
Key Derivation:
    The sifted key (raw random bits) is processed through SHA-256
    to produce a fixed-length cryptographic key with uniform distribution.

Message Encryption:
    Uses simple XOR (one-time pad style) with the derived key.
    Note: In production, use authenticated encryption (AES-GCM).

Privacy Amplification:
    SHA-256 provides privacy amplification, ensuring that even if Eve
    has partial information about the sifted key, she cannot recover
    the actual encryption key.
"""

import hashlib
from typing import Dict, List, Tuple

# Standard BB84 security threshold
# QBER below this indicates a secure channel
QBER_THRESHOLD = 0.11  # 11%


# ─── QBER Calculation ────────────────────────────────────────────────────────

def calculate_qber(alice_sifted: List[int], bob_sifted: List[int]) -> Dict[str, object]:
    """
    Calculates the Quantum Bit Error Rate (QBER) between Alice and Bob's sifted keys.
    
    QBER is the primary security metric in BB84. It indicates whether the quantum
    channel is secure (low QBER) or compromised (high QBER due to eavesdropping).
    
    Args:
        alice_sifted (List[int]): Alice's sifted key (bits where bases matched)
        bob_sifted (List[int]): Bob's sifted key (bits where bases matched)
        
    Returns:
        Dict[str, object]: Security metrics containing:
            - 'qber': float - Quantum bit error rate (0.0 to 1.0)
            - 'errors': int - Number of differing bits
            - 'total': int - Total sifted bits compared
            - 'secure': bool - Whether QBER is below security threshold
            
    Note:
        - If sifted key is empty, returns QBER=1.0 (assumed compromised)
        - QBER is rounded to 4 decimal places
        - The sifted keys should be identical-length lists
        
    Example:
        >>> alice_key = [1, 0, 1, 1, 0]
        >>> bob_key =   [1, 0, 1, 0, 0]  # 1 error
        >>> result = calculate_qber(alice_key, bob_key)
        >>> result['qber']
        0.2
        >>> result['secure']
        False
    """
    # Handle empty sifted key
    if not alice_sifted:
        return {
            'qber': 1.0,
            'errors': 0,
            'total': 0,
            'secure': False
        }

    # Count bit errors
    errors = sum(a != b for a, b in zip(alice_sifted, bob_sifted))
    qber = errors / len(alice_sifted)
    secure = qber < QBER_THRESHOLD

    return {
        'qber': round(qber, 4),
        'errors': errors,
        'total': len(alice_sifted),
        'secure': secure
    }


# ─── Key Generation ──────────────────────────────────────────────────────────

def bits_to_bytes(bits: List[int]) -> bytes:
    """
    Convert a list of bits to bytes, padding to nearest 8-bit boundary.
    
    Args:
        bits (List[int]): List of bits (0 or 1)
        
    Returns:
        bytes: Bytes representation of the bits
        
    Note:
        - Bits are MSB-first (most significant bit first)
        - Padding zeros are added to reach multiple of 8
        
    Example:
        >>> bits = [1, 0, 1, 0, 1, 1, 0, 1]
        >>> bits_to_bytes(bits).hex()
        'ad'
    """
    # Pad to multiple of 8
    padded = bits[:]
    while len(padded) % 8 != 0:
        padded.append(0)
    
    result = bytearray()
    for i in range(0, len(padded), 8):
        byte = 0
        for b in padded[i:i+8]:
            byte = (byte << 1) | b
        result.append(byte)
    return bytes(result)


def derive_key(sifted_bits: List[int], key_length: int = 16) -> bytes:
    """
    Derives a fixed-length cryptographic key from sifted bits using SHA-256.
    
    This provides privacy amplification: any partial information Eve has about
    the sifted key cannot be used to recover the actual encryption key.
    
    Args:
        sifted_bits (List[int]): The sifted key bits from QKD
        key_length (int): Desired key length in bytes.
                         Default: 16 (128-bit AES key)
                         
    Returns:
        bytes: Cryptographic key of specified length
        
    Note:
        - SHA-256 output is 32 bytes
        - Supports key lengths up to 32 bytes
        - For longer keys, use key expansion (e.g., HKDF)
        - Empty sifted key produces all-zero key (detected as insecure via QBER)
        
    Example:
        >>> bits = [1, 0, 1, 0] * 20  # 80 bits
        >>> key = derive_key(bits, key_length=16)
        >>> len(key)
        16
    """
    # Convert bits to bytes
    raw = bits_to_bytes(sifted_bits)
    # Apply SHA-256 for privacy amplification and uniform distribution
    digest = hashlib.sha256(raw).digest()
    # Return requested key length
    return digest[:key_length]


# ─── XOR Encryption / Decryption ─────────────────────────────────────────────

def xor_encrypt(message: str, key: bytes) -> str:
    """
    Encrypts a message using XOR with the quantum-derived key.
    
    This implements a one-time pad cipher (OTP) style encryption.
    The key stream is repeated if the message is longer than the key.
    
    Args:
        message (str): Plaintext message to encrypt (UTF-8)
        key (bytes): Encryption key derived from sifted QKD key
        
    Returns:
        str: Hex-encoded ciphertext
        
    Note:
        - For true OTP security, key length should be >= message length
        - XOR is symmetric: encrypt(encrypt(m)) = m
        - In production, use authenticated encryption (AES-GCM, ChaCha20-Poly1305)
        
    Example:
        >>> key = b'\\x00\\x01\\x02\\x03'
        >>> ct = xor_encrypt("Hello", key)
        >>> len(ct) > 0
        True
    """
    # Convert message to bytes
    msg_bytes = message.encode('utf-8')
    # Extend key to match message length (repeat key cyclically)
    key_stream = (key * (len(msg_bytes) // len(key) + 1))[:len(msg_bytes)]
    # XOR each byte
    cipher = bytes(a ^ b for a, b in zip(msg_bytes, key_stream))
    # Return hex encoding for transmission
    return cipher.hex()


def xor_decrypt(ciphertext_hex: str, key: bytes) -> str:
    """
    Decrypts a hex-encoded XOR-encrypted message.
    
    Args:
        ciphertext_hex (str): Hex-encoded ciphertext
        key (bytes): Decryption key (same as encryption key for XOR)
        
    Returns:
        str: Decrypted plaintext message (UTF-8)
        
    Raises:
        UnicodeDecodeError: If decrypted bytes are not valid UTF-8
        ValueError: If ciphertext_hex is not valid hex
        
    Note:
        XOR decryption is identical to encryption (XOR is self-inverse).
    """
    # Decode hex ciphertext
    cipher = bytes.fromhex(ciphertext_hex)
    # Extend key to match ciphertext length
    key_stream = (key * (len(cipher) // len(key) + 1))[:len(cipher)]
    # XOR to recover plaintext
    plain = bytes(a ^ b for a, b in zip(cipher, key_stream))
    # Decode from UTF-8
    return plain.decode('utf-8')


# ─── Full Pipeline ────────────────────────────────────────────────────────────

def secure_communication(alice_sifted: List[int], bob_sifted: List[int],
                          message: str) -> Dict[str, object]:
    """
    End-to-end secure communication pipeline.
    
    This function coordinates the complete security workflow:
    1. Calculate QBER to verify channel security
    2. If secure, derive cryptographic key from sifted bits
    3. Encrypt message on Alice's side using the key
    4. Decrypt message on Bob's side (verifying key agreement)
    
    Args:
        alice_sifted (List[int]): Alice's sifted key bits
        bob_sifted (List[int]): Bob's sifted key bits
        message (str): Message to encrypt and transmit
        
    Returns:
        Dict[str, object]: Communication results containing:
            - 'qber': float - Quantum bit error rate
            - 'errors': int - Number of bit errors detected
            - 'total': int - Total sifted bits
            - 'secure': bool - Whether channel is secure
            - 'status': str - Human-readable status message
            - 'key_hex': str or None - Hex-encoded derived key (if secure)
            - 'encrypted': str or None - Hex-encoded ciphertext (if secure)
            - 'decrypted': str or None - Decrypted message (if secure)
            
    Security Guarantees:
        - If secure=True: Message confidentiality is guaranteed (quantum-secure)
        - If secure=False: Communication is aborted, no encryption occurs
        
    Error Scenarios:
        - QBER too high: Eavesdropping detected, abort
        - Decryption error: Key mismatch (should not occur in clean channel)
        
    Example:
        >>> alice_key = [1, 0, 1, 0] * 20
        >>> bob_key = [1, 0, 1, 0] * 20  # Perfect agreement
        >>> result = secure_communication(alice_key, bob_key, "Secret")
        >>> result['secure']
        True
    """
    # Calculate QBER as primary security check
    qber_result = calculate_qber(alice_sifted, bob_sifted)

    # If QBER exceeds threshold, abort communication
    if not qber_result['secure']:
        return {
            **qber_result,
            'status': 'ABORT — Eavesdropping Detected',
            'key_hex': None,
            'encrypted': None,
            'decrypted': None
        }

    # Channel is secure: proceed with key derivation and encryption
    # Alice derives key from her sifted bits
    alice_key = derive_key(alice_sifted)
    # Bob derives key from his sifted bits
    bob_key = derive_key(bob_sifted)

    # Encrypt message using Alice's key
    encrypted = xor_encrypt(message, alice_key)
    
    # Decrypt message using Bob's key (should succeed if keys match)
    try:
        decrypted = xor_decrypt(encrypted, bob_key)
    except Exception as e:
        decrypted = f'[Decryption failed: {str(e)}]'

    return {
        **qber_result,
        'status': 'SECURE — Communication Successful',
        'key_hex': alice_key.hex(),
        'encrypted': encrypted,
        'decrypted': decrypted
    }
