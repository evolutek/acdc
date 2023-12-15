import time

"""
Frame timing:
loop:
    compute part begin
    ...
    compute par end & wait part begin
    ...
    wait part end
"""

class FrameRateControler:
    def __init__(self, fps) -> None:
        self.compute_part_begin = -1
        self.compute_part_end = -1
        self.compute_part_finished = False
        self.measure_start_time = -1
        self.measured_fps = 0
        self.fps = fps
        self.correction_time = 0
        self.delta_correction_time = 0
        self.frames = 0

    def begin_frame(self):
        self.compute_part_begin = time.time()
        self.frames += 1

    def _end_compute_part(self):
        if self.compute_part_finished: return
        self.compute_part_end = time.time()
        self.compute_part_finished = True

    def get_fps(self):
        self._end_compute_part()
        self.measure_delta_time = self.compute_part_end - self.measure_start_time
        if self.measure_delta_time >= 1:
            self.measured_fps = self.frames / self.measure_delta_time
            self.measure_start_time = self.compute_part_end
            self.frames = 0
        return self.measured_fps

    def get_time_to_wait(self):
        self._end_compute_part()
        frame_delta_time = self.compute_part_end - self.compute_part_begin
        self.correction_time = max(0, 1 / self.fps - frame_delta_time + self.delta_correction_time)
        return self.correction_time

    def end_frame(self):
        correction_end_time = time.time()
        self.delta_correction_time = self.correction_time - (correction_end_time - self.compute_part_end)
        self.compute_part_finished = False
