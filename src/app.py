from streamers import Streamer, refresh_streamers, write_live_streamers
from filedog import Filedog, FiledogCallback
from streamdog import Streamdog, StreamdogCallback
#import bot

class FileChangeCallback(FiledogCallback):
  def accept(self, file: str) -> None:
    if file == 'streamers.txt':
      refresh_streamers()
      print("Refreshing streamer list")

class StreamChangeCallback(StreamdogCallback):
  def accept(self, streamer: Streamer, title: str | None) -> None:
    print('Stream state changed', streamer, title)
  
  def test(self, live: list) -> None:
    write_live_streamers(live)


def main():
  refresh_streamers()

  fd = Filedog('./data')
  fd.run(FileChangeCallback())

  sd = Streamdog()
  sd.run(StreamChangeCallback())


if __name__ == '__main__':
  print('starting streamdog...')
  main()