

""" Module continuously checks db.processQueue for ids and processes them
    when it happens.
"""

# TODO multiprocessing

import traceback
from pymongo import MongoClient
from js_play import play
from time import sleep

if __name__ == "__main__":
    print("Initialized")
    while True:
        client = MongoClient("mongodb://127.0.0.1:3001/meteor")
        db = client["meteor"]
        match = db.processQueue.find_one()

        if match != None:
            # Begin processing
            id_ = match["id"]

            print("Processing {0}...".format(id_))

            try:
                play(id_)
            except Exception as e:
                traceback.print_exc()

            # Tell meteor it is done
            db.processQueue.delete_one({ "id" : id_ }).deleted_count
            db.sessions.update_one({ "_id" : id_ }, { "$set" : { "pydone": True }})
        sleep(1)
