import os
import re
import requests
import sys
from bs4 import BeautifulSoup

def get_page_title(url):
    """Extracts the page title from <div class="bt_title"> or falls back to <title>."""
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        response = requests.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        title_div = soup.find("div", class_="bt_title", id="bt_title")
        title = title_div.text.strip() if title_div else soup.title.string.strip() if soup.title else "Unknown"
        
        print(f"✅ Title found: {title}")
        return re.sub(r'[\\/:*?"<>|]', "_", title)
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching page: {e}")
        return "Unknown"

def main():
    if len(sys.argv) != 2:
        print('Usage: python batch_download.py "path_to_txt_file.txt"')
        return

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    file_type = input("What type of file do you want to download? (e.g., pdf): ").strip()
    threads = input("How many threads should be used?: ").strip()

    with open(file_path, "r", encoding="utf-8") as f:
        links = [line.strip() for line in f if line.strip()]

    if not links:
        print("Error: The file is empty.")
        return

    batch_lines = [
        "@echo off",
        "setlocal enabledelayedexpansion",
        "chcp 65001 > nul",  # Enable UTF-8 support
        "cls",
        "color 0A",  # Green text color
        "set /a count=0",
        "set /a total=0",
        f'for /f "usebackq delims=" %%A in ("{file_path}") do set /a total+=1',
        "echo Downloading...\n",
    ]

    for link in links:
        folder_name = get_page_title(link)
        output_dir = f"./dl/{folder_name}"
        command = f'vk_downloader.exe --output_dir "{output_dir}" --file_type {file_type} "{link}" --threads {threads}'
        batch_lines.append(command)

    batch_lines.append("echo Download completed!")
    batch_lines.append("pause")

    with open("batch_download.cmd", "w", encoding="utf-8") as batch_file:
        batch_file.write("\n".join(batch_lines))

    print("✅ 'batch_download.cmd' file successfully created.")

if __name__ == "__main__":
    main()
