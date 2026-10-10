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

md_json = json.dumps(md)

html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Extending Nmap NSE: Two Custom Audit Scripts for SMTP and FTP - Dhanishkanth</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.5.1/github-markdown-light.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <style>
        body {
            box-sizing: border-box;
            min-width: 200px;
            max-width: 980px;
            margin: 0 auto;
            padding: 45px 25px;
            background-color: #ffffff;
            color: #24292f;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif;
            line-height: 1.6;
        }
        .header-meta {
            margin-bottom: 25px;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        .badge {
            background-color: #0969da;
            color: #ffffff;
            font-size: 13px;
            font-weight: 600;
            padding: 5px 12px;
            border-radius: 16px;
        }
        .badge-green {
            background-color: #1a7f37;
        }
        .badge-purple {
            background-color: #8250df;
        }
        .markdown-body {
            background-color: #ffffff !important;
            color: #24292f !important;
        }
        .markdown-body pre {
            background-color: #f6f8fa !important;
            border: 1px solid #d0d7de !important;
            border-radius: 8px;
        }
        .markdown-body table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        .markdown-body table th {
            background-color: #f6f8fa;
            color: #24292f;
            font-weight: 600;
        }
        .markdown-body table th, .markdown-body table td {
            border: 1px solid #d0d7de;
            padding: 8px 12px;
        }
        .markdown-body img {
            border: 1px solid #d0d7de;
            border-radius: 8px;
            max-width: 100%;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin: 15px 0;
        }
        footer {
            margin-top: 60px;
            border-top: 1px solid #d0d7de;
            padding-top: 25px;
            text-align: center;
            font-size: 14px;
            color: #57606a;
        }
    </style>
</head>
<body>
    <div class="header-meta">
        <span class="badge">VIT Chennai</span>
        <span class="badge badge-green">Cybersecurity Assignment</span>
        <span class="badge badge-purple">B.Tech CSE (24BCE1348)</span>
    </div>
    <div id="content" class="markdown-body"></div>
    <footer>
        <p>Technical Blog Post by <strong>Dhanishkanth (24BCE1348)</strong> &bull; School of Computer Science and Engineering &bull; VIT Chennai &bull; October 2026</p>
    </footer>
    <script>
        const rawMd = """ + md_json + """;
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
print("index.html rebuilt with clean white background successfully!")
