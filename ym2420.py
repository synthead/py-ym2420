#!/usr/bin/python


from gpio_controller import GPIOController
from register_data import RegisterData


gpio_controller = GPIOController(
    CS=104, A0=83, D0=88, D1=116, D2=115, D3=101, D4=100, D5=108, D6=97, D7=87)

register_data = RegisterData()

def write_changes():
  for address, bits in register_data.pending_writes.items():
    gpio_controller.write(address, bits)

  register_data.pending_writes.clear()

write_changes()
