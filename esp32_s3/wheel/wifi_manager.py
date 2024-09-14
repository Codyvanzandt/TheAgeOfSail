import os
import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
import json

class WiFiManager:
    def __init__(self, ssid=None, password=None):
        self.ssid = ssid or os.getenv('CIRCUITPY_WIFI_SSID')
        self.password = password or os.getenv('CIRCUITPY_WIFI_PASSWORD')
        self.wifi = wifi.radio
        self.pool = None
        self.session = None

    def connect_wifi(self):
        print(f"Connecting to {self.ssid}")
        self.wifi.connect(self.ssid, self.password)
        print(f"Connected to {self.ssid}")
        self.pool = socketpool.SocketPool(self.wifi)

    def create_session(self):
        self.session = adafruit_requests.Session(self.pool, ssl.create_default_context())

    def make_request(self, url, method='GET', data=None):
        if not self.session:
            raise RuntimeError("Session not created. Call create_session() first.")

        if method == 'GET':
            response = self.session.get(url)
        elif method == 'POST':
            headers = {'Content-Type': 'application/json'}
            response = self.session.post(url, data=json.dumps(data), headers=headers)
        else:
            raise ValueError("Unsupported HTTP method")
        return response.json()
