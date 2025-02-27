import os
import re
import requests
import sys
from bs4 import BeautifulSoup

def get_page_title(url):
    """ Extracts the page title from <div class="bt_title"> or falls back to <title>. """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # 1️⃣ Extract from <div class="bt_title">
            title_div = soup.find("div", {"class": "bt_title"})
            if title_div:
                title = title_div.text.strip()
                print(f"✅ Title found (bt_title): {title}")
            else:
                # 2️⃣ Fallback to <title> tag
                title = soup.title.string.strip() if soup.title else "unknown"
                print(f"⚠️ Fallback title (<title> tag): {title}")

            # 3️⃣ If still not found, try regex extraction
            if title.lower() == "unknown":
                match = re.search(r'<div class="bt_title".*?>(.*?)</div>', response.text, re.DOTALL | re.IGNORECASE)
                if match:
                    title = match.group(1).strip()
                    print(f"✅ Title extracted via regex: {title}")

            # Sanitize the title for safe folder names
            return re.sub(r'[\\/:*?"<>|]', '_', title)

    except requests.RequestException as e:
        print(f"❌ Error fetching page: {e}")

    return "unknown"

def main():
    if len(sys.argv) != 2:
        print("Usage: python batch_download.py \"path_to_txt_file.txt\"")
        return

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    file_type = input("What type of file do you want to download? (e.g., pdf): ").strip()
    threads = input("How many threads should be used?: ").strip()

    batch_lines = [
        "@echo off",
        "setlocal enabledelayedexpansion",
        "chcp 65001 > nul",  # Enable UTF-8 support
        "cls",
        "color 0A",  # Green text color
        "set /a count=0",
        "set /a total=0",
        f'for /f "usebackq delims=" %%A in ("{file_path}") do set /a total+=1',
        'echo Downloading...'
    ]

    with open(file_path, "r", encoding="utf-8") as f:
        links = [line.strip() for line in f if line.strip()]

    for link in links:
        folder_name = get_page_title(link)
        output_dir = f"./dl/{folder_name}"  # ✅ Fixed output folder path
        command = f'vk_downloader.exe --output_dir "{output_dir}" --file_type {file_type} "{link}" --threads {threads}'
        batch_lines.append(command)
        batch_lines.append('set /a count+=1')
        batch_lines.append('echo [[92m✔ Completed[0m] !count!/!total! downloads finished.')  # ✅ Fixed display bug

    batch_lines.append("echo Download completed!")
    batch_lines.append("pause")

    with open("batch_download.cmd", "w", encoding="utf-8") as batch_file:
        batch_file.write("\n".join(batch_lines))

    print()
    print("✅ 'batch_download.cmd' file successfully created.")

if __name__ == "__main__":
    main()
