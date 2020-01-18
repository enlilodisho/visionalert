import sys
import json
from TCPServer import TCPServer

# Load config
config = None
try:
    with open('config.json', 'r') as configFile:
        config = configFile.read()
    if config is not None:
        config = json.loads(config)
except:
    print("ERROR! Configuration file not found.", file=sys.stderr)
    exit()

# Starts VisionAlert Server
server = TCPServer(config['port']);
try:
    server.start()
except KeyboardInterrupt:
    server.stop()
    print("Bye")
    sys.exit()
