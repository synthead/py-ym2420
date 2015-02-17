import wiringpi2


class DigitalOutPin(object):
  def __init__(self, gpio_channel):
    self.gpio_channel = gpio_channel
    wiringpi2.pinMode(gpio_channel, 1)

  def write(self, state):
    wiringpi2.digitalWrite(self.gpio_channel, state)


class YM2420(object):
  def __init__(self, IC, CS, A0, Dn):
    self.IC, self.CS, self.A0 = [DigitalOutPin(pin) for pin in (IC, CS, A0)]
    self.Dn = [DigitalOutPin(pin) for pin in Dn]

    self.reset()

  def reset(self):
    self.IC.write(0)
    self.CS.write(1)
    self.A0.write(1)
    self.IC.write(1)

  def write(self, address, content):
    print("0x{0:02x}: {1}".format(address, content))

    for bit, pin in enumerate(self.Dn):
      pin.write((address >> bit) % 2)

    self.A0.write(0)
    self.CS.write(0)
    self.CS.write(1)

    for bit, pin in zip(content, self.Dn):
      pin.write(bit)

    self.A0.write(1)
    self.CS.write(0)
    self.CS.write(1)


class AnalogInputPin(object):
  def __init__(
      self, analog_pin, min_value=0, max_value=1019, sample_size=10):
    self.analog_pin = analog_pin
    self.min_value = min_value
    self.max_value = max_value
    self.sample_size = sample_size
    self.values = [self.read_raw()] * self.sample_size

  def read_raw(self):
    return wiringpi2.analogRead(self.analog_pin)

  def read(self):
    self.values.pop(0)
    self.values.append(self.read_raw())
    return sum(self.values) / self.sample_size

  def read_percent(self):
    value = self.read()

    if value <= self.min_value:
      return 0
    elif value >= self.max_value:
      return 100
    else:
      return (
          (self.read() - self.min_value) / (self.max_value - self.min_value)
          ) * 100


wiringpi2.wiringPiSetupGpio()
