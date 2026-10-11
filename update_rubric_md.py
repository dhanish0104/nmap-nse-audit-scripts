import base64

def get_b64(path):
    with open(path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode()

img1 = get_b64('c:/DA-1BLOG/screenshots/smtp_risky_comparison.png')
img2 = get_b64('c:/DA-1BLOG/screenshots/smtp_secure_scan.png')
img3 = get_b64('c:/DA-1BLOG/screenshots/ftp_anon_plus_output.png')

with open('C:/Program Files (x86)/Nmap/scripts/smtp-commands.nse', 'r', encoding='utf-8') as f:
    orig_smtp = f.read()

with open('c:/DA-1BLOG/smtp-risk-check.nse', 'r', encoding='utf-8') as f:
    enh_smtp = f.read()

with open('c:/DA-1BLOG/ftp-anon-plus.nse', 'r', encoding='utf-8') as f:
    enh_ftp = f.read()

md_rubric = f"""# Enhancing Base Nmap NSE Scripts: Automated Risk Checking for SMTP and FTP Services

**Author Name:** Dhanishkanth

---

## Intro to Nmap
Network Mapper (**Nmap**) is an open-source tool for network discovery, host enumeration, and security auditing. It allows system administrators and security researchers to discover active hosts across a network, identify open TCP and UDP ports, detect running services and version numbers, and determine underlying operating systems.

Nmap includes the **Nmap Scripting Engine (NSE)**, which executes automation scripts written in the **Lua** programming language. NSE allows users to extend Nmap's core functionality beyond standard port scanning into vulnerability verification, advanced discovery, and network compliance checks. While standard Nmap scripts collect raw banners and output from services, custom NSE scripts can actively analyze protocol replies in real time and evaluate whether the target service violates security best practices.

---

## Nmap reference script1 (*.nse script only)

```lua
{orig_smtp}
```

---

## Nmap reference script1 description

The stock Nmap script `smtp-commands.nse` (authored by Jasey DePriest) connects to an SMTP service on standard mail ports (25, 465, or 587). It initiates an application-layer handshake by sending the `EHLO` command with the local domain to gather Extended SMTP (ESMTP) keywords advertised by the server. It then issues a `HELP` command to retrieve additional supported commands.

The script strips SMTP response codes (`250-`, `214-`) using Lua string substitutions, trims extra whitespace, and formats the output into a single comma-separated list of supported commands.

**Limitation:** The reference script functions strictly as an informational discovery tool. It reports the raw commands supported by the target server without evaluating whether any of those commands introduce a security risk or whether critical protection mechanisms (such as transport encryption) are missing.

---

## Nmap reference script1 output

```cmd
nmap -Pn --script=smtp-commands -p 25 127.0.0.1
```

```text
PORT   STATE SERVICE
25/tcp open  smtp
| smtp-commands: testmail.local Hello, SIZE 33554432, VRFY, EXPN, 8BITMIME, HELP
|_ Supported commands: HELO EHLO MAIL RCPT DATA QUIT HELP
```

*Analysis of Output:* The reference script outputs `VRFY` and `EXPN` as regular commands without flagging that they can be leveraged by attackers for username harvesting. It also fails to notify the user that `STARTTLS` is missing.

---

## Nmap reference script1 enhancement options 1 and 2

To transform the base script into an active security evaluation tool, two distinct enhancement options were developed:

### Enhancement Option 1: Automated SMTP Security Risk Assessment (`smtp-risk-check.nse`)
1. **User Enumeration Detection:** Inspect the combined `EHLO` and `HELP` responses for the presence of the `VRFY` (Verify) and `EXPN` (Expand) commands. If advertised by the server, flag the finding with:  
   `[!] User enumeration possible via VRFY/EXPN`
2. **Missing Encryption Warning:** Verify whether the server advertises `STARTTLS`. If missing, output a security alert:  
   `[!] STARTTLS not advertised -- mail may be sent/received unencrypted`
3. **Preserved Core Compatibility:** Retain the socket handling of `go()` while adding a dedicated evaluation function `check_risks()` to append findings beneath the command list.

### Enhancement Option 2: Automated Sensitive File Detection in Anonymous FTP (`ftp-anon-plus.nse`)
1. **Sensitive Filename Pattern Matching:** Extend anonymous FTP directory listing parsing with a regular expression pattern table (`SENSITIVE_PATTERNS`) targeting configuration secrets, private keys, backups, and user databases (e.g., `.env`, `id_rsa`, `backup.zip`, `config`, `passwd`).
2. **Inline File Tagging:** Mark matched files with `[NSE: sensitive]` alongside standard `[NSE: writeable]` permissions tags.
3. **Findings Summary Footer:** Append a consolidated summary line:  
   `Sensitive files detected: <list of files>`

---

## Nmap newly generated script with enhancement option1 (*.nse script only)

```lua
{enh_smtp}
```

---

## Nmap newly generated script with enhancement option1 description

The enhanced script `smtp-risk-check.nse` builds upon `smtp-commands.nse` by adding an active security evaluation layer:

1. **`check_risks(combined_text)` Function:** Inspects the combined text returned from both `EHLO` and `HELP`:
   - Scans for `VRFY` and `EXPN`. These commands allow unauthenticated clients to verify whether usernames exist on the mail server. When detected, the script flags a potential user enumeration vector.
   - Scans for `STARTTLS`. In the absence of `STARTTLS`, mail is transmitted in cleartext over port 25, vulnerable to interception. If `STARTTLS` is missing, the script flags an unencrypted transmission risk.
2. **Action Pipeline Integration:** The main `action` function executes `go()` to retrieve supported commands, combines the output into a single string, evaluates it through `check_risks()`, and appends the warning flags directly underneath the supported commands list.

---

## Nmap newly generated script with enhancement option1 output

### Test A: Risky Server Mode (VRFY/EXPN present, STARTTLS missing)
```cmd
nmap -Pn --script=C:\\Users\\dhani\\smtp-commands-customs.nse -p 25 127.0.0.1
```

```text
PORT   STATE SERVICE
25/tcp open  smtp
| smtp-commands-customs: testmail.local Hello, SIZE 33554432, VRFY, EXPN, 8BITMIME, HELP
|  Supported commands: HELO EHLO MAIL RCPT DATA QUIT HELP
|  [!] User enumeration possible via VRFY/EXPN
|_ [!] STARTTLS not advertised -- mail may be sent/received unencrypted
```

<p align="center">
  <img src="{img1}" alt="SMTP Risky Server Output Comparison" style="max-width:100%; border:1px solid #ddd; border-radius:8px; box-shadow:0 4px 10px rgba(0,0,0,0.08); margin:15px 0;" />
  <br><em>Figure 1: Back-to-back execution on the risky SMTP server showing the original script vs the newly enhanced script with [!] warnings.</em>
</p>

### Test B: Secure Server Mode (STARTTLS present, VRFY/EXPN absent)
```cmd
nmap -Pn --script=C:\\Users\\dhani\\smtp-commands-customs.nse -p 25 127.0.0.1
```

```text
PORT   STATE SERVICE
25/tcp open  smtp
| smtp-commands-customs: testmail.local Hello, SIZE 33554432, STARTTLS, 8BITMIME, HELP
|_ Supported commands: HELO EHLO MAIL RCPT DATA QUIT HELP
```

<p align="center">
  <img src="{img2}" alt="SMTP Secure Server Scan Output" style="max-width:100%; border:1px solid #ddd; border-radius:8px; box-shadow:0 4px 10px rgba(0,0,0,0.08); margin:15px 0;" />
  <br><em>Figure 2: Execution on the secure server confirming that zero warning lines appear when the server is properly configured.</em>
</p>

---

## Nmap newly generated script with enhancement option2 (*.nse script only)

```lua
{enh_ftp}
```

---

## Nmap newly generated script with enhancement option2 description

The newly generated script `ftp-anon-plus.nse` enhances `ftp-anon.nse` by adding automated sensitive filename detection:

1. **`get_entry_name(item)`:** Parses standard UNIX `LIST` directory responses using the regex `([^%s]+)$` to extract the filename from each entry.
2. **`SENSITIVE_PATTERNS` Dictionary:** Defines 16 regex patterns targeting high-value files:
   - Environment files: `^%.env$`, `^%.env%.`
   - SSH and cryptographic credentials: `^id_rsa`, `^id_dsa`, `^%.ssh$`
   - Web & server configs: `^%.htaccess$`, `^config$`
   - User database files: `^passwd$`, `^shadow$`
   - Backups and database archives: `^backup`, `^database`, `^secret`, `^token`, `^private`
3. **`is_sensitive(name)` Function:** Performs case-insensitive matching against each pattern in the dictionary.
4. **Tagging and Summarizing:** Checks each directory entry for write permissions (adding `[NSE: writeable]`) and sensitive filename patterns (adding `[NSE: sensitive]`). If sensitive files are detected, appends a summary footer:  
   `Sensitive files detected: <list of files>`

---

## Nmap newly generated script with enhancement option2 output

```cmd
nmap -Pn --script=C:\\Users\\dhani\\ftp-anon-custom.nse -p 21 127.0.0.1
```

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

<p align="center">
  <img src="{img3}" alt="FTP Scan Output with Sensitive Files Tagged" style="max-width:100%; border:1px solid #ddd; border-radius:8px; box-shadow:0 4px 10px rgba(0,0,0,0.08); margin:15px 0;" />
  <br><em>Figure 3: Output of ftp-anon-custom showing sensitive files flagged with [NSE: sensitive] and summarized at the bottom, while benign files (readme.txt) remain untagged.</em>
</p>

---

## Learning outcomes

1. **Nmap Scripting Engine (NSE) Mechanics:** Gained hands-on experience developing Lua scripts for Nmap, leveraging `portrule` conditional triggers, socket management through `nmap`, and formatting with `stdnse`.
2. **Application-Layer Protocol Analysis:** Explored the operational mechanics of SMTP (RFC 821/5321) greeting exchanges (`EHLO`, `HELP`), standard response status codes (`220`, `250`, `214`), and transport layer security upgrades via `STARTTLS`.
3. **Identification of Information Disclosure Vectors:** Learned how legacy mail commands (`VRFY`, `EXPN`) facilitate user enumeration, and how anonymous FTP services expose critical assets when file naming conventions are not audited.
4. **Pattern-Matching Implementation:** Developed regex-based classification logic in Lua to parse unstructured directory listings and detect sensitive files during active scans.
5. **Practical Reconnaissance Debugging:** Solved real-world scanning obstacles on Windows, including firewall ping filtering (bypassed with `-Pn`), socket address collisions (`taskkill`), and silent authentication rejections (FTP code `530`).

---

## GitHub repo link where the two enhanced scripts are found :

All source code, testing environments, and documentation are hosted on GitHub:  
👉 **GitHub Repository Link:** [https://github.com/dhanish0104/nmap-nse-audit-scripts](https://github.com/dhanish0104/nmap-nse-audit-scripts)

---

## Conclusion

Extending Nmap's base scripts in Lua demonstrates how network scanning can be elevated into automated security risk evaluation. By adding lightweight pattern matching and protocol verification logic, the two enhanced scripts transform passive banner and directory data into immediate, actionable security findings without requiring complex third-party vulnerability scanners. This project highlights the practical value of script extensibility in network security workflows.

---

## Acknowledgements

This work builds upon scripts provided by the open-source Nmap Project community:
- **`smtp-commands.nse`:** Originally authored by **Jasey DePriest**.
- **`ftp-anon.nse`:** Originally authored by **Eddie Bell**, **Rob Nicholls**, **Ange Gutek**, and **David Fifield**.

All socket management and core protocol implementations are credited to the original authors and the Nmap development team.
"""

with open('c:/DA-1BLOG/BLOG_POST.md', 'w', encoding='utf-8') as f:
    f.write(md_rubric)

print("BLOG_POST.md successfully updated with exact rubric!")
