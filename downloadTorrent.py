# import libtorrent
import libtorrent as lt
from time import sleep
from IPython.display import display
import ipywidgets as widgets
# create a session object
ses = lt.session()

# set the listen and outgoing interfaces
ses.listen_on(6881, 6891)
downloads = []

# create a torrent info object from a torrent file
torrent_file = "./payback.torrent"
info = lt.torrent_info(torrent_file)

# create a torrent handle from the torrent info object
params = {
    "ti": info,
    "save_path": "./torrents"
}
downloads.append(ses.add_torrent(params))

state_str = [
    "queued",
    "checking",
    "downloading metadata",
    "downloading",
    "finished",
    "seeding",
    "allocating",
    "checking fastresume",
]

layout = widgets.Layout(width="auto")
style = {"description_width": "initial"}
download_bars = [
    widgets.FloatSlider(
        step=0.01, disabled=True, layout=layout, style=style
    )
    for _ in downloads
]
display(*download_bars)

while downloads:
    next_shift = 0
    for index, download in enumerate(downloads[:]):
        bar = download_bars[index + next_shift]
        if not download.is_seed():
            s = download.status()

            bar.description = " ".join(
                [
                    download.name(),
                    str(s.download_rate / 1000),
                    "kB/s",
                    state_str[s.state],
                ]
            )
            bar.value = s.progress * 100
        else:
            next_shift -= 1
            ses.remove_torrent(download)
            downloads.remove(download)
            bar.close()
            download_bars.remove(bar)
            print(download.name(), "complete")
    sleep(1)