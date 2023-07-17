import libtorrent as lt

def download_torrent(torrent_file_path, save_path):
    ses = lt.session()
    params = {
        'save_path': save_path,
        'storage_mode': lt.storage_mode_t(2),  # storage_mode_t(2) = StorageMode(allocate_sparse)
        'duplicate_is_error': True
    }

    try:
        # Add the torrent to the session
        handle = lt.add_magnet_uri(ses, torrent_file_path, params)

        print("Downloading torrent. Press Ctrl+C to stop.")
        while not handle.is_seed():
            s = handle.status()

            state_str = ['queued', 'checking', 'downloading metadata', 'downloading', 'finished', 'seeding', 'allocating']
            print(f"\r{handle.name()} - {state_str[s.state]} - Progress: {s.progress * 100:.2f}% - "
                  f"Download Speed: {s.download_rate / 1024:.2f} KB/s - "
                  f"Upload Speed: {s.upload_rate / 1024:.2f} KB/s", end=' ')

            alerts = ses.pop_alerts()
            for alert in alerts:
                if alert.category() & lt.alert.category_t.error_notification:
                    print(alert)

    except KeyboardInterrupt:
        print("\nTorrent download stopped by the user.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # The 'handle' variable should be defined before attempting to remove it
        if 'handle' in locals():
            ses.remove_torrent(handle)

if __name__ == "__main__":
    # Replace the following torrent_file_path and save_path with your desired values
    torrent_file_path = "./payback.torrent"
    save_path = "./torrents/"

    download_torrent(torrent_file_path, save_path)
