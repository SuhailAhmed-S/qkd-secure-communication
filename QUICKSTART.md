# Quick Start: Distributed QKD System

## 🚀 Setup in 4 Terminal Windows

### Terminal 1: Start Alice (Sender)
```bash
cd c:\Users\rosha\OneDrive\Documents\GitHub\qkd-secure-communication
python alice_server_improved.py
```

### Terminal 2: Start Eve (Eavesdropper)
```bash
cd c:\Users\rosha\OneDrive\Documents\GitHub\qkd-secure-communication
python eve_server_improved.py
```

### Terminal 3: Start Bob (Receiver)
```bash
cd c:\Users\rosha\OneDrive\Documents\GitHub\qkd-secure-communication
python bob_server_improved.py
```

### Terminal 4: Start Flask Web App
```bash
cd c:\Users\rosha\OneDrive\Documents\GitHub\qkd-secure-communication
python app.py
```

## 📱 Open Web Interface

Once all servers are running, open your browser:

**URL**: `http://localhost:8000`

## 🎯 Run Your First Simulation

1. **Check Server Status** (right panel should show all 3 green dots)
2. **Configure Simulation**:
   - Qubits: 100
   - Message: "Hello, Quantum World!"
   - Eve: **Disabled**
3. **Click**: "▶ Run QKD Simulation"
4. **Watch**:
   - Protocol flow animation (Alice → Eve → Bob → Sifting)
   - Live message feed showing all communication
   - Results appear in the center
   - Green status = ✅ SECURE

## 🔴 Test Eavesdropping Detection

1. **Enable Eve**: Toggle the "Eve" switch to **Enabled**
2. **Run Simulation** with same settings
3. **Compare Results**:
   - Without Eve: QBER ~0% ✓
   - With Eve: QBER ~25% ✗

## 📊 Understanding the Display

### Left Panel (Control)
- Qubit count: How many quantum bits to transmit
- Message: Text to encrypt
- Eve Toggle: Enable/disable eavesdropper
- Run Button: Start the protocol

### Center Panel (Results)
- **Protocol Flow**: Shows Alice → Eve → Bob → Sifting progress
- **Metrics**: QBER%, sifted key length, errors
- **Encryption**: Shows encrypted and decrypted message
- **Qubit Table**: Detailed breakdown of each qubit

### Right Panel (Communication)
- **Server Status**: 3 dots showing Alice/Eve/Bob status
- **Message Feed**: Real-time communication log
- Shows what each participant is doing

## 🔑 Key Results to Look For

### Scenario 1: No Eavesdropping
```
Status: ✅ SECURE
QBER: 0.00%
Message encrypted successfully!
```

### Scenario 2: With Eavesdropping
```
Status: 🚨 COMPROMISED
QBER: 25.00%
Channel compromised - no encryption!
```

## 📋 Example Output in Message Feed

```
[14:23:45] SYSTEM: Checking server connectivity...
[14:23:45] SYSTEM: ALICE server is online
[14:23:45] SYSTEM: EVE server is online
[14:23:45] SYSTEM: BOB server is online
[14:23:45] SYSTEM: Starting QKD protocol with 100 qubits
[14:23:45] ALICE: Preparing 100 qubits...
[14:23:45] ALICE: Sending qubits to Eve...
[14:23:46] EVE: Received 100 qubits from Alice
[14:23:46] EVE: Forwarding qubits without interception...
[14:23:46] EVE: Forwarding to Bob...
[14:23:46] BOB: Received 100 qubits
[14:23:46] BOB: Measuring qubits in random bases...
[14:23:46] BOB: Sending 100 measurement bases to Eve...
[14:23:46] ALICE: Received Bob's 100 measurement bases
[14:23:46] ALICE: Performing basis reconciliation (sifting)...
[14:23:46] ALICE: Sifted key length: 47 bits
[14:23:46] ALICE: QBER: 0.00% (0 errors / 47 bits)
[14:23:46] ALICE: ✓ Channel is SECURE
[14:23:46] SYSTEM: QKD Protocol completed: SECURE — Communication Successful
```

## 🐛 Troubleshooting

### "Alice server is offline"
- Check Terminal 1 is running
- Restart Alice server

### "Eve server is offline"
- Check Terminal 2 is running
- Restart Eve server

### "Bob server is offline"
- Check Terminal 3 is running
- Restart Bob server

### No message feed updates
- Check Flask is running (Terminal 4)
- Refresh browser
- Clear messages and try again

### Simulation timeout
- Make sure all 3 servers are running
- Try smaller qubit count (50 instead of 100)
- Check network/system load

## 💡 What's Happening

### Without Eve:
```
Alice sends: [random bits in random bases]
    ↓
Eve forwards: [same bits]
    ↓
Bob receives: [mostly same bits if bases match]
    ↓
QBER = 0% (no errors) → SECURE
```

### With Eve:
```
Alice sends: [random bits in random bases]
    ↓
Eve intercepts: [measures in WRONG bases 50% of time]
    ↓
Eve forwards: [wrong bits when bases don't match]
    ↓
Bob receives: [modified bits]
    ↓
QBER = 25% (many errors) → COMPROMISED!
```

## 🎓 Next Steps

1. **Experiment**: Try different qubit counts (50, 200, 500)
2. **Observe**: See how QBER and sifted key change
3. **Test**: Run multiple simulations back-to-back
4. **Compare**: Switch Eve on/off to see impact
5. **Learn**: Read DISTRIBUTED_SETUP.md for deep dive

## 📚 Files

- `alice_server_improved.py` - Alice server
- `bob_server_improved.py` - Bob server
- `eve_server_improved.py` - Eve server
- `app.py` - Flask web application
- `DISTRIBUTED_SETUP.md` - Complete documentation

---

**Enjoy exploring quantum cryptography!** 🎉⚛🔐
