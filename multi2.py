import requests
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

def download_chunk(url, start_byte, end_byte, local_filename, progress_bar):
    headers = {'Range': f'bytes={start_byte}-{end_byte}'}
    response = requests.get(url, headers=headers, stream=True)
    response.raise_for_status()

    chunk_size = 8192
    total_size = end_byte - start_byte + 1
    downloaded_size = 0

    with open(local_filename, 'rb+') as file:
        file.seek(start_byte)
        for chunk in response.iter_content(chunk_size=chunk_size):
            file.write(chunk)
            downloaded_size += len(chunk)
            progress_bar.update(len(chunk))

def download_file(url, local_filename, num_threads=8):
    with requests.head(url) as response:
        response.raise_for_status()
        file_size = int(response.headers['Content-Length'])

    with tqdm(total=file_size, unit='B', unit_scale=True, desc='Downloading', miniters=1) as progress_bar:
        chunk_size = file_size // num_threads
        ranges = [(i * chunk_size, (i + 1) * chunk_size - 1) for i in range(num_threads - 1)]
        ranges.append(((num_threads - 1) * chunk_size, file_size))

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(download_chunk, url, start, end, local_filename, progress_bar) for (start, end) in ranges]

            # Wait for all threads to complete their tasks
            for future in as_completed(futures):
                future.result()

if __name__ == "__main__":
    file_url = "https://tinypon.s3.amazonaws.com/thumbnails/Telegram+Desktop.rar"
    local_file_path = "./file.rar"

    download_file(file_url, local_file_path, num_threads=8)
