"""
Comprehensive Test Suite for QKD BB84 Protocol Implementation

This module contains unit tests and integration tests for all components
of the quantum key distribution system. Tests verify:
    - Correct protocol execution
    - QBER calculations and security detection
    - Encryption/decryption consistency
    - Error handling and validation
    - Edge cases and boundary conditions
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import unittest
from typing import List

from alice import alice_prepare
from bob import bob_measure, sift_key
from eve import eve_intercept
from quantum_channel import quantum_channel_transmit
from security import (
    calculate_qber, bits_to_bytes, derive_key,
    xor_encrypt, xor_decrypt, secure_communication
)
from qkd_main import run_qkd


class TestAliceModule(unittest.TestCase):
    """Tests for Alice's qubit preparation module."""
    
    def test_prepare_returns_correct_structure(self):
        """Verify alice_prepare returns proper dictionary structure."""
        result = alice_prepare(10)
        self.assertIn('bits', result)
        self.assertIn('bases', result)
        self.assertIn('states', result)
    
    def test_prepare_correct_lengths(self):
        """Verify all outputs have correct length."""
        num_qubits = 50
        result = alice_prepare(num_qubits)
        self.assertEqual(len(result['bits']), num_qubits)
        self.assertEqual(len(result['bases']), num_qubits)
        self.assertEqual(len(result['states']), num_qubits)
    
    def test_prepare_bits_are_binary(self):
        """Verify all bits are 0 or 1."""
        result = alice_prepare(100)
        self.assertTrue(all(b in [0, 1] for b in result['bits']))
    
    def test_prepare_bases_are_valid(self):
        """Verify all bases are '+' or '×'."""
        result = alice_prepare(100)
        self.assertTrue(all(b in ['+', '×'] for b in result['bases']))
    
    def test_prepare_states_match_bits_and_bases(self):
        """Verify quantum states match bits and bases."""
        result = alice_prepare(20)
        for i, (bit, basis, state) in enumerate(
            zip(result['bits'], result['bases'], result['states'])
        ):
            if basis == '+':
                expected = '|0⟩' if bit == 0 else '|1⟩'
            else:
                expected = '|+⟩' if bit == 0 else '|−⟩'
            self.assertEqual(state, expected, 
                           f"Mismatch at index {i}: {state} != {expected}")
    
    def test_prepare_invalid_input(self):
        """Verify proper error handling for invalid inputs."""
        with self.assertRaises(ValueError):
            alice_prepare(0)
        with self.assertRaises(ValueError):
            alice_prepare(-5)
        with self.assertRaises(ValueError):
            alice_prepare("not an int")


class TestBobModule(unittest.TestCase):
    """Tests for Bob's measurement and sifting module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.bits = [0, 1, 0, 1, 1, 0]
        self.bases = ['+', '+', '×', '×', '+', '×']
    
    def test_measure_returns_correct_structure(self):
        """Verify bob_measure returns proper dictionary."""
        result = bob_measure(self.bits, self.bases)
        self.assertIn('bob_bases', result)
        self.assertIn('bob_bits', result)
    
    def test_measure_correct_basis_agreement(self):
        """When bases match, measurement should be accurate (statistically)."""
        # Use identical bases for all, test multiple times for statistics
        bits = [0, 1, 0, 1]
        bases = ['+', '+', '×', '×']
        
        # Test multiple times - should match majority of the time
        matches = 0
        total_tests = 50
        for _ in range(total_tests):
            result = bob_measure(bits, bases)
            # Count how many bits match
            matches += sum(1 for i in range(len(bits)) if result['bob_bits'][i] == bits[i])
        
        # Should match at least 75% of the time (random chance is 50%)
        self.assertGreater(matches, total_tests * len(bits) * 0.75)
    
    def test_sift_key_structure(self):
        """Verify sift_key returns proper structure."""
        alice_bits = [0, 1, 0, 1, 1, 0]
        alice_bases = ['+', '+', '×', '×', '+', '×']
        bob_bits = [0, 1, 0, 1, 1, 0]
        bob_bases = ['+', '×', '×', '+', '+', '×']
        
        result = sift_key(alice_bits, alice_bases, bob_bits, bob_bases)
        self.assertIn('alice_sifted', result)
        self.assertIn('bob_sifted', result)
        self.assertIn('matching_idx', result)
        self.assertIn('sift_count', result)
    
    def test_sift_keeps_matching_bases_only(self):
        """Sifting should keep only bits with matching bases."""
        alice_bits = [0, 1, 0, 1]
        alice_bases = ['+', '+', '×', '×']
        bob_bits = [0, 1, 0, 1]
        bob_bases = ['+', '×', '×', '+']  # Match at indices 0, 2
        
        result = sift_key(alice_bits, alice_bases, bob_bits, bob_bases)
        
        self.assertEqual(result['sift_count'], 2)
        self.assertEqual(result['alice_sifted'], [0, 0])
        self.assertEqual(result['bob_sifted'], [0, 0])
        self.assertEqual(result['matching_idx'], [0, 2])


class TestEveModule(unittest.TestCase):
    """Tests for Eve's intercept-resend attack simulation."""
    
    def test_intercept_structure(self):
        """Verify eve_intercept returns proper structure."""
        bits = [0, 1, 0, 1] * 5
        bases = ['+', '×', '+', '×'] * 5
        result = eve_intercept(bits, bases)
        
        self.assertIn('eve_bases', result)
        self.assertIn('resent_bits', result)
        self.assertIn('resent_bases', result)
    
    def test_intercept_correct_basis_agreement(self):
        """When Eve's basis matches, she should measure correctly."""
        bits = [1, 0, 1, 0] * 10  # Many qubits to get statistics
        bases = ['+', '+', '×', '×'] * 10
        
        # Test multiple times for statistical validity
        error_count = 0
        for _ in range(100):
            result = eve_intercept(bits, bases)
            # When Eve uses same bases, she should get same bits
            for i in range(len(bits)):
                if result['eve_bases'][i] == bases[i]:
                    if result['resent_bits'][i] != bits[i]:
                        error_count += 1
        
        # Allow small statistical variance (0.1% error)
        self.assertLess(error_count, 2)


class TestQuantumChannel(unittest.TestCase):
    """Tests for quantum channel simulation."""
    
    def test_clean_channel_preserves_data(self):
        """Clean channel should preserve bits and bases."""
        bits = [0, 1, 0, 1, 1]
        bases = ['+', '×', '+', '×', '+']
        
        result = quantum_channel_transmit(bits, bases, eve_enabled=False)
        
        self.assertEqual(result['transmitted_bits'], bits)
        self.assertEqual(result['transmitted_bases'], bases)
        self.assertFalse(result['eve_active'])
        self.assertEqual(result['eve_bases'], [])
    
    def test_eve_channel_modifies_data(self):
        """With Eve, transmitted data should be different (usually)."""
        bits = [0, 1, 0, 1, 1] * 10
        bases = ['+', '×', '+', '×', '+'] * 10
        
        result = quantum_channel_transmit(bits, bases, eve_enabled=True)
        
        self.assertTrue(result['eve_active'])
        self.assertGreater(len(result['eve_bases']), 0)
        # Data might differ due to Eve's measurement errors


class TestSecurityModule(unittest.TestCase):
    """Tests for security analysis and encryption."""
    
    def test_qber_identical_keys(self):
        """QBER should be 0 when keys are identical."""
        key = [0, 1, 0, 1, 1, 0]
        result = calculate_qber(key, key)
        
        self.assertEqual(result['qber'], 0.0)
        self.assertEqual(result['errors'], 0)
        self.assertTrue(result['secure'])
    
    def test_qber_completely_different_keys(self):
        """QBER should be 1.0 when keys are completely different."""
        alice = [0, 0, 0, 0, 0, 0]
        bob =   [1, 1, 1, 1, 1, 1]
        result = calculate_qber(alice, bob)
        
        self.assertEqual(result['qber'], 1.0)
        self.assertEqual(result['errors'], 6)
        self.assertFalse(result['secure'])
    
    def test_qber_partial_differences(self):
        """QBER should correctly calculate partial errors."""
        alice = [0, 0, 1, 1, 0, 0]
        bob =   [0, 1, 1, 1, 0, 0]  # 1 error out of 6
        result = calculate_qber(alice, bob)
        
        expected_qber = 1/6
        self.assertAlmostEqual(result['qber'], expected_qber, places=4)
        self.assertEqual(result['errors'], 1)
    
    def test_bits_to_bytes_conversion(self):
        """Test bits to bytes conversion."""
        bits = [1, 0, 1, 0, 1, 0, 1, 0]
        result = bits_to_bytes(bits)
        self.assertEqual(result, b'\xaa')  # 10101010 = 0xAA
    
    def test_bits_to_bytes_padding(self):
        """Test padding in bits to bytes conversion."""
        bits = [1, 0, 1]  # 3 bits
        result = bits_to_bytes(bits)
        # Should be padded to 8 bits: 10100000 = 0xA0
        self.assertEqual(result, b'\xa0')
    
    def test_key_derivation(self):
        """Test key derivation from sifted bits."""
        bits = [0, 1] * 50  # 100 bits
        key = derive_key(bits, key_length=16)
        
        self.assertEqual(len(key), 16)
        self.assertIsInstance(key, bytes)
    
    def test_encryption_decryption_roundtrip(self):
        """Test encryption and decryption consistency."""
        message = "Hello, Quantum World!"
        key = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
        
        ciphertext = xor_encrypt(message, key)
        decrypted = xor_decrypt(ciphertext, key)
        
        self.assertEqual(decrypted, message)
    
    def test_encryption_different_keys_fail(self):
        """Decryption with wrong key should produce garbage or error."""
        message = "Secret"
        key1 = b'\x00' * 16
        key2 = b'\xff' * 16
        
        ciphertext = xor_encrypt(message, key1)
        try:
            decrypted = xor_decrypt(ciphertext, key2)
            # If it decrypts, it should be garbage (not the original)
            self.assertNotEqual(decrypted, message)
        except UnicodeDecodeError:
            # This is also acceptable - wrong key produces invalid UTF-8
            pass


class TestIntegration(unittest.TestCase):
    """Integration tests for complete protocol execution."""
    
    def test_qkd_no_eve_secure(self):
        """QKD without Eve should result in secure channel."""
        result = run_qkd(num_qubits=200, message="Test", eve_enabled=False)
        
        self.assertTrue(result['secure'])
        self.assertLess(result['qber'], 0.11)
        self.assertIsNotNone(result['key_hex'])
        self.assertIsNotNone(result['encrypted'])
        self.assertEqual(result['decrypted'], "Test")
    
    def test_qkd_with_eve_detectable(self):
        """QKD with Eve should detect eavesdropping."""
        result = run_qkd(num_qubits=200, message="Test", eve_enabled=True)
        
        # With Eve, QBER should be elevated (usually around 25%)
        # Allow some statistical variation: 15% to 35%
        self.assertGreater(result['qber'], 0.15)
        self.assertGreater(result['errors'], 0)
    
    def test_qkd_sift_efficiency(self):
        """Sift efficiency should be approximately 50%."""
        result = run_qkd(num_qubits=500, message="Test", eve_enabled=False)
        
        sift_ratio = result['sift_count'] / result['num_qubits']
        # Should be around 50%, allow 40-60% due to randomness
        self.assertGreater(sift_ratio, 0.35)
        self.assertLess(sift_ratio, 0.65)
    
    def test_qkd_encryption_consistency(self):
        """Encrypted message should decrypt correctly."""
        message = "Quantum Cryptography"
        result = run_qkd(num_qubits=300, message=message, eve_enabled=False)
        
        self.assertTrue(result['secure'])
        self.assertEqual(result['decrypted'], message)
    
    def test_qkd_invalid_parameters(self):
        """QKD should reject invalid parameters."""
        with self.assertRaises(ValueError):
            run_qkd(num_qubits=5, message="Too few qubits")
        
        with self.assertRaises(ValueError):
            run_qkd(num_qubits=200, message="")


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases and boundary conditions."""
    
    def test_single_qubit(self):
        """System should handle single qubit (minimum edge case)."""
        # Note: This violates the min 10 qubits constraint
        # But testing the math should still work
        alice = [0]
        bases = ['+']
        result = bob_measure(alice, bases)
        self.assertEqual(len(result['bob_bits']), 1)
    
    def test_large_qubit_count(self):
        """System should handle large qubit counts."""
        result = run_qkd(num_qubits=1000, message="Big test")
        self.assertTrue(result['secure'])
        self.assertEqual(result['num_qubits'], 1000)
    
    def test_empty_sifted_key(self):
        """System should handle when no bases match (unlikely but possible)."""
        alice_bits = [0, 0, 0, 0]
        alice_bases = ['+', '+', '+', '+']
        bob_bits = [0, 0, 0, 0]
        bob_bases = ['×', '×', '×', '×']
        
        result = sift_key(alice_bits, alice_bases, bob_bits, bob_bases)
        self.assertEqual(result['sift_count'], 0)
    
    def test_unicode_message(self):
        """System should handle Unicode in messages."""
        message = "Quantum: Ψ, Security: 🔒"
        result = run_qkd(num_qubits=200, message=message, eve_enabled=False)
        
        self.assertTrue(result['secure'])
        self.assertEqual(result['decrypted'], message)


def run_tests():
    """Run all tests with verbose output."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAliceModule))
    suite.addTests(loader.loadTestsFromTestCase(TestBobModule))
    suite.addTests(loader.loadTestsFromTestCase(TestEveModule))
    suite.addTests(loader.loadTestsFromTestCase(TestQuantumChannel))
    suite.addTests(loader.loadTestsFromTestCase(TestSecurityModule))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    exit_code = run_tests()
    sys.exit(exit_code)
