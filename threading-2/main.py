import datetime
import logging
import os
import threading

import requests
import simplejson

WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'
WEATHER_API_CITY_ID_LIST = [2312249, 709717, 706483, 703448, 5056033]
WEATHER_API_KEY = '75fa43decdce61a9d32c4f0cbd62e10c'
WITH_LOCK_RESULTS_PATH = 'with_lock_weather.txt'
WITHOUT_LOCK_RESULTS_PATH = 'without_lock_weather.txt'
MAIN_THREAD_RESULTS_PATH = 'weather.txt'
PATHES_LIST = [WITH_LOCK_RESULTS_PATH, WITHOUT_LOCK_RESULTS_PATH, MAIN_THREAD_RESULTS_PATH]

logging.getLogger("requests").setLevel(logging.ERROR)
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.basicConfig(
    filename='threading-2.log',
    level=logging.DEBUG,
    filemode='w',
    format='(%(threadName)-9s) %(message)s'
)


def log_finished_chunk_interval(label: str, interval: datetime.timedelta):
    logging.debug(
        'In {0} was finished after {1} seconds of work!'.format(
            label,
            str(interval).split(':')[-1],
        )
    )


def fetch_url(city_id_list: list, filename: str, lock: threading.RLock = None):
    for id in city_id_list:
        response = requests.get(
            url=WEATHER_API_URL,
            params={'id': id, 'appid': WEATHER_API_KEY}
        )
        logging.debug('Got info about city with id={0} in {1}'.format(id, threading.current_thread().name))

        data = simplejson.dumps(
            {id: simplejson.loads(response.text)['name'], 'thread_name': threading.current_thread().name}
        )

        if lock:
            lock.acquire()

        for character in data:
            with open(filename, 'a') as weather_file:
                weather_file.write(character)
                if character is data[-1]:
                    weather_file.write("\n")
        if lock:
            lock.release()


def call_in_threads(filename, task_type: str, lock: threading.RLock = None, ):
    threads_list = []
    in_threads_started = datetime.datetime.now()

    for i in range(5):
        t = threading.Thread(target=fetch_url, args=(WEATHER_API_CITY_ID_LIST, filename, lock))
        t.start()
        threads_list.append(t)

    for thread in threads_list:
        thread.join()

    in_threads_finished = datetime.datetime.now()
    log_finished_chunk_interval(task_type, in_threads_finished - in_threads_started)


if __name__ == '__main__':
    for path in PATHES_LIST:
        if os.path.exists(path):
            os.remove(path)

    lock = threading.RLock()

    call_in_threads(WITH_LOCK_RESULTS_PATH, 'multithreading with lock', lock)
    logging.debug('----------------------------------------------------------------------')

    call_in_threads(WITHOUT_LOCK_RESULTS_PATH, 'multithreading without lock')
    logging.debug('----------------------------------------------------------------------')

    started = datetime.datetime.now()

    for i in range(5):
        fetch_url(city_id_list=WEATHER_API_CITY_ID_LIST, filename=MAIN_THREAD_RESULTS_PATH)

    finished = datetime.datetime.now()
    log_finished_chunk_interval('in main thread', finished - started)
