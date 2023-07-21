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

    with tqdm(total=file_size, unit='B', unit_scale=True, desc='Downloading', miniters=1) as overall_progress_bar:
        chunk_size = file_size // num_threads
        ranges = [(i * chunk_size, (i + 1) * chunk_size - 1) for i in range(num_threads - 1)]
        ranges.append(((num_threads - 1) * chunk_size, file_size))

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            progress_bars = [tqdm(total=(end - start), unit='B', unit_scale=True, desc=f'Thread {i + 1}', miniters=1)
                             for i, (start, end) in enumerate(ranges)]

            futures = [executor.submit(download_chunk, url, start, end, local_filename, pb)
                       for (start, end), pb in zip(ranges, progress_bars)]

            # Wait for all threads to complete their tasks
            for future in as_completed(futures):
                future.result()

            # Close individual thread progress bars
            for pb in progress_bars:
                pb.close()

    # Shutdown the executor to ensure all threads are terminated
    executor.shutdown(wait=True)

def main_progress_bar(total_size, progress_bars):
    with tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading', miniters=1) as main_bar:
        for pb in progress_bars:
            while not pb.n == pb.total:
                main_bar.n = sum(pb.n for pb in progress_bars)
                main_bar.refresh()

if __name__ == "__main__":
    file_url = "https://tinypon.s3.amazonaws.com/thumbnails/Telegram+Desktop.rar"
    local_file_path = "./file.rar"
    num_threads = 8

    with requests.head(file_url) as response:
        file_size = int(response.headers['Content-Length'])

    chunk_size = file_size // num_threads
    ranges = [(i * chunk_size, (i + 1) * chunk_size - 1) for i in range(num_threads - 1)]
    ranges.append(((num_threads - 1) * chunk_size, file_size))

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        progress_bars = [tqdm(total=(end - start), unit='B', unit_scale=True, desc=f'Thread {i + 1}', miniters=1)
                         for i, (start, end) in enumerate(ranges)]

        futures = [executor.submit(download_chunk, file_url, start, end, local_file_path, pb)
                   for (start, end), pb in zip(ranges, progress_bars)]

        main_progress_bar(file_size, progress_bars)

        # Wait for all threads to complete their tasks
        for future in as_completed(futures):
            future.result()

        # Close individual thread progress bars
        for pb in progress_bars:
            pb.close()
