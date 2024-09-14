# SPDX-FileCopyrightText: 2020 Brent Rubell for Adafruit Industries
# SPDX-License-Identifier: MIT
from wifi_manager import WiFiManager
from rotary_encoder import RotaryEncoder


def main():
    ENDPOINT = "http://10.0.0.25:8000"

    client = WiFiManager()
    client.connect_wifi()
    client.create_session()

    rotary = RotaryEncoder()

    while True:
        heading = rotary.read()
        if heading:
            data = {"ship_id": "ship1", "key" : "heading", "value" : heading}
            response = client.make_request(f"{ENDPOINT}/update_ship", method='POST', data=data)

    print("Done")

if __name__ == "__main__":
    main()
