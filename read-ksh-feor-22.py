import csv
import re
import time
import requests
from bs4 import BeautifulSoup

# Base and list URLs for Hungarian KSH FEOR-08
BASE_URL = "https://www.ksh.hu/docs/szolgaltatasok/hun/feor08/"
LIST_URL = f"{BASE_URL}feorlista.html"

def fetch_item_description(code):
    """
    Crawls the unique sub-page for a 4-digit code and concatenates
    all descriptive text found inside CSS classes starting with 'occ_'.
    """
    # KSH places item pages in a subfolder named after the 1st digit of the code
    first_digit = code[0]
    sub_page_url = f"{BASE_URL}{first_digit}/{code}.html"

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        # Prevent hammering the server
        time.sleep(0.5)

        response = requests.get(sub_page_url, headers=headers, timeout=10)
        if response.status_code != 200:
            return "" # Fallback if specific page missing

        response.encoding = 'utf-8'
        sub_soup = BeautifulSoup(response.text, 'html.parser')

        # Extract and compile all text blocks where class name starts with 'occ_'
        description_pieces = []

        # Targets classes like 'occ_feladat', 'occ_jellemzo', 'occ_munkakor'
        occ_elements = sub_soup.find_all(class_=re.compile(r'^occ_'))

        for element in occ_elements:
            text_block = element.get_text(" ", strip=True)
            if text_block:
                description_pieces.append(text_block)

        # Return a single cleaned string wrapped neatly for CSV injection
        return "\n".join(description_pieces)

    except Exception as e:
        print(f"  [Warning] Failed to fetch description for code {code}: {e}")
        return ""

def scrape_complete_feor():
    print(f"1. Fetching structural tree from {LIST_URL}...")
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    try:
        response = requests.get(LIST_URL, headers=headers)
        response.raise_for_status()
        response.encoding = 'utf-8'
    except Exception as e:
        print(f"Error connecting to KSH main page: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    code_pattern = re.compile(r'^(\d{1,4})\s+(.+)$')

    scraped_rows = []
    current_major_group = "Ismeretlen"
    current_subgroup = ""

    # Parse hierarchy
    all_elements = soup.find_all(['li', 'p', 'div'])
    for element in all_elements:
        text = element.get_text(strip=True)
        if not text:
            continue

        match = code_pattern.match(text)
        if match:
            code = match.group(1)
            name = match.group(2).strip()

            if len(code) == 1:
                current_major_group = element.get_text(strip=False).split("\n")[0]
                # current_major_group = f" {name} "
                # current_major_group = f"{code} - {name}"
                current_subgroup = ""
            elif len(code) in [2, 3]:
                if (current_subgroup==""):
                    current_subgroup += element.get_text(strip=False).split("\n")[0]
                else:
                    current_subgroup += " -> " + element.get_text(strip=False).split("\n")[0]
                # current_subgroup = f" {code} - {name} "
            elif len(code) == 4:
                group_context = current_major_group
                if current_subgroup:
                    group_context += f" -> {current_subgroup} "

                scraped_rows.append({
                    "code": code,
                    "item major group": current_major_group,
                    "item sub groups": group_context,
                    "item name": name,
                    "item description": ""  # Filled during next step
                })

    total_items = len(scraped_rows)
    print(f"2. Structure mapped. Found {total_items} target 4-digit codes.")
    print("3. Deep-crawling description sub-pages (this will take a few minutes)...")

    # Iterate and enrich descriptions line by line
    for idx, row in enumerate(scraped_rows, 1):
        code_to_fetch = row["code"]
        print(f"   [{idx}/{total_items}] Crawling details for Code: {code_to_fetch} - {row['item name'][:30]}...")

        # Dynamically execute our sub-scraper function
        detailed_text = fetch_item_description(code_to_fetch)
        row["item description"] = detailed_text

    # Write data output into target file
    csv_file = "feor08_with_occ_descriptions-222.csv"
    headers = ["code", "item major group", "item sub groups", "item name", "item description"]

    with open(csv_file, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(scraped_rows)

    print(f"\nFinished! All data exported seamlessly to '{csv_file}'.")

if __name__ == "__main__":
    scrape_complete_feor()
