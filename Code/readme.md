Setup commands:
```sh
sudo -i
cd /path/to/project
apt install -y python3-opencv
apt install -y opencv-data
apt install -y python3-picamera2 --no-install-recommends
python -m venv --system-site-packages venv
. ./venv/bin/activate
pip install -r requirements.txt
exit
libcamera-hello --list-cameras
```

If you are under Wayland run:
```sh
export QT_QPA_PLATFORM=xcb
```
