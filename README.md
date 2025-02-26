# VkDownloader - Command Line Usage

The **VkDownloader** is a command-line program that allows you to scrape and download files from a specified URL. You can customize the output directory, file type, and the number of simultaneous downloads using the command-line arguments.

## Arguments

- `url` (required):
  - **Type**: `str`
  - **Description**: The URL you want to scrape files from. This is a required argument and must be provided.

- `--output_dir` (optional):
  - **Type**: `str`
  - **Default**: `./downloads`
  - **Description**: The directory where the downloaded files will be saved. If not provided, the default directory `./downloads` will be used.

- `--file_type` (optional):
  - **Type**: `str`
  - **Default**: `pdf`
  - **Description**: The type of file to download (e.g., `pdf`, `jpg`, `mp3`). If not specified, the program will default to downloading PDF files.

- `--threads` (optional):
  - **Type**: `int`
  - **Default**: `1`
  - **Description**: The number of simultaneous downloads to run. The default value is `1`, but you can increase this for faster downloads depending on your network connection.

## Example Usage

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

## Notes
- Ensure the provided URL points to a valid location for file scraping.
- The program will attempt to download the specified file type from the given URL, saving them in the specified directory.
- If you choose to use multiple threads for downloading, it can significantly speed up the process, depending on the file sizes and network conditions.

