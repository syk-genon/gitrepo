import os
import sys
import io
import re
import json

sys.path.append(r"C:\Users\exbxda13\gdrive-classifier")
from gdrive_helper import get_drive_service
from googleapiclient.http import MediaIoBaseDownload

proj_dir = r"D:\workspace\GEMINI\saryung_200"
os.makedirs(proj_dir, exist_ok=True)

service = get_drive_service(
    r"C:\Users\exbxda13\gdrive-classifier\credentials.json",
    r"C:\Users\exbxda13\gdrive-classifier\token.json"
)
file_id = "15_DBGo83crxpZdxdSGtaYrOq4Ic_exG2"

fh = io.BytesIO()
req = service.files().get_media(fileId=file_id)
downloader = MediaIoBaseDownload(fh, req)
done = False
while not done:
    _, done = downloader.next_chunk()

text = fh.getvalue().decode("utf-8", errors="ignore")
orig_path = os.path.join(proj_dir, "original_160.txt")
with open(orig_path, "w", encoding="utf-8") as f:
    f.write(text)

# Parse intro metadata and all 160 chapters
pattern = re.compile(r'^제(\d+)화\.\s*(.+)$', re.MULTILINE)
matches = list(pattern.finditer(text))
print(f"Found {len(matches)} chapters in original_160.txt")

chapters = []
for i, m in enumerate(matches):
    ep_num = int(m.group(1))
    ep_title = m.group(2).strip()
    start = m.end()
    end = matches[i+1].start() if i + 1 < len(matches) else len(text)
    body = text[start:end].strip()
    body = re.sub(r'[-=]{10,}', '', body).strip()
    chapters.append({
        "orig_ep": ep_num,
        "title": ep_title,
        "length": len(body),
        "body": body
    })

with open(os.path.join(proj_dir, "original_160_parsed.json"), "w", encoding="utf-8") as f:
    json.dump(chapters, f, ensure_ascii=False, indent=2)

# Print all 160 titles and lengths
for c in chapters:
    print(f"제{c['orig_ep']}화. {c['title']} ({c['length']}자)")
