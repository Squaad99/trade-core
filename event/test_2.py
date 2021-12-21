import sched
import threading
import time

scheduler = sched.scheduler(time.time, time.sleep)

# Set up a global to be modified by the threads
counter = 0


def increment_counter(name):
    global counter
    print('EVENT:', time.time(), name)
    counter += 1
    print('NOW:', counter)


print('START:', time.time())
e1 = scheduler.enter(5, 1, increment_counter, ('Liverpool match on TV',))
e2 = scheduler.enter(8, 1, increment_counter, ('Take the rubbish bin out',))


def worker():
    print("running worker")
    scheduler.run


# Start a thread to run the events
t = threading.Thread(target=worker, args=())
t.start()

time.sleep(60)