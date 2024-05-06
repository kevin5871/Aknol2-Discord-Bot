from enum import Enum

class Platform(Enum):
  AFREECA = 1
  CHZZK = 2
  YOUTUBE = 3

def chr2platform(c: str) -> Platform:
  if c == 'a':
    return Platform.AFREECA
  elif c == 'c':
    return Platform.CHZZK
  elif c == 'y':
    return Platform.YOUTUBE
  else:
    raise ValueError(f"Platform not found for char '{c}'")

def platform2chr(platform) -> str:
  if platform == Platform.AFREECA:
    return 'a'
  elif platform == Platform.CHZZK:
    return 'c'
  elif platform == Platform.YOUTUBE:
    return 'y'
  else:
    raise ValueError(f"Char not found for platform {platform}")