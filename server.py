import time
import requests
import os
import glob
import xml.etree.ElementTree as ET
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

##### Configure these! #####

# The file path to your savegame.xml:
path = ""

# The path to your game's Teardown/data/requests folder (make the requests folder if it does not exist):
requests_folder = ""

############################

uuid = ""

class EventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global uuid

        if event.event_type == 'modified' and 'savegame.xml' in event.src_path:
            # Parse savegame to retrieve request UUID and URL
            data = open(path, 'r').read()
            result = data[:data.index('<tool>')] + data[data.index('</reward>') + 9:]

            xml_data = ET.fromstring(result)
            new_uuid = xml_data.find('./savegame/mod/local-net/request_uuid').get('value')

            # Ensure this is a new job
            if new_uuid != uuid:
                uuid = new_uuid
                print(f"new request recieved: {uuid}")
                request_url = xml_data.find('./savegame/mod/local-net/request_url').get('value')

                # Clear any existing request files in the requests folder
                files = glob.glob(requests_folder + "*")
                for f in files:
                    os.remove(f)

                # Make the HTTP request
                response = requests.get(request_url).text

                # Create the response file
                new_file_contents = f'return [[{response}]]'
                open(requests_folder + uuid + ".lua", 'w').write(new_file_contents)

                print("sent response")

event_handler = EventHandler()
observer = Observer()
observer.schedule(event_handler, path="C:/Users/lucia/AppData/Local/Teardown", recursive=False)
observer.start()

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
