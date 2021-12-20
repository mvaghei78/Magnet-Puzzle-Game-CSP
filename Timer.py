import time
import datetime
class Timer:
    def __init__(self):
        self.start_time = time.perf_counter()

    def endTimer(self):
        self.end_time = time.perf_counter()
        Seconds = int(self.end_time - self.start_time)
        time_str = datetime.timedelta(seconds=Seconds)
        return time_str