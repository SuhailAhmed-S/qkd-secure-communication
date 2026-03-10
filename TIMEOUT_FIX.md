# Troubleshooting: "No response from Alice server (timeout)" Error

## Root Cause
Flask is waiting for Alice to send results back on port 9999, but Alice never connects. This happens when the communication chain breaks between Alice → Eve → Bob.

---

## ✅ SOLUTION: Proper Server Startup Order

### Step 1: Open 4 Terminal Windows

**Terminal 1 - Eve Server**
```bash
python eve_server_improved.py
```
Wait for: `Listening on port 5002...`

**Terminal 2 - Bob Server**
```bash
python bob_server_improved.py
```
Wait for: `Listening on port 5003...`

**Terminal 3 - Alice Server**
```bash
python alice_server_improved.py
```
Wait for: `Listening on port 5004...`

**Terminal 4 - Flask Web App**
```bash
python app.py
```
Wait for: `Running on http://0.0.0.0:8000`

### Step 2: Verify All Servers Are Running
Check that you see these messages in each terminal:
- Eve: `Listening on port 5002...`
- Bob: `Listening on port 5003...`
- Alice: `Listening on port 5004...`
- Flask: `Running on http://0.0.0.0:8000`

### Step 3: Open Browser
Go to: **http://localhost:8000**

### Step 4: Run Protocol
1. Set "Number of Qubits" to 100
2. Enter a message (or use default)
3. Toggle "Enable Eve" if desired
4. Click "Run Protocol"

---

## 🔍 What Should Happen

### Expected Console Output

**Alice Terminal** (should show):
```
[ALICE] Received config: {'num_qubits': 100, 'message': 'Hello QKD!', 'eve_enabled': False}
[ALICE] Preparing 100 qubits...
[ALICE] Sending qubits to Eve...
[ALICE] ✓ Successfully sent qubits to Eve
[ALICE] Listening on port 5005 for Bob's response...
[ALICE] Received connection from ('127.0.0.1', XXXXX)
[ALICE] ✓ Successfully received Bob's data
[ALICE] QBER: 0.00% (0 errors / 50 bits)
[ALICE] ✓ Channel is SECURE (QBER < 11.0%)
[ALICE] Sending results to Flask...
[ALICE] Protocol complete
```

**Eve Terminal** (should show):
```
[EVE] Received 100 qubits from Alice
[EVE] Intercepting qubits...
[EVE] Forwarding to Bob...
[EVE] Listening on port 5004 for Bob's response...
[EVE] Received connection from ('127.0.0.1', XXXXX)
[EVE] ✓ Successfully received Bob's data
[EVE] Forwarding Bob's data to Alice...
[EVE] ✓ Successfully forwarded Bob's data to Alice
[EVE] Transaction complete
```

**Bob Terminal** (should show):
```
[BOB] Received 100 qubits
[BOB] Measuring qubits in random bases...
[BOB] Sending 100 measurement bases to Eve...
[BOB] ✓ Successfully sent response to Eve
[BOB] Measurement complete
```

**Flask Terminal** (should show):
```
[SYSTEM] Checking server connectivity...
[SYSTEM] ALICE server is online
[SYSTEM] EVE server is online
[SYSTEM] BOB server is online
[SYSTEM] Starting QKD protocol with 100 qubits
[SYSTEM] Sending data to alice on port 5004 (attempt 1/3)
[SYSTEM] Successfully sent data to alice
[SYSTEM] Waiting for result from Alice on port 9999 (timeout: 30s)...
[SYSTEM] Listening for Alice result...
[SYSTEM] Connection from ('127.0.0.1', XXXXX) for result
[SYSTEM] Received 5000+ bytes of result data
[SYSTEM] Result parsed successfully
[SYSTEM] QKD Protocol completed: SECURE — Communication Successful
```

---

## ❌ Common Issues & Fixes

### Issue 1: "Connection refused" when Alice tries to connect to Eve
**Cause**: Eve server not running
**Fix**: Start Eve server first (Terminal 1)

### Issue 2: "Timeout waiting for Bob's response" in Alice terminal
**Cause**: Bob or Eve server not running
**Fix**: Start both Bob and Eve servers before Alice

### Issue 3: "Failed to forward to Alice" in Eve terminal
**Cause**: Alice not listening on port 5005
**Fix**: Make sure Alice server is running and listening

### Issue 4: "Port already in use" error
**Cause**: Previous server instance still running
**Fix**: 
```bash
# Windows - find and kill process
netstat -ano | findstr :5002
taskkill /PID <PID> /F

# Or wait 30 seconds and try again
```

### Issue 5: Flask shows "One or more servers are offline"
**Cause**: One or more servers not running
**Fix**: Check all 3 servers are running and listening

---

## 🧪 Testing the Connection Chain

### Test 1: Check Eve is listening
```bash
netstat -ano | findstr :5002
```
Should show: `LISTENING`

### Test 2: Check Bob is listening
```bash
netstat -ano | findstr :5003
```
Should show: `LISTENING`

### Test 3: Check Alice is listening
```bash
netstat -ano | findstr :5004
```
Should show: `LISTENING`

### Test 4: Check Flask is listening
```bash
netstat -ano | findstr :8000
```
Should show: `LISTENING`

---

## 🔧 Manual Testing (Without Web UI)

### Test Standalone Mode (No servers needed)
```bash
python qkd_main.py
```

This runs the complete protocol in one process and should work immediately.

---

## 📋 Startup Checklist

- [ ] Terminal 1: Eve server running (`Listening on port 5002...`)
- [ ] Terminal 2: Bob server running (`Listening on port 5003...`)
- [ ] Terminal 3: Alice server running (`Listening on port 5004...`)
- [ ] Terminal 4: Flask app running (`Running on http://0.0.0.0:8000`)
- [ ] Browser: Navigate to http://localhost:8000
- [ ] Web UI: Shows "All servers online"
- [ ] Run Protocol: Click button and wait for results

---

## 🚀 Quick Fix Script

If you keep getting timeout errors, use this batch file (Windows):

**start_all.bat**
```batch
@echo off
echo Starting QKD System...
echo.

echo Starting Eve Server...
start "Eve Server" cmd /k python eve_server_improved.py

timeout /t 2

echo Starting Bob Server...
start "Bob Server" cmd /k python bob_server_improved.py

timeout /t 2

echo Starting Alice Server...
start "Alice Server" cmd /k python alice_server_improved.py

timeout /t 2

echo Starting Flask App...
start "Flask App" cmd /k python app.py

timeout /t 3

echo.
echo All servers started! Opening browser...
start http://localhost:8000

echo Done!
```

Save as `start_all.bat` in the project directory and run it.

---

## 📞 Still Having Issues?

1. **Check server console output** - Look for error messages
2. **Verify all 4 servers are running** - Use `netstat` to check ports
3. **Try standalone mode first** - `python qkd_main.py`
4. **Check firewall** - Make sure localhost ports aren't blocked
5. **Restart all servers** - Kill all processes and start fresh

---

## ✅ Verification

After fixing, you should see:
- ✓ All 4 servers running
- ✓ Web UI shows "All servers online"
- ✓ Protocol runs without timeout
- ✓ Results display with QBER and encryption

---

**Last Updated**: 2024
**Status**: All fixes applied ✅
