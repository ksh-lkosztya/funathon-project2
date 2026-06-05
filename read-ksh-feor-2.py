import csv
import re
import requests
from bs4 import BeautifulSoup

# URL of the official Hungarian KSH FEOR-08 Interactive List
URL = "https://www.ksh.hu/docs/szolgaltatasok/hun/feor08/feorlista.html"

def scrape_feor():
    print(f"Fetching data from {URL}...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
        # Force correct Hungarian UTF-8 encoding
        response.encoding = 'utf-8'
    except Exception as e:
        print(f"Error fetching the page: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # KSH displays codes inside list tags or paragraph blocks (often plain text or simple links)
    # This regex identifies 1 to 4 digit codes at the beginning of the text line
    code_pattern = re.compile(r'^(\d{1,4})\s+(.+)$')

    scraped_rows = []

    # Tracking parent contexts dynamically to populate "item group name"
    current_major_group = "Ismeretlen" # 1-digit level
    current_subgroup = ""             # 2 or 3-digit level

    # Loop through list items or text blocks containing the classification items
    # Note: KSH uses standard list <li> tags for the accordion tree structure
    for element in soup.find_all(['li', 'p', 'div']):
        text = element.get_text(strip=True)
        if not text:
            continue

        match = code_pattern.match(text)
        if match:
            code = match.group(1)
            name = match.group(2).strip()

            # Layer 1: Major Group (1 digit, e.g., "1 GAZDASÁGI...")
            if len(code) == 1:
                current_major_group = f"{code} - {name}"
                current_subgroup = "" # Reset subgroup

            # Layer 2: Subgroups (2 or 3 digits, e.g., "11" or "111")
            elif len(code) in [2, 3]:
                current_subgroup = f"{code} - {name}"

            # Layer 3: Final Occupational Item (4 digits, e.g., "1110")
            elif len(code) == 4:
                # Combine major and minor groups to create a precise 'item group name'
                group_context = current_major_group
                if current_subgroup:
                    group_context += f" -> {current_subgroup}"

                # Append formatted data matching your exact requested columns
                scraped_rows.append({
                    "code": code,
                    "item group name": group_context,
                    "item name": name,
                    "item description": "" # Kept blank as requested to match your target layout
                })

    # Save to your desired flat CSV format
    csv_file = "ksh_feor08_codes_and_names.csv"
    headers = ["code", "item group name", "item name", "item description"]

    with open(csv_file, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(scraped_rows)

    print(f"Success! Extracted {len(scraped_rows)} occupations into '{csv_file}'.")

if __name__ == "__main__":
    scrape_feor()
