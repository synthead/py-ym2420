import wiringpi2
import time


class GPIOController(object):
  class pin(object):
    def __init__(self, gpio_channel, initial_state):
      self.gpio_channel = gpio_channel
      wiringpi2.pinMode(gpio_channel, 1)
      self.write(initial_state)

    def write(self, state):
      wiringpi2.digitalWrite(self.gpio_channel, state)

    def high(self):
      self.write(1)

    def low(self):
      self.write(0)

  def __init__(
      self, CS, A0, D0, D1, D2, D3, D4, D5, D6, D7, write_time=0.001):
    wiringpi2.wiringPiSetupGpio()

    self.write_time = write_time

    self.CS = self.pin(CS, 1)
    self.A0 = self.pin(A0, 1)
    self.Dn = (
        self.pin(D0, 0), self.pin(D1, 0), self.pin(D2, 0), self.pin(D3, 0),
        self.pin(D4, 0), self.pin(D5, 0), self.pin(D6, 0), self.pin(D7, 0))

    # time.sleep(2)

  def write(self, address, bits):
    for pin, bit in enumerate(format(address, '08b')):
      self.Dn[pin].write(int(bit))
    self.A0.low()
    time.sleep(self.write_time)
    self.CS.low()
    time.sleep(self.write_time)
    self.CS.high()
    time.sleep(self.write_time)

    self.A0.high()
    for pin, bit in enumerate(bits):
      self.Dn[pin].write(bit)
    self.CS.low()
    time.sleep(self.write_time)
    self.CS.high()
    time.sleep(self.write_time)

    print("%s: %s" % (format(address, '02x').upper(), bits))
