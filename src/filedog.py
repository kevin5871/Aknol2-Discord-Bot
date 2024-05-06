import hashlib
import os
import threading
import time
import logging
import pathlib

class FiledogCallback:
  def accept(self, file: str) -> None:
    pass

class Filedog:
  dir: str = None
  running: bool = False
  thread: threading.Thread = None
  logger: logging.Logger = logging.getLogger('watchdog')

  def __init__(self, dir: str, /) -> None:
    self.dir = dir

  def __run_thread(self, callback: FiledogCallback, /) -> None:
    file_hashes: dict[str, str] = {}

    for file in os.listdir(self.dir):
      with open(pathlib.Path(self.dir).joinpath(file), 'rb') as f:
        file_hashes[file] = hashlib.sha1(f.read()).hexdigest()

    while True:
      for file in os.listdir(self.dir):
        with open(pathlib.Path(self.dir).joinpath(file), 'rb') as f:
          sha1 = hashlib.sha1(f.read()).hexdigest()
          if sha1 != file_hashes[file]:
            callback.accept(file)
            file_hashes[file] = sha1
            self.logger.info(f'File {file} changed')
      time.sleep(1)

  def run(self, callback: FiledogCallback) -> None:
    if self.running:
      raise ValueError('Watchdog already started')

    self.running = True
    self.thread = threading.Thread(target=self.__run_thread, args=(callback, ))
    self.thread.start()