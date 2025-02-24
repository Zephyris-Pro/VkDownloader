import argparse
import os
import re
import json
import requests
from bs4 import BeautifulSoup
from urllib import parse
from concurrent.futures import ThreadPoolExecutor


class VKDownloader:
    def __init__(self, url, output_dir, file_type, threads):
        self.url = url
        self.output_dir = output_dir
        self.file_type = file_type
        self.threads = threads
        self.session = requests.Session()
        self.session.headers["User-Agent"] = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        )
        os.makedirs(self.output_dir, exist_ok=True)

    def get_page_count(self, content):
        soup = BeautifulSoup(content, "html.parser")
        div = soup.find("div", class_="pg_pages bt_pages", id="bt_pages")
        return len(div.find_all("a")) if div and len(div) != 0 else 1

    def find_files(self, content):
        soup = BeautifulSoup(content, "html.parser")
        return [
            "https://vk.com" + a.get("href")
            for a in soup.find_all("a", class_="page_doc_title")
        ]

    def extract_file_url(self, content):

        regex = rf"https:\\/\\/psv4\.userapi\.com\\/s\\/v1\\/d\\/[-\w]+\\/([^\\/]+\.{self.file_type})"
        match = re.search(regex, content)
        return match.group(0).replace("\\/", "/") if match else None

    def get_filename(self, url):
        return parse.unquote(parse.urlparse(url).path.split("/")[-1])

    def download_file(self, file_url):
        try:
            file_page_content = self.session.get(file_url).content.decode("latin-1")
            file_download_url = self.extract_file_url(file_page_content)
            if file_download_url:
                filename = self.get_filename(file_download_url)
                file_path = os.path.join(self.output_dir, filename)
                print(f"Downloading {filename}...")

                with open(file_path, "wb") as file:
                    file.write(self.session.get(file_download_url).content)
                print(f"{filename} downloaded successfully!")
        except Exception as e:
            print(f"Error downloading {file_url}: {e}")

    def download_files(self):
        response = self.session.get(self.url)
        files = self.find_files(response.content)

        total_pages = self.get_page_count(response.content)

        self.session.headers["x-requested-with"] = "XMLHttpRequest"
        for page in range(2, total_pages + 1):
            print(f"Scraping page {page}...")
            payload = {"al": 1, "al_ad": 0, "offset": page * 10, "part": 1}
            json_data = json.loads(
                self.session.post(self.url, data=payload).content.decode("latin-1")
            )
            html_data = json_data.get("payload", [])[1][2]
            files.extend(self.find_files(html_data))
        del self.session.headers["x-requested-with"]

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            executor.map(self.download_file, files)


def main():
    parser = argparse.ArgumentParser(description="VK File Downloader")
    parser.add_argument("url", type=str, help="URL to scrape")
    parser.add_argument(
        "--output_dir", type=str, default="./downloads", help="Output directory"
    )
    parser.add_argument(
        "--file_type", type=str, default="pdf", help="File type to download"
    )
    parser.add_argument(
        "--threads", type=int, default=1, help="Number of simultaneous downloads"
    )
    args = parser.parse_args()

    downloader = VKDownloader(args.url, args.output_dir, args.file_type, args.threads)
    downloader.download_files()


if __name__ == "__main__":
    main()
