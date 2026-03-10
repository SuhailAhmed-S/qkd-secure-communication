# 🚀 QUICK REFERENCE CARD

## One-Command Start (in 4 Terminals)

### Terminal 1 - Alice Server
```bash
python alice_server_improved.py
```

### Terminal 2 - Eve Server  
```bash
python eve_server_improved.py
```

### Terminal 3 - Bob Server
```bash
python bob_server_improved.py
```

### Terminal 4 - Flask Web App
```bash
python app.py
```

### Browser - Open Web Interface
```
http://localhost:8000
```

---

## What Happens When You Click "Run QKD Simulation"

```
1. Web sends config → Alice (port 5004)
2. Alice prepares 100 qubits
3. Alice sends qubits → Eve (port 5002)
4. Eve forwards → Bob (port 5003)
5. Bob measures in random bases
6. Bob sends bases → Eve → Alice (port 5005)
7. Alice calculates QBER and encrypts
8. Alice sends results → Flask (port 9999)
9. Web displays results + message feed
```

**Total Time**: ~2 seconds

---

## Test Scenarios

### Test 1: Secure Communication
- Eve: **OFF**
- Qubits: 100
- Expected: ✅ QBER ~0%, Status: SECURE

### Test 2: Eavesdropping Detection
- Eve: **ON**
- Qubits: 100
- Expected: ❌ QBER ~25%, Status: COMPROMISED

### Test 3: Larger Key
- Eve: **OFF**
- Qubits: 500
- Expected: ✅ ~250-bit sifted key

---

## What You See in Real-Time

### Right Panel - Server Status
```
Alice: 🟢 Online
Eve:   🟢 Online  
Bob:   🟢 Online
```

### Right Panel - Message Feed
```
[14:23:45] ALICE: Preparing 100 qubits...
[14:23:46] ALICE: Sending qubits to Eve...
[14:23:46] EVE: Received 100 qubits
[14:23:46] EVE: Forwarding to Bob...
[14:23:46] BOB: Measuring qubits...
[14:23:47] ALICE: Sifted key: 47 bits
[14:23:47] ALICE: QBER: 0.00%
[14:23:47] ALICE: ✓ SECURE
```

### Center Panel - Results
```
📊 Metrics
  100 Qubits Transmitted
  47 Sifted Key Length
  0.00% QBER
  0 Bit Errors

✅ Status: SECURE
  Communication Successful

🔐 Encryption
  Key: 3ad4e44a4306fb62b2df0ab7069c67b9
  Encrypted: 6eb1973e...
  Decrypted: Hello, Quantum World! ✓
```

---

## Network Ports

| Server | Port | Listen/Connect |
|--------|------|----------------|
| Alice | 5004 | Listen (Flask) |
| Alice | 5005 | Connect (from Eve) |
| Eve | 5002 | Listen (Alice) |
| Eve | 5004 | Connect (to Bob) |
| Eve | 5005 | Listen (Bob response) |
| Bob | 5003 | Listen (Eve) |
| Bob | 5004 | Connect (to Eve) |
| Flask | 8000 | Listen (browser) |
| Flask | 9999 | Listen (Alice results) |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Server offline" | Check all 4 terminals are running |
| Simulation timeout | Reduce qubits to 50 |
| Connection refused | Check ports 5002-5005, 8000, 9999 free |
| No message feed | Refresh browser, click Clear |
| QBER always high | Normal with high noise; try with 100 qubits |

---

## Key Results

### No Eve
```
QBER: 0-2%
Status: ✅ SECURE
Encryption: ON
```

### With Eve  
```
QBER: 24-26%
Status: ❌ COMPROMISED
Encryption: OFF
```

---

## Documentation Map

```
NEED HELP?
    ↓
    ├─ "How do I start?" → QUICKSTART.md
    ├─ "What works?" → IMPLEMENTATION_SUMMARY.md
    ├─ "How does it work?" → DISTRIBUTED_SETUP.md
    ├─ "Where's the code?" → FILE_INVENTORY.md
    └─ "Everything else?" → README.md
```

---

## Key Commands

```bash
# Start servers
python alice_server_improved.py
python bob_server_improved.py
python eve_server_improved.py

# Start web app
python app.py

# Check if running (in another terminal)
netstat -an | grep 500
```

---

## Expected Flow Visualization

```
┌─ User Browser ─────────────────────┐
│ Configure: 100 qubits, "Hello"    │
│ Eve: OFF                          │
│ Click: Run                        │
└────────────┬──────────────────────┘
             │ Config
             ▼
    ┌────────────────┐
    │ Alice Server   │
    │ :5004          │
    ├────────────────┤
    │ • Prepare bits │
    │ • Send to Eve  │
    │ • Get response │
    │ • Calc QBER    │
    │ • Encrypt      │
    │ • Send results │
    └────┬────┬──────┘
         │    │
    Config│   │Results
         │    │ (port 9999)
   Qubits│    │
    (5002)    │
         │    ▼
         ├──→┌──────────────┐
         │   │ Eve Server   │
         │   │ :5002        │
         │   ├──────────────┤
         │   │ • Get qubits │
         │   │ • Forward    │
         │   │ • Get resp.  │
         │   │ • Send back  │
         │   └──┬───────────┘
         │      │
         │      │ (port 5003)
         │      │
         │      ▼
         │   ┌──────────────┐
         │   │ Bob Server   │
         │   │ :5003        │
         │   ├──────────────┤
         │   │ • Get qubits │
         │   │ • Measure    │
         │   │ • Send bases │
         │   └──────────────┘
         │
         ▼
    ┌──────────────────┐
    │ Web Interface    │
    │ :8000            │
    ├──────────────────┤
    │ • Show results   │
    │ • Live messages  │
    │ • Status lights  │
    │ • Metrics        │
    └──────────────────┘
```

---

## File Reference

### To Run Distributed System
```
❌ qkd_main.py  (local simulation)
✅ alice_server_improved.py
✅ bob_server_improved.py
✅ eve_server_improved.py
✅ app.py
```

### Core Logic (Don't Modify)
```
alice.py → alice_prepare()
bob.py → bob_measure()
eve.py → eve_intercept()
security.py → calculate_qber()
```

### Web Templates
```
templates/home.html
templates/simulator.html ← MAIN (has 3-column layout)
templates/documentation.html
```

---

## Performance Expectations

| Qubits | Time | Sifted Key | QBER (no Eve) |
|--------|------|------------|---------------|
| 50 | ~1s | 20-25 bits | ~0% |
| 100 | ~1s | 40-50 bits | ~0% |
| 200 | ~2s | 80-100 bits | ~0% |
| 500 | ~3s | 200-250 bits | ~0% |
| 1000 | ~4s | 400-500 bits | ~0% |

---

## Success Checklist

- [ ] All 4 terminals running (no errors)
- [ ] Browser shows http://localhost:8000
- [ ] Server status shows 3 green dots
- [ ] Can click "Run QKD Simulation"
- [ ] Results display correctly
- [ ] Message feed updates
- [ ] Eve OFF = SECURE, Eve ON = COMPROMISED

---

## Quick Facts

- **Protocol**: BB84 Quantum Key Distribution
- **Security**: Information-theoretic (physics-based)
- **Eavesdropping**: Detectable via QBER > 11%
- **Qubits**: Photon polarization (simulated)
- **Network**: TCP/IP sockets over localhost
- **Web**: Flask with real-time updates
- **Purpose**: Educational quantum cryptography

---

## Next Steps After Setup

1. **Observe**: Watch protocol work without Eve
2. **Enable Eve**: See how eavesdropping is detected
3. **Change Qubits**: See impact on sifted key size
4. **Read Docs**: Understand quantum mechanics
5. **Experiment**: Test different scenarios

---

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║  You have a complete distributed QKD system running!     ║
║                                                           ║
║  Alice, Bob, and Eve are separate server processes.     ║
║  Web interface monitors everything in real-time.        ║
║  Message feed shows exactly what's happening.           ║
║                                                           ║
║  Ready to explore quantum cryptography! 🚀⚛🔐          ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

---

**Last Updated**: March 5, 2026  
**Status**: ✅ Complete and Ready
