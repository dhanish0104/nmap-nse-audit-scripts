import base64

def get_b64(path):
    with open(path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode()

img1 = get_b64('c:/DA-1BLOG/screenshots/smtp_risky_comparison.png')
img2 = get_b64('c:/DA-1BLOG/screenshots/smtp_secure_scan.png')
img3 = get_b64('c:/DA-1BLOG/screenshots/ftp_anon_plus_output.png')

# Read reference script (original smtp-commands.nse)
with open('C:/Program Files (x86)/Nmap/scripts/smtp-commands.nse', 'r', encoding='utf-8') as f:
    orig_smtp = f.read()

# Read enhanced script 1 (smtp-risk-check.nse)
with open('c:/DA-1BLOG/smtp-risk-check.nse', 'r', encoding='utf-8') as f:
    enh_smtp = f.read()

# Read enhanced script 2 (ftp-anon-plus.nse)
with open('c:/DA-1BLOG/ftp-anon-plus.nse', 'r', encoding='utf-8') as f:
    enh_ftp = f.read()

content_md = f"""# Enhancing Base Nmap NSE Scripts: Automated Risk Checking for SMTP and FTP Services

**Author Name:** Dhanishkanth

---

## 1. Intro to Nmap
Network Mapper (**Nmap**) is an open-source utility for network discovery, host enumeration, and security auditing. It allows system administrators and security researchers to identify active hosts on a network, detect open TCP/UDP ports, recognize running services and their application versions, and identify underlying operating systems.

At the core of Nmap's extensibility is the **Nmap Scripting Engine (NSE)**. NSE executes scripts written in the **Lua** programming language, enabling tasks ranging from advanced service detection and vulnerability scanning to automated network asset checks. While default discovery scripts gather raw banners and commands, custom NSE scripts allow administrators to analyze protocol responses on the fly and detect security misconfigurations directly within the scan workflow.

---

## 2. Nmap Reference Script 1 (*.nse script only)

### Script Name: `smtp-commands.nse`
*Original author: Jasey DePriest (Nmap Project)*

```lua
{orig_smtp}
```

---

## 3. Nmap Reference Script 1 Description

The stock Nmap script `smtp-commands.nse` connects to an SMTP service on ports 25, 465, or 587. It executes the standard greeting handshake (`EHLO`) to retrieve the list of Extended SMTP (ESMTP) keywords advertised by the server, and subsequently issues a `HELP` command to obtain additional supported verb lists. 

It normalizes line endings and removes standard response status codes (e.g., `250`, `214`), concatenating the results into a comma-separated list of commands supported by the remote mail server.

**Limitation of the Reference Script:** The reference script is purely informational. It collects and prints the list of commands returned by the server, but it does not analyze whether any of those capabilities pose a security risk (such as user enumeration commands) or whether essential security controls (such as transport layer encryption) are missing.

---

## 4. Nmap Reference Script 1 Output

When executed against an SMTP service on port 25:
```cmd
nmap -Pn --script=smtp-commands -p 25 127.0.0.1
```

**Observed Output:**
```text
PORT   STATE SERVICE
25/tcp open  smtp
| smtp-commands: testmail.local Hello, SIZE 33554432, VRFY, EXPN, 8BITMIME, HELP
|_ Supported commands: HELO EHLO MAIL RCPT DATA QUIT HELP
```

As shown in the output, the reference script lists `VRFY` and `EXPN` as plain text commands without assessing the fact that these commands can be used by attackers to enumerate local user mailboxes. It also does not alert the user that `STARTTLS` is absent.

---

## 5. Nmap Reference Script 1 Enhancement Options 1 and 2

To upgrade the base discovery script into an automated security evaluation tool, two key enhancement options were designed and implemented:

### Enhancement Option 1: Automated SMTP Security Risk Assessment (`smtp-risk-check.nse`)
1. **User Enumeration Detection:** Inspect the combined response from `EHLO` and `HELP` for the presence of the `VRFY` (Verify) and `EXPN` (Expand) commands. If advertised, flag the finding with `[!] User enumeration possible via VRFY/EXPN`.
2. **Missing Encryption Warning:** Check if the `STARTTLS` keyword is advertised in the server capabilities. If missing, warn with `[!] STARTTLS not advertised -- mail may be sent/received unencrypted`.
3. **Preserved Core Compatibility:** Retain the original socket connection logic in `go()` while adding a dedicated `check_risks()` function to evaluate findings without breaking standard output formatting.

### Enhancement Option 2: Automated Sensitive File Detection in Anonymous FTP (`ftp-anon-plus.nse`)
1. **Sensitive Filename Pattern Matching:** Extend anonymous FTP directory parsing with a regex pattern table (`SENSITIVE_PATTERNS`) targeting confidential assets such as `.env`, `id_rsa`, `backup.zip`, `config`, and `passwd`.
2. **Inline File Tagging:** Tag matched files with `[NSE: sensitive]` alongside standard `[NSE: writeable]` permissions tags.
3. **Consolidated Findings Summary:** Add a summary line `Sensitive files detected: ...` to give administrators an immediate overview of exposed high-risk files.

---

## 6. Nmap Newly Generated Script with Enhancement Option 1 (*.nse script only)

### Script Name: `smtp-risk-check.nse` (run as `smtp-commands-customs.nse`)

```lua
{enh_smtp}
```

---

## 7. Nmap Newly Generated Script with Enhancement Option 1 Description

The newly generated script `smtp-risk-check.nse` builds upon `smtp-commands.nse` by adding an active security evaluation layer:

1. **`check_risks(combined_text)` Function:** A dedicated helper function converts the combined output of `EHLO` and `HELP` to uppercase and executes two security checks:
   - It searches for `VRFY` and `EXPN`. These legacy RFC commands allow unauthenticated clients to test whether usernames exist on the mail server. When detected, the script constructs a warning alert indicating potential user enumeration.
   - It searches for `STARTTLS`. In the absence of `STARTTLS`, mail is transmitted in cleartext over port 25, vulnerable to interception. If `STARTTLS` is not found, the script generates an encryption warning.
2. **Action Pipeline Integration:** The main `action` function executes `go()` to retrieve supported commands, combines the output into a single string, evaluates it through `check_risks()`, and appends the warning flags directly underneath the supported commands list.

---

## 8. Nmap Newly Generated Script with Enhancement Option 1 Output

### Test A: Execution on Risky Server (VRFY/EXPN present, STARTTLS missing)
```cmd
nmap -Pn --script=C:\\Users\\dhani\\smtp-commands-customs.nse -p 25 127.0.0.1
```

**Observed Terminal Output:**
```text
PORT   STATE SERVICE
25/tcp open  smtp
| smtp-commands-customs: testmail.local Hello, SIZE 33554432, VRFY, EXPN, 8BITMIME, HELP
|  Supported commands: HELO EHLO MAIL RCPT DATA QUIT HELP
|  [!] User enumeration possible via VRFY/EXPN
|_ [!] STARTTLS not advertised -- mail may be sent/received unencrypted
```

**Output Comparison Screenshot (Risky Mode vs Original):**  
<p align="center">
  <img src="{img1}" alt="SMTP Risky Server Output Comparison" style="max-width:100%; border:1px solid #ddd; border-radius:8px; box-shadow:0 4px 10px rgba(0,0,0,0.1); margin:15px 0;" />
  <br><em>Figure 1: Back-to-back execution on the risky SMTP server showing the original script vs the newly enhanced script with [!] warnings.</em>
</p>

### Test B: Execution on Secure Server (STARTTLS advertised, VRFY/EXPN absent)
```cmd
nmap -Pn --script=C:\\Users\\dhani\\smtp-commands-customs.nse -p 25 127.0.0.1
```

**Observed Terminal Output:**
```text
PORT   STATE SERVICE
25/tcp open  smtp
| smtp-commands-customs: testmail.local Hello, SIZE 33554432, STARTTLS, 8BITMIME, HELP
|_ Supported commands: HELO EHLO MAIL RCPT DATA QUIT HELP
```

**Screenshot on Secure Server (No false positive warnings):**  
<p align="center">
  <img src="{img2}" alt="SMTP Secure Server Scan Output" style="max-width:100%; border:1px solid #ddd; border-radius:8px; box-shadow:0 4px 10px rgba(0,0,0,0.1); margin:15px 0;" />
  <br><em>Figure 2: Execution on the secure server confirming that zero warning lines appear when the server is properly configured.</em>
</p>

---

## 9. Nmap Newly Generated Script with Enhancement Option 2 (*.nse script only)

### Script Name: `ftp-anon-plus.nse` (run as `ftp-anon-custom.nse`)

```lua
{enh_ftp}
```

---

## 10. Nmap Newly Generated Script with Enhancement Option 2 Description

The newly generated script `ftp-anon-plus.nse` enhances the standard anonymous FTP check (`ftp-anon.nse`) by introducing automated sensitive filename detection:

1. **`get_entry_name(item)`:** Parses standard UNIX `LIST` format lines using the regex pattern `([^%s]+)$` to extract the individual file or folder name.
2. **`SENSITIVE_PATTERNS` Table:** A predefined list of 16 regex patterns targeting high-value files:
   - Environment configurations: `^%.env$`, `^%.env%.`
   - Web server configurations: `^%.htaccess$`, `^config$`
   - SSH and cryptographic credentials: `^id_rsa`, `^id_dsa`, `^%.ssh$`
   - System user stores: `^passwd$`, `^shadow$`
   - Backups and database archives: `^backup`, `^database`, `^secret`, `^token`, `^private`
3. **`is_sensitive(name)` Function:** Matches each filename against the pattern list in a case-insensitive manner.
4. **Tagging and Summarizing:** For every directory entry returned, the script checks write permissions (adding `[NSE: writeable]`) and sensitive filename patterns (adding `[NSE: sensitive]`). If sensitive files are detected, a consolidated summary line is appended at the bottom: `Sensitive files detected: <list of files>`.

---

## 11. Nmap Newly Generated Script with Enhancement Option 2 Output

When executed against FileZilla Server hosting dummy files (`.env`, `backup.zip`, `config`, `id_rsa`, `passwd`, and a benign control file `readme.txt`):

```cmd
nmap -Pn --script=C:\\Users\\dhani\\ftp-anon-custom.nse -p 21 127.0.0.1
```

**Observed Terminal Output:**
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

**FTP Comparison Screenshot:**  
<p align="center">
  <img src="{img3}" alt="FTP Scan Output with Sensitive Files Tagged" style="max-width:100%; border:1px solid #ddd; border-radius:8px; box-shadow:0 4px 10px rgba(0,0,0,0.1); margin:15px 0;" />
  <br><em>Figure 3: Output of ftp-anon-custom showing sensitive files flagged with [NSE: sensitive] and summarized at the bottom, while benign files (readme.txt) remain untagged.</em>
</p>

---

## 12. Learning Outcomes

1. **Mastery of Nmap Scripting Engine (NSE) Architecture:** Gained in-depth understanding of Lua scripting in Nmap, specifically how `portrule` triggers scripts and how `action(host, port)` interacts with low-level network sockets using `nmap`, `shortport`, and `stdnse` libraries.
2. **Application-Layer Protocol Nuances:** Learned the operational mechanics of SMTP (RFC 821/5321) greeting sequences (`EHLO`, `HELP`), standard status codes (`220`, `250`, `214`), and the importance of opportunistic TLS upgrades via `STARTTLS`.
3. **Secure Configuration Auditing:** Understood why commands like `VRFY` and `EXPN` should be disabled on production mail servers to prevent directory harvesting attacks.
4. **Regex-Based Asset Discovery:** Developed pattern-matching algorithms to parse unstructured directory listings and detect sensitive enterprise data exposed through unauthenticated FTP services.
5. **Practical Network Troubleshooting on Windows:** Resolved real-world network reconnaissance issues, including firewall ping filtering (fixed with `-Pn`), socket address collisions (`taskkill`), and silent authentication rejections (FTP code `530`).

---

## 13. GitHub Repo Link Where the Two Enhanced Scripts are Found

All scripts, testing environments, and scan outputs are open-source and hosted on GitHub:  
👉 **GitHub Repository Link:** [https://github.com/dhanish0104/nmap-nse-audit-scripts](https://github.com/dhanish0104/nmap-nse-audit-scripts)

---

## 14. Conclusion

Extending Nmap's default discovery scripts demonstrates how standard network reconnaissance can be upgraded into proactive security evaluation. By adding lightweight Lua pattern-matching and capability verification logic, the enhanced scripts transform raw protocol banners into immediate, actionable security findings without requiring bulky third-party scanners. This exercise illustrates how network security practitioners can customize open-source tooling to fit specific audit policies and harden organizational infrastructure.

---

## 15. Acknowledgements

This project was built upon the open-source scripts provided by the Nmap Project community:
- **`smtp-commands.nse`:** Originally authored by **Jasey DePriest**.
- **`ftp-anon.nse`:** Originally authored by **Eddie Bell**, **Rob Nicholls**, **Ange Gutek**, and **David Fifield**.

Gratitude is extended to the open-source security community for creating and maintaining the Nmap Scripting Engine.
"""

with open('c:/DA-1BLOG/BLOG1_BLOGGER.md', 'w', encoding='utf-8') as f:
    f.write(content_md)

print("BLOG1_BLOGGER.md created successfully")
