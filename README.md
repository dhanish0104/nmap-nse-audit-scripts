# Custom Nmap NSE Security Audit Scripts

> **Coursework Project:** Cybersecurity Lab Assignment  
> **Student:** Dhanishkanth (24BCE1348)  
> **Department:** Computer Science and Engineering, Vellore Institute of Technology (VIT), Chennai  
> **Repository:** https://github.com/dhanish0104/nmap-nse-audit-scripts  

This repository contains two custom Nmap Scripting Engine (NSE) scripts that extend default Nmap scripts by adding an automated security-audit layer.

---

## 📂 Scripts Included

| Script | Based On | Original Authors | Key Features Added |
| :--- | :--- | :--- | :--- |
| [`smtp-risk-check.nse`](./smtp-risk-check.nse) | `smtp-commands.nse` | Jasey DePriest | • Flags user enumeration risk (`VRFY` / `EXPN`)<br>• Flags missing transport encryption (`STARTTLS`) |
| [`ftp-anon-plus.nse`](./ftp-anon-plus.nse) | `ftp-anon.nse` | Eddie Bell, Rob Nicholls, Ange Gutek, David Fifield | • Highlights sensitive filenames (`.env`, `id_rsa`, `backup.zip`, `passwd`, etc.) with `[NSE: sensitive]`<br>• Outputs a summarized findings line |

---

## 🚀 Usage on Windows

### 1. SMTP Security Check
Scan target SMTP service on port 25, 465, or 587:
```cmd
nmap -Pn --script=smtp-risk-check.nse -p 25,465,587 127.0.0.1
```

**Observed Output (Risky Mode):**
```text
PORT   STATE SERVICE
25/tcp open  smtp
| smtp-commands-customs: testmail.local Hello, SIZE 33554432, VRFY, EXPN, 8BITMIME, HELP
|  Supported commands: HELO EHLO MAIL RCPT DATA QUIT HELP
|  [!] User enumeration possible via VRFY/EXPN
|_ [!] STARTTLS not advertised -- mail may be sent/received unencrypted
```

### 2. FTP Anonymous & Sensitive File Audit
Scan target FTP service on port 21 or 990:
```cmd
nmap -Pn --script=ftp-anon-plus.nse -p 21,990 127.0.0.1
```

**Observed Output:**
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

---

## 🛠️ Testing Environment
Simulated testing was performed on `127.0.0.1` (Windows 11) using:
- **FileZilla Server 1.12.6** configured with an anonymous user directory (`C:\ftp-test`).
- A custom dual-mode Python socket server ([`fakesmtp.py`](./fakesmtp.py)) to test both vulnerable (`VRFY`/`EXPN`) and secure (`STARTTLS`) response logic.

---

## ⚖️ Ethics & Legal Disclaimer
These scripts are intended solely for educational purposes and authorized penetration testing. Do not execute scans against systems or networks without explicit permission.

---

## 📜 Acknowledgements
Special thanks to the original authors of `smtp-commands.nse` and `ftp-anon.nse` from the Nmap Project community:
- `smtp-commands.nse`: Jasey DePriest
- `ftp-anon.nse`: Eddie Bell, Rob Nicholls, Ange Gutek, and David Fifield
