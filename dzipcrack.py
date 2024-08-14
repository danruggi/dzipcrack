import os,sys
import time
import itertools
import string
import pyzipper
import threading
from ctypes import c_wchar_p
from multiprocessing import Pool, cpu_count, Manager

from libs.menu import *
from libs.logger import LoggerFactory

logger = LoggerFactory.get_logger(sys.path[0], "scrapers.tripadvisor.log",
                                  log_level='DEBUG',
                                  stdout_flag=True)

def get_charset(conf):
    characters = ""
    if 'a' in conf['CHARSET']:
        characters += string.ascii_lowercase
    if 'A' in conf['CHARSET']:
        characters += string.ascii_uppercase
    if '1' in conf['CHARSET']:
        characters += string.digits
    if '!' in conf['CHARSET']:
        characters += string.punctuation

    return characters

def generate_strings(conf):

    characters = get_charset(conf)

    starts = conf.get('STARTS', '')
    middle = conf.get('MIDDLE', '')
    ends = conf.get('ENDS', '')
    min_length = conf.get('LMIN', 1)
    max_length = conf.get('LMAX', 20)

    min_var_length_after = min_length - len(starts) - len(middle) - len(ends)
    max_var_length_after = max_length - len(starts) - len(middle) - len(ends)

    if min_var_length_after < 0 or max_var_length_after < 0:
        raise ValueError("Minimum length is too short for the given starts, middle, and ends parts.")

    # Generate combinations for variable part
    for length in range(min_var_length_after, max_var_length_after + 1):
        for combination in itertools.product(characters, repeat=length):
            variable_part = ''.join(combination)
            if not middle:
                yield starts + variable_part + ends
            else:
                for x in range(0, len(variable_part)+1):
                    middle_var_part = variable_part[:x] + middle + variable_part[x:]
                    yield starts + middle_var_part + ends


def crack_zip_bruteforce_worker(args):
    conf, start_index, chunk_size, password_found_event, counter, shared_string = args
    with pyzipper.AESZipFile(conf['FILE'], 'r', compression=pyzipper.ZIP_DEFLATED, encryption=pyzipper.WZ_AES) as pyzfile:
        for i, s in enumerate(itertools.islice(generate_strings(conf), start_index, start_index + chunk_size), start_index):
            if password_found_event.is_set():
                return None  # Another process found the password
            counter.value += 1
            shared_string.value = s
            # if counter.value % 10000 == 0:
            #     logger.info('[%s], testing %s', counter.value, shared_string.value)
            try:
                pyzfile.extractall(pwd=str.encode(s))
                logger.info(f"Password found: {s}")
                password_found_event.set()
                counter.value = -1
                return s
            except Exception as e:
                # logger.error(e)
                continue
    return None

def monitor_progress(counter, shared_string, interval=15):
    start_time = time.time()
    last_count = 0

    while True:
        time.sleep(interval)
        current_count = counter.value
        elapsed_time = time.time() - start_time
        speed = (current_count - last_count) / interval
        logger.info(f"Checked {current_count} combinations, Speed: {speed:.2f} combinations/second, Last string: {shared_string.value}")
        last_count = current_count

        # Stop the thread if the counter is set to a sentinel value (e.g., -1)
        if counter.value == -1:
            break

def crack_zip_bruteforce(conf):
    num_cores = cpu_count()
    chunk_size = 100000  # Number of combinations each process will try at a time

    with Manager() as manager:
        password_found_event = manager.Event()
        counter = manager.Value('i', 0)
        shared_string = manager.Value(c_wchar_p, "")

        # Start monitoring thread
        monitor_thread = threading.Thread(target=monitor_progress, args=(counter, shared_string))
        monitor_thread.start()

        pool = Pool(num_cores)

        # Prepare arguments for workers
        tasks = [(conf, i * chunk_size, chunk_size, password_found_event, counter, shared_string) for i in range(num_cores)]
        results = pool.map(crack_zip_bruteforce_worker, tasks)

        for result in results:
            if result:
                logger.info(f"Password found by one of the processes: {result}")
                pool.terminate()
                break
        else:
            logger.info("Password not found.")

        pool.close()
        pool.join()

        return result

if __name__ == '__main__':
    logger.info("Begin Cracking")
    conf = menu()
    print(conf)
    if not os.path.isfile(conf['FILE']):
        logger.error("File %s not found", conf['FILE'])
        quit()

    if conf['B']:
        password = crack_zip_bruteforce(conf);
        logger.info("Password found: %s", password)
