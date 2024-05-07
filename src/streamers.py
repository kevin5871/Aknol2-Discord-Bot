from dataclasses import dataclass
from platforms import Platform, chr2platform, platform2chr
from dotenv import load_dotenv

import os
import requests

load_dotenv(verbose=True)
NID_AUT = os.getenv('NID_AUT')
NID_SES = os.getenv('NID_SES')

@dataclass
class Streamer:
  platform: Platform
  uid: str
  name: str

  def get_stream(self, ret, i) -> tuple:
    try :
      if self.platform == Platform.AFREECA:
        ret[i] = (self, self.__get_afreeca(self.uid))
      elif self.platform == Platform.CHZZK:
        ret[i] = (self, self.__get_chzzk(self.uid))
      else:
        ret[i] = (self, None)
    except Exception as e:
      print('error while seraching ' + self.name, '(' + e + ')')
      ret[i] = (self, None)

  def __get_chzzk(self, hash, /) -> str | None:
    res = requests.get(
      f'https://api.chzzk.naver.com/service/v1/channels/{hash}/live-detail',
      headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
      },
      cookies={
        'NID_AUT': NID_AUT,
        'NID_SES': NID_SES,
      }
    ).json()
    try :
      if res['content']['status'] == 'OPEN' and (
        res['content']['liveCategory'] == 'Minecraft' or 
        '놀' in res['content']['liveTitle'] or
        ('마' in res['content']['liveTitle'] and '크' in res['content']['liveTitle'])
      ):
        return res['content']['liveTitle']
      else:
        return None
    except :
      return None

  def __get_afreeca(self, bid, /) -> str | None:
    res = requests.post(
      'https://live.afreecatv.com/afreeca/player_live_api.php', 
      data={ 'bid': bid }, 
      headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'
      }
    ).json()
    if res['CHANNEL']['RESULT'] == 1 and (
      res['CHANNEL']['CATE'] == '00040017' or 
      '놀' in res['CHANNEL']['TITLE'] or
      ('마' in res['CHANNEL']['TITLE'] and '크' in res['CHANNEL']['TITLE'])
    ):
      return res['CHANNEL']['TITLE']
    else:
      return None

  def __hash__(self) -> int:
    return hash((self.uid, self.name))

_streamers: list[Streamer] = []
uid2streamer: dict[str, Streamer] = dict()

def parse_streamer(s: str) -> Streamer:
  ss = s.strip().split(',')
  return Streamer(chr2platform(ss[0]), ss[1], ','.join(ss[2:]))

def read_streamers() -> list[Streamer]:
  with open('./data/streamers.txt', 'r', encoding='utf-8') as f:
    return list(map(parse_streamer, f.readlines()))

def write_streamers(streamers: list[Streamer]) -> None:
  with open('./data/streamers.txt', 'w', encoding='utf-8') as f:
    for streamer in streamers:
      f.write(f'{platform2chr(streamer.platform)},{streamer.uid},{streamer.name}\n')

def get_streamers() -> list[Streamer]:
  return _streamers[:]

def get_streamer(uid: str) -> Streamer:
  return uid2streamer[uid]

def append_streamer(streamer: Streamer):
  _streamers.append(streamer)
  uid2streamer[streamer.uid] = streamer
  write_streamers(_streamers)

def refresh_streamers() -> list[Streamer]:
  global _streamers
  _streamers = read_streamers()
  for streamer in _streamers:
    uid2streamer[streamer.uid] = streamer

def write_live_streamers(streamers: list[Streamer]) -> None:
  with open('./data/live_streamers.txt', 'w', encoding='utf-8') as f:
    for streamer in streamers:
      f.write(f'{platform2chr(streamer.platform)},{streamer.uid},{streamer.name}\n')
