import json
import os
from datetime import datetime


FILE="data/sai_memory.json"


def remember(event):

    data=[]

    if os.path.exists(FILE):
        with open(FILE) as f:
            data=json.load(f)

    data.append({
        "time":str(datetime.now()),
        "event":event
    })


    with open(FILE,"w") as f:
        json.dump(data,f,indent=4)



def recall():

    if not os.path.exists(FILE):
        return []

    with open(FILE) as f:
        return json.load(f)