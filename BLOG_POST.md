# Extending Nmap NSE: Two Custom Audit Scripts for SMTP and FTP

**Author:** Dhanishkanth  
**Roll No / Registration:** 24BCE1348  
**Department:** Computer Science and Engineering, Vellore Institute of Technology (VIT), Chennai  
**Date:** October 2026  
**Tags:** `nmap`, `nse`, `cybersecurity`, `lua`, `networking`  

---

## 1. Introduction

Network reconnaissance is one of the foundational phases of any security assessment. Nmap (Network Mapper) is a standard tool for discovering hosts and open ports. Beyond port scanning, Nmap includes the **Nmap Scripting Engine (NSE)**, which runs scripts written in the Lua programming language.

Nmap ships with over 600 scripts. Many discovery scripts are purely informational: they collect facts but don't judge whether those facts are a risk. For a hands-on cybersecurity assignment in my B.Tech CSE program at VIT Chennai, I wanted to explore the gap between scanning (collecting facts) and auditing (judging them against good security practice).

I extended two existing Nmap scripts with a small evaluation layer:
- **`smtp-risk-check.nse`** (extends `smtp-commands.nse`): flags a mail server that advertises `VRFY` or `EXPN` (possible user enumeration) and warns when `STARTTLS` is not advertised (mail may travel unencrypted).
- **`ftp-anon-plus.nse`** (extends `ftp-anon.nse`): after confirming anonymous FTP access, tags filenames that look sensitive (such as `.env`, `id_rsa`, `backup.zip`, and `passwd`) and prints a summary line.

> [!NOTE]
> **Ethics and authorization:** All scans in this article ran against `127.0.0.1` (my own computer) on test services I set up myself. Never scan systems or networks without the owner's explicit permission.

---

## 2. Background: Scanning vs. Auditing

```
+-----------------------------------+
|      Traditional NSE Scripts      |
|  - Connects to the service        |
|  - Requests capabilities/files    | ===> "Here is what the server returned."
|  - Prints raw output              |
+-----------------------------------+
                  |
                  v
+-----------------------------------+
|     Custom Audit Layer (added)    |
|  - Inspects what came back        |
|  - Compares it to risky patterns  | ===> "[!] User enumeration possible"
|  - Prints actionable notes        |      "[NSE: sensitive] id_rsa"
+-----------------------------------+
```

### SMTP: Why These Features Matter
- **VRFY and EXPN (user enumeration):** `VRFY` asks a mail server whether a mailbox exists. `EXPN` asks it to list the members of a mailing list. Both were designed for debugging, but an attacker can use them to confirm valid usernames without sending any mail, for example to build phishing target lists.
- **Missing STARTTLS (unencrypted mail):** Plain SMTP sends commands, credentials, and message content in cleartext. `STARTTLS` upgrades the connection to TLS. Plain SMTP is like a **postcard** that anyone along the route can read, and `STARTTLS` is the **sealed envelope**. If a server does not advertise `STARTTLS`, a client has no standard way to encrypt the session.

### FTP: Why These Features Matter
- **Anonymous access:** An FTP server that accepts the anonymous user lets anyone browse (and sometimes change) its files without credentials.
- **Sensitive filenames:** Misconfigured anonymous FTP folders often contain backups (`backup.zip`), credentials (`passwd`), private keys (`id_rsa`), configuration files (`config`), and environment secrets (`.env`). The stock `ftp-anon.nse` tags writable files with `[NSE: writeable]`, but it does not flag sensitive-looking names.

---

## 3. Test Lab Setup

I did not use external virtual machines such as Metasploitable2. Everything ran on my own Windows PC and was scanned at `127.0.0.1`, which keeps the lab controlled and reproducible.

### Environment
- **Operating system:** Windows (build 10.0.26200.9550)
- **Scanner:** Nmap 7.99, run from Command Prompt
- **Python:** 3.12.5
- **FTP server:** FileZilla Server 1.12.6
- **SMTP targets:** Two small simulated SMTP servers written in Python (`fakesmtp.py`), not real mail servers

### A. FTP Service (FileZilla Server)
I created an anonymous user mapped to `C:\ftp-test` with Read + Write access, and placed dummy files (each containing the text `"test"`) in the folder:
- `.env`
- `backup.zip`
- `config`
- `id_rsa`
- `passwd`
- `readme.txt` *(control file: should NOT be flagged)*

Two of my Python test scripts (`fakesmtp.py` and `smtpserver.py`) were also saved in this folder, so they appear in the FTP listing below.

### B. SMTP Service (Simulated, Two Modes)
To test both the "risky" case and the "secure" case, I wrote a small server that listens on `127.0.0.1:25` and can run in two modes:
- **`risky`:** advertises `VRFY` and `EXPN`, no `STARTTLS`
- **`secure`:** advertises `STARTTLS`, no `VRFY` or `EXPN`

```python
import socket, sys, threading

# Accept 'risky' or 'secure' as an argument
mode = sys.argv[1] if len(sys.argv) > 1 else "risky"

if mode == "risky":
    EHLO = (b"250-testmail.local Hello\r\n250-SIZE 33554432\r\n"
            b"250-VRFY\r\n250-EXPN\r\n250-8BITMIME\r\n250 HELP\r\n")
else:  # secure mode
    EHLO = (b"250-testmail.local Hello\r\n250-SIZE 33554432\r\n"
            b"250-STARTTLS\r\n250-8BITMIME\r\n250 HELP\r\n")

HELP = b"214 Supported commands: HELO EHLO MAIL RCPT DATA QUIT HELP\r\n"

def handle(conn):
    conn.sendall(b"220 testmail.local ESMTP\r\n")
    buf = b""
    while True:
        data = conn.recv(1024)
        if not data:
            break
        buf += data
        while b"\r\n" in buf:
            line, buf = buf.split(b"\r\n", 1)
            cmd = line.upper().split(b" ")[0]
            if cmd in (b"EHLO", b"HELO"):
                conn.sendall(EHLO)
            elif cmd == b"HELP":
                conn.sendall(HELP)
            elif cmd == b"QUIT":
                conn.sendall(b"221 Bye\r\n")
                conn.close()
                return
            else:
                conn.sendall(b"250 OK\r\n")
    conn.close()

s = socket.socket()
s.bind(("127.0.0.1", 25))
s.listen(5)
print("Fake SMTP server (" + mode + " mode) on 127.0.0.1:25. Ctrl+C to stop.")
while True:
    c, _ = s.accept()
    threading.Thread(target=handle, args=(c,), daemon=True).start()
```

---

## 4. Script 1: `smtp-risk-check.nse`

- **Original script:** `smtp-commands.nse` by Jasey DePriest. It connects to port 25, 465, or 587, sends `EHLO` and `HELP`, cleans up the replies, and prints the supported commands.
- **File I ran:** `smtp-commands-customs.nse`. This article calls it `smtp-risk-check.nse`, so Nmap's output heading shows the file name I actually ran.

### What I Added
I left the original `go()` function (connection, `EHLO`, `HELP`, text cleanup) unchanged. I added a `check_risks()` function and a few lines in `action()` that call it.

```lua
-- Added feature: search the combined EHLO/HELP text for risky findings
local function check_risks(combined_text)
  local findings = {}
  local upper_text = combined_text:upper()

  local risky = {}
  if upper_text:find("VRFY") then
    table.insert(risky, "VRFY")
  end
  if upper_text:find("EXPN") then
    table.insert(risky, "EXPN")
  end
  if #risky > 0 then
    table.insert(findings, "[!] User enumeration possible via " .. table.concat(risky, "/"))
  end

  if not upper_text:find("STARTTLS") then
    table.insert(findings, "[!] STARTTLS not advertised -- mail may be sent/received unencrypted")
  end

  return findings
end
```

In `action()`, after getting the command lists:

```lua
      -- Added: run the risk check on the combined EHLO + HELP text
      local combined = table.concat(final, " ")
      local findings = check_risks(combined)

      for _, f in ipairs(findings) do
        table.insert(final, f)
      end

      return table.concat(final, "\n ")
```

### Test A: Risky Server

In one Command Prompt:
```cmd
python C:\ftp-test\fakesmtp.py risky
```

In a second window:
```cmd
nmap -Pn --script=C:\Users\dhani\smtp-commands-customs.nse -p 25 127.0.0.1
nmap -Pn --script=smtp-commands -p 25 127.0.0.1
```

**Custom script (`smtp-commands-customs`):**
```text
PORT   STATE SERVICE
25/tcp open  smtp
| smtp-commands-customs: testmail.local Hello, SIZE 33554432, VRFY, EXPN, 8BITMIME, HELP
|  Supported commands: HELO EHLO MAIL RCPT DATA QUIT HELP
|  [!] User enumeration possible via VRFY/EXPN
|_ [!] STARTTLS not advertised -- mail may be sent/received unencrypted
```

**Original `smtp-commands`:**
```text
PORT   STATE SERVICE
25/tcp open  smtp
| smtp-commands: testmail.local Hello, SIZE 33554432, VRFY, EXPN, 8BITMIME, HELP
|_ Supported commands: HELO EHLO MAIL RCPT DATA QUIT HELP
```

![SMTP Risky Server Scan Comparison](screenshots/smtp_risky_comparison.png)  
*Figure 1: The custom script prints the command lists plus two `[!]` warning flags, while the original script outputs raw commands only.*

---

### Test B: Secure Server

To show the script evaluates the server instead of always printing warnings, I restarted the simulator in secure mode:

```cmd
python C:\ftp-test\fakesmtp.py secure
nmap -Pn --script=C:\Users\dhani\smtp-commands-customs.nse -p 25 127.0.0.1
```

**Observed Output:**
```text
PORT   STATE SERVICE
25/tcp open  smtp
| smtp-commands-customs: testmail.local Hello, SIZE 33554432, STARTTLS, 8BITMIME, HELP
|_ Supported commands: HELO EHLO MAIL RCPT DATA QUIT HELP
```

No `[!]` lines appeared, because `STARTTLS` was advertised and `VRFY`/`EXPN` were not.

![SMTP Secure Server Scan Output](screenshots/smtp_secure_scan.png)  
*Figure 2: On the secure server, the script prints the command lists with zero warnings.*

---

## 5. Script 2: `ftp-anon-plus.nse`

- **Original script:** `ftp-anon.nse` by Eddie Bell, Rob Nicholls, Ange Gutek, and David Fifield. It tries an anonymous login (anonymous with password `IEUser@`), lists the root directory, and tags writable entries with `[NSE: writeable]`.
- **File I ran:** `ftp-anon-custom.nse`. This article calls it `ftp-anon-plus.nse`.

### What I Added
A list of filename patterns, a function to test a name against them, a check inside the directory loop, and a summary line.

```lua
-- Added feature: Sensitive filename detection
local SENSITIVE_PATTERNS = {
  "^%.env$", "^%.env%.", "^%.htaccess$", "^id_rsa", "^id_dsa",
  "^passwd$", "^shadow$", "^%.ssh$", "^config$", "^backup",
  "^database", "^secret", "^token", "^private", "^pass$", "^pwd$",
}

local function is_sensitive(name)
  local lower = string.lower(name)
  for _, pattern in ipairs(SENSITIVE_PATTERNS) do
    if lower:match(pattern) then
      return true
    end
  end
  return false
end
```

Inside the listing loop:

```lua
for _, item in ipairs(listing) do
  local entry_name = get_entry_name(item)

  -- Existing writeable check
  if string.match(item, "^[d-].......w.") then
    item = item .. " [NSE: writeable]"
  end

  -- Added: sensitive filename check
  if entry_name and is_sensitive(entry_name) then
    item = item .. " [NSE: sensitive]"
    sensitive_files[#sensitive_files + 1] = entry_name
  end

  result[#result + 1] = item
end

-- Added: summary line for sensitive files found
if #sensitive_files > 0 then
  result[#result + 1] = ""
  result[#result + 1] = "Sensitive files detected: " .. table.concat(sensitive_files, ", ")
end
```

### Test: Original vs. Custom

The original `ftp-anon` normally lists files too. To make the comparison easier to see, I switched its listing off with `maxlist=0`:

```cmd
nmap -Pn --script=ftp-anon --script-args ftp-anon.maxlist=0 -p 21 127.0.0.1
nmap -Pn --script=C:\Users\dhani\ftp-anon-custom.nse -p 21 127.0.0.1
```

**Original `ftp-anon` (listing switched off):**
```text
PORT   STATE SERVICE
21/tcp open  ftp
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
```

**My script (`ftp-anon-custom`):**
```text
PORT   STATE SERVICE
21/tcp open  ftp
| ftp-anon-custom: Anonymous FTP login allowed (FTP code 230)
| -rw-rw-rw- 1 ftp ftp               7 Oct 09 15:57 .env [NSE: writeable] [NSE: sensitive]
| -rw-rw-rw- 1 ftp ftp               7 Oct 09 15:57 backup.zip [NSE: writeable] [NSE: sensitive]
| -rw-rw-rw- 1 ftp ftp               7 Oct 09 15:57 config [NSE: writeable] [NSE: sensitive]
| -rw-rw-rw- 1 ftp ftp            1403 Oct 10 13:36 fakesmtp.py [NSE: writeable]
| -rw-rw-rw- 1 ftp ftp               7 Oct 09 15:57 id_rsa [NSE: writeable] [NSE: sensitive]
| -rw-rw-rw- 1 ftp ftp               7 Oct 09 15:57 passwd [NSE: writeable] [NSE: sensitive]
| -rw-rw-rw- 1 ftp ftp               7 Oct 09 15:57 readme.txt [NSE: writeable]
| -rw-rw-rw- 1 ftp ftp             735 Oct 10 11:58 smtpserver.py [NSE: writeable]
| 
|_Sensitive files detected: .env, backup.zip, config, id_rsa, passwd
```

### Observations
1. `.env`, `backup.zip`, `config`, `id_rsa`, and `passwd` were tagged `[NSE: sensitive]`.
2. `readme.txt`, `fakesmtp.py`, and `smtpserver.py` got only the `[NSE: writeable]` tag and no `[NSE: sensitive]` tag, which shows the check matches patterns instead of flagging everything.
3. Every file is tagged writeable because FileZilla reports them as world-writable (`-rw-rw-rw-`), which matches the Read + Write access I gave the test user.
4. The summary line lists all sensitive findings at a glance.

![FTP Scan Comparison with Sensitive Files Flagged](screenshots/ftp_anon_plus_output.png)  
*Figure 3: Original ftp-anon reports only that anonymous login is allowed (when maxlist=0), while custom script lists the files, tags sensitive ones, and appends a summary.*

---

## 6. How to Install and Run on Windows

### Step 1: Save the Scripts
Put them in your user folder, for example:
- `C:\Users\<username>\smtp-risk-check.nse`
- `C:\Users\<username>\ftp-anon-plus.nse`

*(Alternatively, copy them into `C:\Program Files (x86)\Nmap\scripts\` which needs Administrator rights, and run `nmap --script-updatedb`).*

### Step 2: Run from Command Prompt
```cmd
:: SMTP (ports 25, 465, 587)
nmap -Pn --script=%USERPROFILE%\smtp-risk-check.nse -p 25,465,587 127.0.0.1

:: FTP (ports 21, 990)
nmap -Pn --script=%USERPROFILE%\ftp-anon-plus.nse -p 21,990 127.0.0.1
```

> **Why `-Pn`?** It tells Nmap to skip its ping check and scan the ports directly. Without it, Nmap may report "host seems down" for a machine that blocks ping, and skip the scan.

When you run a script by file name, Nmap labels its output with that file name. That is why my output headings read `smtp-commands-customs` and `ftp-anon-custom`.

---

## 7. Troubleshooting: Problems I Hit

1. **"Host seems down" and "filtered" ports:**  
   My first scan targeted my PC's own LAN IP. Nmap reported the host as down, and after adding `-Pn` the ports showed as filtered. No mail or FTP service was running on my PC at that point, and Windows Firewall also blocks inbound connections by default. Setting up test services and scanning `127.0.0.1` with `-Pn` fixed it.

2. **Silent FTP results (the 530 login code):**  
   At first, both the original `ftp-anon` and my script printed nothing under port 21. A manual FTP login with a blank password worked, so I tested the exact login Nmap uses:
   ```cmd
   curl -v --user anonymous:IEUser@ ftp://127.0.0.1/
   ```
   FileZilla answered `530 Login incorrect`. The anonymous account only accepted its own stored password, not the `IEUser@` that Nmap sends. In `ftp-anon.nse`, a 530 reply makes the script return nothing:
   ```lua
   elseif code == 421 or code == 530 then
     -- Don't log known error codes.
   ```
   So a refused login looks the same as "no output". I changed the anonymous user's authentication setting in FileZilla until the same `curl` command returned `230 Login successful`, and then both scripts worked. A silent result does not always mean "no anonymous access".

3. **A non-standard HELP reply and a busy port:**  
   My first SMTP test server (Python's `aiosmtpd`) answered `HELP` with code `250`, while the standard reply is `214`. My Nmap trace showed that reply arriving, but the "Supported commands" line never appeared in the output. The script most likely discards `HELP` replies that don't use code 214, though I did not confirm this in Nmap's source. Later attempts to start a new server also failed with `WinError 10048` ("only one usage of each socket address"), because an old Python process still held port 25. I found it with `netstat -ano`, ended it with `taskkill /PID <pid> /F`, and switched to my own simple server (`fakesmtp.py`) that sends standard replies.

4. **Script file names:**  
   Nmap reported `did not match a category, filename, or directory` when I used a name that didn't exist. I had saved several copies with similar names (for example `ftp-anon-custom.nse` and `ftp-anon-customs.nse`). Running `dir C:\Users\dhani\*.nse*` showed the real names.

5. **Npcap warning:**  
   Every run printed `Could not import all necessary Npcap functions... Resorting to connect() mode`. I did not fix it. These scans use plain TCP connections, and they worked normally in that mode.

---

## 8. Limitations and Future Work

- **VRFY is flagged when advertised, not tested:** The script reports `VRFY` and `EXPN` when the server lists them. Some mail servers list `VRFY` but answer every query with a generic reply, so the warning means "possible", not "confirmed". A deeper script could send a real `VRFY` request and examine the answer.
- **Only the text the server returns is checked:** If a server hides a command or answers `HELP` in a non-standard way, the script can miss it, as I saw with my first test server.
- **Root directory only:** `ftp-anon-plus.nse` inspects only the top-level folder. Sensitive files are often in subfolders such as `/pub/backup/`.
- **Filename matching only:** The script cannot see inside files. A file with an innocent name can still hold secrets, and a file named `config` may hold nothing sensitive.
- **Simulated SMTP servers:** The SMTP results come from small simulated servers, so they show that the detection logic works, not how it behaves against every real mail server.

---

## 9. Ethics and Legal Notice

Scanning systems without permission can be illegal (for example under India's IT Act or the US CFAA). Only scan machines you own or have written authorization to test. Use your own computer, lab virtual machines, or platforms built for practice.

---

## 10. Acknowledgements and Credits

These scripts build on work by the Nmap Project and its contributors:
- **`smtp-commands.nse`:** Jasey DePriest
- **`ftp-anon.nse`:** Eddie Bell, Rob Nicholls, Ange Gutek, and David Fifield

The connection handling and protocol parsing are the original authors' work. My additions are `check_risks()` (SMTP) and `SENSITIVE_PATTERNS`, `is_sensitive()`, and the summary line (FTP).

Source code and test servers:  
👉 **GitHub:** [https://github.com/dhanish0104/nmap-nse-audit-scripts](https://github.com/dhanish0104/nmap-nse-audit-scripts)

---

## 11. Conclusion

Extending Nmap scripts in Lua is an approachable way to learn how network protocols behave at the application layer. With a few dozen lines of pattern matching, two scripts that only report facts now also point out two common misconfigurations. The troubleshooting along the way taught me as much as the scripts did: how Windows firewalls affect scans, how a silent result can hide a failed login, and why testing against both a risky and a secure target matters.
