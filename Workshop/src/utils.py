class VideoProvider:
    def read(self):
        raise NotImplementedError("VideoProvider.read()")

class MemoryVideoProvider(VideoProvider):
    def init(self):
        self.frame = None

    def write(self, frame):
        self.frame = frame

    def read(self):
        return self.frame
