# VkDownloader - Command Line Usage

**VkDownloader** is a command-line program designed to scrape and download files from a specified URL. It allows customization of the output directory, file type, and the number of simultaneous downloads using command-line arguments. Additionally, it includes a batch download feature to automate multiple downloads.

## Table of Contents

1. [Installation](#installation)
2. [Usage](#usage)
    - [Basic Usage](#basic-usage)
    - [Batch Download](#batch-download)
3. [Arguments](#arguments)
4. [Examples](#examples)
5. [Notes](#notes)


## Installation

To use VkDownloader, ensure you have Python installed on your system. Clone the repository and navigate to the directory containing the script.

```bash
git clone https://github.com/Zephyris-Pro/VkDownloader.git
cd VkDownloader
```

## Usage

### Basic Usage

The basic usage of VkDownloader involves specifying the URL from which you want to download files. You can customize the download process using various command-line arguments.

```bash
python vk_downloader.py [arguments] <url>
```

### Batch Download

The batch download feature allows you to automate the download of files from multiple URLs listed in a text file. This is particularly useful for downloading a large number of files in sequence.

```bash
python batch_download_file_creator.py "path_to_txt_file.txt"
```

#### How It Works

1. **Input File**: The script reads a text file containing a list of URLs. Each URL should be on a new line.
2. **Title Extraction**: For each URL, the script extracts the page title to use as the folder name for downloaded files. It first attempts to extract the title from a `<div class="bt_title">` element. If not found, it falls back to the `<title>` tag. If both methods fail, it uses a regex to search for the title within the page content.
3. **Batch Script Generation**: The script generates a Windows batch file (`batch_download.cmd`) that, when executed, will download files from each URL using `vk_downloader.exe`. The batch file includes commands to set the output directory and file type, and it supports multi-threaded downloads.
4. **Execution**: Running the generated batch file will initiate the download process for all listed URLs.

## Arguments

- `url` (required):
  - **Type**: `str`
  - **Description**: The URL you want to scrape files from. This is a required argument and must be provided.

- `--output_dir` (optional):
  - **Type**: `str`
  - **Default**: `./dl`
  - **Description**: The directory where the downloaded files will be saved. If not provided, the default directory `./dl` will be used.

- `--file_type` (optional):
  - **Type**: `str`
  - **Default**: `pdf`
  - **Description**: The type of file to download (e.g., `pdf`, `jpg`, `mp3`). If not specified, the program will default to downloading PDF files.

- `--threads` (optional):
  - **Type**: `int`
  - **Default**: `1`
  - **Description**: The number of simultaneous downloads to run. The default value is `1`, but you can increase this for faster downloads depending on your network connection.

## Examples

1. **Download PDF files from a URL and save them to a custom output directory:**

   ```bash
   python vk_downloader.py --output_dir ./my_files https://vk.com/topic-........._........
   ```

2. **Download JPG files with multiple threads:**

   ```bash
   python vk_downloader.py --file_type jpg --threads 5 https://vk.com/topic-........._........
   ```

3. **Download files with a custom file type (e.g., MP3) and specify a custom output directory:**

   ```bash
   python vk_downloader.py --file_type mp3 --output_dir ./audio_files https://vk.com/topic-........._........
   ```

4. **Create a batch download script:**

   ```bash
   python batch_download_file_creator.py "links.txt"
   ```

   This will generate a `batch_download.cmd` file that you can run to download files from all URLs listed in `links.txt` in bulk mode.

## Notes

- Ensure the provided URL points to a valid location for file scraping.
- The program will attempt to download the specified file type from the given URL, saving them in the specified directory.
- If you choose to use multiple threads for downloading, it can significantly speed up the process, depending on the file sizes and network conditions.
- The batch download script requires a text file containing a list of URLs, one per line.

## END
