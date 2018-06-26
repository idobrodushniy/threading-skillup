import threading
import time
import logging
import datetime

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',
                    filename='threading-3.log'
                    )

a = 0


def consumer(cv):
    global a
    logging.debug('Consumer thread started ... - {0}'.format(datetime.datetime.now()))
    while True:
        with cv:
            logging.debug(
                'Consumer waiting ... - {0}'.format(
                    datetime.datetime.now()
                )
            )
            cv.wait()
            a += 1
            logging.debug('Consumer consumed the resource a={0} - {1}'.format(a, datetime.datetime.now()))
            time.sleep(1)


def producer(cv):
    logging.debug('Producer thread started ... - {0}'.format(datetime.datetime.now()))
    while True:
        with cv:
            logging.debug('Making resource available - {0}'.format(datetime.datetime.now()))
            logging.debug('Notifying to all consumers - {0}'.format(datetime.datetime.now()))
            cv.notifyAll()
        time.sleep(10)


if __name__ == '__main__':
    condition = threading.Condition()
    threads = []
    for i in range(2):
        cs = threading.Thread(target=consumer, name='CONSUMER-{}'.format(i), args=(condition,), daemon=True)
        threads.append(cs)

    for i in threads:
        i.start()

    time.sleep(3)

    pd = threading.Thread(target=producer, name='PRODUCER', args=(condition,), daemon=True)
    pd.start()
    time.sleep(30)
