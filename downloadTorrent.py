# import libtorrent
import libtorrent as lt
from time import sleep
# create a session object
ses = lt.session()

# listen on a port range
ses.listen_on(6881, 6891)

# create a torrent info object from a torrent file
torrent_file = "./payback.torrent"
info = lt.torrent_info(torrent_file)

# create a torrent handle from the torrent info object
handle = ses.add_torrent({"ti": info})

# print some info
print("Name:", info.name())
print("Size:", info.total_size())
print("Files:", info.num_files())
print("Trackers:", info.num_trackers())

# set the download path
path = "./torrents"
handle.set_download_limit(0) # unlimited download speed
handle.set_upload_limit(0) # unlimited upload speed
handle.set_sequential_download(True) # download pieces in order
handle.move_storage(path) # move the files to the download path

# start downloading
print("Downloading...")
while not handle.is_seed():
    # get the status of the download
    status = handle.status()
    # print some status info
    print("Progress: %.2f%%" % (status.progress * 100))
    print("Download rate: %.2f KB/s" % (status.download_rate / 1024))
    print("Upload rate: %.2f KB/s" % (status.upload_rate / 1024))
    print("Peers: %d" % status.num_peers)
    print("Seeds: %d" % status.num_seeds)
    print("State:", status.state)
    # wait for a second
    sleep(1)

# download finished
print("Download finished.")
