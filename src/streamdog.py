from streamers import Streamer, get_streamers
from platforms import Platform
from pprint import pprint

import threading
import time
import logging
import json

class StreamdogCallback:
  def accept(self, streamer: Streamer, title: str | None) -> None:
    pass

  def test(self, live: list) -> None:
    pass

class Streamdog:
  running: bool = False
  thread: threading.Thread = None
  logger: logging.Logger = logging.getLogger('streamdog')

  def __run_thread(self, callback: StreamdogCallback, /) -> None:
    prev_stream_title: dict[str, str] = {}
    streamers: list[Streamer] = get_streamers()
    threads: list[threading.Thread] = [None] * len(streamers)
    ret: list[tuple[Streamer, str]] = [None] * len(streamers)

    for i in range(len(streamers)):
      t = threading.Thread(target=streamers[i].get_stream, args=(ret, i))
      threads[i] = t
      t.start()

    for t in threads:
      t.join()

    prev_stream_title = dict(filter(lambda x: x and x[1], ret))

    while True:
      time.sleep(15) # 새로고침 주기

      stream_title: dict[str, str] = {}
      streamers = get_streamers()
      threads = [None] * len(streamers)
      ret = [None] * len(streamers)

      for i in range(len(streamers)):
        t = threading.Thread(target=streamers[i].get_stream, args=(ret, i))
        threads[i] = t
        t.start()

      for t in threads:
        t.join()

      stream_title = dict(filter(lambda x: x and x[1], ret))
      for streamer in (set(prev_stream_title.keys()) - set(stream_title.keys())):
        with open('./pipe.json', 'w') as file :
          json.dump({'notification': [streamer.name + '님이 방송을 종료하였습니다.']}, file)
        print('[-]', streamer)
        callback.accept(streamer, None)

      for streamer in (set(stream_title.keys()) - set(prev_stream_title.keys())):
        url = ''
        if streamer.platform == Platform.CHZZK :
            url = 'https://chzzk.naver.com/live/' + streamer.uid
        elif streamer.platform == Platform.AFREECA :
            url = 'https://play.afreecatv.com/' + streamer.uid
        with open('./pipe.json', 'w') as file :
          json.dump({'notification': [streamer.name + '님이 방송을 시작하였습니다. ' + '('+ dict(map(lambda x: (x[0].name, x[1]), stream_title.items()))[streamer.name]+ ')' + '\n<' + url + '>']}, file)
        print('[+]', streamer)
        callback.accept(streamer, stream_title[streamer])


      live_streamers = []
      for i in range(0, len(stream_title)) :
        if stream_title[list(stream_title.keys())[i]] != None :
          live_streamers.append(list(stream_title.keys())[i])

      callback.test(live_streamers)

      prev_stream_title = stream_title


  def run(self, callback: StreamdogCallback) -> None:
    if self.running:
      raise ValueError('Watchdog already started')

    self.running = True
    self.thread = threading.Thread(target=self.__run_thread, args=(callback, ))
    self.thread.start()