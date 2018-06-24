import logging
import threading
from datetime import datetime
from time import sleep

logging.basicConfig(filename='threading-1.log', level=logging.DEBUG, filemode='w')


def log_finished_chunk_interval(label: str, interval):
    logging.debug(
        'In {0} was finished after {1} seconds of work!'.format(
            label,
            str(interval).split(':')[-1],
        )
    )


def display_numbers(count: int):
    for i in range(count):
        logging.debug('{0} in thread {1}'.format(i, threading.current_thread().name))
        sleep(0.5)


if __name__ == '__main__':
    threads_list = []

    in_threads_started = datetime.now()

    # Call display_numbers method in 5 threads
    for i in range(5):
        t = threading.Thread(target=display_numbers, args=(5,))
        t.start()
        threads_list.append(t)

    for thread in threads_list:
        thread.join()

    in_threads_finished = datetime.now()

    log_finished_chunk_interval('multithreading', in_threads_finished - in_threads_started)

    # Call display_numbers method by sync in main thread
    for i in range(5):
        display_numbers(5)

    in_main_thread_finished = datetime.now()
    log_finished_chunk_interval('main_thread', in_main_thread_finished - in_threads_finished)
