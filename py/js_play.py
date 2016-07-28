
""" Module that takes a configuration and input signal from a JSON file
    and calculates the output signal, saving it as a JSON file.
"""

import sys
import json

if __name__ == "__main__":
    fname = sys.argv[1]

    json_input = None
    with open(fname, "rb") as f:
        json_input = json.loads(f.read())

    # Convert arrays to filter
    print(json_input)
