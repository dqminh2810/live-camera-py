# Live camera py
Live camera developed with picamera2 module & Flask, hosted by Gunicorn, expose to Internet by Cloudflare

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

## Expose to internet
### Ngrok (no require register domain name) [optional]
- Install Ngrok then launch `ngrok http 5000`
- `Connect to your service by ngrok given domain address`

### Cloudflare tunnel (require register domain name) [recommend]
[Guide](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
- Register your domain name with any provider
- Create cloudflare tunnel
- Update your NS provider with cloudflare NS
- Install cloudflare & setup tunnel on your host
- Connect your service to tunnel (provide hostname (subdomain + domain) & service address)
- Create cloudflare DNS record for your service
- `Connect to your service by your hostname`

### Port forward (require access to router & permission to open public port) [not recommend]
- Enable firewall inbound/outbound port on your host
- Check with your ISP if it allow NAT forward incoming connections for port forwading 
- Connect to router & configure port forwarding for your host IP address with specific port
- `Connect to your service by your public IP address`