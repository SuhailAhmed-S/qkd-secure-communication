# QKD BB84 Distributed System Guide

## Overview

The QKD BB84 implementation now supports **distributed communication** where Alice, Bob, and Eve run as separate server processes on different computers/terminals, communicating via TCP sockets. This provides a realistic simulation of quantum key distribution in a networked environment.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Flask Web Interface                      │
│                    (http://localhost:8000)                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
       ┌───────────────┼───────────────┐
       │               │               │
       ↓               ↓               ↓
   ┌────────┐      ┌────────┐      ┌────────┐
   │ Alice  │      │  Eve   │      │  Bob   │
   │Server  │      │Server  │      │Server  │
   │ :5004  │      │ :5002  │      │ :5003  │
   └───┬────┘      └───┬────┘      └───┬────┘
       │                │                │
       └────────────────┴────────────────┘
       (TCP Socket Communication)
```

## Getting Started

### Step 1: Start Alice Server (Terminal 1)

```bash
python alice_server_improved.py
```

Expected output:
```
======================================================================
  ALICE SERVER — Quantum Key Distribution Transmitter
======================================================================
Listening on port 5004...

Waiting for configuration from Flask...
```

### Step 2: Start Eve Server (Terminal 2)

```bash
python eve_server_improved.py
```

Expected output:
```
======================================================================
  EVE SERVER — Quantum Channel Eavesdropper
======================================================================
Listening on port 5002...

Waiting for Alice's qubits...
```

### Step 3: Start Bob Server (Terminal 3)

```bash
python bob_server_improved.py
```

Expected output:
```
======================================================================
  BOB SERVER — Quantum Receiver
======================================================================
Listening on port 5003...

Waiting for qubits...
```

### Step 4: Start Flask Web Application (Terminal 4)

```bash
python app.py
```

Expected output:
```
 * Running on http://127.0.0.1:8000
```

### Step 5: Open Web Browser

Navigate to: **http://localhost:8000**

## Communication Flow

### Normal Sequence (Eve Disabled)

```
1. Web interface sends config to Alice (port 5004)
   └─> Alice prepares 100 qubits

2. Alice → Eve (port 5002)
   └─> Sends quantum bits and bases

3. Eve → Bob (port 5003)
   └─> Forwards qubits to Bob

4. Bob measures in random bases
   └─> Sends measurement bases to Eve (port 5004)

5. Eve → Alice (port 5005)
   └─> Forwards Bob's measurement data

6. Alice performs sifting and QBER calculation
   └─> Sends results back to Flask (port 9999)

7. Web interface displays results with real-time message feed
```

### Eavesdropping Sequence (Eve Enabled)

```
Same as above, but:
- In step 2: Eve INTERCEPTS qubits
  └─> Eve measures in random bases
  └─> Eve re-sends modified qubits
  └─> Alice & Bob detect high QBER (~25%)
```

## Real-Time Message Feed

The web interface shows all communication:

- **ALICE**: "Preparing 100 qubits..."
- **ALICE**: "Sending qubits to Eve..."
- **EVE**: "Received 100 qubits from Alice"
- **EVE**: "Intercepting qubits..."
- **EVE**: "Forwarding to Bob..."
- **BOB**: "Received 100 qubits"
- **BOB**: "Measuring qubits in random bases..."
- **ALICE**: "Sifted key length: 47 bits"
- **ALICE**: "QBER: 0.00% (0 errors / 47 bits)"
- **ALICE**: "✓ Channel is SECURE"

## Server Status Monitoring

The web interface displays real-time server status:

```
┌─────────┬────────┬─────────┐
│ Alice   │  Eve   │   Bob   │
├─────────┼────────┼─────────┤
│ 🟢 Online│🟢Online│🟢Online │
└─────────┴────────┴─────────┘
```

Color indicators:
- 🟢 **Green**: Server is online and responding
- 🔴 **Red**: Server is offline
- 🟡 **Yellow**: Unknown status

## Testing Scenarios

### Scenario 1: Secure Communication (No Eve)

1. Start Alice, Eve, Bob, Flask
2. In web interface:
   - Set Qubits: 200
   - Message: "Secret Data"
   - Eve: **Disabled**
3. Click "Run QKD Simulation"

**Expected Result:**
- ✅ QBER: 0-5%
- ✅ Status: SECURE
- ✅ Message encrypted and decrypted

### Scenario 2: Eavesdropping Detection (Eve Active)

1. Start Alice, Eve, Bob, Flask
2. In web interface:
   - Set Qubits: 200
   - Message: "Secret Data"
   - Eve: **Enabled**
3. Click "Run QKD Simulation"

**Expected Result:**
- ❌ QBER: ~25%
- ❌ Status: COMPROMISED
- ❌ Encryption disabled (key not generated)
- 📊 Message feed shows Eve's interception

### Scenario 3: Bob Offline

1. Start Alice, Eve, Flask (don't start Bob)
2. Try to run simulation

**Expected Result:**
- ⚠️ Error message: "Bob server is offline"
- 🔴 Server status shows Bob as offline

## Network Configuration

### Local Network (Same Computer)

All servers run on `localhost` (127.0.0.1):
- Alice: localhost:5004
- Eve: localhost:5002
- Bob: localhost:5003
- Flask: localhost:8000

### Remote Network (Different Computers)

To run on different computers:

1. Edit `alice_server_improved.py`:
   ```python
   EVE_HOST = '192.168.1.100'  # Eve's computer IP
   BOB_PORT = 5003
   ```

2. Edit `eve_server_improved.py`:
   ```python
   BOB_HOST = '192.168.1.101'   # Bob's computer IP
   ```

3. Edit `bob_server_improved.py`:
   ```python
   EVE_RESPONSE_HOST = '192.168.1.100'  # Eve's computer IP
   ```

4. Update `app.py`:
   ```python
   SERVERS = {
       'alice': {'host': '192.168.1.102', 'port': 5004},
       'eve': {'host': '192.168.1.100', 'port': 5002},
       'bob': {'host': '192.168.1.101', 'port': 5003}
   }
   ```

## Troubleshooting

### "Alice server is offline"

**Problem**: Alice server not responding
**Solutions**:
1. Make sure Alice is running: `python alice_server_improved.py`
2. Check port 5004 is not blocked: `netstat -an | grep 5004`
3. Firewall may be blocking: Allow port 5004

### "Connection refused"

**Problem**: Can't connect to a server
**Solutions**:
1. Verify server is running
2. Check port number matches
3. For remote networks: verify IP address is correct
4. Check firewall rules

### Simulation times out

**Problem**: Protocol takes too long
**Solutions**:
1. Reduce qubit count to 100 or less
2. Check network latency if remote
3. Increase timeout in `app.py`: `wait_for_result(timeout=60)`

### QBER is always high

**Problem**: Even with Eve disabled, QBER > 5%
**Solutions**:
1. Network interference: Increase qubit count
2. Implementation issue: Check server logs
3. Try with exactly 100 qubits first

## Ports Used

| Service | Port | Purpose |
|---------|------|---------|
| Alice   | 5004 | Listen for config from Flask |
| Eve     | 5002 | Receive qubits from Alice |
| Eve     | 5004 | Send to Bob |
| Bob     | 5003 | Receive from Eve |
| Bob     | 5004 | Send response to Eve |
| Alice   | 5005 | Receive from Eve |
| Flask   | 8000 | Web interface |
| Flask   | 9999 | Receive results from Alice |

## Performance Metrics

### With 100 Qubits

| Metric | Value |
|--------|-------|
| Total Time | ~1-2 seconds |
| Sifted Key | ~40-50 bits |
| QBER (no Eve) | 0-2% |
| QBER (Eve) | ~25% |

### With 1000 Qubits

| Metric | Value |
|--------|-------|
| Total Time | ~3-5 seconds |
| Sifted Key | ~400-500 bits |
| QBER (no Eve) | 0-2% |
| QBER (Eve) | ~25% |

## Advanced Features

### Custom Message Encryption

Send any text message through the quantum channel:

```
Message: "Hello from Alice to Bob!"
Encrypted: "6a...9f" (hex)
Decrypted: "Hello from Alice to Bob!" ✓
```

### QBER Threshold Analysis

The protocol uses QBER < 11% as the security threshold:

```
QBER < 5%   → No eavesdropping, noise acceptable
QBER 5-11%  → Borderline, investigate
QBER > 11%  → Likely eavesdropping, abort
```

### Real-Time Monitoring

Watch the quantum protocol in real-time:

1. Open web interface
2. Watch protocol flow visualization
3. See live message feed
4. Monitor server status
5. View final encryption results

## Educational Value

This distributed setup demonstrates:

✓ **Quantum Mechanics**: Photon polarization and measurement
✓ **Cryptography**: BB84 protocol and security analysis
✓ **Networking**: TCP/IP socket programming
✓ **Distributed Systems**: Multi-server coordination
✓ **Real-time Communication**: Live status monitoring
✓ **Eavesdropping Detection**: QBER-based security

---

**Remember**: This is an educational simulation. Real QKD systems require specialized quantum optical hardware and additional security measures!
