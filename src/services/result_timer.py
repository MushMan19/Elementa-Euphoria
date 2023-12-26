import threading

def wait_for_time(func, flag, *args):
    stop_flag = flag['stop_flag']
    stop_flag.set()
    lock = threading.Lock()
    display_thread = threading.Thread(target=func, args=args)
    display_thread.start()
    return display_thread
        
def create_threading_event():
    return {'stop_flag': threading.Event()}

def end_threads(threads):
    for thread in threads:
        thread.join()