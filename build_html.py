import base64
import json

with open('c:/DA-1BLOG/BLOG_POST.md', 'r', encoding='utf-8') as f:
    md = f.read()

md_json = json.dumps(md)

html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enhancing Base Nmap NSE Scripts: Automated Risk Checking for SMTP and FTP Services | Dhanishkanth</title>
    
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
            --surface-bg: #ffffff;
            --page-bg: #f8fafc;
            --border: #e2e8f0;
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
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            z-index: 100;
            padding: 14px 24px;
        }
        .nav-inner {
            max-width: 1040px;
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
            background: var(--text-main);
            color: #ffffff;
            transition: all 0.2s ease;
        }
        .nav-btn:hover {
            background: #334155;
        }

        /* Hero Container */
        .hero-banner {
            max-width: 1040px;
            margin: 35px auto 25px auto;
            padding: 0 24px;
        }
        .hero-card {
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 36px 40px;
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
        .hero-title {
            font-size: 28px;
            font-weight: 800;
            color: #0f172a;
            line-height: 1.3;
            margin: 0 0 16px 0;
            letter-spacing: -0.4px;
        }
        .hero-author-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-top: 20px;
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
            width: 42px;
            height: 42px;
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
            font-size: 13px;
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
            max-width: 1040px;
            margin: 0 auto 60px auto;
            padding: 0 24px;
        }
        .article-card {
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 44px 48px;
            box-shadow: 0 4px 20px -4px rgba(15, 23, 42, 0.05);
        }

        /* Typography & Markdown Polish */
        .markdown-body {
            font-family: var(--font-sans) !important;
            color: #1e293b !important;
            font-size: 15.5px !important;
            line-height: 1.75 !important;
            background-color: transparent !important;
        }
        .markdown-body h1 {
            display: none; /* Already rendered in Hero */
        }
        .markdown-body h2 {
            font-family: var(--font-sans) !important;
            font-weight: 700 !important;
            font-size: 22px !important;
            color: #0f172a !important;
            border-bottom: 1px solid #e2e8f0 !important;
            margin-top: 36px !important;
            margin-bottom: 16px !important;
            padding-bottom: 8px !important;
            letter-spacing: -0.3px;
        }
        .markdown-body h3 {
            font-size: 18px !important;
            font-weight: 700 !important;
            color: #1e293b !important;
            margin-top: 24px !important;
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
            padding: 16px 20px !important;
            box-shadow: inset 0 1px 2px rgba(0,0,0,0.02);
            overflow-x: auto;
        }
        .markdown-body pre code {
            background-color: transparent !important;
            color: #334155 !important;
            padding: 0 !important;
        }
        .markdown-body img {
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.06);
            margin: 15px 0 6px 0;
            max-width: 100%;
        }
        .markdown-body em {
            color: var(--text-muted);
            font-size: 13.5px;
        }

        /* Footer */
        .site-footer {
            border-top: 1px solid var(--border);
            background: #ffffff;
            padding: 35px 24px;
            text-align: center;
            color: var(--text-muted);
            font-size: 14px;
        }

        @media (max-width: 768px) {
            .hero-card { padding: 24px; }
            .article-card { padding: 24px; }
            .hero-title { font-size: 22px; }
            .hero-author-bar { flex-direction: column; align-items: flex-start; }
        }
    </style>
</head>
<body>

    <!-- Sticky Navbar -->
    <header class="top-navbar">
        <div class="nav-inner">
            <a href="#" class="nav-brand">
                <span>🛡️ Nmap Script Enhancements Blog</span>
            </a>
            <div class="nav-links">
                <a href="https://github.com/dhanish0104/nmap-nse-audit-scripts" target="_blank" class="nav-btn">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/></svg>
                    <span>GitHub Repo</span>
                </a>
            </div>
        </div>
    </header>

    <!-- Hero Card Banner -->
    <div class="hero-banner">
        <div class="hero-card">
            <h1 class="hero-title">Enhancing Base Nmap NSE Scripts: Automated Risk Checking for SMTP and FTP Services</h1>
            
            <div class="hero-author-bar">
                <div class="author-info">
                    <div class="author-avatar">D</div>
                    <div>
                        <div class="author-details-name">Author: Dhanishkanth</div>
                        <div class="author-details-role">Cybersecurity Assignment</div>
                    </div>
                </div>
                <div class="meta-pills">
                    <span>⚡ Lua &bull; Nmap 7.99</span>
                    <span>&bull;</span>
                    <span>⏱️ 10 min read</span>
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
        <p><strong>Enhancing Base Nmap NSE Scripts: Automated Risk Checking for SMTP and FTP Services</strong></p>
        <p>Author: <strong>Dhanishkanth</strong></p>
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

print("index.html successfully updated to match exact rubric headings and Author: Dhanishkanth!")
