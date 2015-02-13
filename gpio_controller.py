import wiringpi2


class DigitalOutPin(object):
  def __init__(self, gpio_channel):
    self.gpio_channel = gpio_channel
    wiringpi2.pinMode(gpio_channel, 1)

  def write(self, state):
    wiringpi2.digitalWrite(self.gpio_channel, state)


class YM2420(object):
  def __init__(self, IC, CS, A0, Dn):
    wiringpi2.wiringPiSetupGpio()

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
