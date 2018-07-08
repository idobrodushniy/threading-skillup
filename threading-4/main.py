import random, time
import logging
from threading import BoundedSemaphore, Thread

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',
                    filename='threading-4.log',
                    filemode='w'
                    )

max_items = 5
container = BoundedSemaphore(max_items)


def producer(nloops):
    for i in range(nloops):
        time.sleep(random.randrange(2, 5))
        try:
            container.release()
            logging.debug("Produced an item.")
        except ValueError:
            logging.debug("Full, skipping.")


def consumer(nloops):
    for i in range(nloops):
        time.sleep(random.randrange(2, 5))
        if container.acquire(False):
            logging.debug("Consumed an item.")
        else:
            logging.debug("Empty, skipping.")


threads = []
nloops = random.randrange(3, 6)

logging.debug("Starting with %s items." % max_items)

threads.append(Thread(target=producer, args=(nloops,)))
threads.append(Thread(target=consumer, args=(random.randrange(nloops, nloops + max_items + 2),)))
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

logging.debug("All done.")
