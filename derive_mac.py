#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

BASE_MAC = '02:42:ac:'
node_id = int(sys.argv[1])

#Convert node_id into HEX
padded_hex = format(node_id, '06x')

derived_addr = BASE_MAC + padded_hex[0:2] + ":" + padded_hex[2:4] + ":" + padded_hex[4:6]
print derived_addr

