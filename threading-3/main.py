import threading
import time
import logging
import datetime

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',
                    # filename='threading-3.log',
                    filemode='w'
                    )

city_list = ['London', 'Moscow', 'Glasgow', 'New York', 'California', 'Berlin', 'Paris']


def consumer(cv):
    logging.debug('Consumer thread started ... - {0}'.format(datetime.datetime.now()))
    while len(city_list) > 0:
        with cv:
            cv.acquire()
            logging.debug(
                'Consumer waiting ... - {0}'.format(
                    datetime.datetime.now()
                )
            )
            cv.wait()
            element = city_list.pop()
            logging.debug('Consumer consumed the resource element={0} - {1}'.format(element, datetime.datetime.now()))
            cv.release()


def producer(cv):
    logging.debug('Producer thread started ... - {0}'.format(datetime.datetime.now()))
    while len(city_list) > 0:
        with cv:
            logging.debug('Notifying to consumer - {0}'.format(datetime.datetime.now()))
            cv.notify()
        time.sleep(0.5)


if __name__ == '__main__':
    condition = threading.Condition()
    threads = []
    for i in range(3):
        cs = threading.Thread(target=consumer, name='CONSUMER-{}'.format(i), args=(condition,))
        threads.append(cs)

    for i in threads:
        i.start()

    time.sleep(3)

    pd = threading.Thread(target=producer, name='PRODUCER', args=(condition,))
    pd.start()

    # while len(city_list) > 0:
    #     time.sleep(1)
    threads.append(pd)
    for thread in threads:
        print('joined!')
        thread.join()
