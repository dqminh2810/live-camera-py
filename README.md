Live camera developed with Flask & picamera2 library, hosted by Gunicorn, expose to Internet by Cloudflare
# Live camera py

## Requirements
### Software
- Python 3
- Docker
- docker-compose
- Debian v12 (bookworm) support picamera2 module
### Hardware
- Raspberry Pi 4B
- Integrated Pi camera

## Test pi camera available
- `libcamera-hello -t 1`

## Build & Launch
### Docker
- `docker-compose up -d`
- Check logs - `docker logs -f {your-app-id}`

### Systemd (optional)
- To execute `docker-compose up` as a systemd service
- Copy systemd sercvice file - `cp ./live-camera-py.service /etc/systemd/system/live-camera-py.service`
- Enable auto start automatically at system boot - `systemctl enable live-camera-py.service`
- Start - `systemctl start live-camera-py.service`
- Restart your host - `shutdown -r now`
- Check logs - `systemctl status live-camera-py.service` || `journalctl -xeu live-camera-py.service`

## Expose to internet
### Ngrok (no require register domain name) [optional]
- Install Ngrok then launch `ngrok http 5000`
- `Connect to your service by ngrok given domain address`

### Cloudflare tunnel (require register DNS)
[Guide](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/)
- Register your domain name with any provider
- Create cloudflare tunnel
- Update your NS provider with cloudflare NS
- Install cloudflare connector & setup tunnel on your host
- Connect your service to tunnel (provide hostname [subdomain + domain] & service address [internal IP address])
- Create cloudflare DNS record for your service
- `Connect to your service by your Fucly Qualified Domain Name (subdomain + domain)`

### Port forward (require access to router & permissions to open public port) [not recommend]
- Enable firewall inbound/outbound port on your host
- Check with your ISP if it allow NAT forward enter connections for port forwading 
- Connect to router & configure port forwarding for your internal host IP address with specific port
- Register your domain name with any provider
- Create DNS record for your service & link to your external IP address
- `Connect to your service by your domain registered`

