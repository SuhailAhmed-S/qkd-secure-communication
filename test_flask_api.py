#!/usr/bin/env python3
"""Test the actual Flask API endpoint to verify the fix"""

from app import app
import json

print("\n" + "="*70)
print("  FLASK API ENDPOINT TEST")
print("="*70)

# Create Flask test client
with app.test_client() as client:
    print("\n✓ Testing POST /api/run_qkd endpoint...\n")
    
    # Send a test request
    response = client.post(
        '/api/run_qkd',
        data=json.dumps({
            'num_qubits': 50,
            'message': 'Test Message',
            'eve_enabled': False
        }),
        content_type='application/json'
    )
    
    # Check response status
    print(f"  Status Code: {response.status_code}")
    if response.status_code == 200:
        print("  ✓ Request successful\n")
    else:
        print("  ✗ Request failed\n")
        exit(1)
    
    # Parse response
    data = response.get_json()
    
    # Verify all required fields are present
    print("✓ Verifying response fields:\n")
    
    required_fields = {
        'num_qubits': int,
        'sift_count': int,
        'qber': float,
        'amplified_key_length': int,  # ← NEW FIELD
        'amplified_key': str,          # ← NEW FIELD
        'sift': dict,                  # ← NEW FIELD
        'sift_matches': int,           # ← NEW FIELD
        'sift_key_bits': list,         # ← NEW FIELD
        'secure': bool,
        'message': str,
        'encrypted': str,
        'decrypted': str,
    }
    
    all_present = True
    for field, expected_type in required_fields.items():
        present = field in data
        if present:
            actual = data[field]
            if isinstance(actual, expected_type) or (expected_type == list and isinstance(actual, (list, type(None)))):
                print(f"  ✓ {field:25} = {str(actual)[:50] if isinstance(actual, (str, list)) else actual}")
            else:
                print(f"  ✗ {field:25} (type mismatch: expected {expected_type.__name__})")
                all_present = False
        else:
            print(f"  ✗ {field:25} MISSING")
            all_present = False
    
    # Verify sift substructure
    print("\n✓ Verifying sift object structure:\n")
    if 'sift' in data and isinstance(data['sift'], dict):
        sift_fields = ['alice_qubits', 'alice_bases', 'bob_bases', 'bob_measurements', 'alice_sifted']
        for field in sift_fields:
            if field in data['sift']:
                count = len(data['sift'][field])
                print(f"  ✓ sift.{field:25} = {count} items")
            else:
                print(f"  ✗ sift.{field:25} MISSING")
                all_present = False
    
    # Summary
    print("\n" + "="*70)
    if all_present:
        print("  ✅ ALL FIELDS PRESENT - SIMULATOR WILL DISPLAY CORRECTLY")
        print("="*70)
        print("\n  Measurements table: " + ("✓ Will display" if data.get('sift', {}).get('alice_qubits') else "✗ No data"))
        print("  Amplified key:     " + ("✓ Will display" if data.get('amplified_key_length', 0) > 0 else "✗ No data"))
        print("\n")
    else:
        print("  ✗ SOME FIELDS MISSING")
        print("="*70)
        exit(1)
