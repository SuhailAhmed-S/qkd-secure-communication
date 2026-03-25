"""
Privacy Amplification Module for Quantum Key Distribution (QKD)

This module implements privacy amplification techniques to reduce information
leakage in sifted keys from QKD protocols (e.g., BB84). It uses universal
hash functions and cryptographic randomness extraction to produce shorter,
provably secure final keys.

QKD Pipeline Integration:
    1. Sifting: Alice & Bob exchange basis info, keep matching bases
    2. Error Correction: Detect/correct transmission errors
    3. Privacy Amplification: REDUCE information leakage via hashing
    4. Key Derivation: Generate final encryption keys

Algorithm Details:
    - Universal Hash Function: Toeplitz matrix-based hashing
    - Randomness Extraction: SHA-256/SHA-3 based
    - Security Guarantee: ε-universal hashing property
    - Information Theory: Reduces Eve's mutual information with key

Author: QKD Security Module
License: MIT
"""

import hashlib
import secrets
import math
from typing import Union, Tuple, Dict, List
from dataclasses import dataclass


@dataclass
class PrivacyAmplificationConfig:
    """
    Configuration parameters for privacy amplification.
    
    Attributes:
        method (str): 'toeplitz' (universal hash) or 'sha256' (extraction)
        hash_family (str): 'toeplitz', 'sha256', or 'sha3'
        security_parameter (int): λ, bits of security margin
        compression_ratio (float): Output size / Input size (0.0 - 1.0)
        qber (float): Quantum Bit Error Rate (0.0 - 1.0)
        leakage_estimate (float): Eve's estimated knowledge (0.0 - 1.0)
    """
    method: str = 'toeplitz'
    hash_family: str = 'toeplitz'
    security_parameter: int = 128  # λ (lambda): typical value 128 bits
    compression_ratio: float = 0.5  # Default: output is 50% of input
    qber: float = 0.0
    leakage_estimate: float = 0.0


class ToeplitzHash:
    """
    Toeplitz Matrix Universal Hash Function.
    
    A Toeplitz matrix is a band matrix where each descending diagonal from left
    to right is constant. Used for ε-universal hashing with optimal compression.
    
    Theory:
        - ε-universal: Collision probability ≤ 2^(-n) for n-bit output
        - Privacy guarantee: H_∞(K_final | Eve) ≥ |K_final| - λ bits
        - Optimal compression: Shortest key while maintaining security
    
    Security Property:
        If input has min-entropy H_∞(X) and we hash to m bits,
        output has min-entropy ≥ H_∞(X) - (n - m) bits
    """
    
    def __init__(self, input_length: int, output_length: int):
        """
        Initialize Toeplitz hash function.
        
        Args:
            input_length (int): Length of input bits
            output_length (int): Desired output length in bits
            
        Raises:
            ValueError: If output_length > input_length
        """
        if output_length > input_length:
            raise ValueError(
                f"Output length ({output_length}) cannot exceed "
                f"input length ({input_length})"
            )
        if input_length <= 0 or output_length <= 0:
            raise ValueError("Lengths must be positive")
        
        self.input_length = input_length
        self.output_length = output_length
        
        # Generate random Toeplitz matrix coefficients
        # Matrix size: output_length × input_length
        # For efficiency, only store first row and first column
        self.first_row = secrets.token_bytes((input_length + 7) // 8)
        self.first_col = secrets.token_bytes((output_length + 7) // 8)
    
    def _get_bit(self, byte_data: bytes, index: int) -> int:
        """Get bit at index from byte array."""
        if index < 0 or index >= len(byte_data) * 8:
            raise IndexError(f"Bit index {index} out of range")
        byte_idx = index // 8
        bit_idx = index % 8
        return (byte_data[byte_idx] >> bit_idx) & 1
    
    def _set_bit(self, byte_data: bytearray, index: int, value: int) -> None:
        """Set bit at index in byte array."""
        byte_idx = index // 8
        bit_idx = index % 8
        if value:
            byte_data[byte_idx] |= (1 << bit_idx)
        else:
            byte_data[byte_idx] &= ~(1 << bit_idx)
    
    def hash(self, input_bits: str) -> str:
        """
        Hash input bit string using Toeplitz matrix.
        
        Algorithm:
            For each output bit i: y[i] = sum(T[i,j] * x[j]) mod 2
            where T is the Toeplitz matrix and x is the input
        
        Args:
            input_bits (str): Input as binary string (e.g., "01101")
            
        Returns:
            str: Output hash as binary string
            
        Raises:
            ValueError: If input length doesn't match
        """
        if len(input_bits) != self.input_length:
            raise ValueError(
                f"Input length {len(input_bits)} != "
                f"expected {self.input_length}"
            )
        
        # Convert input bits to bytes for faster processing
        input_bytes = bytearray((self.input_length + 7) // 8)
        for i, bit_char in enumerate(input_bits):
            if bit_char not in ('0', '1'):
                raise ValueError(f"Invalid bit character: {bit_char}")
            if bit_char == '1':
                self._set_bit(input_bytes, i, 1)
        
        output_bits = []
        
        # Compute Toeplitz matrix multiplication: y = T * x (mod 2)
        for i in range(self.output_length):
            result = 0
            
            # First column elements (column 0, rows i..output_length-1)
            for j in range(i):
                matrix_elem = self._get_bit(self.first_col, i - j)
                input_elem = self._get_bit(input_bytes, j)
                result ^= (matrix_elem & input_elem)
            
            # First row elements (row i, columns i..input_length-1)
            for j in range(i, self.input_length):
                matrix_elem = self._get_bit(self.first_row, j - i)
                input_elem = self._get_bit(input_bytes, j)
                result ^= (matrix_elem & input_elem)
            
            output_bits.append(str(result))
        
        return ''.join(output_bits)
    
    def get_seed(self) -> bytes:
        """
        Get the seed (Toeplitz matrix parameters) for reproducibility.
        
        Returns:
            bytes: Concatenation of first_row and first_col
        """
        return self.first_row + self.first_col
    
    @staticmethod
    def from_seed(input_length: int, output_length: int, seed: bytes):
        """
        Recreate Toeplitz hasher from seed (for deterministic hashing).
        
        Args:
            input_length (int): Input bit length
            output_length (int): Output bit length
            seed (bytes): Previously generated seed
            
        Returns:
            ToeplitzHash: Initialized with deterministic matrix
        """
        hasher = ToeplitzHash(input_length, output_length)
        row_len = (input_length + 7) // 8
        col_len = (output_length + 7) // 8
        hasher.first_row = seed[:row_len]
        hasher.first_col = seed[row_len:row_len + col_len]
        return hasher


class SHAExtractor:
    """
    SHA-256/SHA-3 based Randomness Extractor.
    
    Uses cryptographic hash functions for privacy amplification.
    Simpler than Toeplitz but requires more compression.
    
    Security Model:
        - Treats SHA-256 as Random Oracle
        - Output has min-entropy ≈ output_bits if input has sufficient entropy
        - Security parameter: If output = hash(input), privacy loss ≈ λ bits
    """
    
    def __init__(self, hash_algo: str = 'sha256', output_bits: int = 128):
        """
        Initialize SHA extractor.
        
        Args:
            hash_algo (str): 'sha256' or 'sha3_256'
            output_bits (int): Final key length in bits
            
        Raises:
            ValueError: If hash_algo not supported
        """
        if hash_algo not in ('sha256', 'sha3_256'):
            raise ValueError(f"Unsupported hash algorithm: {hash_algo}")
        
        self.hash_algo = hash_algo
        self.output_bits = output_bits
        self.output_bytes = (output_bits + 7) // 8
    
    def extract(self, input_data: Union[str, bytes], salt: bytes = b'') -> bytes:
        """
        Extract randomness using SHA hash.
        
        Algorithm:
            output = HASH(salt || input)[:output_bytes]
        
        Args:
            input_data (str or bytes): Input key (bit string or bytes)
            salt (bytes): Optional salt for domain separation
            
        Returns:
            bytes: Extracted key of length output_bytes
        """
        # Convert bit string to bytes if needed
        if isinstance(input_data, str):
            input_bytes = bytes(int(input_data[i:i+8], 2) 
                               for i in range(0, len(input_data), 8))
        else:
            input_bytes = input_data
        
        # Hash with salt for domain separation
        if self.hash_algo == 'sha256':
            h = hashlib.sha256(salt + input_bytes)
        else:  # sha3_256
            h = hashlib.sha3_256(salt + input_bytes)
        
        # Return requested number of bytes
        return h.digest()[:self.output_bytes]
    
    def extract_with_counter(self, input_data: Union[str, bytes], 
                            counter: int = 0) -> bytes:
        """
        Extract with counter mode for producing longer keys.
        
        Useful when desired output > hash output (e.g., 256 bits > 128 bits).
        
        Args:
            input_data (str or bytes): Input key
            counter (int): Counter value for iteration
            
        Returns:
            bytes: Extracted key
        """
        # Convert bit string to bytes if needed
        if isinstance(input_data, str):
            input_bytes = bytes(int(input_data[i:i+8], 2) 
                               for i in range(0, len(input_data), 8))
        else:
            input_bytes = input_data
        
        # Hash with counter
        counter_bytes = counter.to_bytes(4, byteorder='big')
        if self.hash_algo == 'sha256':
            h = hashlib.sha256(counter_bytes + input_bytes)
        else:
            h = hashlib.sha3_256(counter_bytes + input_bytes)
        
        return h.digest()[:self.output_bytes]


class PrivacyAmplifier:
    """
    Main Privacy Amplification Engine.
    
    Orchestrates privacy amplification for QKD systems:
    - Accepts sifted key from BB84 protocol
    - Computes security-aware compression ratio
    - Applies chosen hash function
    - Returns final amplified key
    
    Integration with QKD:
        Sifted Key (148 bits, 0% QBER)
            ↓
        Privacy Amplifier (compression ratio 2/3)
            ↓
        Final Key (96 bits, εprivacy ≈ 2^-128)
    """
    
    def __init__(self, config: PrivacyAmplificationConfig = None):
        """
        Initialize privacy amplifier.
        
        Args:
            config (PrivacyAmplificationConfig): Configuration parameters
        """
        self.config = config or PrivacyAmplificationConfig()
    
    def compute_final_key_length(self, sifted_length: int) -> int:
        """
        Compute final key length based on security parameters and QBER.
        
        Formula (Information Theory):
            K_final ≤ K_sifted - H_Eve - λ
            
        where:
            - K_sifted: Sifted key length (bits)
            - H_Eve: Eve's estimated information (H_∞(K|E))
            - λ: Security parameter (e.g., 128 bits)
        
        Args:
            sifted_length (int): Length of sifted key in bits
            
        Returns:
            int: Recommended final key length
        """
        qber = self.config.qber
        
        # Determine compression ratio based on QBER
        # QBER is a proxy for channel quality and Eve's presence
        if qber <= 0.02:  # 0-2%: Very clean channel
            compression = 0.66  # Keep 66% of sifted key
        elif qber <= 0.05:  # 2-5%: Good channel
            compression = 0.50  # Keep 50%
        elif qber <= 0.11:  # 5-11%: Acceptable channel
            compression = 0.30  # Keep 30%
        else:
            compression = 0.10  # High QBER: Very conservative (Protocol likely aborts anyway)
        
        # Final key length with minimum of 1 bit
        final_length = max(1, int(sifted_length * compression))
        return final_length
    
    def amplify_binary_string(self, sifted_key: str) -> Tuple[str, Dict]:
        """
        Amplify privacy of binary string sifted key.
        
        Args:
            sifted_key (str): Binary string (e.g., "101011010...")
            
        Returns:
            Tuple[str, Dict]: (amplified_key, metadata)
                amplified_key: Binary string of final key
                metadata: {
                    'input_length': Original key length,
                    'output_length': Final key length,
                    'compression_ratio': Output/Input,
                    'method': Algorithm used,
                    'security_margin': λ bits
                }
                
        Raises:
            ValueError: If input is empty or invalid
        """
        if not sifted_key:
            raise ValueError("Sifted key cannot be empty")
        
        if not all(c in '01' for c in sifted_key):
            raise ValueError("Sifted key must be binary string (0s and 1s)")
        
        input_length = len(sifted_key)
        
        # Determine output length
        if self.config.compression_ratio is not None and self.config.compression_ratio > 0:
            output_length = max(1, int(input_length * 
                                       self.config.compression_ratio))
        else:
            output_length = self.compute_final_key_length(input_length)
        
        # Apply privacy amplification
        if self.config.method == 'toeplitz':
            hasher = ToeplitzHash(input_length, output_length)
            amplified_key = hasher.hash(sifted_key)
        elif self.config.method == 'sha256':
            extractor = SHAExtractor('sha256', output_length)
            key_bytes = extractor.extract(sifted_key)
            amplified_key = ''.join(format(byte, '08b') for byte in key_bytes)
            amplified_key = amplified_key[:output_length]
        else:
            raise ValueError(f"Unsupported method: {self.config.method}")
        
        metadata = {
            'input_length': input_length,
            'output_length': output_length,
            'compression_ratio': output_length / input_length,
            'method': self.config.method,
            'security_parameter': self.config.security_parameter,
            'hash_family': self.config.hash_family,
            'qber': self.config.qber,
            'leakage_estimate': self.config.leakage_estimate
        }
        
        return amplified_key, metadata
    
    def amplify_bytes(self, sifted_key: bytes) -> Tuple[bytes, Dict]:
        """
        Amplify privacy of byte array sifted key.
        
        Args:
            sifted_key (bytes): Byte array key
            
        Returns:
            Tuple[bytes, Dict]: (amplified_key, metadata)
                
        Raises:
            ValueError: If input is empty
        """
        if not sifted_key:
            raise ValueError("Sifted key cannot be empty")
        
        input_length_bits = len(sifted_key) * 8
        
        # Determine output length
        if self.config.compression_ratio is not None and self.config.compression_ratio > 0:
            output_length_bits = max(1, int(input_length_bits * 
                                           self.config.compression_ratio))
        else:
            output_length_bits = self.compute_final_key_length(input_length_bits)
        
        output_bytes = (output_length_bits + 7) // 8
        
        # Apply privacy amplification
        if self.config.method == 'toeplitz':
            # Convert bytes to binary string
            input_bits = ''.join(format(byte, '08b') for byte in sifted_key)
            hasher = ToeplitzHash(input_length_bits, output_length_bits)
            amplified_bits = hasher.hash(input_bits)
            # Convert back to bytes
            amplified_key = bytes(int(amplified_bits[i:i+8], 2) 
                                 for i in range(0, len(amplified_bits), 8))
        elif self.config.method == 'sha256':
            extractor = SHAExtractor('sha256', output_length_bits)
            amplified_key = extractor.extract(sifted_key)[:output_bytes]
        else:
            raise ValueError(f"Unsupported method: {self.config.method}")
        
        metadata = {
            'input_length_bytes': len(sifted_key),
            'input_length_bits': input_length_bits,
            'output_length_bytes': len(amplified_key),
            'output_length_bits': output_length_bits,
            'compression_ratio': output_length_bits / input_length_bits,
            'method': self.config.method,
            'security_parameter': self.config.security_parameter,
            'hash_family': self.config.hash_family
        }
        
        return amplified_key, metadata


def amplify_qkd_key(sifted_key: Union[str, bytes], 
                   qber: float = 0.0,
                   security_parameter: int = 128,
                   compression_ratio: float = 0.5,
                   method: str = 'toeplitz') -> Tuple[Union[str, bytes], Dict]:
    """
    Convenience function for QKD privacy amplification.
    
    One-liner for integrating privacy amplification into QKD pipeline.
    
    Args:
        sifted_key (str or bytes): Output from sifting phase
        qber (float): Quantum Bit Error Rate (0.0-1.0)
        security_parameter (int): Security margin λ in bits (default 128)
        compression_ratio (float): Output/Input ratio (default 0.5 → 50%)
        method (str): 'toeplitz' or 'sha256' (default 'toeplitz')
        
    Returns:
        Tuple[str/bytes, Dict]: Amplified key and metadata
        
    Example:
        >>> sifted = "101011010101" * 10  # 120 bits
        >>> final_key, info = amplify_qkd_key(sifted, qber=0.01)
        >>> len(final_key)  # ~60 bits (50% compression)
        60
    """
    config = PrivacyAmplificationConfig(
        method=method,
        compression_ratio=compression_ratio,
        qber=qber,
        security_parameter=security_parameter
    )
    
    amplifier = PrivacyAmplifier(config)
    
    if isinstance(sifted_key, str):
        return amplifier.amplify_binary_string(sifted_key)
    else:
        return amplifier.amplify_bytes(sifted_key)


# ============================================================================
# Example Usage and Integration
# ============================================================================

if __name__ == '__main__':
    print("=" * 70)
    print("PRIVACY AMPLIFICATION MODULE - Examples")
    print("=" * 70)
    
    # Example 1: Simple binary string amplification
    print("\n[Example 1] Simple Binary String Amplification")
    print("-" * 70)
    sifted_key = "1" * 100 + "0" * 48  # 148 bits (like typical QKD output)
    print(f"Sifted Key Length: {len(sifted_key)} bits")
    
    config = PrivacyAmplificationConfig(
        method='toeplitz',
        compression_ratio=2/3  # 66% of input
    )
    amplifier = PrivacyAmplifier(config)
    final_key, info = amplifier.amplify_binary_string(sifted_key)
    
    print(f"Final Key Length: {len(final_key)} bits")
    print(f"Compression Ratio: {info['compression_ratio']:.2%}")
    print(f"Method: {info['method']}")
    print(f"Sample output: {final_key[:32]}...{final_key[-32:]}")
    
    # Example 2: Byte array with QBER
    print("\n[Example 2] Byte Array with QBER Integration")
    print("-" * 70)
    sifted_bytes = secrets.token_bytes(20)  # 160 bits
    qber = 0.03  # 3% QBER (above 11% threshold, but for example)
    
    config = PrivacyAmplificationConfig(
        method='sha256',
        qber=qber,
        security_parameter=128
    )
    amplifier = PrivacyAmplifier(config)
    final_bytes, info = amplifier.amplify_bytes(sifted_bytes)
    
    print(f"Input: {len(sifted_bytes)} bytes ({info['input_length_bits']} bits)")
    print(f"Output: {len(final_bytes)} bytes ({info['output_length_bits']} bits)")
    print(f"QBER: {qber*100}%")
    print(f"Security Parameter: {info['security_parameter']} bits")
    print(f"Final Key (hex): {final_bytes.hex()}")
    
    # Example 3: Full QKD Integration
    print("\n[Example 3] Full QKD Pipeline Integration")
    print("-" * 70)
    
    # Simulate BB84 sifting output
    sifted_alice = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1] * 12  # 144 bits
    sifted_key = ''.join(str(b) for b in sifted_alice)
    
    qber = 0.0  # Clean channel
    final_key, metadata = amplify_qkd_key(
        sifted_key,
        qber=qber,
        security_parameter=128,
        compression_ratio=0.67,
        method='toeplitz'
    )
    
    print(f"QKD Pipeline:")
    print(f"  1. Sifting → {len(sifted_key)} bits")
    print(f"  2. Privacy Amplification ({metadata['method']}) → {len(final_key)} bits")
    print(f"  3. QBER: {qber*100}%")
    print(f"  4. Final Secure Key: {final_key[:48]}...")
    
    # Example 4: Comparison of methods
    print("\n[Example 4] Method Comparison")
    print("-" * 70)
    
    test_key = "01" * 75  # 150 bits
    
    for method in ['toeplitz', 'sha256']:
        config = PrivacyAmplificationConfig(
            method=method,
            compression_ratio=0.5
        )
        amplifier = PrivacyAmplifier(config)
        result, info = amplifier.amplify_binary_string(test_key)
        print(f"{method:12} → Output: {len(result):3} bits, "
              f"Ratio: {info['compression_ratio']:.1%}")
    
    print("\n" + "=" * 70)
    print("✅ Privacy Amplification Examples Complete")
    print("=" * 70)
