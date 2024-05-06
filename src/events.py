from dataclasses import dataclass
from datetime import datetime
from streamers import Streamer, get_streamer

@dataclass
class Event:
  created_at: datetime
  related: tuple[Streamer]
  description: str

_events: list[Event] = []

def parse_event(s: str) -> Event:
  ss = s.strip().split(' ')
  return Event(datetime.fromisoformat(ss[0]), tuple(map(get_streamer, filter(lambda x: x, ss[1].split(',')))), ' '.join(s[2:]))

def read_events() -> list[Event]:
  with open('./data/events.txt', 'r', encoding='utf-8') as f:
    return list(map(parse_event, f.readlines()))

def write_events(events: list[Event]) -> None:
  with open('./data/streamers.txt', 'w', encoding='utf-8') as f:
    for event in events:
      f.write(f'{event.created_at.isoformat()} {",".join(map(Streamer.uid, event.related))} {event.description}\n')

def get_events() -> list[Event]:
  return _events[:]

def append_event(event: Event):
  _events.append(event)
  write_events(_events)

def refresh_events() -> list[Event]:
  global _events
  _events = read_events()