import re
import subprocess
from pathlib import Path

html_path = Path(r"C:\Users\Otabek\.gemini\antigravity\scratch\sat-master-bot\webapp\index.html")
content = html_path.read_text(encoding="utf-8")

match = re.search(r"<script>(.*?)</script>", content, re.DOTALL)
if not match:
    print("No script found!")
    exit(1)

js_code = match.group(1)

# Write to test file
test_file = Path("test_bundle.js")
test_file.write_text(js_code, encoding="utf-8")

# Run node --check
res = subprocess.run(["node", "--check", str(test_file)], capture_output=True, text=True)
print("Node return code:", res.returncode)
if res.returncode != 0:
    print("Stderr:", res.stderr)
else:
    print("JavaScript syntax is 100% VALID!")
