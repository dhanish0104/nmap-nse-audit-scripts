import base64
import json

def get_b64(path):
    with open(path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode()

img1 = get_b64('c:/DA-1BLOG/screenshots/smtp_risky_comparison.png')
img2 = get_b64('c:/DA-1BLOG/screenshots/smtp_secure_scan.png')
img3 = get_b64('c:/DA-1BLOG/screenshots/ftp_anon_plus_output.png')

with open('c:/DA-1BLOG/BLOG_POST.md', 'r', encoding='utf-8') as f:
    md = f.read()

# Replace image paths with base64 data URIs
md = md.replace('screenshots/smtp_risky_comparison.png', img1)
md = md.replace('screenshots/smtp_secure_scan.png', img2)
md = md.replace('screenshots/ftp_anon_plus_output.png', img3)

# Replace the ASCII diagram in Markdown with an interactive modern HTML workflow component
ascii_block = """```
+-------------------------------------------------------------+
|                TRADITIONAL RECONNAISSANCE                   |
|  1. Connects to the service via TCP socket                  |
|  2. Sends protocol queries (e.g. EHLO, HELP, LIST)          |
|  3. Formats and prints raw server replies                   |
|  ===> Output: "Here is everything the server reported."      |
+-------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------+
|            CUSTOM SECURITY AUDIT LAYER (ADDED)              |
|  4. Intercepts the raw protocol data inside Lua memory      |
|  5. Evaluates features against security configuration rules |
|  6. Performs pattern matching on sensitive assets           |
|  ===> Output: "[!] User enumeration possible via VRFY/EXPN" |
|               "[!] STARTTLS not advertised"                 |
|               "[NSE: sensitive] backup.zip, id_rsa"         |
+-------------------------------------------------------------+
```"""

workflow_html = """
<div class="pipeline-container">
  <!-- Step 1: Traditional Reconnaissance -->
  <div class="pipeline-card stage-passive">
    <div class="pipeline-header">
      <div class="stage-tag tag-blue">Phase 1 &bull; Standard Reconnaissance</div>
      <span class="stage-role">Original Nmap NSE Behavior</span>
    </div>
    <div class="pipeline-body">
      <div class="pipeline-step">
        <span class="step-num">1</span>
        <span class="step-text">Connects to remote target via raw TCP socket (port 25 / 21)</span>
      </div>
      <div class="pipeline-step">
        <span class="step-num">2</span>
        <span class="step-text">Transmits standard RFC protocol queries (<code>EHLO</code>, <code>HELP</code>, <code>LIST</code>)</span>
      </div>
      <div class="pipeline-step">
        <span class="step-num">3</span>
        <span class="step-text">Passively parses responses and displays unjudged output to user</span>
      </div>
    </div>
    <div class="pipeline-output output-passive">
      <span class="output-label">Output Characteristic:</span>
      <code>"Informational only &bull; Reports facts without assessing risk"</code>
    </div>
  </div>

  <!-- Connector -->
  <div class="pipeline-connector">
    <div class="connector-line"></div>
    <div class="connector-badge">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 5v14M19 12l-7 7-7-7"/></svg>
      <span>Custom Lua Security Audit Engine</span>
    </div>
    <div class="connector-line"></div>
  </div>

  <!-- Step 2: Custom Audit Layer -->
  <div class="pipeline-card stage-audit">
    <div class="pipeline-header">
      <div class="stage-tag tag-green">Phase 2 &bull; Active Security Audit</div>
      <span class="stage-role">Dhanishkanth's Custom Extension</span>
    </div>
    <div class="pipeline-body">
      <div class="pipeline-step">
        <span class="step-num step-audit">4</span>
        <span class="step-text">Intercepts raw responses in Lua memory before terminal formatting</span>
      </div>
      <div class="pipeline-step">
        <span class="step-num step-audit">5</span>
        <span class="step-text">Evaluates capabilities against hardening policies (checks for <code>VRFY</code>, <code>EXPN</code>, and <code>STARTTLS</code>)</span>
      </div>
      <div class="pipeline-step">
        <span class="step-num step-audit">6</span>
        <span class="step-text">Runs regex pattern matching (<code>SENSITIVE_PATTERNS</code>) against exposed directory listings</span>
      </div>
    </div>
    <div class="pipeline-output output-audit">
      <span class="output-label">Actionable Findings:</span>
      <div class="tag-row">
        <span class="pill-warning">[!] User enumeration possible via VRFY/EXPN</span>
        <span class="pill-warning">[!] STARTTLS not advertised</span>
        <span class="pill-danger">[NSE: sensitive] .env, id_rsa, backup.zip</span>
      </div>
    </div>
  </div>
</div>
"""

md = md.replace(ascii_block, workflow_html)

# Also support fallback replacement if exact block differed slightly
alt_ascii = """```
+-----------------------------------+
|      Traditional NSE Scripts      |
|  - Connects to service            |
|  - Requests capabilities/files    | ===> "Here is what the server returned."
|  - Prints raw output              |
+-----------------------------------+
                  |
                  v
+-----------------------------------+
|     Custom Audit Layer (Added)    |
|  - Inspects returned capabilities |
|  - Compares against risky patterns| ===> "[!] Risk Flag: User enumeration possible"
|  - Emits actionable security notes|      "[NSE: sensitive] Found .env, id_rsa"
+-----------------------------------+
```"""
md = md.replace(alt_ascii, workflow_html)

md_json = json.dumps(md)

html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Extending Nmap NSE: Two Custom Audit Scripts for SMTP and FTP | Dhanishkanth</title>
    
    <!-- Modern Typography -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    
    <!-- Markdown & Syntax Highlighting -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.5.1/github-markdown-light.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>

    <style>
        :root {
            --primary: #0969da;
            --primary-hover: #0550ae;
            --primary-subtle: #ddf4ff;
            --success: #1a7f37;
            --success-subtle: #dafbe1;
            --warning: #9a6700;
            --warning-subtle: #fff8c5;
            --danger: #cf222e;
            --danger-subtle: #ffebe9;
            --surface-bg: #ffffff;
            --page-bg: #f8fafc;
            --border: #e2e8f0;
            --border-hover: #cbd5e1;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            --font-mono: 'JetBrains Mono', Menlo, Monaco, Consolas, monospace;
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            padding: 0;
            background-color: var(--page-bg);
            color: var(--text-main);
            font-family: var(--font-sans);
            line-height: 1.7;
            -webkit-font-smoothing: antialiased;
        }

        /* Top Navigation Header */
        .top-navbar {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 100;
            padding: 14px 24px;
        }
        .nav-inner {
            max-width: 1080px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .nav-brand {
            display: flex;
            align-items: center;
            gap: 12px;
            font-weight: 700;
            font-size: 15px;
            color: var(--text-main);
            text-decoration: none;
        }
        .nav-brand-badge {
            background: #eff6ff;
            color: var(--primary);
            font-size: 11px;
            font-weight: 700;
            padding: 4px 8px;
            border-radius: 6px;
            border: 1px solid #bfdbfe;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .nav-links {
            display: flex;
            align-items: center;
            gap: 16px;
        }
        .nav-btn {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 13px;
            font-weight: 600;
            text-decoration: none;
            padding: 7px 14px;
            border-radius: 8px;
            transition: all 0.2s ease;
        }
        .nav-btn-secondary {
            background: #ffffff;
            color: #334155;
            border: 1px solid var(--border);
        }
        .nav-btn-secondary:hover {
            background: #f1f5f9;
            border-color: #cbd5e1;
        }
        .nav-btn-primary {
            background: var(--text-main);
            color: #ffffff;
        }
        .nav-btn-primary:hover {
            background: #334155;
            color: #ffffff;
        }

        /* Hero Container */
        .hero-banner {
            max-width: 1080px;
            margin: 40px auto 30px auto;
            padding: 0 24px;
        }
        .hero-card {
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 40px;
            box-shadow: 0 4px 20px -4px rgba(15, 23, 42, 0.05);
            position: relative;
            overflow: hidden;
        }
        .hero-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(90deg, #0969da, #8250df, #1a7f37);
        }
        .hero-tags {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }
        .hero-tag {
            font-size: 12px;
            font-weight: 600;
            padding: 4px 10px;
            border-radius: 20px;
        }
        .tag-vit { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }
        .tag-course { background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; }
        .tag-reg { background: #faf5ff; color: #7e22ce; border: 1px solid #e9d5ff; }

        .hero-title {
            font-size: 32px;
            font-weight: 800;
            color: #0f172a;
            line-height: 1.25;
            margin: 0 0 16px 0;
            letter-spacing: -0.5px;
        }
        .hero-subtitle {
            font-size: 16px;
            color: #475569;
            margin: 0 0 24px 0;
            line-height: 1.6;
        }
        .hero-author-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-top: 24px;
            border-top: 1px solid #f1f5f9;
            flex-wrap: wrap;
            gap: 16px;
        }
        .author-info {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .author-avatar {
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: linear-gradient(135deg, #0969da, #8250df);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 16px;
        }
        .author-details-name {
            font-size: 15px;
            font-weight: 700;
            color: var(--text-main);
        }
        .author-details-role {
            font-size: 12px;
            color: var(--text-muted);
        }
        .meta-pills {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 13px;
            color: var(--text-muted);
        }

        /* Main Content Layout */
        .main-wrapper {
            max-width: 1080px;
            margin: 0 auto 60px auto;
            padding: 0 24px;
        }
        .article-card {
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 48px;
            box-shadow: 0 4px 20px -4px rgba(15, 23, 42, 0.05);
        }

        /* Modern Workflow Component (Replaces ASCII diagram) */
        .pipeline-container {
            margin: 35px 0;
            display: flex;
            flex-direction: column;
            gap: 0;
        }
        .pipeline-card {
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .pipeline-card:hover {
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.05);
        }
        .stage-passive {
            border-left: 5px solid #0969da;
        }
        .stage-audit {
            border-left: 5px solid #1a7f37;
            background: #fcfdfc;
        }
        .pipeline-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            flex-wrap: wrap;
            gap: 8px;
        }
        .stage-tag {
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.6px;
            padding: 4px 10px;
            border-radius: 6px;
        }
        .tag-blue { background: #eff6ff; color: #1d4ed8; }
        .tag-green { background: #f0fdf4; color: #15803d; }
        .stage-role {
            font-size: 13px;
            color: var(--text-muted);
            font-weight: 500;
        }
        .pipeline-body {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 16px;
        }
        .pipeline-step {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            font-size: 14px;
            color: #334155;
        }
        .step-num {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 22px;
            height: 22px;
            background: #e2e8f0;
            color: #475569;
            border-radius: 50%;
            font-size: 11px;
            font-weight: 700;
            flex-shrink: 0;
            margin-top: 2px;
        }
        .step-num.step-audit {
            background: #dcfce7;
            color: #15803d;
        }
        .pipeline-output {
            background: #f8fafc;
            border: 1px dashed var(--border);
            border-radius: 8px;
            padding: 12px 16px;
            font-size: 13px;
        }
        .output-label {
            font-weight: 600;
            color: #475569;
            margin-right: 8px;
        }
        .pipeline-connector {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 16px 0;
            position: relative;
        }
        .connector-line {
            height: 1px;
            background: #cbd5e1;
            flex: 1;
        }
        .connector-badge {
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 20px;
            padding: 6px 14px;
            font-size: 12px;
            font-weight: 600;
            color: #0f172a;
            display: flex;
            align-items: center;
            gap: 6px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.04);
            z-index: 2;
        }
        .tag-row {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: 6px;
        }
        .pill-warning {
            background: #fffbeb;
            color: #b45309;
            border: 1px solid #fef3c7;
            padding: 4px 10px;
            border-radius: 6px;
            font-family: var(--font-mono);
            font-size: 12px;
            font-weight: 600;
        }
        .pill-danger {
            background: #fef2f2;
            color: #b91c1c;
            border: 1px solid #fee2e2;
            padding: 4px 10px;
            border-radius: 6px;
            font-family: var(--font-mono);
            font-size: 12px;
            font-weight: 600;
        }

        /* Typography & Markdown Polish */
        .markdown-body {
            font-family: var(--font-sans) !important;
            color: #1e293b !important;
            font-size: 16px !important;
            line-height: 1.75 !important;
        }
        .markdown-body h1, .markdown-body h2, .markdown-body h3, .markdown-body h4 {
            font-family: var(--font-sans) !important;
            font-weight: 700 !important;
            color: #0f172a !important;
            border-bottom: none !important;
            margin-top: 36px !important;
            margin-bottom: 16px !important;
            letter-spacing: -0.3px;
        }
        .markdown-body h2 {
            font-size: 24px !important;
            padding-bottom: 8px;
            border-bottom: 1px solid #e2e8f0 !important;
        }
        .markdown-body h3 {
            font-size: 19px !important;
        }
        .markdown-body code {
            font-family: var(--font-mono) !important;
            font-size: 13.5px !important;
            background-color: #f1f5f9 !important;
            color: #0969da !important;
            padding: 3px 6px !important;
            border-radius: 6px !important;
        }
        .markdown-body pre {
            background-color: #f8fafc !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 10px !important;
            padding: 18px 20px !important;
            box-shadow: inset 0 1px 2px rgba(0,0,0,0.02);
            overflow-x: auto;
        }
        .markdown-body pre code {
            background-color: transparent !important;
            color: #334155 !important;
            padding: 0 !important;
        }
        .markdown-body blockquote {
            border-left: 4px solid var(--primary) !important;
            background: #f0f7ff !important;
            color: #1e293b !important;
            border-radius: 0 8px 8px 0;
            padding: 14px 20px !important;
            margin: 20px 0 !important;
        }
        .markdown-body table {
            border-collapse: separate !important;
            border-spacing: 0 !important;
            width: 100% !important;
            margin: 25px 0 !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 10px !important;
            overflow: hidden;
        }
        .markdown-body table th {
            background-color: #f8fafc !important;
            color: #0f172a !important;
            font-weight: 700 !important;
            border: none !important;
            border-bottom: 1px solid #e2e8f0 !important;
            padding: 12px 16px !important;
            text-align: left;
        }
        .markdown-body table td {
            border: none !important;
            border-bottom: 1px solid #f1f5f9 !important;
            padding: 12px 16px !important;
            color: #334155 !important;
        }
        .markdown-body table tr:last-child td {
            border-bottom: none !important;
        }
        .markdown-body img {
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.06);
            margin: 20px 0 8px 0;
            max-width: 100%;
            transition: transform 0.2s;
        }
        .markdown-body em {
            color: var(--text-muted);
            font-size: 14px;
            display: block;
            margin-bottom: 24px;
        }

        /* Footer */
        .site-footer {
            border-top: 1px solid var(--border);
            background: #ffffff;
            padding: 40px 24px;
            text-align: center;
            color: var(--text-muted);
            font-size: 14px;
        }
        .footer-inner {
            max-width: 1080px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 12px;
            align-items: center;
        }
        .footer-badges {
            display: flex;
            gap: 8px;
        }

        @media (max-width: 768px) {
            .hero-card { padding: 24px; }
            .article-card { padding: 24px; }
            .hero-title { font-size: 24px; }
            .hero-author-bar { flex-direction: column; align-items: flex-start; }
        }
    </style>
</head>
<body>

    <!-- Sticky Navbar -->
    <header class="top-navbar">
        <div class="nav-inner">
            <a href="#" class="nav-brand">
                <span>🛡️ Cybersecurity Lab Writeup</span>
                <span class="nav-brand-badge">VIT Chennai</span>
            </a>
            <div class="nav-links">
                <a href="https://github.com/dhanish0104/nmap-nse-audit-scripts" target="_blank" class="nav-btn nav-btn-primary">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>
                    <span>GitHub Repo</span>
                </a>
            </div>
        </div>
    </header>

    <!-- Hero Card Banner -->
    <div class="hero-banner">
        <div class="hero-card">
            <div class="hero-tags">
                <span class="hero-tag tag-vit">🏛️ VIT Chennai</span>
                <span class="hero-tag tag-course">💻 B.Tech Computer Science &amp; Engineering</span>
                <span class="hero-tag tag-reg">🎓 Reg: 24BCE1348</span>
            </div>
            <h1 class="hero-title">Extending Nmap NSE: Two Custom Audit Scripts for SMTP and FTP</h1>
            <p class="hero-subtitle">Transforming informational network reconnaissance into automated security posture evaluation through Lua-based active policy checking.</p>
            
            <div class="hero-author-bar">
                <div class="author-info">
                    <div class="author-avatar">D</div>
                    <div>
                        <div class="author-details-name">Dhanishkanth</div>
                        <div class="author-details-role">B.Tech Student, School of Computer Science and Engineering</div>
                    </div>
                </div>
                <div class="meta-pills">
                    <span>📅 October 2026</span>
                    <span>&bull;</span>
                    <span>⏱️ 10 min read</span>
                    <span>&bull;</span>
                    <span>⚡ Lua &bull; Nmap 7.99</span>
                </div>
            </div>
        </div>
    </div>

    <!-- Article Content -->
    <main class="main-wrapper">
        <article class="article-card">
            <div id="content" class="markdown-body"></div>
        </article>
    </main>

    <!-- Footer -->
    <footer class="site-footer">
        <div class="footer-inner">
            <p><strong>Extending Nmap NSE: Two Custom Audit Scripts for SMTP and FTP</strong></p>
            <p>Authored by <strong>Dhanishkanth (24BCE1348)</strong> &bull; School of Computer Science and Engineering &bull; Vellore Institute of Technology, Chennai</p>
            <div class="footer-badges">
                <span class="hero-tag tag-vit">VIT Chennai</span>
                <span class="hero-tag tag-course">Cybersecurity Assignment</span>
            </div>
        </div>
    </footer>

    <!-- Markdown Render Script -->
    <script>
        const rawMd = """ + md_json + """;
        marked.setOptions({
            highlight: function(code, lang) {
                if (lang && hljs.getLanguage(lang)) {
                    return hljs.highlight(code, { language: lang }).value;
                }
                return hljs.highlightAuto(code).value;
            }
        });
        document.getElementById('content').innerHTML = marked.parse(rawMd);
        document.querySelectorAll('pre code').forEach((el) => {
            hljs.highlightElement(el);
        });
    </script>
</body>
</html>
"""

with open('c:/DA-1BLOG/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Modern high-end UI built successfully!")
