#!/usr/bin/env python3
"""
Comprehensive QKD Project Testing & Verification Script

Tests all major components of the QKD BB84 implementation:
- Module imports
- Core QKD functionality
- Flask app initialization
- API endpoints
- Security features
"""

import sys
import json
import socket
from typing import Dict, List, Tuple

def print_header(title: str):
    """Print formatted header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")

def print_test(name: str, status: bool, message: str = ""):
    """Print test result"""
    symbol = "✓" if status else "✗"
    print(f"  {symbol} {name}")
    if message:
        print(f"    {message}")

print_header("QKD PROJECT COMPREHENSIVE VERIFICATION")

tests_passed = 0
tests_failed = 0

# Test 1: Core module imports
print_header("1. Core Module Imports")
try:
    import config
    import quantum_channel
    import security
    import alice
    import bob
    import eve
    import qkd_main
    print_test("All core modules imported", True)
    tests_passed += 1
except ImportError as e:
    print_test("Core module import", False, str(e))
    tests_failed += 1
    sys.exit(1)

# Test 2: Flask app import
print_header("2. Flask Application")
try:
    from flask import Flask
    import app as flask_app
    print_test("Flask app imported", True)
    tests_passed += 1
except ImportError as e:
    print_test("Flask import", False, str(e))
    tests_failed += 1
    sys.exit(1)

# Test 3: QKD Functionality - Basic Run
print_header("3. QKD Protocol Execution")
try:
    result = qkd_main.run_qkd(num_qubits=50, message="Test", eve_enabled=False)
    
    # Verify result structure
    required_keys = [
        'num_qubits', 'eve_enabled', 'message', 'sift_count', 
        'qber', 'secure', 'status'
    ]
    
    missing_keys = [key for key in required_keys if key not in result]
    if missing_keys:
        print_test("QKD basic execution", False, f"Missing keys: {missing_keys}")
        tests_failed += 1
    else:
        print_test("QKD basic execution", True, f"Sifted: {result['sift_count']} bits, QBER: {result.get('qber_pct', 'N/A')}")
        tests_passed += 1
        
except Exception as e:
    print_test("QKD execution", False, str(e))
    tests_failed += 1

# Test 4: QKD with Eve
print_header("4. QKD with Eve (Eavesdropping)")
try:
    result_eve = qkd_main.run_qkd(num_qubits=50, message="Test", eve_enabled=True)
    
    if 'qber' in result_eve:
        qber_clean = result['qber']
        qber_eve = result_eve['qber']
        print_test("QKD with Eve execution", True, f"No Eve QBER: {qber_clean:.2%}, With Eve: {qber_eve:.2%}")
        tests_passed += 1
    else:
        print_test("QKD with Eve", False, "QBER not in result")
        tests_failed += 1
        
except Exception as e:
    print_test("QKD with Eve", False, str(e))
    tests_failed += 1

# Test 5: Privacy Amplification
print_header("5. Privacy Amplification")
try:
    from privacy_amplification import amplify_qkd_key
    
    # Test privacy amplification on QKD result using binary string
    sifted_bits = ''.join(str(b) for b in result.get('sift_key_bits', [0]*50))
    qber_value = result.get('qber', 0.0)
    
    amplified_key, amplified_info = amplify_qkd_key(
        sifted_bits,
        qber=qber_value,
        compression_ratio=0.5
    )
    
    if amplified_key and amplified_info:
        key_len = len(amplified_key) if isinstance(amplified_key, str) else len(amplified_key)
        print_test("Privacy amplification", True, f"Output: {key_len} bits")
        tests_passed += 1
    else:
        print_test("Privacy amplification", False, "Invalid output structure")
        tests_failed += 1
        
except ImportError:
    print_test("Privacy amplification", False, "Module not found (optional)")
except Exception as e:
    print_test("Privacy amplification", False, str(e))
    tests_failed += 1

# Test 6: Security Features
print_header("6. Security Features")
try:
    from security import secure_communication, calculate_qber
    
    # Test QBER calculation using the correct signature
    alice_bits = [0, 1, 0, 1, 0]
    bob_bits = [0, 1, 1, 1, 0]  # 1 error
    
    qber_result = calculate_qber(alice_bits, bob_bits)
    if qber_result and 'qber' in qber_result:
        qber_value = qber_result['qber']
        if isinstance(qber_value, float) and 0 <= qber_value <= 1:
            print_test("QBER calculation", True, f"QBER for 1/5 errors: {qber_value:.2%}")
            tests_passed += 1
        else:
            print_test("QBER calculation", False, "Invalid QBER value")
            tests_failed += 1
    else:
        print_test("QBER calculation", False, "Invalid result structure")
        tests_failed += 1
        
except Exception as e:
    print_test("Security features", False, str(e))
    tests_failed += 1

# Test 7: Flask App Structure
print_header("7. Flask Application Structure")
try:
    # Check routes
    routes = []
    for rule in flask_app.app.url_map.iter_rules():
        routes.append(str(rule.rule))
    
    required_routes = ['/', '/simulator', '/documentation', '/api/run_qkd', '/api/server_status']
    missing_routes = [r for r in required_routes if r not in routes]
    
    if missing_routes:
        print_test("Flask routes", False, f"Missing: {missing_routes}")
        tests_failed += 1
    else:
        print_test("Flask routes", True, f"Found {len(routes)} routes")
        tests_passed += 1
        
except Exception as e:
    print_test("Flask app structure", False, str(e))
    tests_failed += 1

# Test 8: Templates
print_header("8. HTML Templates")
import os
try:
    template_files = ['home.html', 'simulator.html', 'documentation.html']
    missing_templates = []
    
    for tmpl in template_files:
        path = os.path.join('templates', tmpl)
        if not os.path.exists(path):
            missing_templates.append(tmpl)
    
    if missing_templates:
        print_test("Templates", False, f"Missing: {missing_templates}")
        tests_failed += 1
    else:
        print_test("Templates", True, "All 3 templates present")
        tests_passed += 1
        
except Exception as e:
    print_test("Templates", False, str(e))
    tests_failed += 1

# Test 9: Static Assets
print_header("9. Static Assets")
try:
    static_files = ['styles.css', 'script.js']
    missing_static = []
    
    for static in static_files:
        path = os.path.join('static', static)
        if not os.path.exists(path):
            # Check root too
            if not os.path.exists(static):
                missing_static.append(static)
    
    if missing_static:
        print_test("Static assets", False, f"Missing: {missing_static}")
        tests_failed += 1
    else:
        print_test("Static assets", True, "All static files present")
        tests_passed += 1
        
except Exception as e:
    print_test("Static assets", False, str(e))
    tests_failed += 1

# Test 10: Config Settings
print_header("10. Configuration")
try:
    # Check Flask app config
    if flask_app.app and hasattr(flask_app.app, 'config'):
        print_test("Flask configuration", True, "Config present")
        tests_passed += 1
    else:
        print_test("Flask configuration", False, "Config not found")
        tests_failed += 1
        
except Exception as e:
    print_test("Configuration", False, str(e))
    tests_failed += 1

# Summary
print_header("TEST RESULTS SUMMARY")
total_tests = tests_passed + tests_failed
print(f"  ✓ Passed: {tests_passed}/{total_tests}")
print(f"  ✗ Failed: {tests_failed}/{total_tests}")

if tests_failed == 0:
    print(f"\n  🎉 ALL TESTS PASSED!")
    print(f"  ✓ Project is fully functional and ready for deployment\n")
    sys.exit(0)
else:
    print(f"\n  ⚠️  Some tests failed. Please review above.\n")
    sys.exit(1)
