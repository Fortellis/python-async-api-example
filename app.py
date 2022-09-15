import time, sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import json

import requests

class EventHandler(FileSystemEventHandler):
    print("Handler Called")
    def on_modified(self, event):
        print(f'event type: {event.event_type}  path : {event.src_path}')
        with open('payload.json', 'r') as f:
            lines = json.load(f)
            print(lines)
            response = requests.post(
                '{yourWebhookURL}/{yourChannel}',
                json = lines,
                headers= {
                    'Accept':'application/json',
                    'Cache-Control':'no-cache'
                    }
                )
            print(response)

src_path = sys.argv[1] if len(sys.argv) > 1 else '.'

event_handler=EventHandler()
observer = Observer()
observer.schedule(event_handler, path=src_path, recursive=True)
print("Monitoring started")
observer.start()
try:
    while(True):
        print('timer', flush=True)
        time.sleep(10 )
except KeyboardInterrupt:
    observer.stop()
observer.join()
