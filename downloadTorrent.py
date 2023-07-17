from torrentp import TorrentDownloader
torrent_file = TorrentDownloader("payback.torrent", '.')
torrent_file.start_download()