from torrentp import TorrentDownloader
torrent_file_name = input("Enter torrent name: ")
torrent_file = TorrentDownloader(torrent_file_name, '.')
torrent_file.start_download()