import collections


class RegisterData(object):
  def __init__(self):
    self.register_data = {
        address: [0] * 8 for address in (
            0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x0E, 0x10, 0x11,
            0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18, 0x20, 0x21, 0x22, 0x23,
            0x24, 0x25, 0x26, 0x27, 0x28, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35,
            0x36, 0x37, 0x38)}
    self.pending_writes = collections.OrderedDict()

  def _add_pending_write(self, address):
    if address in self.pending_writes:
      del self.pending_writes[address]

    self.pending_writes[address] = self.register_data[address]

  def set_bit(self, address, bit, value):
    self.register_data[address][bit] = value
    self._add_pending_write(address)

  def set_range(self, address, first_bit, last_bit, value):
    self.register_data[address][first_bit:last_bit + 1] = [
        (value >> bit) % 2 for bit in range(last_bit + 1 - first_bit)]
    self._add_pending_write(address)

  def set_byte(self, address, value):
    self.set_range(address, 0, 7, value)

  def frequency(self, index, value):
    upper_frequency = [(value >> bit) % 2 for bit in range(4, 9)]
    if upper_frequency != self.register_data[0x10 + index][:5]:
      self.register_data[0x10 + index][:5] = upper_frequency
      self._add_pending_write(0x10 + index)

    lower_frequency = [(value >> bit) % 2 for bit in range(4)]
    if lower_frequency != self.register_data[0x20 + index][:4]:
      self.register_data[0x20 + index][:4] = lower_frequency
      self._add_pending_write(0x20 + index)

  def amplitude_modulation(self, index, value):
    self.set_bit(0x00 + index, 7, value)

  def vibrato(self, index, value):
    self.set_bit(0x00 + index, 6, value)

  def sustained_sound(self, index, value):
    self.set_bit(0x00 + index, 5, value)

  def rate_key_scale(self, index, value):
    self.set_bit(0x00 + index, 4, value)

  def multi_sample_wave(self, index, value):
    self.set_range(0x00 + index, 0, 3, value)

  def level_key_scale(self, index, value):
    self.set_range(0x02 + index, 6, 7, value)

  def modulation_index(self, value):
    self.set_range(0x02, 0, 5, value)

  def wave_distortion(self, value):
    self.set_range(0x03, 3, 4, value)

  def fm_feedback_constant(self, value):
    self.set_range(0x03, 0, 2, value)

  def attack(self, index, value):
    self.set_range(0x04 + index, 4, 7, value)

  def decay(self, index, value):
    self.set_range(0x04 + index, 0, 3, value)

  def sustain(self, index, value):
    self.set_range(0x06 + index, 4, 7, value)

  def release(self, index, value):
    self.set_range(0x06 + index, 0, 3, value)

  def rhythm_sound_mode(self, value):
    self.set_bit(0x0E, 5, value)

  def rhythm_instruments(self, value):
    self.set_range(0x0E, 0, 4, value)

  def f_number_lsb(self, index, value):
    self.set_range(0x10 + index, 0, 7, value)

  def sustain_on(self, index, value):
    self.set_bit(0x20 + index, 5, value)

  def key_on(self, index, value):
    self.set_bit(0x20 + index, 4, value)

  def octave(self, index, value):
    self.set_range(0x20 + index, 1, 3, value)

  def f_number_msb(self, index, value):
    self.set_bit(0x20 + index, 0, value)

  def instrument(self, index, value):
    self.set_range(0x30 + index, 4, 7, value)

  def volume(self, index, value):
    self.set_range(0x30 + index, 0, 3, value)
