#!/usr/bin/env python3
"""
Diagnostic script to test QKD server communication chain
"""

import socket
import json
import time
import sys

def test_port(host, port, name):
    """Test if a port is listening"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2.0)
            result = s.connect_ex((host, port))
            if result == 0:
                print(f"✓ {name:20} ({host}:{port:5}) - LISTENING")
                return True
            else:
                print(f"✗ {name:20} ({host}:{port:5}) - NOT LISTENING")
                return False
    except Exception as e:
        print(f"✗ {name:20} ({host}:{port:5}) - ERROR: {str(e)}")
        return False

def main():
    print("=" * 70)
    print("  QKD SERVER DIAGNOSTIC TOOL")
    print("=" * 70)
    print()
    
    print("Checking server ports...")
    print("-" * 70)
    
    servers = [
        ('localhost', 5002, 'Eve Server'),
        ('localhost', 5003, 'Bob Server'),
        ('localhost', 5004, 'Alice Server'),
        ('localhost', 8000, 'Flask Web App'),
        ('localhost', 9999, 'Flask Result Listener'),
    ]
    
    results = {}
    for host, port, name in servers:
        results[name] = test_port(host, port, name)
    
    print()
    print("=" * 70)
    print("  DIAGNOSTIC SUMMARY")
    print("=" * 70)
    
    all_online = all(results.values())
    
    if all_online:
        print("✓ All servers are online and listening!")
        print()
        print("Next steps:")
        print("1. Open http://localhost:8000 in your browser")
        print("2. Click 'Run Protocol'")
        print("3. Check the message feed for errors")
    else:
        print("✗ Some servers are not running:")
        print()
        for name, status in results.items():
            if not status:
                print(f"  - {name} is NOT running")
        print()
        print("Start the missing servers:")
        if not results['Eve Server']:
            print("  Terminal 1: python eve_server_improved.py")
        if not results['Bob Server']:
            print("  Terminal 2: python bob_server_improved.py")
        if not results['Alice Server']:
            print("  Terminal 3: python alice_server_improved.py")
        if not results['Flask Web App']:
            print("  Terminal 4: python app.py")
    
    print()
    print("=" * 70)
    
    # Return exit code based on status
    return 0 if all_online else 1

if __name__ == '__main__':
    sys.exit(main())
