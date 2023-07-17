# import libtorrent
import libtorrent as lt
from time import sleep
# create a session object
ses = lt.session()

# set the listen and outgoing interfaces
ses.set_settings({
    "listen_interfaces": "0.0.0.0:6881",
    "outgoing_interfaces": "0.0.0.0"
})

# create a torrent info object from a torrent file
torrent_file = "./payback.torrent"
info = lt.torrent_info(torrent_file)

# create a torrent handle from the torrent info object
params = {
    "ti": info,
    "save_path": "./torrents"
}
handle = ses.add_torrent(params)

# print some info
print("Name:", info.name())
print("Size:", info.total_size())
print("Files:", info.num_files())
print("Trackers:", info.num_trackers())

# set the download and upload limits
handle.set_download_limit(0) # unlimited download speed
handle.set_upload_limit(0) # unlimited upload speed
handle.set_sequential_download(True) # download pieces in order

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
