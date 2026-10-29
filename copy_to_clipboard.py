import markdown
import subprocess

with open('c:/DA-1BLOG/BLOG1_BLOGGER.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Convert markdown to html with fenced code blocks and tables
html = markdown.markdown(text, extensions=['fenced_code', 'tables'])

# Save to a text file
with open('c:/DA-1BLOG/blogger_paste_ready.txt', 'w', encoding='utf-8') as f:
    f.write(html)

# Put directly into Windows Clipboard using PowerShell Set-Clipboard
cmd = 'Get-Content -Path "c:/DA-1BLOG/blogger_paste_ready.txt" -Raw -Encoding utf8 | Set-Clipboard'
subprocess.run(['powershell', '-Command', cmd], check=True)

print("SUCCESS: Full HTML has been copied directly to your Windows Clipboard!")
