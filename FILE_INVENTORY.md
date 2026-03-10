# 📑 Project File Structure & Complete Inventory

## 🎯 Project: QKD BB84 Distributed Quantum Key Distribution

---

## 📂 Directory Structure

```
qkd-secure-communication/
│
├── 📄 Core Protocol Files
│   ├── alice.py                      - Alice's qubit preparation logic
│   ├── bob.py                        - Bob's measurement logic
│   ├── eve.py                        - Eve's interception logic
│   ├── quantum_channel.py            - Quantum transmission simulation
│   ├── security.py                   - QBER calculation & key derivation
│   └── qkd_main.py                   - Main orchestration logic
│
├── 🖥️  Distributed Server Files (New!)
│   ├── alice_server.py               - Original Alice server (basic)
│   ├── alice_server_improved.py      - ✨ IMPROVED Alice server (with web interface)
│   ├── bob_server.py                 - Original Bob server (basic)
│   ├── bob_server_improved.py        - ✨ IMPROVED Bob server (with web interface)
│   ├── eve_server.py                 - Original Eve server (basic)
│   └── eve_server_improved.py        - ✨ IMPROVED Eve server (with web interface)
│
├── 🌐 Web Application Files
│   ├── app.py                        - ✨ Flask web application (UPDATED)
│   │   └─ Features:
│   │      - Server connectivity checks
│   │      - Real-time message logging
│   │      - API endpoints for distributed communication
│   │      - Live server status monitoring
│   │
│   └── templates/
│       ├── home.html                 - Home page (overview & features)
│       ├── simulator.html            - ✨ Interactive simulator (ENHANCED)
│       │   └─ Features:
│       │      - 3-column layout (controls, results, messages)
│       │      - Real-time server status display
│       │      - Live message feed
│       │      - Protocol flow visualization
│       │      - Qubit analysis table
│       │
│       └── documentation.html        - Comprehensive protocol guide
│
├── 📖 Documentation Files (New!)
│   ├── QUICKSTART.md                 - ✨ Copy-paste quick start guide
│   ├── DISTRIBUTED_SETUP.md          - ✨ Complete distributed architecture guide
│   ├── IMPLEMENTATION_SUMMARY.md      - ✨ Implementation overview & features
│   ├── README.md                      - Full project documentation
│   ├── SUMMARY.md                     - Project summary
│   └── PROJECT_OVERVIEW.md            - Project overview
│
├── 🧪 Test & Configuration Files
│   ├── test_qkd.py                   - Unit tests for QKD protocol
│   ├── test_flask.py                 - Simple Flask test server
│   ├── config.py                      - Configuration constants
│   ├── setup.py                       - Setup/installation script
│   │
│   └── index.html                    - Static HTML (if needed)
│
└── 🎨 Static Files
    └── Root-level HTML
        ├── index.html                - Root index file
```

---

## 🆕 New/Modified Files for Distributed System

### ✨ Server Implementations (Best for Web)

| File | Purpose | Port | Status |
|------|---------|------|--------|
| `alice_server_improved.py` | Alice with web integration | 5004 | ✨ NEW |
| `bob_server_improved.py` | Bob with web integration | 5003 | ✨ NEW |
| `eve_server_improved.py` | Eve with web integration | 5002 | ✨ NEW |

### 🔧 Updated Web Components

| File | Changes | Status |
|------|---------|--------|
| `app.py` | Added server status, message logging, result handling | ✨ UPDATED |
| `templates/simulator.html` | Added 3-column layout, message feed, server status | ✨ UPDATED |

### 📚 New Documentation

| File | Contents | Status |
|------|----------|--------|
| `QUICKSTART.md` | Copy-paste setup instructions | ✨ NEW |
| `DISTRIBUTED_SETUP.md` | Complete architecture & advanced setup | ✨ NEW |
| `IMPLEMENTATION_SUMMARY.md` | What was built & how to use it | ✨ NEW |

---

## 📋 File Descriptions

### Core Protocol (Do Not Modify)

#### `alice.py`
- Function: `alice_prepare(num_qubits)`
- Returns: dict with bits, bases, states
- Used by: All Alice implementations

#### `bob.py`
- Function: `bob_measure(alice_bases, num_qubits)`
- Returns: dict with measured bits and bases
- Used by: All Bob implementations

#### `eve.py`
- Function: `eve_intercept(alice_bits, alice_bases)`
- Returns: dict with intercepted data
- Used by: All Eve implementations

#### `security.py`
- `calculate_qber(alice_bits, bob_bits)` - Computes error rate
- `derive_key(sifted_bits)` - SHA-256 key generation
- `xor_encrypt(message, key_hex)` - Message encryption

#### `quantum_channel.py`
- Simulates quantum transmission
- Handles photon loss simulation
- Used by: Protocol orchestration

#### `qkd_main.py`
- `run_qkd(num_qubits, message, eve_enabled)` - Complete protocol
- Returns: Full result dict with all metrics
- Used by: Local simulation mode

---

### Distributed Servers

#### `alice_server_improved.py` ✨ RECOMMENDED

**What it does:**
1. Listens on port 5004 for configuration
2. Prepares quantum bits
3. Sends to Eve
4. Receives Bob's measurements from Eve
5. Calculates QBER and derives key
6. Sends encrypted message and results to Flask

**How to run:**
```bash
python alice_server_improved.py
```

**Output example:**
```
======================================================================
  ALICE SERVER — Quantum Key Distribution Transmitter
======================================================================
Listening on port 5004...

[ALICE] Preparing 100 qubits...
[ALICE] Sending qubits to Eve...
[ALICE] Received Bob's 100 measurement bases
[ALICE] Sifted key length: 47 bits
[ALICE] QBER: 0.00%
[ALICE] ✓ Channel is SECURE
```

#### `eve_server_improved.py` ✨ RECOMMENDED

**What it does:**
1. Receives qubits from Alice (port 5002)
2. Optionally intercepts/measures them
3. Forwards to Bob (port 5003)
4. Receives Bob's response (port 5004)
5. Forwards back to Alice (port 5005)

**How to run:**
```bash
python eve_server_improved.py
```

#### `bob_server_improved.py` ✨ RECOMMENDED

**What it does:**
1. Listens for qubits on port 5003
2. Measures in random bases
3. Sends measurement data back to Eve (port 5004)

**How to run:**
```bash
python bob_server_improved.py
```

---

### Web Application

#### `app.py` ✨ UPDATED

**New Features:**
- `check_server_status(server_name)` - Checks if Alice/Bob/Eve online
- `add_message(sender, message, type)` - Logs communication
- `send_to_server(server_name, data)` - Sends config to Alice
- `wait_for_result(timeout)` - Waits for results from Alice
- `/api/server_status` - Returns status of all servers
- `/api/messages` - Returns message log
- `/api/clear_messages` - Clears message log

**API Endpoints:**
- `GET /` - Home page
- `GET /simulator` - Simulator page
- `GET /documentation` - Documentation page
- `POST /api/run_qkd` - Execute protocol
- `GET /api/server_status` - Server status
- `GET /api/messages` - Message log
- `POST /api/clear_messages` - Clear messages

---

### Templates

#### `templates/simulator.html` ✨ UPDATED

**New Layout:**
```
┌──────────────┬──────────────────┬──────────────┐
│  Controls    │     Results      │   Messages   │
├──────────────┼──────────────────┼──────────────┤
│ Qubits       │ Protocol Flow    │ Server Status│
│ Message      │ Metrics          │ Message Feed │
│ Eve Toggle   │ Encryption       │ (Real-time)  │
│ Run Button   │ Qubit Table      │              │
└──────────────┴──────────────────┴──────────────┘
```

**New Features:**
- Real-time server status (3 colored dots)
- Live message feed (auto-scrolling)
- Server connectivity checks
- Clear messages button

#### `templates/home.html`

Home page with protocol overview, features, navigation

#### `templates/documentation.html`

Comprehensive documentation on BB84, quantum mechanics, security analysis

---

### Documentation

#### `QUICKSTART.md` ✨ NEW

**Contents:**
- Copy-paste setup instructions
- 4-terminal quick start
- Example output
- Test scenarios
- Troubleshooting checklist

**Best for:** Getting started immediately

#### `DISTRIBUTED_SETUP.md` ✨ NEW

**Contents:**
- Architecture diagram
- Detailed protocol flow (with/without Eve)
- Network configuration (local & remote)
- Performance metrics
- Advanced features
- Complete troubleshooting guide

**Best for:** Understanding the system deeply

#### `IMPLEMENTATION_SUMMARY.md` ✨ NEW

**Contents:**
- What was built
- Getting started guide
- Protocol flow explanation
- Real-time features
- Test scenarios
- Performance data
- Educational outcomes

**Best for:** Learning what the system does

#### `README.md`

Full project documentation with all details

---

## 🔌 Port Usage Summary

```
Alice Server:    5004 (listen), 5005 (connect)
Eve Server:      5002 (listen), 5004 (connect), 5005 (listen)
Bob Server:      5003 (listen), 5004 (connect)
Flask Web:       8000 (listen)
Flask Results:   9999 (listen) - receives from Alice
```

---

## 🎯 File Dependencies

### For Distributed Simulation
```
flask_app (app.py)
    ↓
alice_server_improved.py
    ├─ alice.py
    ├─ security.py
    ├─ quantum_channel.py
    └─ eve_server_improved.py
        ├─ eve.py
        └─ bob_server_improved.py
            └─ bob.py
```

### For Web Interface
```
http://localhost:8000
    ↓
app.py
    ├─ templates/home.html
    ├─ templates/simulator.html
    └─ templates/documentation.html
```

---

## 📊 Statistics

| Category | Count |
|----------|-------|
| Python Files | 16 |
| New Server Implementations | 3 |
| Updated Files | 2 |
| HTML Templates | 4 |
| Documentation Files | 4 |
| API Endpoints | 6 |
| Configuration Ports | 5 |

---

## ✅ Checklist for Using the System

### Setup
- [ ] Clone/download repository
- [ ] Install Python 3.8+
- [ ] Install Flask: `pip install flask`
- [ ] All files present in directory

### Running Distributed System
- [ ] Terminal 1: `python alice_server_improved.py`
- [ ] Terminal 2: `python eve_server_improved.py`
- [ ] Terminal 3: `python bob_server_improved.py`
- [ ] Terminal 4: `python app.py`
- [ ] Browser: Open `http://localhost:8000`

### Testing
- [ ] Server status shows all 3 online (green dots)
- [ ] Can run simulation (click button)
- [ ] Results display correctly
- [ ] Message feed updates
- [ ] Enable Eve shows high QBER

---

## 🚀 Getting Started

1. **Read**: QUICKSTART.md (5 min)
2. **Setup**: Follow 4-terminal setup (2 min)
3. **Run**: Click "Run QKD Simulation" (2 sec)
4. **Observe**: Watch protocol flow & message feed
5. **Learn**: Read IMPLEMENTATION_SUMMARY.md (15 min)

---

## 📞 Need Help?

- **Quick start?** → Read QUICKSTART.md
- **Architecture details?** → Read DISTRIBUTED_SETUP.md
- **What's new?** → Read IMPLEMENTATION_SUMMARY.md
- **Full docs?** → Read README.md
- **Troubleshooting?** → DISTRIBUTED_SETUP.md > Troubleshooting section

---

## 🎓 Learning Path

1. **Beginner**: QUICKSTART.md + run simulator
2. **Intermediate**: IMPLEMENTATION_SUMMARY.md + read code
3. **Advanced**: DISTRIBUTED_SETUP.md + modify servers
4. **Expert**: Read all .py files + experiment

---

**System Status**: ✅ Complete and Ready to Use

Last Updated: March 5, 2026
