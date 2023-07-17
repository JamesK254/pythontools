import os
import requests
from tqdm import tqdm
import time

def download_rar_file(url, save_path):
    try:
        # Send a request to the URL to get the file data
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Get the total file size from the 'Content-Length' header
        total_size = int(response.headers.get('Content-Length', 0))

        # Initialize tqdm to show the progress bar
        progress_bar = tqdm(total=total_size, unit='B', unit_scale=True, desc='Downloading')

        # Open the local file for writing the downloaded content
        with open(save_path, 'wb') as file:
            start_time = time.time()
            downloaded_size = 0

            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
                downloaded_size += len(chunk)
                progress_bar.update(len(chunk))

                # Calculate download speed and update the tqdm description
                elapsed_time = time.time() - start_time
                download_speed = downloaded_size / elapsed_time / 1024  # Convert to KB/s
                progress_bar.set_description(f"Downloading... {download_speed:.2f} KB/s")

        progress_bar.close()
        print(f"Download completed. File saved at {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Replace the following URL and save_path with your desired values
    download_url = "http://fs17.megadb.xyz:8080/d/5lnizvyoy5vxygoid7w3pc2bmbrr2eoqt6x5q2tf53u4o64dqu5nllryb5z2bh5qipuvsiid/Need-for-Speed-Payback-SteamRIP.com.rar"
    save_file_path = "./file.rar"

    download_rar_file(download_url, save_file_path)
