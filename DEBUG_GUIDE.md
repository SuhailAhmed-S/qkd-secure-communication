# Debugging: "No response from Alice server (timeout after 40s)"

## Quick Diagnosis

Run this command to check if all servers are running:

```bash
python diagnose.py
```

This will show you which servers are online and which are missing.

---

## Step-by-Step Debugging

### Step 1: Check All Servers Are Running

Open 4 terminals and verify each shows the correct message:

**Terminal 1 - Eve**:
```bash
python eve_server_improved.py
```
Should show: `Listening on port 5002...`

**Terminal 2 - Bob**:
```bash
python bob_server_improved.py
```
Should show: `Listening on port 5003...`

**Terminal 3 - Alice**:
```bash
python alice_server_improved.py
```
Should show: `Listening on port 5004...`

**Terminal 4 - Flask**:
```bash
python app.py
```
Should show: `Running on http://0.0.0.0:8000`

### Step 2: Check Console Output

When you click "Run Protocol", watch the **Alice terminal** for these messages:

**Good Output** (should see all of these):
```
[ALICE] Received config: {'num_qubits': 100, ...}
[ALICE] Preparing 100 qubits...
[ALICE] Sending qubits to Eve...
[ALICE] ✓ Successfully sent qubits to Eve
[ALICE] Listening on port 5005 for Bob's response...
[ALICE] Received connection from ('127.0.0.1', XXXXX)
[ALICE] ✓ Successfully received Bob's data
[ALICE] QBER: 0.00% (0 errors / 50 bits)
[ALICE] ✓ Channel is SECURE (QBER < 11.0%)
[ALICE] Sending results to Flask...
[ALICE] Sending 5000+ bytes to Flask...
[ALICE] ✓ Successfully sent results to Flask
[ALICE] Protocol complete
```

**Bad Output** (if you see an error):
```
[ALICE ERROR] Failed to connect to Eve: [Errno 10061] No connection could be made...
```

### Step 3: Identify Where It Breaks

Look for the first error message in Alice terminal:

| Error | Cause | Fix |
|-------|-------|-----|
| `Failed to connect to Eve` | Eve server not running | Start Eve server |
| `Timeout waiting for Bob's response` | Bob or Eve not responding | Check Bob and Eve terminals |
| `Failed to receive Bob's data` | Connection issue with Eve | Restart Eve server |
| `Failed to send results to Flask` | Flask listener not ready | Check Flask terminal |

### Step 4: Check Eve Terminal

When Alice sends qubits, Eve should show:
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

If Eve shows an error, that's where the problem is.

### Step 5: Check Bob Terminal

When Eve sends qubits, Bob should show:
```
[BOB] Received 100 qubits
[BOB] Measuring qubits in random bases...
[BOB] Sending 100 measurement bases to Eve...
[BOB] ✓ Successfully sent response to Eve
[BOB] Measurement complete
```

If Bob shows an error, that's where the problem is.

### Step 6: Check Flask Terminal

Flask should show:
```
[SYSTEM] Starting result listener thread...
[SYSTEM] Starting result listener on port 9999 (timeout: 40s)...
[SYSTEM] Result listener ready, waiting for Alice...
[SYSTEM] Checking server connectivity...
[SYSTEM] ALICE server is online
[SYSTEM] EVE server is online
[SYSTEM] BOB server is online
[SYSTEM] Starting QKD protocol with 100 qubits
[SYSTEM] Sending data to alice on port 5004 (attempt 1/3)
[SYSTEM] Successfully sent data to alice
[SYSTEM] Waiting for Alice to complete protocol...
[SYSTEM] Connection from ('127.0.0.1', XXXXX) for result
[SYSTEM] Received 5000+ bytes of result data
[SYSTEM] Result parsed successfully
[SYSTEM] QKD Protocol completed: SECURE — Communication Successful
```

---

## Common Issues & Solutions

### Issue 1: "Connection refused" in Alice terminal

**Error**:
```
[ALICE ERROR] Failed to connect to Eve: [Errno 10061] No connection could be made...
```

**Cause**: Eve server not running

**Solution**:
1. Check Eve terminal - is it showing "Listening on port 5002..."?
2. If not, start Eve: `python eve_server_improved.py`
3. Wait 2 seconds
4. Try again

---

### Issue 2: "Timeout waiting for Bob's response" in Alice terminal

**Error**:
```
[ALICE ERROR] Timeout waiting for Bob's response
```

**Cause**: Bob or Eve not responding

**Solution**:
1. Check Bob terminal - is it showing "Listening on port 5003..."?
2. Check Eve terminal - did it receive Alice's qubits?
3. If Eve shows error, restart Eve server
4. If Bob shows error, restart Bob server
5. Try again

---

### Issue 3: "Failed to send results to Flask" in Alice terminal

**Error**:
```
[ALICE ERROR] Failed to send results to Flask: [Errno 10061] No connection could be made...
```

**Cause**: Flask result listener not ready

**Solution**:
1. Check Flask terminal - is it showing "Result listener ready..."?
2. If not, restart Flask: `python app.py`
3. Wait 2 seconds
4. Try again

---

### Issue 4: Flask shows "No response from Alice server (timeout after 40s)"

**Cause**: Alice never connected back to Flask

**Solution**:
1. Check Alice terminal for errors (see Step 2)
2. If Alice shows "✓ Successfully sent results to Flask", but Flask still times out:
   - This is a threading issue
   - Restart Flask: `python app.py`
   - Try again

---

### Issue 5: All servers running but still timeout

**Cause**: Possible port binding issue or firewall

**Solution**:
1. Kill all servers (Ctrl+C in each terminal)
2. Wait 10 seconds
3. Start servers again in order: Eve → Bob → Alice → Flask
4. Try again

---

## Advanced Debugging

### Check Port Binding

```bash
# Windows
netstat -ano | findstr :5002
netstat -ano | findstr :5003
netstat -ano | findstr :5004
netstat -ano | findstr :8000
netstat -ano | findstr :9999
```

All should show `LISTENING`

### Kill Process Using Port

```bash
# Windows - find PID using port 5002
netstat -ano | findstr :5002

# Kill process with that PID
taskkill /PID <PID> /F
```

### Test Standalone Mode

If distributed mode keeps failing, test standalone:

```bash
python qkd_main.py
```

This should work immediately without any servers.

---

## Checklist Before Running

- [ ] Terminal 1: Eve server running (`Listening on port 5002...`)
- [ ] Terminal 2: Bob server running (`Listening on port 5003...`)
- [ ] Terminal 3: Alice server running (`Listening on port 5004...`)
- [ ] Terminal 4: Flask app running (`Running on http://0.0.0.0:8000`)
- [ ] Browser: Navigate to http://localhost:8000
- [ ] Web UI: Shows "All servers online"
- [ ] Console: No error messages in any terminal
- [ ] Run Protocol: Click button and watch terminals for errors

---

## If All Else Fails

1. **Restart everything**:
   - Kill all 4 servers (Ctrl+C)
   - Wait 30 seconds
   - Start fresh: Eve → Bob → Alice → Flask

2. **Use standalone mode**:
   ```bash
   python qkd_main.py
   ```

3. **Check Python version**:
   ```bash
   python --version
   ```
   Should be 3.8 or higher

4. **Reinstall dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Check for port conflicts**:
   ```bash
   python diagnose.py
   ```

---

## Getting Help

When reporting issues, include:
1. Output from `python diagnose.py`
2. Console output from all 4 terminals
3. Error messages (copy-paste exactly)
4. Python version (`python --version`)
5. OS (Windows/Mac/Linux)

---

**Last Updated**: 2024
**Status**: Debugging guide complete ✅
