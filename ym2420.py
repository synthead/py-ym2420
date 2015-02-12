#!/usr/bin/python


from gpio_controller import GPIOController
from register_data import RegisterData


gpio_controller = GPIOController(
    IC=103, CS=104, A0=118, Dn=(88, 116, 115, 101, 100, 108, 97, 87))

register_data = RegisterData()


def write_changes():
  for address, bits in register_data.pending_writes.items():
    gpio_controller.write(address, bits)

  register_data.pending_writes.clear()


# A nice piano!
register_data.set_byte(16, 171)
register_data.set_byte(48, 48)
register_data.set_byte(32, 28)
write_changes()

import IPython
register_data.key_on(0, 0)
write_changes()

IPython.embed()
