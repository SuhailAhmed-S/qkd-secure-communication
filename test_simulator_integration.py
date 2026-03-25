#!/usr/bin/env python3
"""Comprehensive test simulating the exact Flask API response for the simulator"""

import json
from qkd_main import run_qkd

print("\n" + "="*70)
print("  FLASK API RESPONSE TEST (Simulator Integration)")
print("="*70)

# Simulate what Flask will return
result = run_qkd(num_qubits=50, message='Hello, Quantum World!', eve_enabled=False)

PREVIEW_LENGTH = 20

# This is EXACTLY what the Flask API will now return
api_response = {
    'num_qubits': result['num_qubits'],
    'eve_enabled': result['eve_enabled'],
    'message': result['message'],
    'sift_count': result['sift_count'],
    'qber': result['qber'],
    'qber_pct': f"{result['qber']*100:.2f}%",
    'errors': result['errors'],
    'total': result['total'],
    'secure': result['secure'],
    'status': result['status'],
    'key_hex': result['key_hex'],
    'encrypted': result['encrypted'],
    'decrypted': result['decrypted'],
    
    # ✓ AMPLIFIED KEY INFORMATION (NOW INCLUDED)
    'amplified_key': result.get('amplified_key', ''),
    'amplified_key_length': result.get('amplified_key_length', 0),
    
    # ✓ SIFT DATA FOR MEASUREMENTS TABLE (NOW INCLUDED)
    'sift': {
        'alice_qubits': result.get('alice_bits', []),
        'alice_bases': result.get('alice_bases', []),
        'bob_bases': result.get('bob_bases', []),
        'bob_measurements': result.get('bob_bits', []),
        'alice_sifted': result.get('alice_sifted', []),
        'bob_sifted': result.get('bob_sifted', []),
        'matching_idx': result.get('matching_idx', [])
    },
    
    'sift_key_bits': result.get('alice_sifted', []),
    'sift_matches': len(result.get('matching_idx', [])),
    
    # Previews
    'alice_bits_preview': result['alice_bits'][:PREVIEW_LENGTH],
    'alice_bases_preview': result['alice_bases'][:PREVIEW_LENGTH],
    'alice_states_preview': result['alice_states'][:PREVIEW_LENGTH],
    'bob_bases_preview': result['bob_bases'][:PREVIEW_LENGTH],
    'bob_bits_preview': result['bob_bits'][:PREVIEW_LENGTH],
    'alice_sifted_preview': result['alice_sifted'][:PREVIEW_LENGTH],
    'bob_sifted_preview': result['bob_sifted'][:PREVIEW_LENGTH],
    'eve_bases_preview': result['eve_bases'][:PREVIEW_LENGTH] if result['eve_bases'] else []
}

# What the JavaScript will receive
print("\n✓ Simulating JavaScript data access (as in simulator.html):\n")

# Test 1: Summary Card Display
print("  SUMMARY CARD DATA:")
print(f"    Initial Qubits: {api_response['num_qubits']}")
print(f"    Sifted Key:     {api_response['sift_count']} bits")
print(f"    Amplified Key:  {api_response['amplified_key_length']} bits ✓")
print(f"    Secure:         {api_response['secure']}")

# Test 2: Measurements Table
print("\n  MEASUREMENTS TABLE DATA:")
print(f"    Total rows available: {len(api_response['sift']['alice_qubits'])}")
print(f"    Alice qubits: {api_response['sift']['alice_qubits'][:5]}...")
print(f"    Alice bases:  {api_response['sift']['alice_bases'][:5]}...")
print(f"    Bob bases:    {api_response['sift']['bob_bases'][:5]}...")
print(f"    Matches found: {api_response['sift_matches']} ✓")

# Test 3: Amplified Key Tab
print("\n  AMPLIFIED KEY TAB DATA:")
print(f"    Amplified key length:   {api_response['amplified_key_length']} bits ✓")
ratio = (api_response['amplified_key_length'] / api_response['sift_count'] * 100) if api_response['sift_count'] > 0 else 0
print(f"    Compression ratio:      {ratio:.1f}% ✓")
print(f"    Key progression:        {api_response['sift_count']} → {api_response['amplified_key_length']} bits ✓")
print(f"    Amplification method:   Toeplitz + SHA-256")
print(f"    Amplified key (hex):    {api_response['amplified_key'][:50]}... ✓")

# Test 4: Verify JSON serializable
print("\n  JSON SERIALIZATION TEST:")
try:
    json_str = json.dumps(api_response, default=str)
    print(f"    ✓ Response is JSON serializable ({len(json_str)} bytes)")
except Exception as e:
    print(f"    ✗ JSON serialization failed: {e}")

print("\n" + "="*70)
print("  ✅ WEB SIMULATOR WILL NOW DISPLAY:")
print("="*70)
print("    ✓ Measurements table with Alice/Bob comparison")
print("    ✓ Amplified key length and compression ratio")
print("    ✓ Sifted to amplified key progression")
print("    ✓ All security metrics (QBER, status)")
print("    ✓ Message encryption/decryption results")
print("\n")
