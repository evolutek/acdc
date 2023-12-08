import os
import asyncio
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
import json
from av import VideoFrame
import cv2 as cv


def read_file(filename: str) -> str:
    with open(filename, "r", encoding="utf8") as f:
        text = f.read()
    return text


ASSETS_DIR = os.path.join(os.path.dirname(__file__), ".." + os.sep + "assets/webrtc")


class VideoProvider:
    def read(self):
        raise NotImplementedError("VideoProvider.read()")


class ModularVideoStreamTrack(VideoStreamTrack):
    def __init__(self, video: VideoProvider):
        super().__init__()
        self.video = video

    async def recv(self):
        pts, time_base = await self.next_timestamp()
        frame = VideoFrame.from_ndarray(self.video.read(), format="bgr24")
        frame.pts = pts
        frame.time_base = time_base
        return frame


class OpenCVVideoProvider(VideoProvider):
    def __init__(self):
        self.counter = 0
        self.video = cv.VideoCapture(0)
        if not self.video.isOpened():
            print("Cannot open camera")
            exit(2)
        print("Camera stream successfuly opened")
        ret, frame = self.video.read()
        if not ret:
            print("Failed to retreive first frame: %i" % ret)
            exit(2)
        self.height, self.width, _ = frame.shape

    def read(self):
        ret, img = self.video.read()
        if not ret:
            print("Failed to retreive frame: %i" % ret)
            exit(2)
        return img


class WebRTCServer:
    def __init__(self, port=8080, host="0.0.0.0") -> None:
        self.index_text = read_file(os.path.join(ASSETS_DIR, "index.html"))
        self.client_text = read_file(os.path.join(ASSETS_DIR, "client.js"))
        self.port = port
        self.host = host
        self.connections = set()
        self.video = None

    def set_video_provider(self, video: VideoProvider):
        self.video = ModularVideoStreamTrack(video)

    async def on_shutdown(self, app):
        coros = [pc.close() for pc in self.connections]
        await asyncio.gather(*coros)
        self.connections.clear()

    async def on_get_index(self, request):
        return web.Response(content_type="text/html", text=self.index_text)


    async def on_get_client(self, request):
        return web.Response(content_type="application/javascript", text=self.client_text)

    async def on_offer(self, request):
        params = await request.json()
        offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

        pc = RTCPeerConnection()
        self.connections.add(pc)

        @pc.on("connectionstatechange")
        async def on_connectionstatechange():
            print("Connection state is %s" % pc.connectionState)
            if pc.connectionState == "failed":
                await pc.close()
                self.connections.discard(pc)

        if self.video is not None:
            video_sender = pc.addTrack(self.video)

        await pc.setRemoteDescription(offer)

        answer = await pc.createAnswer()
        await pc.setLocalDescription(answer)

        return web.Response(
            content_type = "application/json",
            text = json.dumps(
                {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
            )
        )

    def run(self, stop_event: list[asyncio.Event]):
        app = web.Application()
        app.on_shutdown.append(self.on_shutdown)
        app.router.add_get("/", self.on_get_index)
        app.router.add_get("/client.js", self.on_get_client)
        app.router.add_post("/offer", self.on_offer)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        if stop_event is not None:
            stop_event[0] = asyncio.Event()

        runner = web.AppRunner(app)
        loop.run_until_complete(runner.setup())

        site = web.TCPSite(runner, self.host, self.port)
        loop.run_until_complete(site.start())

        #web.run_app(app, host=self.host, port=self.port)

        if stop_event is not None and stop_event[0] is not None:
            self.stop_event = stop_event
            loop.run_until_complete(self.wait_until_done())
            loop.close()
        else:
            loop.run_forever()

    async def wait_until_done(self):
        await self.stop_event[0].wait()


if __name__ == "__main__":
    server = WebRTCServer()
    server.set_video_provider(OpenCVVideoProvider())
    server.run()
