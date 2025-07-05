# Live camera py
Live camera build by Flask and hosted by Gunicorn

## Requirements
### Software
- Python v3.11
- Docker v28.1.1
- docker-compose v2.5.0
- Debian v12 (bookworm) support picamera2 module
### Hardware
- Raspberry Pi 4B
- Integrated Pi camera

## Test pi camera available
- `libcamera-hello -t 1 --nopreview`

## Build & Launch
### Docker (Option 1)
- `docker-compose up -d`

### Systemd (Option 2)
- Create Linux service to launch program in background
- Create file `/etc/systemd/system/live-camera-py.service`


```
[Unit]
Description=Live Camera Pi
After=network.target

[Service]
ExecStart=/usr/bin/python3 {your-work-directory}/app.py
WorkingDirectory={your-work-directory}
StandardOutput=inherit
StandardError=inherit
Restart=always
User={your-username}

[Install]
WantedBy=multi-user.target
```

- Start - `systemctl start live-camera-py`
- Enable auto start after system boot - `systemctl enable live-camera-py`