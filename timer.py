import time


class Timer:

    def __init__(self):
        self.start_time = time.perf_counter()
        self.last_time = self.start_time
        self.current_time = 0
        self.elapsed_time = 0
        self.delta_time = 0.016  # ~60fps

    def update(self):
        self.current_time = time.perf_counter()
        self.elapsed_time = self.current_time - self.start_time
        self.delta_time = self.current_time - self.last_time
        self.last_time = self.current_time

    def normalized(self, slow_motion: float) -> float:
        return (self.elapsed_time * slow_motion) % 1
