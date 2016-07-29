

""" Module to clear collections.
"""

# TODO multiprocessing

from pymongo import MongoClient
from js_play import play
from time import sleep

if __name__ == "__main__":
    client = MongoClient("mongodb://127.0.0.1:3001/meteor")
    db = client["meteor"]
    db.processQueue.remove()
