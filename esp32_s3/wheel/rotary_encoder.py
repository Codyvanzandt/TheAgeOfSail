import board
from adafruit_seesaw import seesaw, rotaryio, digitalio

class RotaryEncoder:
    def __init__(self, i2c_bus=board.I2C(), addr=0x36):
        self.seesaw = seesaw.Seesaw(i2c_bus, addr=addr)
        self.seesaw_product = (self.seesaw.get_version() >> 16) & 0xFFFF
        self.encoder = rotaryio.IncrementalEncoder(self.seesaw)
        self.last_position = None

    def read(self):
        position = -self.encoder.position
        if position != self.last_position:
            self.last_position = position
            return self.encode(position)
        return

    def encode(self, position):
        speed_multiplier = 2.5
        # Normalize the encoder value to a 0-359 range
        normalized = (position * speed_multiplier) % 360

        # Handle negative values
        if normalized < 0:
            normalized += 360

        return -int(normalized)

    def reset(self):
        self.encoder.position = 0
        self.last_position = 0# Write your code here :-)
