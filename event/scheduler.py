# Schedule Library imported
import threading

import schedule
import time


def call_event():
    print("Shaurya says Geeksforgeeks")


schedule.every(1).seconds.do(call_event)

# while True:
#     schedule.run_pending()
#     time.sleep(1)

def scheduler_worker():
    print("running worker")
    while True:
        schedule.run_pending()
        time.sleep(1)

t = threading.Thread(target=scheduler_worker, args=())
t.start()

print("dd")