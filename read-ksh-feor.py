import os
import requests
import pdfkit
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pypdf import PdfWriter

# --- CONFIGURATION ---
START_URL = "https://www.ksh.hu/docs/szolgaltatasok/hun/feor08/feorlista.html"
MAX_DEPTH = 1  # 0 = only start page, 1 = also follow links on start page
OUTPUT_FILE = "website_archive.pdf"
TEMP_DIR = "temp_pdfs"

# Ensure temp directory exists
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

visited = set()
queue = [(START_URL, 0)]
pdf_files = []

print(f"Starting recursive crawl of {START_URL}...")

# 1. Recursive Crawl & Convert
while queue:
    url, depth = queue.pop(0)
    if url in visited or depth > MAX_DEPTH:
        continue
    
    visited.add(url)
    print(f"Processing ({depth}): {url}")
    
    try:
        # Convert page to PDF
        temp_pdf = os.path.join(TEMP_DIR, f"page_{len(pdf_files)}.pdf")
        pdfkit.from_url(url, temp_pdf)
        pdf_files.append(temp_pdf)
        
        # Find more links if within depth
        if depth < MAX_DEPTH:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                full_url = urljoin(url, link['href'])
                # Only follow internal links
                if urlparse(full_url).netloc == urlparse(START_URL).netloc:
                    queue.append((full_url, depth + 1))
                    
    except Exception as e:
        print(f"Failed to process {url}: {e}")

# 2. Merge all PDFs
print(f"Merging {len(pdf_files)} pages into {OUTPUT_FILE}...")
merger = PdfWriter()

for pdf in pdf_files:
    merger.append(pdf)

with open(OUTPUT_FILE, "wb") as f:
    merger.write(f)

# 3. Cleanup
for pdf in pdf_files:
    os.remove(pdf)
os.rmdir(TEMP_DIR)

print("Done!")