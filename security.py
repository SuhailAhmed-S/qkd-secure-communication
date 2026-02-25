"""
Module 6: Security Analysis & Communication Module
- Calculates Quantum Bit Error Rate (QBER)
- Decides if channel is secure or compromised
- Encrypts and decrypts messages using the shared sifted key (XOR cipher)

QBER = number of mismatched bits / total sifted bits
Security threshold: QBER < 0.11 (11%) — standard BB84 security bound
"""

import hashlib

QBER_THRESHOLD = 0.11  # 11% — standard BB84 security bound


# ─── QBER Calculation ────────────────────────────────────────────────────────

def calculate_qber(alice_sifted: list, bob_sifted: list) -> dict:
    """Calculates the Quantum Bit Error Rate between Alice and Bob's sifted keys."""
    if not alice_sifted:
        return {'qber': 1.0, 'errors': 0, 'total': 0, 'secure': False}

    errors = sum(a != b for a, b in zip(alice_sifted, bob_sifted))
    qber   = errors / len(alice_sifted)
    secure = qber < QBER_THRESHOLD

    return {
        'qber':   round(qber, 4),
        'errors': errors,
        'total':  len(alice_sifted),
        'secure': secure
    }


# ─── Key Generation ──────────────────────────────────────────────────────────

def bits_to_bytes(bits: list) -> bytes:
    """Convert a list of bits to bytes (pads to nearest 8 bits)."""
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


def derive_key(sifted_bits: list, key_length: int = 16) -> bytes:
    """
    Derives a fixed-length key from sifted bits using SHA-256.
    key_length: bytes (16 = 128-bit key)
    """
    raw = bits_to_bytes(sifted_bits)
    digest = hashlib.sha256(raw).digest()
    return digest[:key_length]


# ─── XOR Encryption / Decryption ─────────────────────────────────────────────

def xor_encrypt(message: str, key: bytes) -> str:
    """
    Encrypts a message using XOR with the quantum-derived key.
    Key is repeated (extended) to match message length.
    Returns hex-encoded ciphertext.
    """
    msg_bytes  = message.encode('utf-8')
    key_stream = (key * (len(msg_bytes) // len(key) + 1))[:len(msg_bytes)]
    cipher     = bytes(a ^ b for a, b in zip(msg_bytes, key_stream))
    return cipher.hex()


def xor_decrypt(ciphertext_hex: str, key: bytes) -> str:
    """Decrypts a hex-encoded XOR-encrypted message."""
    cipher     = bytes.fromhex(ciphertext_hex)
    key_stream = (key * (len(cipher) // len(key) + 1))[:len(cipher)]
    plain      = bytes(a ^ b for a, b in zip(cipher, key_stream))
    return plain.decode('utf-8')


# ─── Full Pipeline ────────────────────────────────────────────────────────────

def secure_communication(alice_sifted: list, bob_sifted: list,
                          message: str) -> dict:
    """
    End-to-end secure communication:
    1. Verify QBER
    2. If secure, derive key, encrypt message on Alice's side
    3. Decrypt on Bob's side
    """
    qber_result = calculate_qber(alice_sifted, bob_sifted)

    if not qber_result['secure']:
        return {
            **qber_result,
            'status':    'ABORT — Eavesdropping Detected',
            'key_hex':   None,
            'encrypted': None,
            'decrypted': None
        }

    # Alice derives key from her sifted bits
    alice_key = derive_key(alice_sifted)
    # Bob derives key from his sifted bits
    bob_key   = derive_key(bob_sifted)

    encrypted  = xor_encrypt(message, alice_key)
    try:
        decrypted = xor_decrypt(encrypted, bob_key)
    except Exception:
        decrypted = '[Decryption failed — keys diverged]'

    return {
        **qber_result,
        'status':    'SECURE — Communication Successful',
        'key_hex':   alice_key.hex(),
        'encrypted': encrypted,
        'decrypted': decrypted
    }
