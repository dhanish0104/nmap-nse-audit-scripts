import re, json

with open("c:/DA-1BLOG/BLOG1_BLOGGER.md", "r", encoding="utf-8") as f:
    text = f.read()

# We will create an HTML file that renders via marked.js in browser and provides a "Copy HTML for Blogger" button!
html_page = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog 1 for Blogger: Nmap Script Enhancements</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.5.1/github-markdown-light.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github.min.css">
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <style>
        body {
            background-color: #f8fafc;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 30px 20px;
        }
        .container {
            max-width: 960px;
            margin: 0 auto;
            background: #ffffff;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.06);
            border: 1px solid #e2e8f0;
        }
        .action-banner {
            background: #eff6ff;
            border: 1px solid #bfdbfe;
            border-radius: 8px;
            padding: 16px 20px;
            margin-bottom: 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }
        .action-btn {
            background: #0969da;
            color: #ffffff;
            border: none;
            padding: 10px 18px;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.2s;
        }
        .action-btn:hover {
            background: #0550ae;
        }
        .markdown-body {
            background: transparent !important;
        }
        .markdown-body pre {
            background-color: #f6f8fa !important;
            border: 1px solid #d0d7de !important;
            border-radius: 6px;
        }
        .markdown-body img {
            border: 1px solid #d0d7de;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="action-banner">
            <div>
                <strong>Blogger.com Ready Post</strong>
                <div style="font-size: 13px; color: #475569; margin-top: 4px;">Click the button below to copy the fully styled HTML directly into your clipboard, ready for Blogger's HTML View!</div>
            </div>
            <button class="action-btn" onclick="copyBloggerHtml()">📋 Copy HTML for Blogger</button>
        </div>
        <div id="content" class="markdown-body"></div>
    </div>

    <script>
        const rawMd = """ + json.dumps(text) + """;
        marked.setOptions({
            highlight: function(code, lang) {
                if (lang && hljs.getLanguage(lang)) {
                    return hljs.highlight(code, { language: lang }).value;
                }
                return hljs.highlightAuto(code).value;
            }
        });
        const parsedHtml = marked.parse(rawMd);
        document.getElementById('content').innerHTML = parsedHtml;

        function copyBloggerHtml() {
            navigator.clipboard.writeText(parsedHtml).then(() => {
                alert('Copied! In Blogger, click the pencil icon -> switch to "HTML view" -> paste directly!');
            }).catch(err => {
                alert('Copy failed: ' + err);
            });
        }
    </script>
</body>
</html>"""

with open("c:/DA-1BLOG/BLOG1_BLOGGER_PASTE.html", "w", encoding="utf-8") as f:
    f.write(html_page)

print("BLOG1_BLOGGER_PASTE.html generated successfully")
